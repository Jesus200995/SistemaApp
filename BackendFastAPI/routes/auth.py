from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from models import User
import bcrypt, jwt, os
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "clave_super_segura")

router = APIRouter(prefix="/auth", tags=["auth"])
bearer_scheme = HTTPBearer()

# 🧩 Modelos Pydantic para validación de datos JSON
class RegisterRequest(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str

class LoginRequest(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existente = db.query(User).filter(User.email == request.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    hashed = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    nuevo = User(
        nombre=request.nombre,
        email=request.email,
        password=hashed,
        rol=request.rol
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"id": nuevo.id, "nombre": nuevo.nombre, "email": nuevo.email}

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    
    if not bcrypt.checkpw(request.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    token = jwt.encode(
        {"id": user.id, "email": user.email, "rol": user.rol},
        SECRET,
        algorithm="HS256"
    )
    return {"token": token, "user": {"id": user.id, "nombre": user.nombre, "rol": user.rol}}

@router.get("/me")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = db.query(User).filter(User.id == payload["id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "rol": user.rol,
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/users")
def list_users(
    page: int = 1,
    limit: int = 6,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        if payload.get("rol") != "admin":
            raise HTTPException(status_code=403, detail="No autorizado")

        total = db.query(User).count()
        users = db.query(User).offset((page - 1) * limit).limit(limit).all()

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "users": [
                {"id": u.id, "nombre": u.nombre, "email": u.email, "rol": u.rol}
                for u in users
            ],
        }
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
