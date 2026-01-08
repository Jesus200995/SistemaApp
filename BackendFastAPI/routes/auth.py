from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from models import User
import bcrypt, jwt, os
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "mi_clave_jwt_2025")

router = APIRouter(prefix="/auth", tags=["auth"])
bearer_scheme = HTTPBearer()

# 🧩 Modelos Pydantic para validación de datos JSON
class RegisterRequest(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str
    curp: str | None = None
    territorio: str | None = None
    telefono: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str

class UpdateUserRequest(BaseModel):
    nombre: str | None = None
    email: str | None = None
    rol: str | None = None
    curp: str | None = None
    territorio: str | None = None
    telefono: str | None = None

class CreateUserByHierarchyRequest(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str
    curp: str | None = None
    territorio: str | None = None
    telefono: str | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario desde el formulario público.
    
    🔐 Seguridad:
    - Valida que no exista un usuario con el mismo email
    - Hash la contraseña con bcrypt
    - Solo permite registro autónomo para técnicos (tecnico_productivo, tecnico_social)
    - Roles superiores (facilitador, territorial, admin) solo pueden ser creados jerárquicamente
    
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
    
    # ✅ Roles permitidos para registro público (solo técnicos)
    roles_publicos_permitidos = ["tecnico_productivo", "tecnico_social"]
    rol = request.rol.lower() if request.rol else "tecnico_productivo"
    
    # ✅ Verificar que solo técnicos puedan registrarse públicamente
    if rol not in roles_publicos_permitidos:
        raise HTTPException(
            status_code=403, 
            detail=f"Solo los técnicos pueden registrarse públicamente. Para roles superiores, contacta a tu superior jerárquico."
        )
    
    # ✅ Verificar si el email ya existe
    existente = db.query(User).filter(User.email == request.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # ✅ Validar CURP si se proporciona (18 caracteres alfanuméricos)
    curp = None
    if request.curp and request.curp.strip():
        curp = request.curp.strip().upper()
        curp_regex = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$'
        if not re.match(curp_regex, curp):
            raise HTTPException(status_code=400, detail="CURP inválido. Debe tener 18 caracteres alfanuméricos en formato válido")
        # Verificar que no exista otro usuario con el mismo CURP
        curp_existente = db.query(User).filter(User.curp == curp).first()
        if curp_existente:
            raise HTTPException(status_code=400, detail="Ya existe un usuario con este CURP")
    
    # ✅ Validar teléfono si se proporciona (exactamente 10 dígitos para México)
    telefono = None
    if request.telefono and request.telefono.strip():
        telefono = re.sub(r'[^0-9]', '', request.telefono)  # Eliminar todo excepto números
        if len(telefono) != 10:
            raise HTTPException(status_code=400, detail=f"El teléfono debe tener exactamente 10 dígitos. Actualmente tiene {len(telefono)} dígitos.")
    
    # ✅ Validar territorio
    territorio = None
    if request.territorio and request.territorio.strip():
        territorio = request.territorio.strip()
    
    # ✅ Hashear contraseña
    hashed = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    # ✅ Crear nuevo usuario (nombre en MAYÚSCULAS)
    nuevo = User(
        nombre=request.nombre.strip().upper(),
        email=request.email.strip().lower(),
        password=hashed,
        rol=rol,
        curp=curp,
        territorio=territorio,
        telefono=telefono,
        superior_id=None  # Será asignado por facilitador después
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

@router.post("/create-user")
def create_user_hierarchical(
    request: CreateUserByHierarchyRequest,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    """
    Crear un usuario de forma jerárquica.
    
    🔐 Jerarquía del Sistema de Administración:
    - Admin (Coordinador Territorial) → puede crear Territoriales
    - Territorial → puede crear Facilitadores
    - Facilitador → puede crear Técnico Productivo o Técnico Social
    
    📧 Notificaciones:
    - Notifica al usuario superior cuando se crea un nuevo usuario
    """
    from models import Notificacion
    import re
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        current_user_id = payload.get("id")
        current_rol_raw = payload.get("rol")
        # ✅ Normalizar rol a minúsculas para evitar problemas de case-sensitivity
        current_rol = current_rol_raw.lower().strip() if current_rol_raw else ""
        print(f"🔍 [CREATE-USER] Rol del token (original): '{current_rol_raw}' → (normalizado): '{current_rol}'")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # ✅ Validar que el usuario actual existe
    current_user = db.query(User).filter(User.id == current_user_id).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuario actual no encontrado")
    
    # ✅ Definir roles permitidos según la jerarquía
    roles_permitidos_por_creador = {
        "admin": ["territorial"],
        "territorial": ["facilitador"],
        "facilitador": ["tecnico_productivo", "tecnico_social"]
    }
    
    # ✅ Verificar permisos de creación
    if current_rol not in roles_permitidos_por_creador:
        raise HTTPException(
            status_code=403, 
            detail=f"El rol '{current_rol}' no tiene permisos para crear usuarios"
        )
    
    roles_permitidos = roles_permitidos_por_creador[current_rol]
    rol_nuevo = request.rol.lower()
    
    if rol_nuevo not in roles_permitidos:
        raise HTTPException(
            status_code=403,
            detail=f"No tienes permiso para crear usuarios con rol '{rol_nuevo}'. Roles permitidos: {', '.join(roles_permitidos)}"
        )
    
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
    
    # ✅ Verificar si el email ya existe
    existente = db.query(User).filter(User.email == request.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # ✅ Validar CURP si se proporciona (18 caracteres alfanuméricos)
    curp = None
    if request.curp and request.curp.strip():
        curp = request.curp.strip().upper()
        curp_regex = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$'
        if not re.match(curp_regex, curp):
            raise HTTPException(status_code=400, detail="CURP inválido. Debe tener 18 caracteres alfanuméricos en formato válido")
        # Verificar que no exista otro usuario con el mismo CURP
        curp_existente = db.query(User).filter(User.curp == curp).first()
        if curp_existente:
            raise HTTPException(status_code=400, detail="Ya existe un usuario con este CURP")
    
    # ✅ Validar teléfono si se proporciona (exactamente 10 dígitos para México)
    telefono = None
    if request.telefono and request.telefono.strip():
        telefono = re.sub(r'[^0-9]', '', request.telefono)  # Eliminar todo excepto números
        if len(telefono) != 10:
            raise HTTPException(status_code=400, detail=f"El teléfono debe tener exactamente 10 dígitos. Actualmente tiene {len(telefono)} dígitos.")
    
    # ✅ Validar territorio
    territorio = None
    if request.territorio and request.territorio.strip():
        territorio = request.territorio.strip()
    
    # ✅ Hashear contraseña
    hashed = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    # ✅ Heredar territorio del usuario creador si no se especifica
    territorio_id_heredado = None
    territorio_heredado = territorio  # El que viene del request
    
    if current_user.territorio_id:
        territorio_id_heredado = current_user.territorio_id
        print(f"📍 Heredando territorio_id del creador: {territorio_id_heredado}")
    
    if not territorio_heredado and current_user.territorio:
        territorio_heredado = current_user.territorio
        print(f"📍 Heredando territorio (nombre) del creador: {territorio_heredado}")
    
    # ✅ Crear nuevo usuario con superior_id y territorio heredado (nombre en MAYÚSCULAS)
    nuevo = User(
        nombre=request.nombre.strip().upper(),
        email=request.email.strip().lower(),
        password=hashed,
        rol=rol_nuevo,
        curp=curp,
        territorio=territorio_heredado,
        territorio_id=territorio_id_heredado,
        telefono=telefono,
        superior_id=current_user_id  # Asignar usuario creador como superior
    )
    
    print(f"✅ Creando usuario: {nuevo.nombre}, rol: {nuevo.rol}, territorio_id: {nuevo.territorio_id}, territorio: {nuevo.territorio}, superior_id: {nuevo.superior_id}")
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    
    # 📧 Crear notificación para el usuario que creó
    try:
        notificacion = Notificacion(
            titulo=f"Usuario creado exitosamente",
            mensaje=f"Has creado al usuario {nuevo.nombre} ({nuevo.email}) como {rol_nuevo.upper().replace('_', ' ')}",
            tipo="success",
            user_destino=current_user_id
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
        "superior_id": nuevo.superior_id,
        "territorio": nuevo.territorio,
        "territorio_id": nuevo.territorio_id,
        "message": f"Usuario {nuevo.nombre} creado exitosamente como {rol_nuevo.upper().replace('_', ' ')}"
    }

@router.get("/roles-permitidos")
def get_roles_permitidos(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    """
    Obtener los roles que el usuario actual puede crear según la jerarquía.
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        current_rol = payload.get("rol")
        # Normalizar el rol a minúsculas para comparación
        current_rol_normalized = current_rol.lower().strip() if current_rol else ""
        print(f"🔍 DEBUG - Rol actual (original): {current_rol}, (normalizado): {current_rol_normalized}")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    roles_permitidos_por_creador = {
        "admin": [
            {"value": "territorial", "label": "Territorial"}
        ],
        "territorial": [
            {"value": "facilitador", "label": "Facilitador"}
        ],
        "facilitador": [
            {"value": "tecnico_productivo", "label": "Técnico Productivo"},
            {"value": "tecnico_social", "label": "Técnico Social"}
        ]
    }
    
    # Usar el rol normalizado para la búsqueda
    roles = roles_permitidos_por_creador.get(current_rol_normalized, [])
    puede_crear = len(roles) > 0
    
    print(f"🔍 DEBUG - Puede crear: {puede_crear}, Roles disponibles: {roles}")
    
    return {
        "puede_crear": puede_crear,
        "rol_actual": current_rol,
        "rol_normalizado": current_rol_normalized,
        "roles_permitidos": roles
    }

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Normalizar email a minúsculas para la búsqueda
    email_normalizado = request.email.strip().lower()
    
    user = db.query(User).filter(User.email == email_normalizado).first()
    if not user:
        # También buscar sin normalizar por si acaso
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            raise HTTPException(status_code=400, detail="Usuario no encontrado")
    
    try:
        password_valido = bcrypt.checkpw(
            request.password.encode("utf-8"), 
            user.password.encode("utf-8")
        )
    except Exception as e:
        print(f"❌ [LOGIN] Error verificando contraseña: {str(e)}")
        raise HTTPException(status_code=400, detail="Error verificando credenciales")
    
    if not password_valido:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    # ✅ Normalizar rol a minúsculas para evitar problemas de case-sensitivity
    rol_normalizado = user.rol.lower().strip() if user.rol else "tecnico_productivo"
    print(f"🔐 [LOGIN] Usuario: {user.email} | Rol DB: '{user.rol}' → Rol normalizado: '{rol_normalizado}'")
    
    token = jwt.encode(
        {"id": user.id, "email": user.email, "rol": rol_normalizado},
        SECRET,
        algorithm="HS256"
    )
    return {
        "token": token, 
        "user": {
            "id": user.id, 
            "nombre": user.nombre, 
            "email": user.email,
            "rol": rol_normalizado,
            "curp": user.curp,
            "territorio": user.territorio,
            "telefono": user.telefono
        }
    }


@router.post("/setup-admin")
def setup_admin(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Crear el primer administrador del sistema.
    
    ⚠️ IMPORTANTE: Este endpoint solo funciona si NO existe ningún admin en el sistema.
    Una vez creado el primer admin, este endpoint deja de funcionar.
    
    Uso: Solo para configuración inicial del sistema.
    """
    import re
    
    # ✅ Verificar si ya existe un admin
    admin_existente = db.query(User).filter(User.rol.ilike("admin")).first()
    if admin_existente:
        raise HTTPException(
            status_code=403, 
            detail="Ya existe un administrador en el sistema. Usa el login para acceder."
        )
    
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
    
    # ✅ Verificar si el email ya existe
    existente = db.query(User).filter(User.email == request.email.strip().lower()).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # ✅ Validar CURP si se proporciona
    curp = None
    if request.curp and request.curp.strip():
        curp = request.curp.strip().upper()
        curp_regex = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$'
        if not re.match(curp_regex, curp):
            raise HTTPException(status_code=400, detail="CURP inválido")
    
    # ✅ Validar teléfono si se proporciona
    telefono = None
    if request.telefono and request.telefono.strip():
        telefono = re.sub(r'[^0-9]', '', request.telefono)
        if len(telefono) < 10:
            raise HTTPException(status_code=400, detail="El teléfono debe tener al menos 10 dígitos")
    
    # ✅ Validar territorio
    territorio = None
    if request.territorio and request.territorio.strip():
        territorio = request.territorio.strip()
    
    # ✅ Hashear contraseña
    hashed = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    # ✅ Crear admin
    nuevo = User(
        nombre=request.nombre.strip(),
        email=request.email.strip().lower(),
        password=hashed,
        rol="admin",
        curp=curp,
        territorio=territorio,
        telefono=telefono,
        superior_id=None
    )
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    
    print(f"✅ [SETUP-ADMIN] Administrador creado: {nuevo.email}")
    
    return {
        "success": True,
        "id": nuevo.id,
        "nombre": nuevo.nombre,
        "email": nuevo.email,
        "rol": nuevo.rol,
        "message": "Administrador creado exitosamente. Ya puedes iniciar sesión."
    }

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
        
        # ✅ Normalizar rol a minúsculas
        rol_normalizado = user.rol.lower().strip() if user.rol else "tecnico_productivo"
        
        return {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "rol": rol_normalizado,
            "curp": user.curp,
            "territorio": user.territorio,
            "telefono": user.telefono,
            "activo": user.activo,
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
        current_rol_raw = payload.get("rol")
        # ✅ Normalizar rol para comparaciones
        current_rol = current_rol_raw.lower().strip() if current_rol_raw else ""
        
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
            query = query.filter(User.rol.ilike(rol))  # Case-insensitive

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
                    "rol": u.rol.lower().strip() if u.rol else "tecnico_productivo",  # ✅ Normalizar
                    "curp": u.curp,
                    "territorio": u.territorio,
                    "telefono": u.telefono,
                    "activo": u.activo,
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
    import re
    
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
        
        # ✅ Actualizar CURP si se proporciona
        if body.curp is not None:
            if body.curp.strip():
                curp = body.curp.strip().upper()
                curp_regex = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$'
                if not re.match(curp_regex, curp):
                    raise HTTPException(status_code=400, detail="CURP inválido")
                # Verificar que no exista otro usuario con el mismo CURP
                curp_existente = db.query(User).filter(User.curp == curp, User.id != user_id).first()
                if curp_existente:
                    raise HTTPException(status_code=400, detail="Ya existe un usuario con este CURP")
                user.curp = curp
            else:
                user.curp = None
        
        # ✅ Actualizar territorio si se proporciona
        if body.territorio is not None:
            user.territorio = body.territorio.strip() if body.territorio.strip() else None
        
        # ✅ Actualizar teléfono si se proporciona
        if body.telefono is not None:
            if body.telefono.strip():
                telefono = re.sub(r'[^0-9]', '', body.telefono)
                if len(telefono) < 10:
                    raise HTTPException(status_code=400, detail="El teléfono debe tener al menos 10 dígitos")
                user.telefono = telefono
            else:
                user.telefono = None

        db.commit()
        db.refresh(user)
        return {
            "success": True, 
            "user": {
                "id": user.id, 
                "nombre": user.nombre, 
                "email": user.email, 
                "rol": user.rol,
                "curp": user.curp,
                "territorio": user.territorio,
                "telefono": user.telefono
            }
        }
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
