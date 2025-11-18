from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from database import get_db
from models import Seguimiento, Sembrador, User
from datetime import datetime
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("SECRET_KEY")

router = APIRouter(prefix="/seguimientos", tags=["Seguimiento de Campo"])
bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    """Extrae y valida el token JWT"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        rol = payload.get("rol")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return {"user_id": user_id, "rol": rol}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")


@router.post("/crear")
def crear_seguimiento(
    data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo seguimiento de campo
    
    Body esperado:
    {
        "sembrador_id": 1,
        "fecha_visita": "2024-01-15T10:30:00",
        "estado_cultivo": "Germinando",
        "observaciones": "Cultivo en buen estado",
        "avance_porcentaje": 25.5,
        "foto_url": "https://..."
    }
    """
    try:
        user_id = current_user["user_id"]
        
        if not data.get("sembrador_id"):
            raise HTTPException(status_code=400, detail="Debe indicar el sembrador")
        
        # Verificar que el sembrador existe
        sembrador = db.query(Sembrador).filter(Sembrador.id == data.get("sembrador_id")).first()
        if not sembrador:
            raise HTTPException(status_code=404, detail="Sembrador no encontrado")
        
        # Crear nuevo seguimiento
        nuevo_seguimiento = Seguimiento(
            sembrador_id=data.get("sembrador_id"),
            user_id=user_id,
            fecha_visita=datetime.fromisoformat(data.get("fecha_visita")) if data.get("fecha_visita") else datetime.now(),
            estado_cultivo=data.get("estado_cultivo"),
            observaciones=data.get("observaciones"),
            avance_porcentaje=data.get("avance_porcentaje", 0.0),
            foto_url=data.get("foto_url")
        )
        
        db.add(nuevo_seguimiento)
        db.commit()
        db.refresh(nuevo_seguimiento)
        
        return {
            "success": True,
            "id": nuevo_seguimiento.id,
            "mensaje": "Seguimiento creado exitosamente"
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error en formato de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear seguimiento: {str(e)}")


@router.get("/")
def listar_seguimientos(
    sembrador_id: int = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista seguimientos con filtrado jerárquico
    
    Parámetros:
    - sembrador_id: (opcional) Filtrar por sembrador
    
    Filtrado:
    - Admin: Ve todos
    - Territorial: Ve de subordinados directos
    - Facilitador: Ve de técnicos bajo supervisión
    - Técnico: Solo sus propios seguimientos
    """
    try:
        user_id = current_user["user_id"]
        rol = current_user["rol"]
        
        query = db.query(
            Seguimiento.id,
            Seguimiento.sembrador_id,
            Seguimiento.user_id,
            Seguimiento.fecha_visita,
            Seguimiento.estado_cultivo,
            Seguimiento.observaciones,
            Seguimiento.avance_porcentaje,
            Seguimiento.foto_url,
            Seguimiento.creado_en,
            Sembrador.nombre.label("sembrador_nombre"),
            Sembrador.comunidad,
            Sembrador.cultivo_principal,
            User.nombre.label("tecnico_nombre"),
            User.rol.label("tecnico_rol")
        ).outerjoin(Sembrador, Seguimiento.sembrador_id == Sembrador.id)\
         .outerjoin(User, Seguimiento.user_id == User.id)
        
        # Aplicar filtrado según rol
        if rol == "admin":
            pass  # Ve todo
        elif rol == "territorial":
            # Ve subordinados directos
            subordinado_ids = [u.id for u in db.query(User).filter(User.superior_id == user_id).all()]
            if subordinado_ids:
                query = query.filter(Seguimiento.user_id.in_(subordinado_ids))
            else:
                return {"success": True, "total": 0, "items": []}
        elif rol in ["facilitador", "gestor_facilitador"]:
            # Ve técnicos bajo supervisión
            tecnico_ids = [u.id for u in db.query(User).filter(
                User.superior_id == user_id,
                User.rol.like("tecnico%")
            ).all()]
            if tecnico_ids:
                query = query.filter(Seguimiento.user_id.in_(tecnico_ids))
            else:
                return {"success": True, "total": 0, "items": []}
        else:
            # Técnico: solo propios
            query = query.filter(Seguimiento.user_id == user_id)
        
        # Filtro adicional por sembrador si se proporciona
        if sembrador_id:
            query = query.filter(Seguimiento.sembrador_id == sembrador_id)
        
        # Ordenar por fecha más reciente
        query = query.order_by(Seguimiento.fecha_visita.desc())
        
        seguimientos = query.all()
        
        items = [
            {
                "id": s[0],
                "sembrador_id": s[1],
                "user_id": s[2],
                "fecha_visita": s[3].isoformat() if s[3] else None,
                "estado_cultivo": s[4],
                "observaciones": s[5],
                "avance_porcentaje": s[6],
                "foto_url": s[7],
                "creado_en": s[8].isoformat() if s[8] else None,
                "sembrador_nombre": s[9],
                "comunidad": s[10],
                "cultivo_principal": s[11],
                "tecnico_nombre": s[12],
                "tecnico_rol": s[13]
            }
            for s in seguimientos
        ]
        
        return {
            "success": True,
            "total": len(items),
            "items": items
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar seguimientos: {str(e)}")


@router.get("/{seguimiento_id}")
def obtener_seguimiento(
    seguimiento_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene un seguimiento específico"""
    try:
        user_id = current_user["user_id"]
        rol = current_user["rol"]
        
        seguimiento = db.query(Seguimiento).filter(Seguimiento.id == seguimiento_id).first()
        
        if not seguimiento:
            raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
        
        # Validar acceso según rol
        if rol == "tecnico" and seguimiento.user_id != user_id:
            raise HTTPException(status_code=403, detail="No tienes acceso a este seguimiento")
        
        # Obtener datos relacionados
        sembrador = db.query(Sembrador).filter(Sembrador.id == seguimiento.sembrador_id).first()
        tecnico = db.query(User).filter(User.id == seguimiento.user_id).first()
        
        return {
            "success": True,
            "id": seguimiento.id,
            "sembrador_id": seguimiento.sembrador_id,
            "sembrador_nombre": sembrador.nombre if sembrador else None,
            "comunidad": sembrador.comunidad if sembrador else None,
            "cultivo_principal": sembrador.cultivo_principal if sembrador else None,
            "user_id": seguimiento.user_id,
            "tecnico_nombre": tecnico.nombre if tecnico else None,
            "tecnico_rol": tecnico.rol if tecnico else None,
            "fecha_visita": seguimiento.fecha_visita.isoformat() if seguimiento.fecha_visita else None,
            "estado_cultivo": seguimiento.estado_cultivo,
            "observaciones": seguimiento.observaciones,
            "avance_porcentaje": seguimiento.avance_porcentaje,
            "foto_url": seguimiento.foto_url,
            "creado_en": seguimiento.creado_en.isoformat() if seguimiento.creado_en else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener seguimiento: {str(e)}")


@router.put("/{seguimiento_id}")
def actualizar_seguimiento(
    seguimiento_id: int,
    data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualiza un seguimiento existente"""
    try:
        user_id = current_user["user_id"]
        
        seguimiento = db.query(Seguimiento).filter(Seguimiento.id == seguimiento_id).first()
        
        if not seguimiento:
            raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
        
        # Solo el creador puede actualizar
        if seguimiento.user_id != user_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para actualizar este seguimiento")
        
        # Actualizar campos
        if "fecha_visita" in data:
            seguimiento.fecha_visita = datetime.fromisoformat(data["fecha_visita"])
        if "estado_cultivo" in data:
            seguimiento.estado_cultivo = data["estado_cultivo"]
        if "observaciones" in data:
            seguimiento.observaciones = data["observaciones"]
        if "avance_porcentaje" in data:
            seguimiento.avance_porcentaje = data["avance_porcentaje"]
        if "foto_url" in data:
            seguimiento.foto_url = data["foto_url"]
        
        db.commit()
        db.refresh(seguimiento)
        
        return {
            "success": True,
            "mensaje": "Seguimiento actualizado exitosamente",
            "id": seguimiento.id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar seguimiento: {str(e)}")


@router.delete("/{seguimiento_id}")
def eliminar_seguimiento(
    seguimiento_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elimina un seguimiento"""
    try:
        user_id = current_user["user_id"]
        
        seguimiento = db.query(Seguimiento).filter(Seguimiento.id == seguimiento_id).first()
        
        if not seguimiento:
            raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
        
        # Solo el creador puede eliminar
        if seguimiento.user_id != user_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este seguimiento")
        
        db.delete(seguimiento)
        db.commit()
        
        return {
            "success": True,
            "mensaje": "Seguimiento eliminado exitosamente"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar seguimiento: {str(e)}")


@router.get("/reportes/por-tecnico")
def reportes_por_tecnico(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Genera reporte de seguimientos por técnico
    Muestra: técnico, cantidad de seguimientos, último seguimiento, avance promedio
    """
    try:
        user_id = current_user["user_id"]
        rol = current_user["rol"]
        
        query = db.query(User).filter(User.id != user_id)
        
        # Filtrar según rol
        if rol == "territorial":
            subordinado_ids = [u.id for u in db.query(User).filter(User.superior_id == user_id).all()]
            query = query.filter(User.id.in_(subordinado_ids))
        elif rol in ["facilitador", "gestor_facilitador"]:
            tecnico_ids = [u.id for u in db.query(User).filter(
                User.superior_id == user_id,
                User.rol.like("tecnico%")
            ).all()]
            query = query.filter(User.id.in_(tecnico_ids))
        else:
            return {"success": True, "items": []}
        
        tecnicos = query.all()
        
        reportes = []
        for tecnico in tecnicos:
            seguimientos = db.query(Seguimiento).filter(Seguimiento.user_id == tecnico.id).all()
            
            if seguimientos:
                avance_promedio = sum([s.avance_porcentaje or 0 for s in seguimientos]) / len(seguimientos)
                ultimo_seguimiento = max([s.fecha_visita for s in seguimientos if s.fecha_visita])
            else:
                avance_promedio = 0
                ultimo_seguimiento = None
            
            reportes.append({
                "tecnico_id": tecnico.id,
                "tecnico_nombre": tecnico.nombre,
                "rol": tecnico.rol,
                "total_seguimientos": len(seguimientos),
                "avance_promedio": round(avance_promedio, 2),
                "ultimo_seguimiento": ultimo_seguimiento.isoformat() if ultimo_seguimiento else None
            })
        
        return {
            "success": True,
            "total": len(reportes),
            "items": reportes
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")


@router.get("/reportes/por-cultivo")
def reportes_por_cultivo(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Genera reporte de seguimientos por cultivo
    Muestra: cultivo, cantidad de sembradores, avance promedio
    """
    try:
        user_id = current_user["user_id"]
        rol = current_user["rol"]
        
        # Construir query base de seguimientos
        query = db.query(Seguimiento)
        
        # Filtrar según rol
        if rol == "territorial":
            subordinado_ids = [u.id for u in db.query(User).filter(User.superior_id == user_id).all()]
            query = query.filter(Seguimiento.user_id.in_(subordinado_ids))
        elif rol in ["facilitador", "gestor_facilitador"]:
            tecnico_ids = [u.id for u in db.query(User).filter(
                User.superior_id == user_id,
                User.rol.like("tecnico%")
            ).all()]
            query = query.filter(Seguimiento.user_id.in_(tecnico_ids))
        elif rol != "admin":
            query = query.filter(Seguimiento.user_id == user_id)
        
        seguimientos = query.all()
        
        # Agrupar por cultivo
        cultivos_map = {}
        
        for seg in seguimientos:
            sembrador = db.query(Sembrador).filter(Sembrador.id == seg.sembrador_id).first()
            
            if sembrador and sembrador.cultivo_principal:
                cultivo = sembrador.cultivo_principal
                
                if cultivo not in cultivos_map:
                    cultivos_map[cultivo] = {
                        "cultivo": cultivo,
                        "sembradores": set(),
                        "avances": []
                    }
                
                cultivos_map[cultivo]["sembradores"].add(seg.sembrador_id)
                cultivos_map[cultivo]["avances"].append(seg.avance_porcentaje or 0)
        
        reportes = []
        for cultivo, data in cultivos_map.items():
            avance_promedio = sum(data["avances"]) / len(data["avances"]) if data["avances"] else 0
            reportes.append({
                "cultivo": cultivo,
                "total_sembradores": len(data["sembradores"]),
                "total_seguimientos": len(data["avances"]),
                "avance_promedio": round(avance_promedio, 2)
            })
        
        return {
            "success": True,
            "total": len(reportes),
            "items": sorted(reportes, key=lambda x: x["avance_promedio"], reverse=True)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")
