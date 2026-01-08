"""
Rutas API para Workflows - Cambios de Adscripción y Actualizaciones de Estructura
Módulo 1: Personal Operativo y Estructura Territorial

Workflows:
1. Cambios de Adscripción: Alta/Baja/Reasignación de personas a CAC/Rutas/Territorios
2. Actualizaciones de Estructura: Crear/Editar/Inactivar maestros (persona/CAC/ruta/territorio)
"""

from fastapi import APIRouter, HTTPException, Depends, Security, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, extract
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from database import get_db
from models import (
    User, Territorio, Ruta, CAC, AsignacionPersonaCAC,
    CambioAdscripcion, ActualizacionEstructura, Notificacion
)
import jwt
import os
import io
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
import uuid
import asyncio

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "mi_clave_jwt_2025")

router = APIRouter(prefix="/workflows", tags=["Workflows"])
bearer_scheme = HTTPBearer()


# ========== BROADCAST HELPER ==========

async def _broadcast_cambio_notificacion(tipo: str, cambio_id: int, accion: str, user_id: int):
    """Enviar notificación WebSocket sobre cambios de adscripción"""
    try:
        from routes.notificaciones import broadcast_notification
        data = {
            "tipo": "cambio_adscripcion",
            "cambio_id": cambio_id,
            "accion": accion,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "mensaje": f"Cambio de adscripción {accion.lower()}"
        }
        await broadcast_notification(data)
        print(f"📡 Broadcast enviado: {accion} en cambio {cambio_id}")
    except Exception as e:
        print(f"⚠️ Error en broadcast: {e}")

def broadcast_sync(tipo: str, cambio_id: int, accion: str, user_id: int):
    """Wrapper síncrono para enviar broadcast"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_broadcast_cambio_notificacion(tipo, cambio_id, accion, user_id))
        loop.close()
    except Exception as e:
        print(f"⚠️ Error en broadcast sync: {e}")


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
        
        # Obtener persona afectada
        persona_afectada = None
        if c.persona_id:
            u = db.query(User).filter(User.id == c.persona_id).first()
            if u:
                persona_afectada = {"id": u.id, "nombre": u.nombre, "rol": u.rol, "activo": u.activo}
        
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
            "persona_id": c.persona_id,
            "persona_afectada": persona_afectada,
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
        "propuesto_por_id": cambio.propuesto_por_id,
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
    
    # 📡 Broadcast WebSocket para notificar creación
    try:
        broadcast_sync("cambio_adscripcion", cambio.id, "CREADO", current_user["user_id"])
    except Exception as e:
        print(f"⚠️ Error broadcast: {e}")
    
    return {"mensaje": "Cambio de adscripción creado", "id": cambio.id, "folio": folio}


@router.delete("/cambios-adscripcion/{cambio_id}")
def eliminar_cambio_adscripcion(
    cambio_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar un cambio de adscripción (solo si no está EN_REVISION)"""
    cambio = db.query(CambioAdscripcion).filter(CambioAdscripcion.id == cambio_id).first()
    if not cambio:
        raise HTTPException(status_code=404, detail="Cambio no encontrado")
    
    # No se pueden eliminar cambios pendientes (EN_REVISION)
    if cambio.estatus == "EN_REVISION":
        raise HTTPException(status_code=400, detail="No se pueden eliminar solicitudes pendientes. Cancela primero la solicitud.")
    
    # Solo el propietario o admin puede eliminar
    rol = current_user.get("rol", "").lower()
    if cambio.propuesto_por_id != current_user["user_id"] and "admin" not in rol:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta solicitud")
    
    folio = cambio.folio
    db.delete(cambio)
    db.commit()
    
    return {"mensaje": f"Solicitud {folio} eliminada correctamente"}


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
    
    # 📡 Broadcast WebSocket
    try:
        broadcast_sync("cambio_adscripcion", cambio_id, "ENVIADO", current_user["user_id"])
    except Exception as e:
        print(f"⚠️ Error broadcast: {e}")
    
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
        
        # Puede aplicar: el propietario (quien propuso) o un admin
        if cambio.propuesto_por_id != user_id and "ADMIN" not in rol:
            raise HTTPException(status_code=403, detail="Solo el propietario o admin puede aplicar cambios")
        
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
    
    # 📡 Enviar notificación WebSocket en tiempo real
    try:
        broadcast_sync("cambio_adscripcion", cambio_id, accion, user_id)
    except Exception as e:
        print(f"⚠️ Error broadcast: {e}")
    
    return {"mensaje": f"Cambio {accion.lower()} exitosamente"}


