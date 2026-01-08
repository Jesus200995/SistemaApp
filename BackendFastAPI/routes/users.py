from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "mi_clave_jwt_2025")

router = APIRouter(prefix="/users", tags=["Usuarios"])
bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    """Extrae y valida el token JWT"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        rol = payload.get("rol")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return {"user_id": user_id, "rol": rol}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")


@router.get("/superiores")
def obtener_usuarios_superiores(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de usuarios a los que se puede enviar solicitud según la jerarquía:
    
    Jerarquía (de menor a mayor):
    - Técnico/Técnico Productivo → puede enviar a Facilitador, Territorial, Admin
    - Facilitador → puede enviar a Territorial, Admin
    - Territorial → puede enviar a Admin
    - Admin → puede enviar a cualquiera
    
    Retorna lista de usuarios con id, nombre, rol y territorio
    """
    rol_actual = current_user["rol"]
    user_id = current_user["user_id"]
    
    print(f"🔍 Usuario {user_id} con rol '{rol_actual}' solicitando superiores")
    
    # Normalizar rol (convertir a minúsculas y reemplazar espacios/guiones)
    rol_normalizado = rol_actual.lower().strip().replace(" ", "_").replace("-", "_")
    
    # Mapeo de roles normalizados a categorías
    # Cualquier variante de "tecnico" (tecnico, tecnico_productivo, técnico, etc.)
    if "tecnico" in rol_normalizado or "técnico" in rol_normalizado:
        categoria_rol = "tecnico"
    elif "facilitador" in rol_normalizado:
        categoria_rol = "facilitador"
    elif "territorial" in rol_normalizado:
        categoria_rol = "territorial"
    elif "admin" in rol_normalizado:
        categoria_rol = "admin"
    else:
        categoria_rol = rol_normalizado
    
    print(f"📂 Rol normalizado: '{rol_normalizado}' -> Categoría: '{categoria_rol}'")
    
    # Definir qué roles pueden recibir solicitudes según la categoría del usuario
    roles_destino = {
        "tecnico": ["facilitador", "territorial", "admin"],
        "facilitador": ["territorial", "admin"],
        "territorial": ["admin"],
        "admin": ["admin", "territorial", "facilitador", "tecnico"]
    }
    
    categorias_destino = roles_destino.get(categoria_rol, [])
    
    if not categorias_destino:
        print(f"⚠️ No hay destinos para el rol '{categoria_rol}'")
        return {"items": [], "mensaje": f"No hay usuarios disponibles para el rol '{rol_actual}'"}
    
    print(f"🎯 Buscando usuarios con roles que contengan: {categorias_destino}")
    
    # Consultar TODOS los usuarios activos excepto el actual
    todos_usuarios = db.query(User).filter(
        User.id != user_id,
        User.activo == True
    ).all()
    
    # Filtrar usuarios cuyo rol normalizado coincida con las categorías destino
    resultado = []
    for u in todos_usuarios:
        rol_usuario = u.rol.lower().strip().replace(" ", "_").replace("-", "_") if u.rol else ""
        
        # Verificar si el rol del usuario pertenece a alguna categoría destino
        es_destino_valido = False
        for cat in categorias_destino:
            if cat in rol_usuario or rol_usuario == cat:
                es_destino_valido = True
                break
        
        if es_destino_valido:
            resultado.append({
                "id": u.id,
                "nombre": u.nombre,
                "rol": u.rol,
                "territorio": u.territorio or "Sin territorio",
                "email": u.email
            })
    
    # Ordenar por rol y nombre
    resultado.sort(key=lambda x: (x["rol"], x["nombre"]))
    
    print(f"✅ Encontrados {len(resultado)} usuarios disponibles")
    
    return {
        "items": resultado,
        "total": len(resultado)
    }


