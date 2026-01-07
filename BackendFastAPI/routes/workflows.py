"""
Rutas API para Workflows - Cambios de Adscripción y Actualizaciones de Estructura
Módulo 1: Personal Operativo y Estructura Territorial

Workflows:
1. Cambios de Adscripción: Alta/Baja/Reasignación de personas a CAC/Rutas/Territorios
2. Actualizaciones de Estructura: Crear/Editar/Inactivar maestros (persona/CAC/ruta/territorio)
"""

from fastapi import APIRouter, HTTPException, Depends, Security, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from database import get_db
from models import (
    User, Territorio, Ruta, CAC, AsignacionPersonaCAC,
    CambioAdscripcion, ActualizacionEstructura, Notificacion
)
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "mi_clave_jwt_2025")

router = APIRouter(prefix="/workflows", tags=["Workflows"])
bearer_scheme = HTTPBearer()


# ========== PYDANTIC MODELS ==========

class CambioAdscripcionCreate(BaseModel):
    tipo_cambio: str  # ALTA, BAJA, REASIGNACION
    objeto: str  # PERSONA_CAC, PERSONA_RUTA, PERSONA_TERRITORIO, CAC_RUTA
    persona_id: Optional[int] = None
    cac_origen_id: Optional[int] = None
    cac_destino_id: Optional[int] = None
    ruta_origen_id: Optional[int] = None
    ruta_destino_id: Optional[int] = None
    territorio_origen_id: Optional[int] = None
    territorio_destino_id: Optional[int] = None
    resumen: Optional[str] = None
    fecha_efecto: Optional[datetime] = None
    destino_id: Optional[int] = None  # Usuario destinatario de la solicitud
    estatus: Optional[str] = None  # Si se envía EN_REVISION, se salta el borrador

class CambioAdscripcionAccion(BaseModel):
    accion: str  # AUTORIZAR, RECHAZAR, APLICAR, CANCELAR, DEVOLVER
    observaciones: Optional[str] = None

class ActualizacionEstructuraCreate(BaseModel):
    tipo_objeto: str  # PERSONA, CAC, RUTA, TERRITORIO
    accion: str  # CREAR, EDITAR, INACTIVAR
    objeto_id: Optional[int] = None
    payload_propuesto: Dict[str, Any]
    resumen: Optional[str] = None

class ActualizacionEstructuraAccion(BaseModel):
    accion: str  # AUTORIZAR, RECHAZAR, APLICAR, CANCELAR
    observaciones: Optional[str] = None


# ========== AUTH HELPERS ==========

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        rol = payload.get("rol", "").upper()
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return {"user_id": user_id, "rol": rol}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")


def generar_folio(prefijo: str = "CA"):
    """Genera un folio único para workflows"""
    fecha = datetime.now().strftime("%Y%m%d")
    codigo = str(uuid.uuid4())[:6].upper()
    return f"{prefijo}-{fecha}-{codigo}"


# ========== CAMBIOS DE ADSCRIPCIÓN ENDPOINTS ==========

