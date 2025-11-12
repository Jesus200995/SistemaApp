from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Ambiental, Productiva, Social, Infraestructura
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET = os.getenv("SECRET_KEY")

router = APIRouter(prefix="/layers", tags=["Capas"])
bearer_scheme = HTTPBearer()


def authorize(credentials: HTTPAuthorizationCredentials):
    """Validar token JWT"""
    try:
        token = credentials.credentials
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Token inválido")


# Obtener todas las capas de un tipo específico
@router.get("/{tipo}")
def get_layer(
    tipo: str,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los puntos de una capa específica.
    Tipos válidos: ambiental, productiva, social, infraestructura
    """
    authorize(credentials)
    
    model_map = {
        "ambiental": Ambiental,
        "productiva": Productiva,
        "social": Social,
        "infraestructura": Infraestructura
    }
    
    if tipo not in model_map:
        raise HTTPException(
            status_code=400,
            detail="Tipo de capa no válido. Usa: ambiental, productiva, social, infraestructura"
        )
    
    items = db.query(model_map[tipo]).all()
    
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
                "created_at": i.created_at
            }
            for i in items
        ]
    }


# Crear nuevo punto en una capa
@router.post("/{tipo}")
def create_layer(
    tipo: str,
    data: dict,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo punto en una capa específica.
    
    Body esperado:
    {
        "nombre": "Nombre del punto",
        "descripcion": "Descripción detallada",
        "lat": 19.4326,
        "lng": -99.1332
    }
    """
    authorize(credentials)
    
    model_map = {
        "ambiental": Ambiental,
        "productiva": Productiva,
        "social": Social,
        "infraestructura": Infraestructura
    }
    
    if tipo not in model_map:
        raise HTTPException(
            status_code=400,
            detail="Tipo de capa no válido. Usa: ambiental, productiva, social, infraestructura"
        )
    
    # Validar que tenga campos requeridos
    if not all(k in data for k in ["nombre", "lat", "lng"]):
        raise HTTPException(
            status_code=400,
            detail="Faltan campos requeridos: nombre, lat, lng"
        )
    
    try:
        obj = model_map[tipo](**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        
        return {
            "success": True,
            "id": obj.id,
            "tipo": tipo,
            "message": f"Punto creado exitosamente en la capa {tipo}"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear punto: {str(e)}")


# Obtener un punto específico
@router.get("/{tipo}/{id}")
def get_layer_item(
    tipo: str,
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    """Obtener un punto específico de una capa"""
    authorize(credentials)
    
    model_map = {
        "ambiental": Ambiental,
        "productiva": Productiva,
        "social": Social,
        "infraestructura": Infraestructura
    }
    
    if tipo not in model_map:
        raise HTTPException(status_code=400, detail="Tipo de capa no válido")
    
    item = db.query(model_map[tipo]).filter(model_map[tipo].id == id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    
    return {
        "id": item.id,
        "nombre": item.nombre,
        "descripcion": item.descripcion,
        "lat": item.lat,
        "lng": item.lng,
        "created_at": item.created_at
    }


# Actualizar un punto
@router.put("/{tipo}/{id}")
def update_layer(
    tipo: str,
    id: int,
    data: dict,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    """Actualizar un punto específico de una capa"""
    authorize(credentials)
    
    model_map = {
        "ambiental": Ambiental,
        "productiva": Productiva,
        "social": Social,
        "infraestructura": Infraestructura
    }
    
    if tipo not in model_map:
        raise HTTPException(status_code=400, detail="Tipo de capa no válido")
    
    item = db.query(model_map[tipo]).filter(model_map[tipo].id == id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    
    # Actualizar campos
    for key, value in data.items():
        if hasattr(item, key) and key != "id" and key != "created_at":
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
            "lng": item.lng
        }
    }


# Eliminar un punto
@router.delete("/{tipo}/{id}")
def delete_layer(
    tipo: str,
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    """Eliminar un punto específico de una capa"""
    authorize(credentials)
    
    model_map = {
        "ambiental": Ambiental,
        "productiva": Productiva,
        "social": Social,
        "infraestructura": Infraestructura
    }
    
    if tipo not in model_map:
        raise HTTPException(status_code=400, detail="Tipo de capa no válido")
    
    item = db.query(model_map[tipo]).filter(model_map[tipo].id == id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Punto no encontrado")
    
    db.delete(item)
    db.commit()
    
    return {
        "success": True,
        "message": f"Punto {id} eliminado exitosamente"
    }
