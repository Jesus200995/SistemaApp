"""
Rutas API para Importaciones de Bases - Solo Administrador
Módulo 1: Personal Operativo y Estructura Territorial

Funcionalidades:
- Subir archivos (Personal, Rutas-CAC)
- Validación automática
- Resolución manual de matches
- Publicación controlada
"""

from fastapi import APIRouter, HTTPException, Depends, Security, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from database import get_db
from models import (
    User, Territorio, Ruta, CAC, 
    Importacion, ImportacionDetalle, Notificacion
)
import jwt
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid
import csv
import io

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "mi_clave_jwt_2025")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads", "importaciones")

# Crear directorio si no existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/importaciones", tags=["Importaciones"])
bearer_scheme = HTTPBearer()


# ========== PYDANTIC MODELS ==========

class ResolverMatchRequest(BaseModel):
    detalle_id: int
    persona_id: Optional[int] = None  # ID de la persona si se encontró match
    es_vacante: bool = False  # Si es vacante, no se asigna persona


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


def require_admin(current_user: dict = Depends(get_current_user)):
    """Solo Admin puede acceder a importaciones"""
    if "ADMIN" not in current_user["rol"]:
        raise HTTPException(status_code=403, detail="Solo el Administrador puede gestionar importaciones")
    return current_user


# ========== IMPORTACIONES ENDPOINTS ==========

