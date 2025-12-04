from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Solicitud, User, Notificacion
import jwt, os
from dotenv import load_dotenv
import asyncio

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "mi_clave_jwt_2025")

# Importar broadcast_notification desde notificaciones
async def broadcast_notification(data: dict):
    """
    Función auxiliar para enviar notificaciones.
    Se importará desde routes.notificaciones
    """
    pass  # Será reemplazado por la importación real

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])
bearer_scheme = HTTPBearer()


@router.post("/")
def crear_solicitud(data: dict,
                    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
                    db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        rol = payload.get("rol")

        nueva = Solicitud(
            tipo=data.get("tipo"),
            descripcion=data.get("descripcion"),
            usuario_id=user_id,
            destino_id=data.get("destino_id")
        )

        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        # 🔔 Crear notificación para el destino
        if data.get("destino_id"):
            usuario_destino = db.query(User).filter(User.id == data.get("destino_id")).first()
            notif = Notificacion(
                titulo="Nueva solicitud recibida",
                mensaje=f"Has recibido una solicitud de {rol} (ID: {user_id}).",
                tipo="solicitud",
                user_destino=data.get("destino_id"),
                usuario_id=user_id,
                solicitud_id=nueva.id
            )
            db.add(notif)
            db.commit()
            db.refresh(notif)

            # 🔄 Emitir en tiempo real (será consumida por WebSocket)
            # Este broadcast se ejecutará en segundo plano
            print(f"✅ Notificación creada para usuario {data.get('destino_id')}: {notif.id}")

        return {"success": True, "solicitud_id": nueva.id}

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.get("/")
def listar_solicitudes(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
                       db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        rol = payload.get("rol")

        query = db.query(Solicitud)

        if rol == "admin":
            pass
        elif rol in ["territorial", "facilitador"]:
            query = query.filter(Solicitud.destino_id == user_id)
        else:
            query = query.filter(Solicitud.usuario_id == user_id)

        return query.order_by(Solicitud.fecha.desc()).all()

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.put("/{id}/estado")
def actualizar_estado(id: int, data: dict,
                      credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
                      db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user_id = payload.get("id")

        solicitud = db.query(Solicitud).filter(Solicitud.id == id).first()
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")

        nuevo_estado = data.get("estado")
        solicitud.estado = nuevo_estado
        db.commit()
        db.refresh(solicitud)

        # 🔔 Enviar notificación al solicitante
        notif = Notificacion(
            titulo="Actualización de solicitud",
            mensaje=f"Tu solicitud ha sido {nuevo_estado}.",
            tipo="respuesta",
            user_destino=solicitud.usuario_id,
            usuario_id=user_id,
            solicitud_id=solicitud.id
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)

        print(f"✅ Notificación de respuesta creada para usuario {solicitud.usuario_id}: {notif.id}")

        return {"success": True, "estado": solicitud.estado}

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
