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
    
    Jerarquía:
    - Técnico → puede enviar a Facilitador, Territorial, Admin
    - Facilitador → puede enviar a Territorial, Admin
    - Territorial → puede enviar a Admin
    - Admin → puede enviar a cualquiera (Admin)
    
    Retorna lista de usuarios con id, nombre, rol y territorio
    """
    rol_actual = current_user["rol"]
    user_id = current_user["user_id"]
    
    # Definir roles superiores según jerarquía
    roles_superiores = {
        "tecnico": ["facilitador", "territorial", "admin"],
        "facilitador": ["territorial", "admin"],
        "territorial": ["admin"],
        "admin": ["admin", "territorial", "facilitador", "tecnico"]  # Admin puede enviar a cualquiera
    }
    
    roles_permitidos = roles_superiores.get(rol_actual, [])
    
    if not roles_permitidos:
        return {"items": [], "mensaje": "No tienes usuarios superiores disponibles"}
    
    # Consultar usuarios con esos roles (excluyendo al usuario actual)
    usuarios = db.query(User).filter(
        User.rol.in_(roles_permitidos),
        User.id != user_id,
        User.activo == True
    ).order_by(User.rol, User.nombre).all()
    
    # Formatear respuesta
    resultado = []
    for u in usuarios:
        resultado.append({
            "id": u.id,
            "nombre": u.nombre,
            "rol": u.rol,
            "territorio": u.territorio or "Sin territorio",
            "email": u.email
        })
    
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
