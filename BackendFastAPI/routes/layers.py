from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Ambiental, Productiva, Social, Infraestructura, User
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET = os.getenv("SECRET_KEY")

router = APIRouter(prefix="/layers", tags=["Capas"])
bearer_scheme = HTTPBearer()

model_map = {
    "ambiental": Ambiental,
    "productiva": Productiva,
    "social": Social,
    "infraestructura": Infraestructura
}


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


# ========== GET: Obtener capas según jerarquía ==========
@router.get("/{tipo}")
def get_layer(
    tipo: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los puntos de una capa específica.
    Aplica filtros según la jerarquía del usuario:
    - admin: Ve todas las capas
    - territorial: Ve capas de usuarios subordinados
    - facilitador: Ve capas de técnicos a su cargo
    - técnico/otro: Ve solo sus propias capas
    """
    if tipo not in model_map:
        raise HTTPException(
            status_code=400,
            detail="Tipo de capa no válido. Usa: ambiental, productiva, social, infraestructura"
        )
    
    user_id = current_user["user_id"]
    rol = current_user["rol"]
    model = model_map[tipo]
    
    query = db.query(model)
    
    # 🔒 Filtros según jerarquía
    if rol == "admin":
        # Admin ve todo
        pass
    elif rol == "territorial":
        # Territorial ve capas de usuarios subordinados
        sub_ids = [u.id for u in db.query(User).filter(User.superior_id == user_id).all()]
        sub_ids.append(user_id)  # Incluye también sus propias capas
        query = query.filter(model.user_id.in_(sub_ids))
    elif rol == "facilitador":
        # Facilitador ve capas de técnicos a su cargo
        sub_ids = [u.id for u in db.query(User).filter(
            User.superior_id == user_id,
            User.rol.like("tecnico%")
        ).all()]
        sub_ids.append(user_id)  # Incluye también sus propias capas
        query = query.filter(model.user_id.in_(sub_ids))
    else:
        # Técnico/otro ve solo sus propias capas
        query = query.filter(model.user_id == user_id)
    
    items = query.all()
    
    return {
        "tipo": tipo,
        "total": len(items),
        "items": [
            {
                "id": i.id,
                "nombre": i.nombre,
                "descripcion": i.descripcion,
                "lat": i.lat,
                "lng": i.lng,
                "user_id": i.user_id,
                "created_at": i.created_at
            }
            for i in items
        ]
    }


# ========== POST: Crear nuevo punto ==========
@router.post("/{tipo}")
def create_layer(
    tipo: str,
    data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo punto en una capa específica.
    El punto se asocia automáticamente al usuario actual.
    
    Body esperado:
    {
        "nombre": "Nombre del punto",
        "descripcion": "Descripción detallada",
        "lat": 19.4326,
        "lng": -99.1332
    }
    """
    if tipo not in model_map:
        raise HTTPException(
            status_code=400,
            detail="Tipo de capa no válido. Usa: ambiental, productiva, social, infraestructura"
        )
    
    # Validar campos requeridos
    if not all(k in data for k in ["nombre", "lat", "lng"]):
        raise HTTPException(
            status_code=400,
            detail="Faltan campos requeridos: nombre, lat, lng"
        )
    
    try:
        user_id = current_user["user_id"]
        model = model_map[tipo]
        
        obj = model(
            nombre=data.get("nombre"),
            descripcion=data.get("descripcion"),
            lat=data.get("lat"),
            lng=data.get("lng"),
            user_id=user_id  # 🔑 Guardar user_id automáticamente
        )
        
        db.add(obj)
        db.commit()
        db.refresh(obj)
        
        return {
            "success": True,
            "id": obj.id,
            "tipo": tipo,
            "user_id": user_id,
            "message": f"Punto creado exitosamente en la capa {tipo}"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear punto: {str(e)}")


# ========== GET: Obtener punto específico ==========
@router.get("/{tipo}/{id}")
def get_layer_item(
    tipo: str,
    id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener un punto específico de una capa"""
    if tipo not in model_map:
        raise HTTPException(status_code=400, detail="Tipo de capa no válido")
    
    model = model_map[tipo]
    item = db.query(model).filter(model.id == id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    
    # 🔒 Verificar permisos de lectura
    user_id = current_user["user_id"]
    rol = current_user["rol"]
    
    if rol != "admin" and item.user_id != user_id:
        # Verificar si está en su jerarquía
        can_view = False
        if rol == "territorial":
            sub_ids = [u.id for u in db.query(User).filter(User.superior_id == user_id).all()]
            can_view = item.user_id in sub_ids
        elif rol == "facilitador":
            sub_ids = [u.id for u in db.query(User).filter(
                User.superior_id == user_id,
                User.rol.like("tecnico%")
            ).all()]
            can_view = item.user_id in sub_ids
        
        if not can_view:
            raise HTTPException(status_code=403, detail="No tienes permiso para ver este punto")
    
    return {
        "id": item.id,
        "nombre": item.nombre,
        "descripcion": item.descripcion,
        "lat": item.lat,
        "lng": item.lng,
        "user_id": item.user_id,
        "created_at": item.created_at
    }


# ========== PUT: Actualizar punto ==========
@router.put("/{tipo}/{id}")
def update_layer(
    tipo: str,
    id: int,
    data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar un punto específico de una capa"""
    if tipo not in model_map:
        raise HTTPException(status_code=400, detail="Tipo de capa no válido")
    
    model = model_map[tipo]
    item = db.query(model).filter(model.id == id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    
    # 🔒 Solo el propietario o admin puede actualizar
    user_id = current_user["user_id"]
    rol = current_user["rol"]
    
    if rol != "admin" and item.user_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar este punto")
    
    # Actualizar campos (excepto id, created_at y user_id)
    for key, value in data.items():
        if hasattr(item, key) and key not in ["id", "created_at", "user_id"]:
            setattr(item, key, value)
    
    db.commit()
    db.refresh(item)
    
    return {
        "success": True,
        "message": f"Punto {id} actualizado exitosamente",
        "item": {
            "id": item.id,
            "nombre": item.nombre,
            "descripcion": item.descripcion,
            "lat": item.lat,
            "lng": item.lng,
            "user_id": item.user_id
        }
    }


# ========== DELETE: Eliminar punto ==========
@router.delete("/{tipo}/{id}")
def delete_layer(
    tipo: str,
    id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar un punto específico de una capa"""
    if tipo not in model_map:
        raise HTTPException(status_code=400, detail="Tipo de capa no válido")
    
    model = model_map[tipo]
    item = db.query(model).filter(model.id == id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    
    # 🔒 Solo el propietario o admin puede eliminar
    user_id = current_user["user_id"]
    rol = current_user["rol"]
    
    if rol != "admin" and item.user_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este punto")
    
    db.delete(item)
    db.commit()
    
    return {
        "success": True,
        "message": f"Punto {id} eliminado exitosamente"
    }