@router.get("/cambios-adscripcion")
def listar_cambios_adscripcion(
    estatus: Optional[str] = None,
    tipo_cambio: Optional[str] = None,
    objeto: Optional[str] = None,
    territorio_id: Optional[int] = None,
    vencidos: Optional[bool] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista cambios de adscripción según filtros y rol del usuario:
    - Admin: ve todos
    - Territorial: ve los de su territorio
    - Facilitador: ve los que propuso y los de su ámbito
    - Técnico: solo los que propuso
    """
    query = db.query(CambioAdscripcion)
    
    if estatus:
        query = query.filter(CambioAdscripcion.estatus == estatus.upper())
    
    if tipo_cambio:
        query = query.filter(CambioAdscripcion.tipo_cambio == tipo_cambio.upper())
    
    if objeto:
        query = query.filter(CambioAdscripcion.objeto == objeto.upper())
    
    if territorio_id:
        query = query.filter(
            or_(
                CambioAdscripcion.territorio_origen_id == territorio_id,
                CambioAdscripcion.territorio_destino_id == territorio_id
            )
        )
    
    if vencidos is not None:
        ahora = datetime.utcnow()
        if vencidos:
            query = query.filter(
                and_(
                    CambioAdscripcion.fecha_limite != None,
                    CambioAdscripcion.fecha_limite < ahora,
                    CambioAdscripcion.estatus.in_(["BORRADOR", "EN_REVISION", "AUTORIZADO"])
                )
            )
        else:
            query = query.filter(
                or_(
                    CambioAdscripcion.fecha_limite == None,
                    CambioAdscripcion.fecha_limite >= ahora
                )
            )
    
    # Filtrar por rol
    rol = current_user["rol"]
    user_id = current_user["user_id"]
    
    if "ADMIN" not in rol:
        if "TECNICO" in rol:
            # Solo los que propuso
            query = query.filter(CambioAdscripcion.propuesto_por_id == user_id)
        elif "FACILITADOR" in rol:
            # Los que propuso + los de su ámbito
            usuario = db.query(User).filter(User.id == user_id).first()
            rutas_ids = db.query(Ruta.id).filter(
                or_(
                    Ruta.facilitador_principal_id == user_id,
                    Ruta.facilitador_apoyo_id == user_id
                )
            ).all()
            rutas_ids = [r[0] for r in rutas_ids]
            
            query = query.filter(
                or_(
                    CambioAdscripcion.propuesto_por_id == user_id,
                    CambioAdscripcion.ruta_origen_id.in_(rutas_ids),
                    CambioAdscripcion.ruta_destino_id.in_(rutas_ids)
                )
            )
        elif "TERRITORIAL" in rol:
            usuario = db.query(User).filter(User.id == user_id).first()
            if usuario and usuario.territorio_id:
                query = query.filter(
                    or_(
                        CambioAdscripcion.territorio_origen_id == usuario.territorio_id,
                        CambioAdscripcion.territorio_destino_id == usuario.territorio_id,
                        CambioAdscripcion.propuesto_por_id == user_id
                    )
                )
    
    cambios = query.order_by(CambioAdscripcion.created_at.desc()).limit(100).all()
    
    result = []
    for c in cambios:
        # Obtener propuesto por
        propuesto_por = None
        if c.propuesto_por_id:
            u = db.query(User).filter(User.id == c.propuesto_por_id).first()
            if u:
                propuesto_por = {"persona_id": u.id, "nombre_completo": u.nombre}
        
        # Obtener destinatario
        destinatario = None
        if c.destino_id:
            u = db.query(User).filter(User.id == c.destino_id).first()
            if u:
                destinatario = {"persona_id": u.id, "nombre_completo": u.nombre}
        
        # Verificar si está vencido
        vencido = False
        if c.fecha_limite and c.estatus in ["EN_REVISION", "AUTORIZADO"]:
            vencido = c.fecha_limite < datetime.utcnow()
        
        result.append({
            "cambio_adscripcion_id": c.id,
            "folio": c.folio,
            "tipo_cambio": c.tipo_cambio,
            "objeto": c.objeto,
            "estatus": c.estatus,
            "resumen": c.resumen,
            "fecha_efecto": c.fecha_efecto.isoformat() if c.fecha_efecto else None,
            "fecha_limite": c.fecha_limite.isoformat() if c.fecha_limite else None,
            "vencido": vencido,
            "propuesto_por": propuesto_por,
            "propuesto_por_id": c.propuesto_por_id,
            "destino_id": c.destino_id,
            "destinatario": destinatario,
            "created_at": c.created_at.isoformat() if c.created_at else None
        })
    
    return {"items": result, "total": len(result)}


@router.get("/cambios-adscripcion/{cambio_id}")
def obtener_cambio_adscripcion(
    cambio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener detalle de un cambio de adscripción"""
    cambio = db.query(CambioAdscripcion).filter(CambioAdscripcion.id == cambio_id).first()
    if not cambio:
        raise HTTPException(status_code=404, detail="Cambio no encontrado")
    
    # Construir resumen antes/después
    antes = {}
    despues = {}
    
    if cambio.objeto == "PERSONA_CAC":
        if cambio.cac_origen_id:
            cac_orig = db.query(CAC).filter(CAC.id == cambio.cac_origen_id).first()
            antes["cac"] = cac_orig.nombre if cac_orig else "N/A"
        if cambio.cac_destino_id:
            cac_dest = db.query(CAC).filter(CAC.id == cambio.cac_destino_id).first()
            despues["cac"] = cac_dest.nombre if cac_dest else "N/A"
    
    if cambio.objeto == "PERSONA_RUTA":
        if cambio.ruta_origen_id:
            ruta_orig = db.query(Ruta).filter(Ruta.id == cambio.ruta_origen_id).first()
            antes["ruta"] = ruta_orig.nombre if ruta_orig else "N/A"
        if cambio.ruta_destino_id:
            ruta_dest = db.query(Ruta).filter(Ruta.id == cambio.ruta_destino_id).first()
            despues["ruta"] = ruta_dest.nombre if ruta_dest else "N/A"
    
    # Persona afectada
    persona = None
    if cambio.persona_id:
        p = db.query(User).filter(User.id == cambio.persona_id).first()
        if p:
            persona = {"id": p.id, "nombre": p.nombre, "curp": p.curp, "rol": p.rol}
    
    # Propuesto, autorizado, aplicado, destinatario
    propuesto_por = autorizado_por = aplicado_por = destinatario = None
    
    if cambio.propuesto_por_id:
        u = db.query(User).filter(User.id == cambio.propuesto_por_id).first()
        propuesto_por = {"id": u.id, "nombre": u.nombre} if u else None
    
    if cambio.autorizado_por_id:
        u = db.query(User).filter(User.id == cambio.autorizado_por_id).first()
        autorizado_por = {"id": u.id, "nombre": u.nombre} if u else None
    
    if cambio.aplicado_por_id:
        u = db.query(User).filter(User.id == cambio.aplicado_por_id).first()
        aplicado_por = {"id": u.id, "nombre": u.nombre} if u else None
    
    if cambio.destino_id:
        u = db.query(User).filter(User.id == cambio.destino_id).first()
        destinatario = {"id": u.id, "nombre_completo": u.nombre, "rol": u.rol} if u else None
    
    return {
        "cambio_adscripcion_id": cambio.id,
        "folio": cambio.folio,
        "tipo_cambio": cambio.tipo_cambio,
        "objeto": cambio.objeto,
        "estatus": cambio.estatus,
        "resumen": cambio.resumen,
        "persona_afectada": persona,
        "antes": antes,
        "despues": despues,
        "fecha_efecto": cambio.fecha_efecto.isoformat() if cambio.fecha_efecto else None,
        "fecha_limite": cambio.fecha_limite.isoformat() if cambio.fecha_limite else None,
        "propuesto_por": propuesto_por,
        "autorizado_por": autorizado_por,
        "aplicado_por": aplicado_por,
        "destino_id": cambio.destino_id,
        "destinatario": destinatario,
        "observaciones": cambio.observaciones,
        "created_at": cambio.created_at.isoformat() if cambio.created_at else None
    }


@router.post("/cambios-adscripcion")
def crear_cambio_adscripcion(
    data: CambioAdscripcionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear un nuevo cambio de adscripción (propuesta)"""
    folio = generar_folio("CA")
    
    # Calcular fecha límite (SLA de 5 días hábiles)
    fecha_limite = datetime.utcnow() + timedelta(days=7)
    
    # Si se envía estatus EN_REVISION, se salta el borrador
    estatus_inicial = "EN_REVISION" if data.estatus == "EN_REVISION" else "BORRADOR"
    
    cambio = CambioAdscripcion(
        folio=folio,
        tipo_cambio=data.tipo_cambio.upper(),
        objeto=data.objeto.upper(),
        persona_id=data.persona_id,
        cac_origen_id=data.cac_origen_id,
        cac_destino_id=data.cac_destino_id,
        ruta_origen_id=data.ruta_origen_id,
        ruta_destino_id=data.ruta_destino_id,
        territorio_origen_id=data.territorio_origen_id,
        territorio_destino_id=data.territorio_destino_id,
        resumen=data.resumen,
        fecha_efecto=data.fecha_efecto,
        fecha_limite=fecha_limite,
        estatus=estatus_inicial,
        propuesto_por_id=current_user["user_id"],
        destino_id=data.destino_id  # Usuario destinatario
    )
    
    db.add(cambio)
    db.commit()
    db.refresh(cambio)
    
    return {"mensaje": "Cambio de adscripción creado", "id": cambio.id, "folio": folio}


@router.post("/cambios-adscripcion/{cambio_id}/enviar-revision")
def enviar_a_revision(
    cambio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enviar cambio de borrador a revisión"""
    cambio = db.query(CambioAdscripcion).filter(CambioAdscripcion.id == cambio_id).first()
    if not cambio:
        raise HTTPException(status_code=404, detail="Cambio no encontrado")
    
    if cambio.estatus != "BORRADOR":
        raise HTTPException(status_code=400, detail="Solo cambios en borrador pueden enviarse a revisión")
    
    if cambio.propuesto_por_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Solo el creador puede enviar a revisión")
    
    cambio.estatus = "EN_REVISION"
    db.commit()
    
    # Crear notificación para superiores
    notif = Notificacion(
        titulo="Nuevo cambio de adscripción pendiente",
        mensaje=f"Cambio {cambio.folio}: {cambio.resumen or cambio.tipo_cambio}",
        tipo="solicitud",
        rol_destino="territorial"
    )
    db.add(notif)
    db.commit()
    
    return {"mensaje": "Cambio enviado a revisión"}


@router.post("/cambios-adscripcion/{cambio_id}/accion")
def ejecutar_accion_cambio(
    cambio_id: int,
    data: CambioAdscripcionAccion,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ejecutar acción sobre un cambio:
    - AUTORIZAR: aprobar (territorial/admin)
    - RECHAZAR: rechazar con observaciones
    - APLICAR: ejecutar cambios en tablas oficiales (admin)
    - CANCELAR: cancelar cambio (creador o admin)
    """
    cambio = db.query(CambioAdscripcion).filter(CambioAdscripcion.id == cambio_id).first()
    if not cambio:
        raise HTTPException(status_code=404, detail="Cambio no encontrado")
    
    accion = data.accion.upper()
    rol = current_user["rol"]
    user_id = current_user["user_id"]
    
    if accion == "AUTORIZAR":
        if cambio.estatus != "EN_REVISION":
            raise HTTPException(status_code=400, detail="Solo cambios en revisión pueden autorizarse")
        
        if "ADMIN" not in rol and "TERRITORIAL" not in rol:
            raise HTTPException(status_code=403, detail="No tiene permisos para autorizar")
        
        cambio.estatus = "AUTORIZADO"
        cambio.autorizado_por_id = user_id
        cambio.observaciones = data.observaciones
        
    elif accion == "RECHAZAR":
        if cambio.estatus not in ["EN_REVISION", "AUTORIZADO"]:
            raise HTTPException(status_code=400, detail="No se puede rechazar en este estado")
        
        if "ADMIN" not in rol and "TERRITORIAL" not in rol:
            raise HTTPException(status_code=403, detail="No tiene permisos para rechazar")
        
        cambio.estatus = "RECHAZADO"
        cambio.observaciones = data.observaciones
        
    elif accion == "APLICAR":
        if cambio.estatus != "AUTORIZADO":
            raise HTTPException(status_code=400, detail="Solo cambios autorizados pueden aplicarse")
        
        if "ADMIN" not in rol:
            raise HTTPException(status_code=403, detail="Solo admin puede aplicar cambios")
        
        # Ejecutar el cambio real
        _aplicar_cambio_adscripcion(cambio, db)
        
        cambio.estatus = "APLICADO"
        cambio.aplicado_por_id = user_id
        
    elif accion == "CANCELAR":
        if cambio.estatus in ["APLICADO", "CANCELADO"]:
            raise HTTPException(status_code=400, detail="No se puede cancelar")
        
        if cambio.propuesto_por_id != user_id and "ADMIN" not in rol:
            raise HTTPException(status_code=403, detail="No tiene permisos para cancelar")
        
        cambio.estatus = "CANCELADO"
        cambio.observaciones = data.observaciones
    
    else:
        raise HTTPException(status_code=400, detail=f"Acción {accion} no válida")
    
    db.commit()
    return {"mensaje": f"Cambio {accion.lower()} exitosamente"}


def _aplicar_cambio_adscripcion(cambio: CambioAdscripcion, db: Session):
    """Aplica los cambios reales en las tablas según el tipo de cambio"""
    
    if cambio.objeto == "PERSONA_CAC":
        # Reasignar persona de una CAC a otra
        if cambio.tipo_cambio == "REASIGNACION":
            # Quitar de CAC origen
            if cambio.cac_origen_id:
                cac_orig = db.query(CAC).filter(CAC.id == cambio.cac_origen_id).first()
                if cac_orig:
                    if cac_orig.tecnico_social_id == cambio.persona_id:
                        cac_orig.tecnico_social_id = None
                    if cac_orig.tecnico_productivo_id == cambio.persona_id:
                        cac_orig.tecnico_productivo_id = None
                    cac_orig.estatus = "VACANTE"
            
            # Agregar a CAC destino
            if cambio.cac_destino_id and cambio.persona_id:
                cac_dest = db.query(CAC).filter(CAC.id == cambio.cac_destino_id).first()
                persona = db.query(User).filter(User.id == cambio.persona_id).first()
                if cac_dest and persona:
                    if "SOCIAL" in (persona.perfil_operativo or "").upper():
                        cac_dest.tecnico_social_id = persona.id
                    else:
                        cac_dest.tecnico_productivo_id = persona.id
                    
                    # Actualizar estatus
                    if cac_dest.tecnico_social_id and cac_dest.tecnico_productivo_id:
                        cac_dest.estatus = "OK"
        
        elif cambio.tipo_cambio == "BAJA":
            if cambio.cac_origen_id:
                cac = db.query(CAC).filter(CAC.id == cambio.cac_origen_id).first()
                if cac:
                    if cac.tecnico_social_id == cambio.persona_id:
                        cac.tecnico_social_id = None
                    if cac.tecnico_productivo_id == cambio.persona_id:
                        cac.tecnico_productivo_id = None
                    cac.estatus = "VACANTE"
        
        elif cambio.tipo_cambio == "ALTA":
            if cambio.cac_destino_id and cambio.persona_id:
                cac = db.query(CAC).filter(CAC.id == cambio.cac_destino_id).first()
                persona = db.query(User).filter(User.id == cambio.persona_id).first()
                if cac and persona:
                    if "SOCIAL" in (persona.perfil_operativo or "").upper():
                        cac.tecnico_social_id = persona.id
                    else:
                        cac.tecnico_productivo_id = persona.id
    
    elif cambio.objeto == "CAC_RUTA":
        # Mover CAC de una ruta a otra
        if cambio.cac_origen_id and cambio.ruta_destino_id:
            cac = db.query(CAC).filter(CAC.id == cambio.cac_origen_id).first()
            if cac:
                cac.ruta_id = cambio.ruta_destino_id
    
    db.commit()


# ========== ACTUALIZACIONES DE ESTRUCTURA ENDPOINTS ==========

@router.get("/actualizaciones-estructura")
def listar_actualizaciones_estructura(
    tipo_objeto: Optional[str] = None,
    accion: Optional[str] = None,
    estatus: Optional[str] = None,
    territorio_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista actualizaciones de estructura pendientes/históricas"""
    query = db.query(ActualizacionEstructura)
    
    if tipo_objeto:
        query = query.filter(ActualizacionEstructura.tipo_objeto == tipo_objeto.upper())
    
    if accion:
        query = query.filter(ActualizacionEstructura.accion == accion.upper())
    
    if estatus:
        query = query.filter(ActualizacionEstructura.estatus == estatus.upper())
    
    # Filtrar por rol
    rol = current_user["rol"]
    user_id = current_user["user_id"]
    
    if "ADMIN" not in rol:
        if "TECNICO" in rol:
            query = query.filter(ActualizacionEstructura.propuesto_por_id == user_id)
        elif "FACILITADOR" in rol or "TERRITORIAL" in rol:
            query = query.filter(
                or_(
                    ActualizacionEstructura.propuesto_por_id == user_id,
                    ActualizacionEstructura.estatus == "EN_REVISION"
                )
            )
    
    actualizaciones = query.order_by(ActualizacionEstructura.created_at.desc()).limit(100).all()
    
    result = []
    for a in actualizaciones:
        propuesto_por = None
        if a.propuesto_por_id:
            u = db.query(User).filter(User.id == a.propuesto_por_id).first()
            if u:
                propuesto_por = {"id": u.id, "nombre": u.nombre}
        
        result.append({
            "actualizacion_id": a.id,
            "folio": a.folio,
            "tipo_objeto": a.tipo_objeto,
            "accion": a.accion,
            "estatus": a.estatus,
            "resumen": a.resumen,
            "payload_propuesto": a.payload_propuesto,
            "propuesto_por": propuesto_por,
            "created_at": a.created_at.isoformat() if a.created_at else None
        })
    
    return {"items": result, "total": len(result)}


@router.get("/actualizaciones-estructura/{actualizacion_id}")
def obtener_actualizacion_estructura(
    actualizacion_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener detalle de actualización con comparador antes/después"""
    act = db.query(ActualizacionEstructura).filter(ActualizacionEstructura.id == actualizacion_id).first()
    if not act:
        raise HTTPException(status_code=404, detail="Actualización no encontrada")
    
    propuesto_por = autorizado_por = aplicado_por = None
    
    if act.propuesto_por_id:
        u = db.query(User).filter(User.id == act.propuesto_por_id).first()
        propuesto_por = {"id": u.id, "nombre": u.nombre} if u else None
    
    if act.autorizado_por_id:
        u = db.query(User).filter(User.id == act.autorizado_por_id).first()
        autorizado_por = {"id": u.id, "nombre": u.nombre} if u else None
    
    if act.aplicado_por_id:
        u = db.query(User).filter(User.id == act.aplicado_por_id).first()
        aplicado_por = {"id": u.id, "nombre": u.nombre} if u else None
    
    return {
        "actualizacion_id": act.id,
        "folio": act.folio,
        "tipo_objeto": act.tipo_objeto,
        "accion": act.accion,
        "objeto_id": act.objeto_id,
        "estatus": act.estatus,
        "resumen": act.resumen,
        "payload_propuesto": act.payload_propuesto,
        "payload_anterior": act.payload_anterior,
        "propuesto_por": propuesto_por,
        "autorizado_por": autorizado_por,
        "aplicado_por": aplicado_por,
        "observaciones": act.observaciones,
        "created_at": act.created_at.isoformat() if act.created_at else None
    }


@router.post("/actualizaciones-estructura")
def crear_actualizacion_estructura(
    data: ActualizacionEstructuraCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear nueva propuesta de actualización de estructura"""
    folio = generar_folio("AE")
    
    # Obtener payload anterior si es edición
    payload_anterior = None
    if data.accion.upper() == "EDITAR" and data.objeto_id:
        if data.tipo_objeto.upper() == "PERSONA":
            obj = db.query(User).filter(User.id == data.objeto_id).first()
            if obj:
                payload_anterior = {
                    "nombre": obj.nombre,
                    "email": obj.email,
                    "telefono": obj.telefono,
                    "curp": obj.curp,
                    "perfil_operativo": obj.perfil_operativo
                }
        elif data.tipo_objeto.upper() == "CAC":
            obj = db.query(CAC).filter(CAC.id == data.objeto_id).first()
            if obj:
                payload_anterior = {
                    "nombre": obj.nombre,
                    "latitud": obj.latitud,
                    "longitud": obj.longitud,
                    "ruta_id": obj.ruta_id
                }
        elif data.tipo_objeto.upper() == "RUTA":
            obj = db.query(Ruta).filter(Ruta.id == data.objeto_id).first()
            if obj:
                payload_anterior = {
                    "nombre": obj.nombre,
                    "territorio_id": obj.territorio_id
                }
        elif data.tipo_objeto.upper() == "TERRITORIO":
            obj = db.query(Territorio).filter(Territorio.id == data.objeto_id).first()
            if obj:
                payload_anterior = {
                    "nombre": obj.nombre,
                    "estado_region": obj.estado_region
                }
    
    actualizacion = ActualizacionEstructura(
        folio=folio,
        tipo_objeto=data.tipo_objeto.upper(),
        accion=data.accion.upper(),
        objeto_id=data.objeto_id,
        payload_propuesto=data.payload_propuesto,
        payload_anterior=payload_anterior,
        resumen=data.resumen,
        estatus="EN_REVISION",
        propuesto_por_id=current_user["user_id"]
    )
    
    db.add(actualizacion)
    db.commit()
    db.refresh(actualizacion)
    
    return {"mensaje": "Actualización creada", "id": actualizacion.id, "folio": folio}


@router.post("/actualizaciones-estructura/{actualizacion_id}/accion")
def ejecutar_accion_actualizacion(
    actualizacion_id: int,
    data: ActualizacionEstructuraAccion,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ejecutar acción sobre actualización:
    - AUTORIZAR
    - RECHAZAR
    - APLICAR
    - CANCELAR
    """
    act = db.query(ActualizacionEstructura).filter(ActualizacionEstructura.id == actualizacion_id).first()
    if not act:
        raise HTTPException(status_code=404, detail="Actualización no encontrada")
    
    accion = data.accion.upper()
    rol = current_user["rol"]
    user_id = current_user["user_id"]
    
    if accion == "AUTORIZAR":
        if act.estatus != "EN_REVISION":
            raise HTTPException(status_code=400, detail="Solo actualizaciones en revisión pueden autorizarse")
        
        if "ADMIN" not in rol and "TERRITORIAL" not in rol:
            raise HTTPException(status_code=403, detail="No tiene permisos para autorizar")
        
        act.estatus = "AUTORIZADO"
        act.autorizado_por_id = user_id
        act.observaciones = data.observaciones
        
    elif accion == "RECHAZAR":
        if act.estatus != "EN_REVISION":
            raise HTTPException(status_code=400, detail="Solo actualizaciones en revisión pueden rechazarse")
        
        act.estatus = "RECHAZADO"
        act.observaciones = data.observaciones
        
    elif accion == "APLICAR":
        if act.estatus != "AUTORIZADO":
            raise HTTPException(status_code=400, detail="Solo actualizaciones autorizadas pueden aplicarse")
        
        if "ADMIN" not in rol:
            raise HTTPException(status_code=403, detail="Solo admin puede aplicar")
        
        # Aplicar cambios
        _aplicar_actualizacion_estructura(act, db)
        
        act.estatus = "APLICADO"
        act.aplicado_por_id = user_id
        
    elif accion == "CANCELAR":
        if act.estatus in ["APLICADO", "CANCELADO"]:
            raise HTTPException(status_code=400, detail="No se puede cancelar")
        
        act.estatus = "CANCELADO"
        act.observaciones = data.observaciones
    
    else:
        raise HTTPException(status_code=400, detail=f"Acción {accion} no válida")
    
    db.commit()
    return {"mensaje": f"Actualización {accion.lower()} exitosamente"}


def _aplicar_actualizacion_estructura(act: ActualizacionEstructura, db: Session):
    """Aplica los cambios de estructura en las tablas correspondientes"""
    
    payload = act.payload_propuesto or {}
    
    if act.tipo_objeto == "PERSONA":
        if act.accion == "EDITAR" and act.objeto_id:
            persona = db.query(User).filter(User.id == act.objeto_id).first()
            if persona:
                for key, value in payload.items():
                    if hasattr(persona, key) and key not in ["id", "password"]:
                        setattr(persona, key, value)
        
        elif act.accion == "INACTIVAR" and act.objeto_id:
            persona = db.query(User).filter(User.id == act.objeto_id).first()
            if persona:
                persona.activo = False
    
    elif act.tipo_objeto == "CAC":
        if act.accion == "CREAR":
            nueva_cac = CAC(
                nombre=payload.get("nombre", "").upper(),
                ruta_id=payload.get("ruta_id"),
                latitud=payload.get("latitud"),
                longitud=payload.get("longitud"),
                estatus="VACANTE"
            )
            db.add(nueva_cac)
        
        elif act.accion == "EDITAR" and act.objeto_id:
            cac = db.query(CAC).filter(CAC.id == act.objeto_id).first()
            if cac:
                for key, value in payload.items():
                    if hasattr(cac, key) and key != "id":
                        setattr(cac, key, value)
        
        elif act.accion == "INACTIVAR" and act.objeto_id:
            cac = db.query(CAC).filter(CAC.id == act.objeto_id).first()
            if cac:
                cac.activo = False
    
    elif act.tipo_objeto == "RUTA":
        if act.accion == "CREAR":
            nueva_ruta = Ruta(
                nombre=payload.get("nombre", "").upper(),
                territorio_id=payload.get("territorio_id")
            )
            db.add(nueva_ruta)
        
        elif act.accion == "EDITAR" and act.objeto_id:
            ruta = db.query(Ruta).filter(Ruta.id == act.objeto_id).first()
            if ruta:
                for key, value in payload.items():
                    if hasattr(ruta, key) and key != "id":
                        setattr(ruta, key, value)
        
        elif act.accion == "INACTIVAR" and act.objeto_id:
            ruta = db.query(Ruta).filter(Ruta.id == act.objeto_id).first()
            if ruta:
                ruta.activo = False
    
    elif act.tipo_objeto == "TERRITORIO":
        if act.accion == "CREAR":
            nuevo_territorio = Territorio(
                nombre=payload.get("nombre", "").upper(),
                estado_region=payload.get("estado_region")
            )
            db.add(nuevo_territorio)
        
        elif act.accion == "EDITAR" and act.objeto_id:
            territorio = db.query(Territorio).filter(Territorio.id == act.objeto_id).first()
            if territorio:
                for key, value in payload.items():
                    if hasattr(territorio, key) and key != "id":
                        setattr(territorio, key, value)
        
        elif act.accion == "INACTIVAR" and act.objeto_id:
            territorio = db.query(Territorio).filter(Territorio.id == act.objeto_id).first()
            if territorio:
                territorio.activo = False
    
    db.commit()


# ========== DASHBOARD OPERATIVO ENDPOINTS ==========

@router.get("/dashboard-operativo")
def dashboard_operativo(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Panel general (dashboard operativo) para Admin:
    - Personal activo por rol
    - Territorios/rutas/CAC activos
    - Cambios vencidos (SLA)
    - Pendientes por autorizar/aplicar
    """
    rol = current_user["rol"]
    
    if "ADMIN" not in rol:
        raise HTTPException(status_code=403, detail="Solo admin puede ver dashboard operativo global")
    
    ahora = datetime.utcnow()
    
    # Personal activo por rol
    personal_por_rol = db.query(
        User.rol, func.count(User.id)
    ).filter(User.activo == True).group_by(User.rol).all()
    
    personal = {r[0]: r[1] for r in personal_por_rol}
    
    # Conteos de estructura
    territorios_activos = db.query(Territorio).filter(Territorio.activo == True).count()
    rutas_activas = db.query(Ruta).filter(Ruta.activo == True).count()
    cac_activas = db.query(CAC).filter(CAC.activo == True).count()
    
    # Cambios vencidos
    cambios_vencidos = db.query(CambioAdscripcion).filter(
        CambioAdscripcion.fecha_limite < ahora,
        CambioAdscripcion.estatus.in_(["BORRADOR", "EN_REVISION", "AUTORIZADO"])
    ).count()
    
    # Pendientes por autorizar
    pendientes_autorizar = db.query(CambioAdscripcion).filter(
        CambioAdscripcion.estatus == "EN_REVISION"
    ).count()
    
    # Autorizados pendientes de aplicar
    pendientes_aplicar = db.query(CambioAdscripcion).filter(
        CambioAdscripcion.estatus == "AUTORIZADO"
    ).count()
    
    # Top 10 territorios con más pendientes
    top_territorios = db.query(
        Territorio.nombre,
        func.count(CambioAdscripcion.id).label("pendientes")
    ).outerjoin(
        CambioAdscripcion,
        or_(
            CambioAdscripcion.territorio_origen_id == Territorio.id,
            CambioAdscripcion.territorio_destino_id == Territorio.id
        )
    ).filter(
        CambioAdscripcion.estatus.in_(["EN_REVISION", "AUTORIZADO"])
    ).group_by(Territorio.id).order_by(func.count(CambioAdscripcion.id).desc()).limit(10).all()
    
    # Movimientos recientes aplicados
    movimientos_recientes = db.query(CambioAdscripcion).filter(
        CambioAdscripcion.estatus == "APLICADO"
    ).order_by(CambioAdscripcion.updated_at.desc()).limit(5).all()
    
    movimientos_list = []
    for m in movimientos_recientes:
        movimientos_list.append({
            "folio": m.folio,
            "tipo": m.tipo_cambio,
            "resumen": m.resumen,
            "fecha": m.updated_at.isoformat() if m.updated_at else None
        })
    
    return {
        "indicadores": {
            "personal_activo": personal,
            "territorios_activos": territorios_activos,
            "rutas_activas": rutas_activas,
            "cac_activas": cac_activas,
            "cambios_vencidos": cambios_vencidos,
            "pendientes_autorizar": pendientes_autorizar,
            "pendientes_aplicar": pendientes_aplicar
        },
        "top_territorios_pendientes": [{"territorio": t[0], "pendientes": t[1]} for t in top_territorios],
        "movimientos_recientes": movimientos_list
    }
