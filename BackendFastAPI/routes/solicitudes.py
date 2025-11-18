from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Solicitud, User
import jwt, os
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("SECRET_KEY")

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])
bearer_scheme = HTTPBearer()


@router.post("/")
def crear_solicitud(data: dict,
                    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
                    db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user_id = payload.get("id")

        nueva = Solicitud(
            tipo=data.get("tipo"),
            descripcion=data.get("descripcion"),
            usuario_id=user_id,
            destino_id=data.get("destino_id")
        )

        db.add(nueva)
        db.commit()
        db.refresh(nueva)
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

        solicitud.estado = data.get("estado")
        db.commit()
        db.refresh(solicitud)
        return {"success": True, "estado": solicitud.estado}

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
