from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Sembrador, User
import jwt, os
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "mi_clave_jwt_2025")

router = APIRouter(prefix="/sembradores", tags=["Sembradores"])
bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme), db: Session = Depends(get_db)):
    """Validar token JWT y obtener usuario actual"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        rol = payload.get("rol")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        return {"user_id": user_id, "rol": rol, "user": user}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ========== POST: Crear nuevo sembrador ==========
@router.post("/")
def crear_sembrador(
    data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo sembrador.
    El sembrador se asocia automáticamente al usuario actual.
    
    Body esperado:
    {
        "nombre": "Nombre del sembrador",
        "curp": "CURP del sembrador (opcional)",
        "comunidad": "Comunidad",
        "territorio": "Territorio",
        "cultivo_principal": "Maíz",
        "telefono": "1234567890"
    }
    """
    try:
        if not data.get("nombre"):
            raise HTTPException(status_code=400, detail="El nombre es obligatorio")
        
        # Validar territorio obligatorio
        if not data.get("territorio"):
            raise HTTPException(status_code=400, detail="El territorio es obligatorio")
        
        user_id = current_user["user_id"]
        
        # Validar CURP si se proporciona
        curp = None
        if data.get("curp") and data.get("curp").strip():
            import re
            curp = data.get("curp").strip().upper()
            if len(curp) != 18:
                raise HTTPException(status_code=400, detail=f"El CURP debe tener exactamente 18 caracteres. Actualmente tiene {len(curp)} caracteres.")
            curp_regex = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$'
            if not re.match(curp_regex, curp):
                raise HTTPException(status_code=400, detail="CURP inválido. Formato: AAAA######HAAAAA## (4 letras + 6 dígitos + H/M + 5 letras + 2 caracteres)")
            # Verificar que no exista otro sembrador con el mismo CURP
            curp_existente = db.query(Sembrador).filter(Sembrador.curp == curp).first()
            if curp_existente:
                raise HTTPException(status_code=400, detail="Ya existe un sembrador con este CURP")
        
        nuevo = Sembrador(
            nombre=data.get("nombre"),
            curp=curp,
            comunidad=data.get("comunidad"),
            territorio=data.get("territorio"),
            cultivo_principal=data.get("cultivo_principal"),
            telefono=data.get("telefono"),
            user_id=user_id
        )
        
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        
        return {
            "success": True,
            "id": nuevo.id,
            "nombre": nuevo.nombre,
            "message": "Sembrador creado exitosamente"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear sembrador: {str(e)}")


# ========== GET: Listar sembradores según jerarquía ==========
@router.get("/")
def listar_sembradores(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de sembradores según el rol del usuario.
    Aplica filtros jerárquicos:
    - admin: Ve todos los sembradores
    - territorial: Ve sembradores de subordinados
    - facilitador: Ve sembradores de técnicos subordinados
    - técnico/otro: Ve solo sus propios sembradores
    """
    try:
        user_id = current_user["user_id"]
        rol = current_user["rol"]
        
        query = db.query(Sembrador)
        
        # 🔒 Filtros según jerarquía
        if rol == "admin":
            # Admin ve todo
            pass
        elif rol == "territorial":
            # Territorial ve sembradores de subordinados
            sub_ids = [u.id for u in db.query(User).filter(User.superior_id == user_id).all()]
            sub_ids.append(user_id)
            query = query.filter(Sembrador.user_id.in_(sub_ids))
        elif rol == "facilitador":
            # Facilitador ve sembradores de técnicos subordinados
            sub_ids = [u.id for u in db.query(User).filter(
                User.superior_id == user_id,
                User.rol.like("tecnico%")
            ).all()]
            sub_ids.append(user_id)
            query = query.filter(Sembrador.user_id.in_(sub_ids))
        else:
            # Técnico/otro ve solo sus propios sembradores
            query = query.filter(Sembrador.user_id == user_id)
        
        sembradores = query.all()
        
        return {
            "total": len(sembradores),
            "items": [
                {
                    "id": s.id,
                    "nombre": s.nombre,
                    "comunidad": s.comunidad,
                    "cultivo_principal": s.cultivo_principal,
                    "telefono": s.telefono,
                    "lat": s.lat,
                    "lng": s.lng,
                    "user_id": s.user_id,
                    "creado_en": s.creado_en
                }
                for s in sembradores
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al listar sembradores: {str(e)}")


# ========== GET: Obtener sembrador específico ==========
@router.get("/{id}")
def obtener_sembrador(
    id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener un sembrador específico"""
    try:
        sembrador = db.query(Sembrador).filter(Sembrador.id == id).first()
        
        if not sembrador:
            raise HTTPException(status_code=404, detail="Sembrador no encontrado")
        
        # 🔒 Verificar permisos de lectura
        user_id = current_user["user_id"]
        rol = current_user["rol"]
        
        if rol != "admin" and sembrador.user_id != user_id:
            # Verificar si está en su jerarquía
            can_view = False
            if rol == "territorial":
                sub_ids = [u.id for u in db.query(User).filter(User.superior_id == user_id).all()]
                can_view = sembrador.user_id in sub_ids
            elif rol == "facilitador":
                sub_ids = [u.id for u in db.query(User).filter(
                    User.superior_id == user_id,
                    User.rol.like("tecnico%")
                ).all()]
                can_view = sembrador.user_id in sub_ids
            
            if not can_view:
                raise HTTPException(status_code=403, detail="No tienes permiso para ver este sembrador")
        
        return {
            "id": sembrador.id,
            "nombre": sembrador.nombre,
            "comunidad": sembrador.comunidad,
            "cultivo_principal": sembrador.cultivo_principal,
            "telefono": sembrador.telefono,
            "lat": sembrador.lat,
            "lng": sembrador.lng,
            "user_id": sembrador.user_id,
            "creado_en": sembrador.creado_en
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener sembrador: {str(e)}")


# ========== PUT: Actualizar sembrador ==========
@router.put("/{id}")
def actualizar_sembrador(
    id: int,
    data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar un sembrador específico"""
    try:
        sembrador = db.query(Sembrador).filter(Sembrador.id == id).first()
        
        if not sembrador:
            raise HTTPException(status_code=404, detail="Sembrador no encontrado")
        
        # 🔒 Solo el propietario o admin puede actualizar
        user_id = current_user["user_id"]
        rol = current_user["rol"]
        
        if rol != "admin" and sembrador.user_id != user_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para actualizar este sembrador")
        
        # Actualizar campos
        if "nombre" in data:
            sembrador.nombre = data["nombre"]
        if "comunidad" in data:
            sembrador.comunidad = data["comunidad"]
        if "cultivo_principal" in data:
            sembrador.cultivo_principal = data["cultivo_principal"]
        if "telefono" in data:
            sembrador.telefono = data["telefono"]
        if "lat" in data:
            sembrador.lat = data["lat"]
        if "lng" in data:
            sembrador.lng = data["lng"]
        
        db.commit()
        db.refresh(sembrador)
        
        return {
            "success": True,
            "message": f"Sembrador {id} actualizado exitosamente",
            "sembrador": {
                "id": sembrador.id,
                "nombre": sembrador.nombre,
                "comunidad": sembrador.comunidad,
                "cultivo_principal": sembrador.cultivo_principal,
                "telefono": sembrador.telefono,
                "lat": sembrador.lat,
                "lng": sembrador.lng,
                "user_id": sembrador.user_id
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar sembrador: {str(e)}")


# ========== DELETE: Eliminar sembrador ==========
@router.delete("/{id}")
def eliminar_sembrador(
    id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar un sembrador específico"""
    try:
        sembrador = db.query(Sembrador).filter(Sembrador.id == id).first()
        
        if not sembrador:
            raise HTTPException(status_code=404, detail="Sembrador no encontrado")
        
        # 🔒 Solo el propietario o admin puede eliminar
        user_id = current_user["user_id"]
        rol = current_user["rol"]
        
        if rol != "admin" and sembrador.user_id != user_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este sembrador")
        
        db.delete(sembrador)
        db.commit()
        
        return {
            "success": True,
            "message": f"Sembrador {id} eliminado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar sembrador: {str(e)}")


# ========== GET: Obtener sembradores para mapa ==========
@router.get("/map")
def obtener_sembradores_mapa(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener sembradores visibles en el mapa según rol y jerarquía.
    
    Filtrado jerárquico:
    - Admin: Ve todos los sembradores
    - Territorial: Ve sembradores de subordinados directos
    - Facilitador: Ve sembradores de técnicos bajo su supervisión
    - Técnico: Solo ve sus propios sembradores
    
    Response: Lista de sembradores con datos para visualizar en mapa
    """
    try:
        user_id = current_user["user_id"]
        rol = current_user["rol"]
        
        query = db.query(Sembrador)
        
        # 🔒 Filtrado jerárquico según rol
        if rol == "admin":
            # Admin ve todos
            pass
        elif rol == "territorial":
            # Territorial ve subordinados directos
            subordinado_ids = [
                u.id for u in db.query(User).filter(User.superior_id == user_id).all()
            ]
            if subordinado_ids:
                query = query.filter(Sembrador.user_id.in_(subordinado_ids))
            else:
                query = query.filter(Sembrador.user_id == user_id)
        elif rol in ["facilitador", "gestor_facilitador"]:
            # Facilitador ve técnicos productivos y sociales bajo su supervisión
            tecnico_ids = [
                u.id for u in db.query(User).filter(
                    User.superior_id == user_id,
                    User.rol.like("tecnico%")
                ).all()
            ]
            if tecnico_ids:
                query = query.filter(Sembrador.user_id.in_(tecnico_ids))
            else:
                query = query.filter(Sembrador.user_id == user_id)
        else:
            # Técnico (productivo o social) ve solo los suyos
            query = query.filter(Sembrador.user_id == user_id)
        
        sembradores = query.all()
        
        # Obtener rol del técnico para diferenciación
        usuarios_cache = {}
        
        resultado = []
        for s in sembradores:
            if s.user_id not in usuarios_cache:
                usuario = db.query(User).filter(User.id == s.user_id).first()
                usuarios_cache[s.user_id] = usuario
            
            usuario = usuarios_cache[s.user_id]
            
            resultado.append({
                "id": s.id,
                "nombre": s.nombre,
                "comunidad": s.comunidad,
                "cultivo": s.cultivo_principal,
                "lat": float(s.lat) if s.lat else None,
                "lng": float(s.lng) if s.lng else None,
                "user_id": s.user_id,
                "tecnico_nombre": usuario.nombre if usuario else "Desconocido",
                "tecnico_rol": usuario.rol if usuario else "desconocido",
                "creado_en": s.creado_en.isoformat() if s.creado_en else None
            })
        
        return {
            "success": True,
            "total": len(resultado),
            "items": resultado
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al obtener sembradores para mapa: {str(e)}")
