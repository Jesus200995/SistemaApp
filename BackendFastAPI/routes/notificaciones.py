from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Notificacion, User
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "tu_clave_secreta")

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])
bearer = HTTPBearer()

# 🔔 Conexiones WebSocket activas
active_connections: List[WebSocket] = []


async def connect_ws(websocket: WebSocket):
    """Conectar cliente WebSocket"""
    await websocket.accept()
    active_connections.append(websocket)
    print(f"✅ Cliente conectado a notificaciones. Total: {len(active_connections)}")


async def disconnect_ws(websocket: WebSocket):
    """Desconectar cliente WebSocket"""
    if websocket in active_connections:
        active_connections.remove(websocket)
    print(f"🔴 Cliente desconectado. Total: {len(active_connections)}")


async def broadcast_notification(data: dict):
    """Enviar notificación a todos los clientes conectados"""
    for connection in active_connections:
        try:
            await connection.send_json(data)
        except Exception as e:
            print(f"❌ Error enviando notificación: {e}")


def verify_token(credentials: HTTPAuthorizationCredentials) -> dict:
    """Verificar JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ✅ WebSocket endpoint
@router.websocket("/ws")
async def websocket_notificaciones(websocket: WebSocket):
    """WebSocket para recibir notificaciones en tiempo real"""
    await connect_ws(websocket)
    try:
        while True:
            # Recibir heartbeat del cliente
            await websocket.receive_text()
    except WebSocketDisconnect:
        await disconnect_ws(websocket)
    except Exception as e:
        print(f"❌ Error en WebSocket: {e}")
        await disconnect_ws(websocket)


# ✅ Crear notificación
@router.post("/crear")
async def crear_notificacion(
    data: dict,
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    db: Session = Depends(get_db)
):
    """
    Crear una nueva notificación y enviarla a todos los clientes conectados
    
    - **titulo**: Título de la notificación
    - **mensaje**: Cuerpo del mensaje
    - **tipo**: info, warning, error, success
    - **rol_destino**: admin, usuario, all
    """
    try:
        # Verificar token
        payload = verify_token(credentials)
        
        # Validar datos
        titulo = data.get("titulo")
        mensaje = data.get("mensaje")
        tipo = data.get("tipo", "info")
        rol_destino = data.get("rol_destino", "all")
        
        if not titulo or not mensaje:
            raise HTTPException(
                status_code=400,
                detail="Título y mensaje son requeridos"
            )
        
        # Crear notificación en BD
        notificacion = Notificacion(
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo,
            rol_destino=rol_destino,
            leido=False
        )
        
        db.add(notificacion)
        db.commit()
        db.refresh(notificacion)
        
        # Enviar a todos los clientes WebSocket
        await broadcast_notification({
            "id": notificacion.id,
            "titulo": notificacion.titulo,
            "mensaje": notificacion.mensaje,
            "tipo": notificacion.tipo,
            "rol_destino": notificacion.rol_destino,
            "timestamp": notificacion.created_at.isoformat()
        })
        
        return {
            "success": True,
            "notificacion_id": notificacion.id,
            "mensaje": "Notificación creada y enviada"
        }
    
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


# ✅ Obtener todas las notificaciones
@router.get("/")
async def obtener_notificaciones(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    db: Session = Depends(get_db)
):
    """Obtener todas las notificaciones (ordenadas por fecha descendente)"""
    try:
        payload = verify_token(credentials)
        
        notificaciones = db.query(Notificacion).order_by(
            Notificacion.created_at.desc()
        ).all()
        
        return {
            "total": len(notificaciones),
            "notificaciones": [
                {
                    "id": n.id,
                    "titulo": n.titulo,
                    "mensaje": n.mensaje,
                    "tipo": n.tipo,
                    "leido": n.leido,
                    "timestamp": n.created_at.isoformat()
                }
                for n in notificaciones
            ]
        }
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


# ✅ Marcar notificación como leída
@router.patch("/{notif_id}/leer")
async def marcar_como_leida(
    notif_id: int,
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    db: Session = Depends(get_db)
):
    """Marcar una notificación como leída"""
    try:
        payload = verify_token(credentials)
        
        notificacion = db.query(Notificacion).filter(
            Notificacion.id == notif_id
        ).first()
        
        if not notificacion:
            raise HTTPException(
                status_code=404,
                detail="Notificación no encontrada"
            )
        
        notificacion.leido = True
        db.commit()
        
        return {
            "success": True,
            "mensaje": "Notificación marcada como leída"
        }
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


# ✅ Eliminar notificación
@router.delete("/{notif_id}")
async def eliminar_notificacion(
    notif_id: int,
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    db: Session = Depends(get_db)
):
    """Eliminar una notificación"""
    try:
        payload = verify_token(credentials)
        
        notificacion = db.query(Notificacion).filter(
            Notificacion.id == notif_id
        ).first()
        
        if not notificacion:
            raise HTTPException(
                status_code=404,
                detail="Notificación no encontrada"
            )
        
        db.delete(notificacion)
        db.commit()
        
        return {
            "success": True,
            "mensaje": "Notificación eliminada"
        }
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


# ✅ Obtener notificaciones no leídas
@router.get("/no-leidas/count")
async def contar_no_leidas(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    db: Session = Depends(get_db)
):
    """Contar notificaciones no leídas"""
    try:
        payload = verify_token(credentials)
        
        count = db.query(Notificacion).filter(
            Notificacion.leido == False
        ).count()
        
        return {
            "no_leidas": count
        }
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


# ✅ Estado del sistema de notificaciones
@router.get("/status/info")
async def notificacion_status():
    """Obtener estado del sistema de notificaciones"""
    return {
        "clientes_conectados": len(active_connections),
        "status": "✅ Sistema de notificaciones funcionando correctamente"
    }
