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

class UpdateUserRequest(BaseModel):
    nombre: str | None = None
    email: str | None = None
    rol: str | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario.
    
    🔐 Seguridad:
    - Valida que no exista un usuario con el mismo email
    - Hash la contraseña con bcrypt
    - Por defecto se registra como "tecnico"
    - Asigna automáticamente el primer territorial como superior
    
    📧 Notificaciones:
    - Notifica al admin cuando se registra un nuevo usuario
    """
    from models import Notificacion
    import re
    
    # ✅ Validar email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, request.email):
        raise HTTPException(status_code=400, detail="Email inválido")
    
    # ✅ Validar nombre (mínimo 2 caracteres)
    if len(request.nombre.strip()) < 2:
        raise HTTPException(status_code=400, detail="El nombre debe tener al menos 2 caracteres")
    
    # ✅ Validar contraseña (mínimo 6 caracteres)
    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")
    
    # ✅ Validar rol permitido
    roles_permitidos = ["tecnico_productivo", "tecnico_social", "facilitador", "territorial", "admin"]
    rol = request.rol.lower() if request.rol else "tecnico_productivo"
    if rol not in roles_permitidos:
        raise HTTPException(status_code=400, detail=f"Rol inválido. Permite: {', '.join(roles_permitidos)}")
    
    # ✅ Verificar si el email ya existe
    existente = db.query(User).filter(User.email == request.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # ✅ Hashear contraseña
    hashed = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    # ✅ Crear nuevo usuario
    nuevo = User(
        nombre=request.nombre.strip(),
        email=request.email.strip().lower(),
        password=hashed,
        rol=rol,
        superior_id=None  # Será asignado por admin después
    )
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    
    # 📧 Crear notificación para los admins
    try:
        notificacion = Notificacion(
            titulo=f"Nuevo usuario registrado",
            mensaje=f"{nuevo.nombre} ({nuevo.email}) se registró como {rol.upper()}",
            tipo="info",
            rol_destino="admin"
        )
        db.add(notificacion)
        db.commit()
    except Exception as e:
        print(f"⚠️ Error al crear notificación: {str(e)}")
        db.rollback()
    
    return {
        "success": True,
        "id": nuevo.id,
        "nombre": nuevo.nombre,
        "email": nuevo.email,
        "rol": nuevo.rol,
        "message": "Usuario registrado exitosamente. Un administrador revisará tu solicitud."
    }

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
    rol: str | None = None,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        current_user_id = payload.get("id")
        current_rol = payload.get("rol")
        
        query = db.query(User)
        
        # 🔒 Filtros según jerarquía del usuario actual
        if current_rol == "admin":
            # Admin ve todos los usuarios
            pass
        elif current_rol == "territorial":
            # Territorial ve solo sus subordinados
            sub_ids = [u.id for u in db.query(User).filter(User.superior_id == current_user_id).all()]
            query = query.filter(User.id.in_(sub_ids))
        elif current_rol == "facilitador":
            # Facilitador ve solo sus técnicos subordinados
            sub_ids = [u.id for u in db.query(User).filter(
                User.superior_id == current_user_id,
                User.rol.like("tecnico%")
            ).all()]
            query = query.filter(User.id.in_(sub_ids))
        else:
            # Otros usuarios solo se ven a sí mismos
            query = query.filter(User.id == current_user_id)
        
        # Filtro adicional por rol si se especifica
        if rol:
            query = query.filter(User.rol == rol)

        total = query.count()
        users = query.offset((page - 1) * limit).limit(limit).all()

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "users": [
                {
                    "id": u.id,
                    "nombre": u.nombre,
                    "email": u.email,
                    "rol": u.rol,
                    "lat": None,
                    "lng": None,
                }
                for u in users
            ],
        }
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    body: UpdateUserRequest,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        if payload.get("rol") != "admin":
            raise HTTPException(status_code=403, detail="No autorizado")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if body.nombre:
            user.nombre = body.nombre
        if body.email:
            user.email = body.email
        if body.rol:
            user.rol = body.rol

        db.commit()
        db.refresh(user)
        return {"success": True, "user": {"id": user.id, "nombre": user.nombre, "email": user.email, "rol": user.rol}}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        if payload.get("rol") != "admin":
            raise HTTPException(status_code=403, detail="No autorizado")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.delete(user)
        db.commit()
        return {"success": True, "message": f"Usuario {user.nombre} eliminado correctamente"}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.get("/admin/overview")
def admin_overview(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    """
    Panel de control global del administrador.
    
    🔐 Seguridad:
    - Solo usuarios con rol "admin" pueden acceder
    - Retorna totales del sistema y métricas clave
    
    📊 Datos retornados:
    - total_usuarios: Cantidad total de usuarios en el sistema
    - total_sembradores: Cantidad total de sembradores
    - total_seguimientos: Cantidad total de seguimientos
    - pendientes: Cantidad de solicitudes en estado "pendiente"
    - promedio_avance: Porcentaje promedio de avance global
    """
    try:
        from models import Sembrador, Seguimiento, Solicitud
        
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        
        if payload.get("rol") != "admin":
            raise HTTPException(status_code=403, detail="Solo el administrador puede acceder")
        
        # ✅ Calcular totales
        total_usuarios = db.query(User).count()
        total_sembradores = db.query(Sembrador).count()
        total_seguimientos = db.query(Seguimiento).count()
        pendientes = db.query(Solicitud).filter(Solicitud.estado == "pendiente").count()
        
        # ✅ Calcular promedio de avance global
        seguimientos = db.query(Seguimiento).all()
        promedio_avance = round(
            (sum([s.avance_porcentaje or 0 for s in seguimientos]) / len(seguimientos)), 2
        ) if len(seguimientos) > 0 else 0
        
        return {
            "total_usuarios": total_usuarios,
            "total_sembradores": total_sembradores,
            "total_seguimientos": total_seguimientos,
            "pendientes": pendientes,
            "promedio_avance": promedio_avance
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        print(f"❌ Error en admin_overview: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