def _aplicar_cambio_adscripcion(cambio: CambioAdscripcion, db: Session):
    """
    Aplica los cambios reales en las tablas según el tipo de cambio.
    
    Tipos de cambio:
    - ALTA: Activa un usuario (activo=True) y/o lo asigna a CAC/Ruta/Territorio
    - BAJA: Desactiva un usuario (activo=False) y lo desvincula de asignaciones
    - REASIGNACION: Cambia la asignación de un usuario de un lugar a otro
    
    También actualiza los campos de seguimiento:
    - estatus_laboral: ACTIVO, BAJA, SUSPENDIDO
    - fecha_alta/fecha_baja: Fecha de la acción
    - fecha_ultima_accion: Timestamp de la última acción
    - motivo_ultima_accion: Justificación del cambio
    - tipo_ultima_accion: ALTA, BAJA, REASIGNACION
    """
    from datetime import datetime
    
    # Obtener la persona afectada
    persona = None
    if cambio.persona_id:
        persona = db.query(User).filter(User.id == cambio.persona_id).first()
    
    ahora = datetime.now()
    
    # === ALTA DE USUARIO ===
    if cambio.tipo_cambio == "ALTA":
        if persona:
            # Activar el usuario
            persona.activo = True
            persona.estatus_laboral = "ACTIVO"
            persona.fecha_alta = ahora
            persona.fecha_baja = None  # Limpiar fecha de baja si existía
            persona.fecha_ultima_accion = ahora
            persona.motivo_ultima_accion = cambio.resumen
            persona.tipo_ultima_accion = "ALTA"
            print(f"✅ Usuario {persona.nombre} activado (activo=True, estatus_laboral=ACTIVO)")
        
        # Si es PERSONA_CAC, asignar a la CAC destino
        if cambio.objeto == "PERSONA_CAC" and cambio.cac_destino_id and persona:
            cac = db.query(CAC).filter(CAC.id == cambio.cac_destino_id).first()
            if cac:
                if "SOCIAL" in (persona.perfil_operativo or "").upper():
                    cac.tecnico_social_id = persona.id
                    print(f"📍 Asignado como Técnico Social a CAC {cac.nombre}")
                else:
                    cac.tecnico_productivo_id = persona.id
                    print(f"📍 Asignado como Técnico Productivo a CAC {cac.nombre}")
                
                # Actualizar estatus CAC
                if cac.tecnico_social_id and cac.tecnico_productivo_id:
                    cac.estatus = "OK"
        
        # Si es PERSONA_RUTA, asignar como facilitador
        if cambio.objeto == "PERSONA_RUTA" and cambio.ruta_destino_id and persona:
            ruta = db.query(Ruta).filter(Ruta.id == cambio.ruta_destino_id).first()
            if ruta:
                if not ruta.facilitador_principal_id:
                    ruta.facilitador_principal_id = persona.id
                    print(f"📍 Asignado como Facilitador Principal a Ruta {ruta.nombre}")
                else:
                    ruta.facilitador_apoyo_id = persona.id
                    print(f"📍 Asignado como Facilitador de Apoyo a Ruta {ruta.nombre}")
        
        # Si es PERSONA_TERRITORIO, asignar territorio
        if cambio.objeto == "PERSONA_TERRITORIO" and cambio.territorio_destino_id and persona:
            territorio = db.query(Territorio).filter(Territorio.id == cambio.territorio_destino_id).first()
            if territorio:
                persona.territorio_id = territorio.id
                persona.territorio = territorio.nombre
                print(f"📍 Asignado a Territorio {territorio.nombre}")
    
    # === BAJA DE USUARIO ===
    elif cambio.tipo_cambio == "BAJA":
        if persona:
            # Desactivar el usuario (NO se elimina, solo se marca como baja)
            persona.activo = False
            persona.estatus_laboral = "BAJA"
            persona.fecha_baja = ahora
            persona.fecha_ultima_accion = ahora
            persona.motivo_ultima_accion = cambio.resumen
            persona.tipo_ultima_accion = "BAJA"
            print(f"❌ Usuario {persona.nombre} dado de baja (activo=False, estatus_laboral=BAJA)")
        
        # Quitar de CAC origen
        if cambio.objeto == "PERSONA_CAC" and cambio.cac_origen_id:
            cac = db.query(CAC).filter(CAC.id == cambio.cac_origen_id).first()
            if cac:
                if cac.tecnico_social_id == cambio.persona_id:
                    cac.tecnico_social_id = None
                    print(f"🔓 Removido como Técnico Social de CAC {cac.nombre}")
                if cac.tecnico_productivo_id == cambio.persona_id:
                    cac.tecnico_productivo_id = None
                    print(f"🔓 Removido como Técnico Productivo de CAC {cac.nombre}")
                cac.estatus = "VACANTE"
        
        # Quitar de Ruta origen
        if cambio.objeto == "PERSONA_RUTA" and cambio.ruta_origen_id:
            ruta = db.query(Ruta).filter(Ruta.id == cambio.ruta_origen_id).first()
            if ruta:
                if ruta.facilitador_principal_id == cambio.persona_id:
                    ruta.facilitador_principal_id = None
                    print(f"🔓 Removido como Facilitador Principal de Ruta {ruta.nombre}")
                if ruta.facilitador_apoyo_id == cambio.persona_id:
                    ruta.facilitador_apoyo_id = None
                    print(f"🔓 Removido como Facilitador de Apoyo de Ruta {ruta.nombre}")
    
    # === REASIGNACION DE USUARIO ===
    elif cambio.tipo_cambio == "REASIGNACION":
        if persona:
            # Actualizar campos de seguimiento (el usuario sigue activo)
            persona.fecha_ultima_accion = ahora
            persona.motivo_ultima_accion = cambio.resumen
            persona.tipo_ultima_accion = "REASIGNACION"
            print(f"🔄 Reasignación de {persona.nombre}")
        
        if cambio.objeto == "PERSONA_CAC":
            # Quitar de CAC origen
            if cambio.cac_origen_id:
                cac_orig = db.query(CAC).filter(CAC.id == cambio.cac_origen_id).first()
                if cac_orig:
                    if cac_orig.tecnico_social_id == cambio.persona_id:
                        cac_orig.tecnico_social_id = None
                    if cac_orig.tecnico_productivo_id == cambio.persona_id:
                        cac_orig.tecnico_productivo_id = None
                    cac_orig.estatus = "VACANTE"
                    print(f"🔓 Removido de CAC origen {cac_orig.nombre}")
            
            # Agregar a CAC destino
            if cambio.cac_destino_id and persona:
                cac_dest = db.query(CAC).filter(CAC.id == cambio.cac_destino_id).first()
                if cac_dest:
                    if "SOCIAL" in (persona.perfil_operativo or "").upper():
                        cac_dest.tecnico_social_id = persona.id
                    else:
                        cac_dest.tecnico_productivo_id = persona.id
                    
                    if cac_dest.tecnico_social_id and cac_dest.tecnico_productivo_id:
                        cac_dest.estatus = "OK"
                    print(f"📍 Asignado a CAC destino {cac_dest.nombre}")
        
        elif cambio.objeto == "PERSONA_RUTA":
            # Quitar de Ruta origen
            if cambio.ruta_origen_id:
                ruta_orig = db.query(Ruta).filter(Ruta.id == cambio.ruta_origen_id).first()
                if ruta_orig:
                    if ruta_orig.facilitador_principal_id == cambio.persona_id:
                        ruta_orig.facilitador_principal_id = None
                    if ruta_orig.facilitador_apoyo_id == cambio.persona_id:
                        ruta_orig.facilitador_apoyo_id = None
                    print(f"🔓 Removido de Ruta origen {ruta_orig.nombre}")
            
            # Agregar a Ruta destino
            if cambio.ruta_destino_id and persona:
                ruta_dest = db.query(Ruta).filter(Ruta.id == cambio.ruta_destino_id).first()
                if ruta_dest:
                    if not ruta_dest.facilitador_principal_id:
                        ruta_dest.facilitador_principal_id = persona.id
                    else:
                        ruta_dest.facilitador_apoyo_id = persona.id
                    print(f"📍 Asignado a Ruta destino {ruta_dest.nombre}")
        
        elif cambio.objeto == "PERSONA_TERRITORIO":
            # Cambiar territorio
            if cambio.territorio_destino_id and persona:
                territorio = db.query(Territorio).filter(Territorio.id == cambio.territorio_destino_id).first()
                if territorio:
                    persona.territorio_id = territorio.id
                    persona.territorio = territorio.nombre
                    print(f"📍 Reasignado a Territorio {territorio.nombre}")
        
        elif cambio.objeto == "CAC_RUTA":
            # Mover CAC de una ruta a otra
            if cambio.cac_origen_id and cambio.ruta_destino_id:
                cac = db.query(CAC).filter(CAC.id == cambio.cac_origen_id).first()
                if cac:
                    cac.ruta_id = cambio.ruta_destino_id
                    print(f"📍 CAC {cac.nombre} movido a nueva ruta")
    
    db.commit()
    print(f"✅ Cambio aplicado exitosamente: {cambio.tipo_cambio} - {cambio.objeto}")


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