@router.get("/mi-superior")
def obtener_mi_superior(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el superior directo del usuario actual (basado en superior_id)
    """
    user_id = current_user["user_id"]
    
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not usuario.superior_id:
        return {"superior": None, "mensaje": "No tienes superior asignado"}
    
    superior = db.query(User).filter(User.id == usuario.superior_id).first()
    if not superior:
        return {"superior": None, "mensaje": "Superior no encontrado"}
    
    return {
        "superior": {
            "id": superior.id,
            "nombre": superior.nombre,
            "rol": superior.rol,
            "territorio": superior.territorio,
            "email": superior.email
        }
    }


@router.get("/subordinados")
def obtener_usuarios_subordinados(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de usuarios subordinados (debajo en la jerarquía) que pueden
    ser afectados por una solicitud de Alta/Baja/Reasignación.
    
    Jerarquía (de mayor a menor):
    - Admin → puede afectar a Territorial, Facilitador, Técnico
    - Territorial → puede afectar a Facilitador, Técnico (de su territorio)
    - Facilitador → puede afectar a Técnico (de su ruta)
    - Técnico → no puede afectar a nadie
    
    Retorna lista de usuarios con id, nombre, rol, territorio, activo
    """
    rol_actual = current_user["rol"]
    user_id = current_user["user_id"]
    
    # Obtener datos del usuario actual
    usuario_actual = db.query(User).filter(User.id == user_id).first()
    
    print(f"🔍 Usuario {user_id} con rol '{rol_actual}' solicitando subordinados")
    
    # Normalizar rol
    rol_normalizado = rol_actual.lower().strip().replace(" ", "_").replace("-", "_")
    
    # Mapeo de roles normalizados a categorías
    if "tecnico" in rol_normalizado or "técnico" in rol_normalizado:
        categoria_rol = "tecnico"
    elif "facilitador" in rol_normalizado:
        categoria_rol = "facilitador"
    elif "territorial" in rol_normalizado:
        categoria_rol = "territorial"
    elif "admin" in rol_normalizado:
        categoria_rol = "admin"
    else:
        categoria_rol = rol_normalizado
    
    print(f"📂 Rol normalizado: '{rol_normalizado}' -> Categoría: '{categoria_rol}'")
    
    # Definir qué roles pueden ser afectados por cada categoría
    roles_subordinados = {
        "admin": ["territorial", "facilitador", "tecnico"],
        "territorial": ["facilitador", "tecnico"],
        "facilitador": ["tecnico"],
        "tecnico": []
    }
    
    categorias_subordinados = roles_subordinados.get(categoria_rol, [])
    
    if not categorias_subordinados:
        print(f"⚠️ No hay subordinados para el rol '{categoria_rol}'")
        return {"items": [], "mensaje": f"No tienes usuarios subordinados"}
    
    print(f"🎯 Buscando usuarios con roles: {categorias_subordinados}")
    
    # Consultar usuarios (según rol y territorio si aplica)
    query = db.query(User).filter(User.id != user_id)
    
    # Si no es admin, filtrar por territorio
    if categoria_rol == "territorial" and usuario_actual and usuario_actual.territorio_id:
        query = query.filter(User.territorio_id == usuario_actual.territorio_id)
    
    todos_usuarios = query.all()
    
    # Filtrar usuarios cuyo rol coincida con categorías subordinadas
    resultado = []
    for u in todos_usuarios:
        rol_usuario = u.rol.lower().strip().replace(" ", "_").replace("-", "_") if u.rol else ""
        
        # Verificar si el rol del usuario pertenece a alguna categoría subordinada
        es_subordinado = False
        for cat in categorias_subordinados:
            if cat in rol_usuario or rol_usuario == cat:
                es_subordinado = True
                break
        
        if es_subordinado:
            resultado.append({
                "id": u.id,
                "nombre": u.nombre,
                "rol": u.rol,
                "perfil_operativo": u.perfil_operativo,
                "territorio": u.territorio or "Sin territorio",
                "email": u.email,
                "activo": u.activo,
                "curp": u.curp
            })
    
    # Ordenar por rol y nombre
    resultado.sort(key=lambda x: (x["rol"], x["nombre"]))
    
    print(f"✅ Encontrados {len(resultado)} usuarios subordinados")
    
    return {
        "items": resultado,
        "total": len(resultado)
    }


@router.get("/me")
def obtener_mi_perfil(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene el perfil del usuario actual
    """
    user_id = current_user["user_id"]
    
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": usuario.rol,
        "territorio": usuario.territorio,
        "telefono": usuario.telefono,
        "curp": usuario.curp,
        "activo": usuario.activo,
        "superior_id": usuario.superior_id
    }
