"""
Rutas API para Estructura Territorial - Sembrando Vida
Módulo 1: Personal Operativo y Estructura Territorial

Maneja:
- Territorios
- Rutas (con facilitador principal y apoyo)
- CAC (Comunidades de Aprendizaje Campesino)
"""

from fastapi import APIRouter, HTTPException, Depends, Security, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import (
    User, Territorio, Ruta, CAC, AsignacionPersonaCAC
)
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "mi_clave_jwt_2025")

router = APIRouter(prefix="/estructura", tags=["Estructura Territorial"])
bearer_scheme = HTTPBearer()


# ========== PYDANTIC MODELS ==========

class TerritorioCreate(BaseModel):
    nombre: str
    estado_region: Optional[str] = None
    responsable_id: Optional[int] = None

class TerritorioUpdate(BaseModel):
    nombre: Optional[str] = None
    estado_region: Optional[str] = None
    responsable_id: Optional[int] = None
    activo: Optional[bool] = None

class RutaCreate(BaseModel):
    nombre: str
    territorio_id: int
    facilitador_principal_id: Optional[int] = None
    facilitador_apoyo_id: Optional[int] = None

class RutaUpdate(BaseModel):
    nombre: Optional[str] = None
    territorio_id: Optional[int] = None
    facilitador_principal_id: Optional[int] = None
    facilitador_apoyo_id: Optional[int] = None
    activo: Optional[bool] = None

class CACCreate(BaseModel):
    nombre: str
    ruta_id: int
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    tecnico_social_id: Optional[int] = None
    tecnico_productivo_id: Optional[int] = None

class CACUpdate(BaseModel):
    nombre: Optional[str] = None
    ruta_id: Optional[int] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    tecnico_social_id: Optional[int] = None
    tecnico_productivo_id: Optional[int] = None
    estatus: Optional[str] = None
    activo: Optional[bool] = None


# ========== AUTH HELPERS ==========

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    """Extrae y valida el token JWT"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        rol = payload.get("rol", "").upper()
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return {"user_id": user_id, "rol": rol}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")


def require_role(allowed_roles: List[str]):
    """Decorator para verificar roles permitidos"""
    def checker(current_user: dict = Depends(get_current_user)):
        rol = current_user["rol"].upper()
        normalized_roles = [r.upper() for r in allowed_roles]
        
        # Mapeo de roles técnicos
        if "TECNICO" in rol:
            rol = "TECNICO"
        
        if rol not in normalized_roles and "ADMIN" not in normalized_roles:
            raise HTTPException(status_code=403, detail=f"Rol {rol} no autorizado para esta operación")
        
        return current_user
    return checker


# ========== TERRITORIOS ENDPOINTS ==========

@router.get("/territorios")
def listar_territorios(
    activo: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista territorios según rol del usuario:
    - Admin: todos los territorios
    - Territorial: solo su territorio
    - Facilitador/Técnico: solo su territorio asignado
    """
    query = db.query(Territorio)
    
    # Filtrar por activo
    if activo is not None:
        query = query.filter(Territorio.activo == activo)
    
    # Búsqueda por nombre
    if search:
        query = query.filter(Territorio.nombre.ilike(f"%{search}%"))
    
    # Filtrar por rol y alcance (scope)
    rol = current_user["rol"].upper()
    user_id = current_user["user_id"]
    
    if "ADMIN" not in rol:
        # Obtener usuario para ver su territorio asignado
        usuario = db.query(User).filter(User.id == user_id).first()
        if usuario and usuario.territorio_id:
            query = query.filter(Territorio.id == usuario.territorio_id)
    
    territorios = query.order_by(Territorio.nombre).all()
    
    # Enriquecer con KPIs
    result = []
    for t in territorios:
        rutas_count = db.query(Ruta).filter(Ruta.territorio_id == t.id, Ruta.activo == True).count()
        cac_count = db.query(CAC).join(Ruta).filter(Ruta.territorio_id == t.id, CAC.activo == True).count()
        
        # Contar vacantes
        vacantes_ts = db.query(CAC).join(Ruta).filter(
            Ruta.territorio_id == t.id, 
            CAC.activo == True,
            CAC.tecnico_social_id == None
        ).count()
        
        vacantes_tp = db.query(CAC).join(Ruta).filter(
            Ruta.territorio_id == t.id, 
            CAC.activo == True,
            CAC.tecnico_productivo_id == None
        ).count()
        
        # Obtener responsable
        responsable = None
        if t.responsable_id:
            resp = db.query(User).filter(User.id == t.responsable_id).first()
            if resp:
                responsable = {"id": resp.id, "nombre": resp.nombre}
        
        result.append({
            "id": t.id,
            "nombre": t.nombre,
            "estado_region": t.estado_region,
            "responsable": responsable,
            "activo": t.activo,
            "kpis": {
                "rutas": rutas_count,
                "cac_total": cac_count,
                "vacantes_ts": vacantes_ts,
                "vacantes_tp": vacantes_tp
            }
        })
    
    return {"items": result, "total": len(result)}


