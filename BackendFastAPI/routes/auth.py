from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import bcrypt, jwt, os
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "clave_super_segura")

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(nombre: str, email: str, password: str, rol: str, db: Session = Depends(get_db)):
    existente = db.query(User).filter(User.email == email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    nuevo = User(nombre=nombre, email=email, password=hashed, rol=rol)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"id": nuevo.id, "nombre": nuevo.nombre, "email": nuevo.email}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    token = jwt.encode({"id": user.id, "email": user.email, "rol": user.rol}, SECRET, algorithm="HS256")
    return {"token": token, "user": {"id": user.id, "nombre": user.nombre, "rol": user.rol}}