@router.get("/")
def listar_importaciones(
    tipo: Optional[str] = None,
    estatus: Optional[str] = None,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Lista todas las importaciones"""
    query = db.query(Importacion)
    
    if tipo:
        query = query.filter(Importacion.tipo == tipo.upper())
    
    if estatus:
        query = query.filter(Importacion.estatus == estatus.upper())
    
    importaciones = query.order_by(Importacion.created_at.desc()).limit(50).all()
    
    result = []
    for imp in importaciones:
        subido_por = None
        if imp.subido_por_id:
            u = db.query(User).filter(User.id == imp.subido_por_id).first()
            if u:
                subido_por = {"id": u.id, "nombre": u.nombre}
        
        result.append({
            "id": imp.id,
            "tipo": imp.tipo,
            "archivo_nombre": imp.archivo_nombre,
            "estatus": imp.estatus,
            "filas_totales": imp.filas_totales,
            "filas_validas": imp.filas_validas,
            "errores_criticos": imp.errores_criticos,
            "warnings": imp.warnings,
            "subido_por": subido_por,
            "fecha_publicacion": imp.fecha_publicacion.isoformat() if imp.fecha_publicacion else None,
            "created_at": imp.created_at.isoformat() if imp.created_at else None
        })
    
    return {"items": result, "total": len(result)}


@router.get("/{importacion_id}")
def obtener_importacion(
    importacion_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Obtener detalle de una importación"""
    imp = db.query(Importacion).filter(Importacion.id == importacion_id).first()
    if not imp:
        raise HTTPException(status_code=404, detail="Importación no encontrada")
    
    # Obtener detalles pendientes de resolución
    detalles_pendientes = db.query(ImportacionDetalle).filter(
        ImportacionDetalle.importacion_id == importacion_id,
        ImportacionDetalle.resuelto == False
    ).all()
    
    detalles_list = []
    for d in detalles_pendientes:
        detalles_list.append({
            "id": d.id,
            "fila_numero": d.fila_numero,
            "datos_originales": d.datos_originales,
            "tipo_problema": d.tipo_problema,
            "resuelto": d.resuelto
        })
    
    subido_por = publicado_por = None
    if imp.subido_por_id:
        u = db.query(User).filter(User.id == imp.subido_por_id).first()
        subido_por = {"id": u.id, "nombre": u.nombre} if u else None
    
    if imp.publicado_por_id:
        u = db.query(User).filter(User.id == imp.publicado_por_id).first()
        publicado_por = {"id": u.id, "nombre": u.nombre} if u else None
    
    return {
        "id": imp.id,
        "tipo": imp.tipo,
        "archivo_nombre": imp.archivo_nombre,
        "estatus": imp.estatus,
        "filas_totales": imp.filas_totales,
        "filas_validas": imp.filas_validas,
        "errores_criticos": imp.errores_criticos,
        "warnings": imp.warnings,
        "notas": imp.notas,
        "subido_por": subido_por,
        "publicado_por": publicado_por,
        "fecha_publicacion": imp.fecha_publicacion.isoformat() if imp.fecha_publicacion else None,
        "detalles_pendientes": detalles_list,
        "puede_publicar": imp.errores_criticos == 0 and imp.estatus == "LISTO_PUBLICAR"
    }


@router.post("/subir")
async def subir_archivo(
    tipo: str = Form(...),
    notas: Optional[str] = Form(None),
    archivo: UploadFile = File(...),
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Subir archivo para importación.
    Tipos: PERSONAL, RUTAS_CAC
    """
    tipo = tipo.upper()
    if tipo not in ["PERSONAL", "RUTAS_CAC"]:
        raise HTTPException(status_code=400, detail="Tipo debe ser PERSONAL o RUTAS_CAC")
    
    # Validar extensión
    if not archivo.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos CSV o Excel")
    
    # Guardar archivo
    file_id = str(uuid.uuid4())[:8]
    filename = f"{file_id}_{archivo.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    content = await archivo.read()
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Crear registro de importación
    importacion = Importacion(
        tipo=tipo,
        archivo_nombre=archivo.filename,
        archivo_path=filepath,
        estatus="PENDIENTE",
        notas=notas,
        subido_por_id=current_user["user_id"]
    )
    
    db.add(importacion)
    db.commit()
    db.refresh(importacion)
    
    return {
        "mensaje": "Archivo subido exitosamente",
        "id": importacion.id,
        "siguiente_paso": f"Ejecutar validación: POST /importaciones/{importacion.id}/validar"
    }


@router.post("/{importacion_id}/validar")
def validar_importacion(
    importacion_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Ejecutar validación del archivo subido.
    Identifica errores críticos, warnings y registros que necesitan resolución manual.
    """
    imp = db.query(Importacion).filter(Importacion.id == importacion_id).first()
    if not imp:
        raise HTTPException(status_code=404, detail="Importación no encontrada")
    
    if imp.estatus not in ["PENDIENTE", "ERROR"]:
        raise HTTPException(status_code=400, detail="Solo se pueden validar importaciones pendientes")
    
    imp.estatus = "VALIDANDO"
    db.commit()
    
    try:
        # Leer archivo
        if imp.archivo_path.endswith('.csv'):
            with open(imp.archivo_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                filas = list(reader)
        else:
            # Para Excel se necesitaría openpyxl
            raise HTTPException(status_code=400, detail="Por ahora solo se soporta CSV")
        
        filas_totales = len(filas)
        filas_validas = 0
        errores_criticos = 0
        warnings = 0
        
        # Validar según tipo
        if imp.tipo == "PERSONAL":
            for i, fila in enumerate(filas, start=2):  # Empezar en 2 por header
                errores_fila = []
                
                # Validaciones críticas
                if not fila.get('nombre'):
                    errores_fila.append("Nombre requerido")
                    errores_criticos += 1
                
                curp = fila.get('curp', '').strip().upper()
                if curp:
                    # Buscar si existe la persona por CURP
                    existente = db.query(User).filter(User.curp == curp).first()
                    if not existente:
                        # Crear detalle para resolución manual
                        detalle = ImportacionDetalle(
                            importacion_id=importacion_id,
                            fila_numero=i,
                            datos_originales=fila,
                            tipo_problema="NO_ENCONTRADO"
                        )
                        db.add(detalle)
                        warnings += 1
                    else:
                        filas_validas += 1
                else:
                    # Sin CURP, crear detalle
                    detalle = ImportacionDetalle(
                        importacion_id=importacion_id,
                        fila_numero=i,
                        datos_originales=fila,
                        tipo_problema="SIN_CURP"
                    )
                    db.add(detalle)
                    warnings += 1
        
        elif imp.tipo == "RUTAS_CAC":
            for i, fila in enumerate(filas, start=2):
                # Validar estructura
                if not fila.get('territorio'):
                    errores_criticos += 1
                    continue
                
                if not fila.get('ruta'):
                    errores_criticos += 1
                    continue
                
                # Verificar si existe territorio
                territorio = db.query(Territorio).filter(
                    Territorio.nombre.ilike(f"%{fila.get('territorio')}%")
                ).first()
                
                if not territorio:
                    detalle = ImportacionDetalle(
                        importacion_id=importacion_id,
                        fila_numero=i,
                        datos_originales=fila,
                        tipo_problema="TERRITORIO_NO_ENCONTRADO"
                    )
                    db.add(detalle)
                    warnings += 1
                else:
                    filas_validas += 1
        
        # Actualizar importación
        imp.filas_totales = filas_totales
        imp.filas_validas = filas_validas
        imp.errores_criticos = errores_criticos
        imp.warnings = warnings
        
        if errores_criticos > 0:
            imp.estatus = "ERROR"
        elif warnings > 0:
            imp.estatus = "LISTO_PUBLICAR"  # Puede publicar pero con warnings
        else:
            imp.estatus = "LISTO_PUBLICAR"
        
        db.commit()
        
        return {
            "mensaje": "Validación completada",
            "filas_totales": filas_totales,
            "filas_validas": filas_validas,
            "errores_criticos": errores_criticos,
            "warnings": warnings,
            "estatus": imp.estatus,
            "puede_publicar": errores_criticos == 0
        }
        
    except Exception as e:
        imp.estatus = "ERROR"
        imp.notas = f"Error en validación: {str(e)}"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Error en validación: {str(e)}")


@router.get("/{importacion_id}/detalles-pendientes")
def obtener_detalles_pendientes(
    importacion_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Obtener registros pendientes de resolución manual"""
    detalles = db.query(ImportacionDetalle).filter(
        ImportacionDetalle.importacion_id == importacion_id,
        ImportacionDetalle.resuelto == False
    ).all()
    
    result = []
    for d in detalles:
        # Buscar posibles coincidencias por nombre
        nombre = d.datos_originales.get('nombre', '') if d.datos_originales else ''
        coincidencias = []
        
        if nombre:
            posibles = db.query(User).filter(
                User.nombre.ilike(f"%{nombre.split()[0]}%") if nombre else False,
                User.activo == True
            ).limit(5).all()
            
            for p in posibles:
                coincidencias.append({
                    "id": p.id,
                    "nombre": p.nombre,
                    "curp": p.curp,
                    "rol": p.rol
                })
        
        result.append({
            "id": d.id,
            "fila_numero": d.fila_numero,
            "datos_originales": d.datos_originales,
            "tipo_problema": d.tipo_problema,
            "coincidencias_sugeridas": coincidencias
        })
    
    return {"items": result, "total": len(result)}


@router.post("/{importacion_id}/resolver-match")
def resolver_match(
    importacion_id: int,
    data: ResolverMatchRequest,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Resolver un registro pendiente (match manual)"""
    detalle = db.query(ImportacionDetalle).filter(
        ImportacionDetalle.id == data.detalle_id,
        ImportacionDetalle.importacion_id == importacion_id
    ).first()
    
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    if data.es_vacante:
        detalle.tipo_problema = "VACANTE"
        detalle.persona_id_resuelto = None
    elif data.persona_id:
        # Verificar que existe la persona
        persona = db.query(User).filter(User.id == data.persona_id).first()
        if not persona:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        detalle.persona_id_resuelto = data.persona_id
    else:
        raise HTTPException(status_code=400, detail="Debe especificar persona_id o marcar como vacante")
    
    detalle.resuelto = True
    
    # Actualizar importación si todos los detalles están resueltos
    pendientes = db.query(ImportacionDetalle).filter(
        ImportacionDetalle.importacion_id == importacion_id,
        ImportacionDetalle.resuelto == False
    ).count()
    
    if pendientes == 0:
        imp = db.query(Importacion).filter(Importacion.id == importacion_id).first()
        if imp and imp.errores_criticos == 0:
            imp.estatus = "LISTO_PUBLICAR"
    
    db.commit()
    
    return {"mensaje": "Match resuelto", "pendientes_restantes": pendientes}


@router.post("/{importacion_id}/publicar")
def publicar_importacion(
    importacion_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Publicar importación: aplicar cambios en tablas oficiales.
    Solo si no hay errores críticos.
    """
    imp = db.query(Importacion).filter(Importacion.id == importacion_id).first()
    if not imp:
        raise HTTPException(status_code=404, detail="Importación no encontrada")
    
    if imp.estatus != "LISTO_PUBLICAR":
        raise HTTPException(status_code=400, detail="La importación no está lista para publicar")
    
    if imp.errores_criticos > 0:
        raise HTTPException(status_code=400, detail="No se puede publicar con errores críticos")
    
    try:
        # Leer archivo y aplicar cambios
        if imp.archivo_path.endswith('.csv'):
            with open(imp.archivo_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                filas = list(reader)
        
        resumen = {
            "territorios_nuevos": 0,
            "rutas_nuevas": 0,
            "cac_nuevas": 0,
            "personas_nuevas": 0,
            "personas_actualizadas": 0,
            "asignaciones_creadas": 0,
            "asignaciones_cerradas": 0
        }
        
        if imp.tipo == "PERSONAL":
            for fila in filas:
                curp = fila.get('curp', '').strip().upper()
                
                if curp:
                    existente = db.query(User).filter(User.curp == curp).first()
                    if existente:
                        # Actualizar datos
                        if fila.get('telefono'):
                            existente.telefono = fila.get('telefono')
                        if fila.get('email'):
                            existente.correo_contacto = fila.get('email')
                        resumen["personas_actualizadas"] += 1
                    else:
                        # Buscar si hay detalle resuelto
                        detalle = db.query(ImportacionDetalle).filter(
                            ImportacionDetalle.importacion_id == importacion_id,
                            ImportacionDetalle.datos_originales.contains({"curp": curp})
                        ).first()
                        
                        if detalle and detalle.persona_id_resuelto:
                            persona = db.query(User).filter(User.id == detalle.persona_id_resuelto).first()
                            if persona:
                                persona.curp = curp
                                resumen["personas_actualizadas"] += 1
        
        elif imp.tipo == "RUTAS_CAC":
            for fila in filas:
                territorio_nombre = fila.get('territorio', '').strip().upper()
                ruta_nombre = fila.get('ruta', '').strip().upper()
                cac_nombre = fila.get('cac', '').strip().upper()
                
                # Buscar o crear territorio
                territorio = db.query(Territorio).filter(
                    Territorio.nombre == territorio_nombre
                ).first()
                
                if not territorio:
                    territorio = Territorio(nombre=territorio_nombre)
                    db.add(territorio)
                    db.flush()
                    resumen["territorios_nuevos"] += 1
                
                # Buscar o crear ruta
                if ruta_nombre:
                    ruta = db.query(Ruta).filter(
                        Ruta.nombre == ruta_nombre,
                        Ruta.territorio_id == territorio.id
                    ).first()
                    
                    if not ruta:
                        ruta = Ruta(nombre=ruta_nombre, territorio_id=territorio.id)
                        db.add(ruta)
                        db.flush()
                        resumen["rutas_nuevas"] += 1
                    
                    # Buscar o crear CAC
                    if cac_nombre:
                        cac = db.query(CAC).filter(
                            CAC.nombre == cac_nombre,
                            CAC.ruta_id == ruta.id
                        ).first()
                        
                        if not cac:
                            cac = CAC(
                                nombre=cac_nombre,
                                ruta_id=ruta.id,
                                latitud=float(fila.get('latitud', 0)) if fila.get('latitud') else None,
                                longitud=float(fila.get('longitud', 0)) if fila.get('longitud') else None,
                                estatus="VACANTE"
                            )
                            db.add(cac)
                            resumen["cac_nuevas"] += 1
        
        # Marcar como publicado
        imp.estatus = "PUBLICADO"
        imp.publicado_por_id = current_user["user_id"]
        imp.fecha_publicacion = datetime.utcnow()
        
        db.commit()
        
        # Crear notificación
        notif = Notificacion(
            titulo="Importación publicada",
            mensaje=f"Se publicó importación de {imp.tipo}: {resumen}",
            tipo="success",
            rol_destino="admin"
        )
        db.add(notif)
        db.commit()
        
        return {
            "mensaje": "Importación publicada exitosamente",
            "resumen": resumen
        }
        
    except Exception as e:
        db.rollback()
        imp.estatus = "ERROR"
        imp.notas = f"Error en publicación: {str(e)}"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Error al publicar: {str(e)}")


@router.get("/{importacion_id}/reporte-errores")
def descargar_reporte_errores(
    importacion_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Obtener reporte de errores en formato JSON (para descarga como CSV en frontend)"""
    imp = db.query(Importacion).filter(Importacion.id == importacion_id).first()
    if not imp:
        raise HTTPException(status_code=404, detail="Importación no encontrada")
    
    detalles = db.query(ImportacionDetalle).filter(
        ImportacionDetalle.importacion_id == importacion_id
    ).all()
    
    errores = []
    for d in detalles:
        errores.append({
            "fila": d.fila_numero,
            "tipo_problema": d.tipo_problema,
            "datos": d.datos_originales,
            "resuelto": d.resuelto
        })
    
    return {
        "importacion_id": importacion_id,
        "archivo": imp.archivo_nombre,
        "total_errores": len(errores),
        "errores": errores
    }