# ========== REPORTES - EXPORTACIÓN EXCEL/PDF ==========

def _obtener_datos_reporte_interno(
    tipo_cambio: Optional[str],
    estatus: Optional[str],
    periodo: Optional[str],
    anio: Optional[int],
    mes: Optional[int],
    semana: Optional[int],
    fecha_inicio: Optional[str],
    fecha_fin: Optional[str],
    solo_vigentes: Optional[bool],  # NUEVO: Para filtrar bajas/altas vigentes
    current_user: dict,
    db: Session
):
    """
    Función interna para obtener datos de reportes.
    Usada tanto por el endpoint como por las exportaciones.
    
    solo_vigentes: Si es True, filtra para mostrar solo cambios "vigentes":
    - Para BAJA: Solo personas que siguen inactivas (no fueron dadas de alta después)
    - Para ALTA: Solo personas que siguen activas (no fueron dadas de baja después)
    """
    user_id = current_user["user_id"]
    rol = current_user["rol"]
    
    query = db.query(CambioAdscripcion)
    
    # Filtrar por usuario (excepto admin que ve todo)
    if "ADMIN" not in rol:
        query = query.filter(
            or_(
                CambioAdscripcion.propuesto_por_id == user_id,
                CambioAdscripcion.destino_id == user_id,
                CambioAdscripcion.persona_id == user_id
            )
        )
    
    # Filtrar por tipo de cambio
    if tipo_cambio:
        query = query.filter(CambioAdscripcion.tipo_cambio == tipo_cambio.upper())
    
    # Filtrar por estatus
    if estatus:
        query = query.filter(CambioAdscripcion.estatus == estatus.upper())
    
    # Filtrar por período
    ahora = datetime.utcnow()
    
    if periodo == "semana":
        if anio and semana:
            inicio_semana = datetime.strptime(f'{anio}-W{semana}-1', "%Y-W%W-%w")
            fin_semana = inicio_semana + timedelta(days=7)
        else:
            inicio_semana = ahora - timedelta(days=ahora.weekday())
            inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
            fin_semana = inicio_semana + timedelta(days=7)
        
        query = query.filter(
            CambioAdscripcion.created_at >= inicio_semana,
            CambioAdscripcion.created_at < fin_semana
        )
    
    elif periodo == "mes":
        if anio and mes:
            inicio_mes = datetime(anio, mes, 1)
            if mes == 12:
                fin_mes = datetime(anio + 1, 1, 1)
            else:
                fin_mes = datetime(anio, mes + 1, 1)
        else:
            inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if ahora.month == 12:
                fin_mes = datetime(ahora.year + 1, 1, 1)
            else:
                fin_mes = ahora.replace(month=ahora.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        query = query.filter(
            CambioAdscripcion.created_at >= inicio_mes,
            CambioAdscripcion.created_at < fin_mes
        )
    
    elif periodo == "trimestre":
        trimestre = (ahora.month - 1) // 3
        inicio_trimestre = datetime(ahora.year, trimestre * 3 + 1, 1)
        if trimestre == 3:
            fin_trimestre = datetime(ahora.year + 1, 1, 1)
        else:
            fin_trimestre = datetime(ahora.year, (trimestre + 1) * 3 + 1, 1)
        
        query = query.filter(
            CambioAdscripcion.created_at >= inicio_trimestre,
            CambioAdscripcion.created_at < fin_trimestre
        )
    
    elif periodo == "anio":
        year = anio if anio else ahora.year
        inicio_anio = datetime(year, 1, 1)
        fin_anio = datetime(year + 1, 1, 1)
        
        query = query.filter(
            CambioAdscripcion.created_at >= inicio_anio,
            CambioAdscripcion.created_at < fin_anio
        )
    
    elif periodo == "custom" and fecha_inicio and fecha_fin:
        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(
                CambioAdscripcion.created_at >= inicio,
                CambioAdscripcion.created_at < fin
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido (usar YYYY-MM-DD)")
    
    # Ordenar por fecha
    cambios = query.order_by(CambioAdscripcion.created_at.desc()).all()
    
    # Construir resultado con detalles
    result = []
    for c in cambios:
        propuesto_por_nombre = ""
        if c.propuesto_por_id:
            u = db.query(User).filter(User.id == c.propuesto_por_id).first()
            propuesto_por_nombre = u.nombre if u else ""
        
        destinatario_nombre = ""
        if c.destino_id:
            u = db.query(User).filter(User.id == c.destino_id).first()
            destinatario_nombre = u.nombre if u else ""
        
        persona_afectada_nombre = ""
        persona_afectada_curp = ""
        persona_activa = True  # Estado actual de la persona
        if c.persona_id:
            u = db.query(User).filter(User.id == c.persona_id).first()
            if u:
                persona_afectada_nombre = u.nombre
                persona_afectada_curp = u.curp or ""
                persona_activa = u.is_active if hasattr(u, 'is_active') else True
        
        # Filtrar por vigencia si se solicita
        if solo_vigentes:
            # Para BAJA: solo incluir si la persona sigue inactiva
            if c.tipo_cambio == "BAJA" and c.estatus == "APLICADO":
                if persona_activa:
                    continue  # Persona fue reactivada, omitir
            # Para ALTA: solo incluir si la persona sigue activa
            elif c.tipo_cambio == "ALTA" and c.estatus == "APLICADO":
                if not persona_activa:
                    continue  # Persona fue dada de baja después, omitir
        
        result.append({
            "id": c.id,
            "folio": c.folio,
            "tipo_cambio": c.tipo_cambio,
            "objeto": c.objeto,
            "estatus": c.estatus,
            "resumen": c.resumen or "",
            "fecha_creacion": c.created_at.strftime("%Y-%m-%d %H:%M") if c.created_at else "",
            "fecha_efecto": c.fecha_efecto.strftime("%Y-%m-%d") if c.fecha_efecto else "",
            "propuesto_por": propuesto_por_nombre,
            "destinatario": destinatario_nombre,
            "persona_afectada": persona_afectada_nombre,
            "curp_afectado": persona_afectada_curp,
            "observaciones": c.observaciones or "",
            "persona_activa": persona_activa  # Estado actual
        })
    
    # Estadísticas resumidas
    total = len(result)
    altas = len([r for r in result if r["tipo_cambio"] == "ALTA"])
    bajas = len([r for r in result if r["tipo_cambio"] == "BAJA"])
    reasignaciones = len([r for r in result if r["tipo_cambio"] == "REASIGNACION"])
    aplicados = len([r for r in result if r["estatus"] == "APLICADO"])
    pendientes = len([r for r in result if r["estatus"] in ["EN_REVISION", "AUTORIZADO"]])
    rechazados = len([r for r in result if r["estatus"] == "RECHAZADO"])
    cancelados = len([r for r in result if r["estatus"] == "CANCELADO"])
    
    # Contadores de vigencia (bajas donde la persona sigue inactiva, altas donde sigue activa)
    bajas_vigentes = len([r for r in result if r["tipo_cambio"] == "BAJA" and r["estatus"] == "APLICADO" and not r.get("persona_activa", True)])
    altas_vigentes = len([r for r in result if r["tipo_cambio"] == "ALTA" and r["estatus"] == "APLICADO" and r.get("persona_activa", True)])
    
    return {
        "items": result,
        "resumen": {
            "total": total,
            "por_tipo": {
                "altas": altas,
                "bajas": bajas,
                "reasignaciones": reasignaciones
            },
            "por_estatus": {
                "aplicados": aplicados,
                "pendientes": pendientes,
                "rechazados": rechazados,
                "cancelados": cancelados
            },
            "vigentes": {
                "bajas_vigentes": bajas_vigentes,
                "altas_vigentes": altas_vigentes
            }
        }
    }


@router.get("/reportes/mis-solicitudes")
def obtener_datos_reporte_endpoint(
    tipo_cambio: Optional[str] = None,
    estatus: Optional[str] = None,
    periodo: Optional[str] = None,
    anio: Optional[int] = None,
    mes: Optional[int] = None,
    semana: Optional[int] = None,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    solo_vigentes: Optional[bool] = False,  # NUEVO: Filtrar solo bajas/altas vigentes
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint para obtener datos de reportes del usuario actual.
    
    solo_vigentes: Si es True, filtra para mostrar solo:
    - Bajas donde la persona sigue inactiva
    - Altas donde la persona sigue activa
    """
    return _obtener_datos_reporte_interno(
        tipo_cambio=tipo_cambio,
        estatus=estatus,
        periodo=periodo,
        anio=anio,
        mes=mes,
        semana=semana,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        solo_vigentes=solo_vigentes,
        current_user=current_user,
        db=db
    )


@router.get("/reportes/exportar-excel")
def exportar_excel(
    tipo_cambio: Optional[str] = None,
    estatus: Optional[str] = None,
    periodo: Optional[str] = None,
    anio: Optional[int] = None,
    mes: Optional[int] = None,
    semana: Optional[int] = None,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    solo_vigentes: Optional[bool] = False,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Exportar reporte a Excel (.xlsx)"""
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError as e:
        print(f"❌ Error importando openpyxl: {e}")
        raise HTTPException(status_code=500, detail="La librería openpyxl no está instalada en el servidor. Contacte al administrador.")
    
    try:
        # Obtener datos usando la función interna
        datos = _obtener_datos_reporte_interno(
            tipo_cambio=tipo_cambio,
            estatus=estatus,
            periodo=periodo,
            anio=anio,
            mes=mes,
            semana=semana,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            solo_vigentes=solo_vigentes,
            current_user=current_user,
            db=db
        )
        
        # Crear workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Reporte Solicitudes"
        
        # Estilos
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_fill = PatternFill(start_color="16A34A", end_color="16A34A", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell_alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        thin_border = Border(
            left=Side(style='thin', color='E5E7EB'),
            right=Side(style='thin', color='E5E7EB'),
            top=Side(style='thin', color='E5E7EB'),
            bottom=Side(style='thin', color='E5E7EB')
        )
        
        # Título del reporte
        ws.merge_cells('A1:K1')
        ws['A1'] = "REPORTE DE SOLICITUDES - SISTEMA DE GESTIÓN"
        ws['A1'].font = Font(bold=True, size=14, color="16A34A")
        ws['A1'].alignment = Alignment(horizontal="center")
        
        # Fecha de generación
        ws.merge_cells('A2:K2')
        ws['A2'] = f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        ws['A2'].font = Font(italic=True, size=10, color="6B7280")
        ws['A2'].alignment = Alignment(horizontal="center")
        
        # Resumen
        resumen = datos["resumen"]
        ws['A4'] = "RESUMEN:"
        ws['A4'].font = Font(bold=True, size=11)
        ws['A5'] = f"Total: {resumen['total']} | Altas: {resumen['por_tipo']['altas']} | Bajas: {resumen['por_tipo']['bajas']} | Reasignaciones: {resumen['por_tipo']['reasignaciones']}"
        ws['A6'] = f"Aplicados: {resumen['por_estatus']['aplicados']} | Pendientes: {resumen['por_estatus']['pendientes']} | Rechazados: {resumen['por_estatus']['rechazados']} | Cancelados: {resumen['por_estatus']['cancelados']}"
        
        # Encabezados de la tabla
        headers = ["Folio", "Tipo", "Objeto", "Estatus", "Fecha Creación", "Persona Afectada", "CURP", "Solicitante", "Destinatario", "Descripción", "Observaciones"]
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=8, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = thin_border
        
        # Datos
        for row_idx, item in enumerate(datos["items"], 9):
            ws.cell(row=row_idx, column=1, value=item["folio"]).border = thin_border
            ws.cell(row=row_idx, column=2, value=item["tipo_cambio"]).border = thin_border
            ws.cell(row=row_idx, column=3, value=item["objeto"]).border = thin_border
            ws.cell(row=row_idx, column=4, value=item["estatus"]).border = thin_border
            ws.cell(row=row_idx, column=5, value=item["fecha_creacion"]).border = thin_border
            ws.cell(row=row_idx, column=6, value=item["persona_afectada"]).border = thin_border
            ws.cell(row=row_idx, column=7, value=item["curp_afectado"]).border = thin_border
            ws.cell(row=row_idx, column=8, value=item["propuesto_por"]).border = thin_border
            ws.cell(row=row_idx, column=9, value=item["destinatario"]).border = thin_border
            ws.cell(row=row_idx, column=10, value=item["resumen"]).border = thin_border
            ws.cell(row=row_idx, column=11, value=item["observaciones"]).border = thin_border
            
            # Aplicar colores según estatus
            estatus_cell = ws.cell(row=row_idx, column=4)
            if item["estatus"] == "APLICADO":
                estatus_cell.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
            elif item["estatus"] == "EN_REVISION":
                estatus_cell.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
            elif item["estatus"] == "RECHAZADO":
                estatus_cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
            elif item["estatus"] == "AUTORIZADO":
                estatus_cell.fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
            
            # Colores según tipo
            tipo_cell = ws.cell(row=row_idx, column=2)
            if item["tipo_cambio"] == "ALTA":
                tipo_cell.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
            elif item["tipo_cambio"] == "BAJA":
                tipo_cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
            elif item["tipo_cambio"] == "REASIGNACION":
                tipo_cell.fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
        
        # Ajustar ancho de columnas
        column_widths = [18, 14, 16, 14, 18, 25, 20, 22, 22, 35, 35]
        for i, width in enumerate(column_widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = width
        
        # Guardar en buffer
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        # Generar nombre de archivo
        fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_solicitudes_{fecha_str}.xlsx"
        
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generando Excel: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al generar el archivo Excel: {str(e)}")


@router.get("/reportes/exportar-pdf")
def exportar_pdf(
    tipo_cambio: Optional[str] = None,
    estatus: Optional[str] = None,
    periodo: Optional[str] = None,
    anio: Optional[int] = None,
    mes: Optional[int] = None,
    semana: Optional[int] = None,
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    solo_vigentes: Optional[bool] = False,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Exportar reporte a PDF"""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError as e:
        print(f"❌ Error importando reportlab: {e}")
        raise HTTPException(status_code=500, detail="La librería reportlab no está instalada en el servidor. Contacte al administrador.")
    
    try:
        # Obtener datos usando la función interna
        datos = _obtener_datos_reporte_interno(
            tipo_cambio=tipo_cambio,
            estatus=estatus,
            periodo=periodo,
            anio=anio,
            mes=mes,
            semana=semana,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            solo_vigentes=solo_vigentes,
            current_user=current_user,
            db=db
        )
        
        # Crear buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#16A34A'),
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6B7280'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        # Título
        elements.append(Paragraph("REPORTE DE SOLICITUDES", title_style))
        elements.append(Paragraph(f"Sistema de Gestión - Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style))
        
        # Resumen
        resumen = datos["resumen"]
        resumen_text = f"""
        <b>Total:</b> {resumen['total']} solicitudes | 
        <b>Altas:</b> {resumen['por_tipo']['altas']} | 
        <b>Bajas:</b> {resumen['por_tipo']['bajas']} | 
        <b>Reasignaciones:</b> {resumen['por_tipo']['reasignaciones']}<br/>
        <b>Aplicados:</b> {resumen['por_estatus']['aplicados']} | 
        <b>Pendientes:</b> {resumen['por_estatus']['pendientes']} | 
        <b>Rechazados:</b> {resumen['por_estatus']['rechazados']} | 
        <b>Cancelados:</b> {resumen['por_estatus']['cancelados']}
        """
        elements.append(Paragraph(resumen_text, styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Tabla de datos
        table_data = [["Folio", "Tipo", "Estatus", "Fecha", "Persona Afectada", "Solicitante", "Descripción"]]
        
        for item in datos["items"]:
            table_data.append([
                item["folio"],
                item["tipo_cambio"],
                item["estatus"],
                item["fecha_creacion"][:10] if item["fecha_creacion"] else "",
                item["persona_afectada"][:25] if item["persona_afectada"] else "",
                item["propuesto_por"][:20] if item["propuesto_por"] else "",
                item["resumen"][:40] + "..." if len(item["resumen"]) > 40 else item["resumen"]
            ])
        
        if len(table_data) > 1:
            table = Table(table_data, colWidths=[1.3*inch, 1*inch, 1*inch, 1*inch, 1.8*inch, 1.5*inch, 2.4*inch])
            
            table.setStyle(TableStyle([
                # Encabezado
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16A34A')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                
                # Cuerpo
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                
                # Bordes
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                
                # Alternar colores de filas
                *[('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F9FAFB')) for i in range(2, len(table_data), 2)]
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No hay datos para mostrar con los filtros seleccionados.", styles['Normal']))
        
        # Construir PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Generar nombre de archivo
        fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_solicitudes_{fecha_str}.pdf"
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generando PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al generar el archivo PDF: {str(e)}")