@router.post("/territorios")
def crear_territorio(
    data: TerritorioCreate,
    current_user: dict = Depends(require_role(["ADMINISTRADOR", "ADMIN"])),
    db: Session = Depends(get_db)
):
    """Crear nuevo territorio (solo Admin)"""
    # Verificar nombre único
    existente = db.query(Territorio).filter(Territorio.nombre == data.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un territorio con ese nombre")
    
    territorio = Territorio(
        nombre=data.nombre.upper(),
        estado_region=data.estado_region,
        responsable_id=data.responsable_id
    )
    
    db.add(territorio)
    db.commit()
    db.refresh(territorio)
    
    return {"mensaje": "Territorio creado exitosamente", "id": territorio.id}


@router.put("/territorios/{territorio_id}")
def actualizar_territorio(
    territorio_id: int,
    data: TerritorioUpdate,
    current_user: dict = Depends(require_role(["ADMINISTRADOR", "ADMIN"])),
    db: Session = Depends(get_db)
):
    """Actualizar territorio (solo Admin)"""
    territorio = db.query(Territorio).filter(Territorio.id == territorio_id).first()
    if not territorio:
        raise HTTPException(status_code=404, detail="Territorio no encontrado")
    
    if data.nombre:
        territorio.nombre = data.nombre.upper()
    if data.estado_region is not None:
        territorio.estado_region = data.estado_region
    if data.responsable_id is not None:
        territorio.responsable_id = data.responsable_id
    if data.activo is not None:
        territorio.activo = data.activo
    
    db.commit()
    return {"mensaje": "Territorio actualizado"}


# ========== RUTAS ENDPOINTS ==========

@router.get("/rutas")
def listar_rutas(
    territorio_id: Optional[int] = None,
    activo: Optional[bool] = None,
    search: Optional[str] = None,
    sin_facilitador: Optional[bool] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista rutas según rol y alcance:
    - Admin: todas las rutas
    - Territorial: rutas de su territorio
    - Facilitador: solo sus rutas asignadas
    """
    query = db.query(Ruta)
    
    if territorio_id:
        query = query.filter(Ruta.territorio_id == territorio_id)
    
    if activo is not None:
        query = query.filter(Ruta.activo == activo)
    
    if search:
        query = query.filter(Ruta.nombre.ilike(f"%{search}%"))
    
    if sin_facilitador:
        query = query.filter(Ruta.facilitador_principal_id == None)
    
    # Filtrar por rol
    rol = current_user["rol"].upper()
    user_id = current_user["user_id"]
    
    if "FACILITADOR" in rol:
        # Solo ver rutas donde es principal o apoyo
        query = query.filter(
            or_(
                Ruta.facilitador_principal_id == user_id,
                Ruta.facilitador_apoyo_id == user_id
            )
        )
    elif "TERRITORIAL" in rol:
        usuario = db.query(User).filter(User.id == user_id).first()
        if usuario and usuario.territorio_id:
            query = query.filter(Ruta.territorio_id == usuario.territorio_id)
    
    rutas = query.order_by(Ruta.nombre).all()
    
    result = []
    for r in rutas:
        # Obtener territorio
        territorio = db.query(Territorio).filter(Territorio.id == r.territorio_id).first()
        
        # Obtener facilitadores
        facilitador_principal = None
        facilitador_apoyo = None
        
        if r.facilitador_principal_id:
            fp = db.query(User).filter(User.id == r.facilitador_principal_id).first()
            if fp:
                facilitador_principal = {"persona_id": fp.id, "nombre_completo": fp.nombre, "tipo_participacion": "PRINCIPAL"}
        
        if r.facilitador_apoyo_id:
            fa = db.query(User).filter(User.id == r.facilitador_apoyo_id).first()
            if fa:
                facilitador_apoyo = {"persona_id": fa.id, "nombre_completo": fa.nombre, "tipo_participacion": "APOYO"}
        
        facilitadores = [f for f in [facilitador_principal, facilitador_apoyo] if f]
        
        # KPIs
        cac_total = db.query(CAC).filter(CAC.ruta_id == r.id, CAC.activo == True).count()
        vacantes_ts = db.query(CAC).filter(CAC.ruta_id == r.id, CAC.activo == True, CAC.tecnico_social_id == None).count()
        vacantes_tp = db.query(CAC).filter(CAC.ruta_id == r.id, CAC.activo == True, CAC.tecnico_productivo_id == None).count()
        
        result.append({
            "ruta_id": r.id,
            "nombre": r.nombre,
            "territorio_id": r.territorio_id,
            "territorio_nombre": territorio.nombre if territorio else None,
            "facilitadores": facilitadores,
            "activo": r.activo,
            "kpis": {
                "cac_total": cac_total,
                "vacantes_ts": vacantes_ts,
                "vacantes_tp": vacantes_tp,
                "pendientes": 0  # TODO: contar cambios pendientes
            }
        })
    
    return {"items": result, "total": len(result)}


@router.post("/rutas")
def crear_ruta(
    data: RutaCreate,
    current_user: dict = Depends(require_role(["ADMINISTRADOR", "ADMIN", "TERRITORIAL"])),
    db: Session = Depends(get_db)
):
    """Crear nueva ruta"""
    # Verificar que existe el territorio
    territorio = db.query(Territorio).filter(Territorio.id == data.territorio_id).first()
    if not territorio:
        raise HTTPException(status_code=404, detail="Territorio no encontrado")
    
    ruta = Ruta(
        nombre=data.nombre.upper(),
        territorio_id=data.territorio_id,
        facilitador_principal_id=data.facilitador_principal_id,
        facilitador_apoyo_id=data.facilitador_apoyo_id
    )
    
    db.add(ruta)
    db.commit()
    db.refresh(ruta)
    
    return {"mensaje": "Ruta creada exitosamente", "id": ruta.id}


@router.put("/rutas/{ruta_id}")
def actualizar_ruta(
    ruta_id: int,
    data: RutaUpdate,
    current_user: dict = Depends(require_role(["ADMINISTRADOR", "ADMIN", "TERRITORIAL"])),
    db: Session = Depends(get_db)
):
    """Actualizar ruta"""
    ruta = db.query(Ruta).filter(Ruta.id == ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    
    if data.nombre:
        ruta.nombre = data.nombre.upper()
    if data.territorio_id:
        ruta.territorio_id = data.territorio_id
    if data.facilitador_principal_id is not None:
        ruta.facilitador_principal_id = data.facilitador_principal_id or None
    if data.facilitador_apoyo_id is not None:
        ruta.facilitador_apoyo_id = data.facilitador_apoyo_id or None
    if data.activo is not None:
        ruta.activo = data.activo
    
    db.commit()
    return {"mensaje": "Ruta actualizada"}


# ========== CAC ENDPOINTS ==========

@router.get("/cac")
def listar_cac(
    ruta_id: Optional[int] = None,
    territorio_id: Optional[int] = None,
    activo: Optional[bool] = None,
    search: Optional[str] = None,
    con_vacante: Optional[bool] = None,
    sin_coordenadas: Optional[bool] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista CAC según rol y alcance:
    - Admin: todas
    - Territorial: CAC de su territorio
    - Facilitador: CAC de sus rutas
    - Técnico: solo sus CAC asignadas
    """
    query = db.query(CAC)
    
    if ruta_id:
        query = query.filter(CAC.ruta_id == ruta_id)
    
    if territorio_id:
        query = query.join(Ruta).filter(Ruta.territorio_id == territorio_id)
    
    if activo is not None:
        query = query.filter(CAC.activo == activo)
    
    if search:
        query = query.filter(CAC.nombre.ilike(f"%{search}%"))
    
    if con_vacante:
        query = query.filter(
            or_(CAC.tecnico_social_id == None, CAC.tecnico_productivo_id == None)
        )
    
    if sin_coordenadas:
        query = query.filter(
            or_(CAC.latitud == None, CAC.longitud == None)
        )
    
    # Filtrar por rol
    rol = current_user["rol"].upper()
    user_id = current_user["user_id"]
    
    if "TECNICO" in rol:
        # Solo CAC donde está asignado
        query = query.filter(
            or_(CAC.tecnico_social_id == user_id, CAC.tecnico_productivo_id == user_id)
        )
    elif "FACILITADOR" in rol:
        # CAC de sus rutas
        rutas_ids = db.query(Ruta.id).filter(
            or_(
                Ruta.facilitador_principal_id == user_id,
                Ruta.facilitador_apoyo_id == user_id
            )
        ).all()
        rutas_ids = [r[0] for r in rutas_ids]
        if rutas_ids:
            query = query.filter(CAC.ruta_id.in_(rutas_ids))
        else:
            return {"items": [], "total": 0}
    elif "TERRITORIAL" in rol:
        usuario = db.query(User).filter(User.id == user_id).first()
        if usuario and usuario.territorio_id:
            query = query.join(Ruta).filter(Ruta.territorio_id == usuario.territorio_id)
    
    cacs = query.order_by(CAC.nombre).all()
    
    result = []
    for c in cacs:
        ruta = db.query(Ruta).filter(Ruta.id == c.ruta_id).first()
        
        # Técnicos asignados
        ts = None
        tp = None
        
        if c.tecnico_social_id:
            u = db.query(User).filter(User.id == c.tecnico_social_id).first()
            if u:
                ts = {"persona_id": u.id, "nombre_completo": u.nombre}
        
        if c.tecnico_productivo_id:
            u = db.query(User).filter(User.id == c.tecnico_productivo_id).first()
            if u:
                tp = {"persona_id": u.id, "nombre_completo": u.nombre}
        
        # Determinar estatus
        estatus = "OK"
        if not c.tecnico_social_id or not c.tecnico_productivo_id:
            estatus = "VACANTE"
        
        result.append({
            "cac_id": c.id,
            "nombre": c.nombre,
            "ruta_id": c.ruta_id,
            "ruta_nombre": ruta.nombre if ruta else None,
            "latitud": c.latitud,
            "longitud": c.longitud,
            "tecnico_social": ts,
            "tecnico_productivo": tp,
            "estatus": estatus,
            "activo": c.activo
        })
    
    return {"items": result, "total": len(result)}


@router.get("/cac/{cac_id}")
def obtener_cac(
    cac_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener detalle de una CAC"""
    cac = db.query(CAC).filter(CAC.id == cac_id).first()
    if not cac:
        raise HTTPException(status_code=404, detail="CAC no encontrada")
    
    ruta = db.query(Ruta).filter(Ruta.id == cac.ruta_id).first()
    territorio = None
    if ruta:
        territorio = db.query(Territorio).filter(Territorio.id == ruta.territorio_id).first()
    
    # Técnicos
    ts = None
    tp = None
    
    if cac.tecnico_social_id:
        u = db.query(User).filter(User.id == cac.tecnico_social_id).first()
        if u:
            ts = {"persona_id": u.id, "nombre_completo": u.nombre, "curp": u.curp, "telefono": u.telefono}
    
    if cac.tecnico_productivo_id:
        u = db.query(User).filter(User.id == cac.tecnico_productivo_id).first()
        if u:
            tp = {"persona_id": u.id, "nombre_completo": u.nombre, "curp": u.curp, "telefono": u.telefono}
    
    # Historial de asignaciones
    historial = db.query(AsignacionPersonaCAC).filter(
        AsignacionPersonaCAC.cac_id == cac_id
    ).order_by(AsignacionPersonaCAC.fecha_inicio.desc()).limit(10).all()
    
    historial_list = []
    for h in historial:
        persona = db.query(User).filter(User.id == h.persona_id).first()
        historial_list.append({
            "persona_nombre": persona.nombre if persona else "Desconocido",
            "tipo": h.tipo_asignacion,
            "fecha_inicio": h.fecha_inicio.isoformat() if h.fecha_inicio else None,
            "fecha_fin": h.fecha_fin.isoformat() if h.fecha_fin else None,
            "activo": h.activo
        })
    
    return {
        "cac_id": cac.id,
        "nombre": cac.nombre,
        "ruta": {"id": ruta.id, "nombre": ruta.nombre} if ruta else None,
        "territorio": {"id": territorio.id, "nombre": territorio.nombre} if territorio else None,
        "latitud": cac.latitud,
        "longitud": cac.longitud,
        "tecnico_social": ts,
        "tecnico_productivo": tp,
        "estatus": cac.estatus,
        "historial": historial_list
    }


@router.post("/cac")
def crear_cac(
    data: CACCreate,
    current_user: dict = Depends(require_role(["ADMINISTRADOR", "ADMIN", "TERRITORIAL", "FACILITADOR"])),
    db: Session = Depends(get_db)
):
    """Crear nueva CAC"""
    # Verificar que existe la ruta
    ruta = db.query(Ruta).filter(Ruta.id == data.ruta_id).first()
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    
    # Determinar estatus inicial
    estatus = "OK"
    if not data.tecnico_social_id or not data.tecnico_productivo_id:
        estatus = "VACANTE"
    
    cac = CAC(
        nombre=data.nombre.upper(),
        ruta_id=data.ruta_id,
        latitud=data.latitud,
        longitud=data.longitud,
        tecnico_social_id=data.tecnico_social_id,
        tecnico_productivo_id=data.tecnico_productivo_id,
        estatus=estatus
    )
    
    db.add(cac)
    db.commit()
    db.refresh(cac)
    
    # Crear asignaciones si hay técnicos
    if data.tecnico_social_id:
        asig = AsignacionPersonaCAC(
            persona_id=data.tecnico_social_id,
            cac_id=cac.id,
            tipo_asignacion="TECNICO_SOCIAL"
        )
        db.add(asig)
    
    if data.tecnico_productivo_id:
        asig = AsignacionPersonaCAC(
            persona_id=data.tecnico_productivo_id,
            cac_id=cac.id,
            tipo_asignacion="TECNICO_PRODUCTIVO"
        )
        db.add(asig)
    
    db.commit()
    
    return {"mensaje": "CAC creada exitosamente", "id": cac.id}


@router.put("/cac/{cac_id}")
def actualizar_cac(
    cac_id: int,
    data: CACUpdate,
    current_user: dict = Depends(require_role(["ADMINISTRADOR", "ADMIN", "TERRITORIAL", "FACILITADOR"])),
    db: Session = Depends(get_db)
):
    """Actualizar CAC"""
    cac = db.query(CAC).filter(CAC.id == cac_id).first()
    if not cac:
        raise HTTPException(status_code=404, detail="CAC no encontrada")
    
    # Guardar técnicos anteriores para historial
    ts_anterior = cac.tecnico_social_id
    tp_anterior = cac.tecnico_productivo_id
    
    if data.nombre:
        cac.nombre = data.nombre.upper()
    if data.ruta_id:
        cac.ruta_id = data.ruta_id
    if data.latitud is not None:
        cac.latitud = data.latitud
    if data.longitud is not None:
        cac.longitud = data.longitud
    if data.tecnico_social_id is not None:
        cac.tecnico_social_id = data.tecnico_social_id or None
    if data.tecnico_productivo_id is not None:
        cac.tecnico_productivo_id = data.tecnico_productivo_id or None
    if data.activo is not None:
        cac.activo = data.activo
    
    # Actualizar estatus
    if not cac.tecnico_social_id or not cac.tecnico_productivo_id:
        cac.estatus = "VACANTE"
    else:
        cac.estatus = "OK"
    
    # Registrar cambios en asignaciones
    if data.tecnico_social_id is not None and data.tecnico_social_id != ts_anterior:
        # Cerrar asignación anterior
        if ts_anterior:
            asig_ant = db.query(AsignacionPersonaCAC).filter(
                AsignacionPersonaCAC.cac_id == cac_id,
                AsignacionPersonaCAC.persona_id == ts_anterior,
                AsignacionPersonaCAC.tipo_asignacion == "TECNICO_SOCIAL",
                AsignacionPersonaCAC.activo == True
            ).first()
            if asig_ant:
                asig_ant.fecha_fin = datetime.utcnow()
                asig_ant.activo = False
        
        # Crear nueva asignación
        if data.tecnico_social_id:
            nueva_asig = AsignacionPersonaCAC(
                persona_id=data.tecnico_social_id,
                cac_id=cac_id,
                tipo_asignacion="TECNICO_SOCIAL"
            )
            db.add(nueva_asig)
    
    if data.tecnico_productivo_id is not None and data.tecnico_productivo_id != tp_anterior:
        if tp_anterior:
            asig_ant = db.query(AsignacionPersonaCAC).filter(
                AsignacionPersonaCAC.cac_id == cac_id,
                AsignacionPersonaCAC.persona_id == tp_anterior,
                AsignacionPersonaCAC.tipo_asignacion == "TECNICO_PRODUCTIVO",
                AsignacionPersonaCAC.activo == True
            ).first()
            if asig_ant:
                asig_ant.fecha_fin = datetime.utcnow()
                asig_ant.activo = False
        
        if data.tecnico_productivo_id:
            nueva_asig = AsignacionPersonaCAC(
                persona_id=data.tecnico_productivo_id,
                cac_id=cac_id,
                tipo_asignacion="TECNICO_PRODUCTIVO"
            )
            db.add(nueva_asig)
    
    db.commit()
    return {"mensaje": "CAC actualizada"}


# ========== DIRECTORIO ENDPOINTS ==========

@router.get("/directorio")
def directorio_personas(
    territorio_id: Optional[int] = None,
    ruta_id: Optional[int] = None,
    rol: Optional[str] = None,
    perfil_operativo: Optional[str] = None,
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    curp: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Directorio de personas filtrable por:
    - Territorio
    - Ruta
    - Rol del sistema
    - Perfil operativo
    - Activo/inactivo
    - Búsqueda por nombre/CURP
    """
    query = db.query(User)
    
    if activo is not None:
        query = query.filter(User.activo == activo)
    
    if search:
        query = query.filter(
            or_(
                User.nombre.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )
    
    if curp:
        query = query.filter(User.curp.ilike(f"%{curp}%"))
    
    if rol:
        query = query.filter(User.rol.ilike(f"%{rol}%"))
    
    if perfil_operativo:
        query = query.filter(User.perfil_operativo == perfil_operativo.upper())
    
    if territorio_id:
        query = query.filter(User.territorio_id == territorio_id)
    
    # ========== FILTRAR POR ALCANCE (SCOPE) SEGÚN ROL ==========
    rol_usuario = current_user["rol"].upper()
    user_id = current_user["user_id"]
    usuario = db.query(User).filter(User.id == user_id).first()
    
    if "ADMIN" in rol_usuario:
        # Admin ve todo - sin filtro adicional
        pass
    elif "TERRITORIAL" in rol_usuario:
        # Territorial ve solo su territorio
        if usuario and usuario.territorio_id:
            query = query.filter(User.territorio_id == usuario.territorio_id)
    elif "FACILITADOR" in rol_usuario:
        # Facilitador ve personal de su(s) ruta(s)
        # Buscar rutas donde es facilitador principal o apoyo
        rutas_facilitador = db.query(Ruta).filter(
            or_(
                Ruta.facilitador_principal_id == user_id,
                Ruta.facilitador_apoyo_id == user_id
            ),
            Ruta.activo == True
        ).all()
        
        ruta_ids = [r.id for r in rutas_facilitador]
        
        if ruta_ids:
            # Obtener técnicos asignados a CAC de esas rutas
            cacs_de_rutas = db.query(CAC).filter(
                CAC.ruta_id.in_(ruta_ids),
                CAC.activo == True
            ).all()
            
            tecnico_ids = set()
            for cac in cacs_de_rutas:
                if cac.tecnico_social_id:
                    tecnico_ids.add(cac.tecnico_social_id)
                if cac.tecnico_productivo_id:
                    tecnico_ids.add(cac.tecnico_productivo_id)
            
            # Incluir también a sí mismo
            tecnico_ids.add(user_id)
            
            query = query.filter(User.id.in_(list(tecnico_ids)))
        else:
            # Si no tiene rutas asignadas, solo verse a sí mismo
            query = query.filter(User.id == user_id)
    elif "TECNICO" in rol_usuario:
        # Técnico ve solo compañeros de sus mismos CAC
        cacs_tecnico = db.query(CAC).filter(
            or_(
                CAC.tecnico_social_id == user_id,
                CAC.tecnico_productivo_id == user_id
            ),
            CAC.activo == True
        ).all()
        
        compañeros_ids = {user_id}  # Incluirse a sí mismo
        
        for cac in cacs_tecnico:
            if cac.tecnico_social_id:
                compañeros_ids.add(cac.tecnico_social_id)
            if cac.tecnico_productivo_id:
                compañeros_ids.add(cac.tecnico_productivo_id)
        
        query = query.filter(User.id.in_(list(compañeros_ids)))
    else:
        # Rol desconocido - solo verse a sí mismo
        query = query.filter(User.id == user_id)
    
    personas = query.order_by(User.nombre).limit(100).all()
    
    result = []
    for p in personas:
        # Determinar ámbito (territorio/rutas/CAC)
        ambito = []
        territorio_nombre = None
        cac_nombre = None
        cacs = []
        
        if p.territorio_id:
            t = db.query(Territorio).filter(Territorio.id == p.territorio_id).first()
            if t:
                territorio_nombre = t.nombre
                ambito.append(f"Territorio: {t.nombre}")
        
        # Buscar CAC asignadas si es técnico
        if "TECNICO" in (p.rol or "").upper():
            cacs = db.query(CAC).filter(
                or_(CAC.tecnico_social_id == p.id, CAC.tecnico_productivo_id == p.id),
                CAC.activo == True
            ).all()
            for c in cacs:
                ambito.append(f"CAC: {c.nombre}")
            if cacs:
                cac_nombre = cacs[0].nombre
        
        result.append({
            "id": p.id,
            "persona_id": p.id,
            "nombre": p.nombre,
            "nombre_completo": p.nombre,
            "curp": p.curp,
            "rol": p.rol,
            "rol_sistema": p.rol,
            "perfil_operativo": p.perfil_operativo,
            "territorio_id": p.territorio_id,
            "territorio_nombre": territorio_nombre,
            "ruta_nombre": None,  # TODO: implementar relación ruta
            "cac_nombre": cac_nombre,
            "ambito": ", ".join(ambito) if ambito else "Sin asignación",
            "correo": p.email,
            "correo_contacto": p.email,
            "telefono": p.telefono,
            "activo": p.activo
        })
    
    # Calcular stats por rol
    territoriales = sum(1 for p in result if p["rol"] and "territorial" in p["rol"].lower())
    facilitadores = sum(1 for p in result if p["rol"] and "facilitador" in p["rol"].lower())
    tecnicos = sum(1 for p in result if p["rol"] and "tecnico" in p["rol"].lower())
    
    return {
        "items": result, 
        "total": len(result),
        "stats": {
            "territoriales": territoriales,
            "facilitadores": facilitadores,
            "tecnicos": tecnicos
        }
    }


@router.get("/buscar-curp")
def buscar_por_curp(
    curp: str,
    current_user: dict = Depends(require_role(["ADMINISTRADOR", "ADMIN", "TERRITORIAL"])),
    db: Session = Depends(get_db)
):
    """
    Búsqueda global controlada por CURP.
    Solo disponible para Territorial y Admin.
    Permite resolver errores de scope sin duplicar personas.
    """
    if len(curp) < 10:
        raise HTTPException(status_code=400, detail="CURP debe tener al menos 10 caracteres")
    
    persona = db.query(User).filter(User.curp.ilike(f"%{curp}%")).first()
    
    if not persona:
        return {"encontrado": False, "mensaje": "Persona no encontrada"}
    
    # Obtener asignaciones actuales
    asignaciones = []
    
    # CAC asignadas
    cacs = db.query(CAC).filter(
        or_(CAC.tecnico_social_id == persona.id, CAC.tecnico_productivo_id == persona.id),
        CAC.activo == True
    ).all()
    
    for c in cacs:
        ruta = db.query(Ruta).filter(Ruta.id == c.ruta_id).first()
        asignaciones.append({
            "tipo": "CAC",
            "nombre": c.nombre,
            "ruta": ruta.nombre if ruta else None
        })
    
    # Rutas donde es facilitador
    rutas = db.query(Ruta).filter(
        or_(Ruta.facilitador_principal_id == persona.id, Ruta.facilitador_apoyo_id == persona.id),
        Ruta.activo == True
    ).all()
    
    for r in rutas:
        tipo = "FACILITADOR_PRINCIPAL" if r.facilitador_principal_id == persona.id else "FACILITADOR_APOYO"
        asignaciones.append({
            "tipo": tipo,
            "nombre": r.nombre
        })
    
    return {
        "encontrado": True,
        "persona": {
            "id": persona.id,
            "nombre": persona.nombre,
            "curp": persona.curp,
            "rol": persona.rol,
            "activo": persona.activo
        },
        "asignaciones": asignaciones
    }
