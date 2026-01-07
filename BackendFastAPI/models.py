from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, func, ForeignKey, Enum, JSON
from database import Base
import enum

# ========== ENUMS PARA WORKFLOWS ==========

class RolSistema(enum.Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    TERRITORIAL = "TERRITORIAL"
    FACILITADOR = "FACILITADOR"
    TECNICO = "TECNICO"

class PerfilOperativo(enum.Enum):
    TERRITORIAL = "TERRITORIAL"
    FACILITADOR = "FACILITADOR"
    TECNICO_SOCIAL = "TECNICO_SOCIAL"
    TECNICO_PRODUCTIVO = "TECNICO_PRODUCTIVO"

class TipoParticipacion(enum.Enum):
    PRINCIPAL = "PRINCIPAL"
    APOYO = "APOYO"

class TipoCambioAdscripcion(enum.Enum):
    ALTA = "ALTA"
    BAJA = "BAJA"
    REASIGNACION = "REASIGNACION"

class ObjetoCambio(enum.Enum):
    PERSONA_CAC = "PERSONA_CAC"
    PERSONA_RUTA = "PERSONA_RUTA"
    PERSONA_TERRITORIO = "PERSONA_TERRITORIO"
    CAC_RUTA = "CAC_RUTA"

class EstatusWorkflow(enum.Enum):
    BORRADOR = "BORRADOR"
    EN_REVISION = "EN_REVISION"
    AUTORIZADO = "AUTORIZADO"
    RECHAZADO = "RECHAZADO"
    APLICADO = "APLICADO"
    CANCELADO = "CANCELADO"

class TipoObjetoEstructura(enum.Enum):
    PERSONA = "PERSONA"
    CAC = "CAC"
    RUTA = "RUTA"
    TERRITORIO = "TERRITORIO"

class AccionEstructura(enum.Enum):
    CREAR = "CREAR"
    EDITAR = "EDITAR"
    INACTIVAR = "INACTIVAR"

class EstatusCAC(enum.Enum):
    OK = "OK"
    VACANTE = "VACANTE"
    PENDIENTE = "PENDIENTE"

# ========== MODELOS PRINCIPALES ==========

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # ADMINISTRADOR, TERRITORIAL, FACILITADOR, TECNICO
    perfil_operativo = Column(String(50), nullable=True)  # TERRITORIAL, FACILITADOR, TECNICO_SOCIAL, TECNICO_PRODUCTIVO
    curp = Column(String(18), nullable=True, unique=True)  # CURP del usuario (18 caracteres)
    territorio_id = Column(Integer, ForeignKey("territorios.id"), nullable=True)  # FK a territorio
    territorio = Column(String(100), nullable=True)  # Territorio nombre (legacy)
    telefono = Column(String(20), nullable=True)  # Número de teléfono
    correo_contacto = Column(String(100), nullable=True)  # Correo de contacto adicional
    activo = Column(Boolean, default=True)
    superior_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 🔑 Jerarquía
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Ambiental(Base):
    __tablename__ = "ambiental"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Productiva(Base):
    __tablename__ = "productiva"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Social(Base):
    __tablename__ = "social"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Infraestructura(Base):
    __tablename__ = "infraestructura"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # solicitud, respuesta, info, warning, error, success
    rol_destino = Column(String(50), nullable=True)  # admin, usuario, all (para notificaciones por rol)
    user_destino = Column(Integer, ForeignKey("users.id"), nullable=True)  # Usuario específico
    leido = Column(Boolean, default=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Usuario que generó la notificación
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id"), nullable=True)  # Vinculación a solicitud
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())


class Sembrador(Base):
    __tablename__ = "sembradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    curp = Column(String(18), nullable=True)  # CURP del sembrador
    comunidad = Column(String(100))
    territorio = Column(String(100), nullable=True)  # Territorio asignado
    cultivo_principal = Column(String(100))
    telefono = Column(String(30))
    user_id = Column(Integer, ForeignKey("users.id"))
    creado_en = Column(DateTime(timezone=True), server_default=func.now())


class Seguimiento(Base):
    __tablename__ = "seguimientos"

    id = Column(Integer, primary_key=True, index=True)
    sembrador_id = Column(Integer, ForeignKey("sembradores.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha_visita = Column(DateTime, nullable=False)
    estado_cultivo = Column(String(100))
    observaciones = Column(Text)
    avance_porcentaje = Column(Float, default=0.0)
    foto_url = Column(String(255), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50))
    descripcion = Column(Text)
    usuario_id = Column(Integer, ForeignKey("users.id"))
    destino_id = Column(Integer, ForeignKey("users.id"))
    estado = Column(String(20), default="pendiente")
    fecha = Column(DateTime(timezone=True), server_default=func.now())


# ========== MODELOS ESTRUCTURA TERRITORIAL (SEMBRANDO VIDA) ==========

class Territorio(Base):
    """
    Representa un territorio geográfico (máximo nivel de estructura).
    Un territorio puede tener múltiples rutas.
    """
    __tablename__ = "territorios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    estado_region = Column(String(100), nullable=True)  # Estado/Región geográfica
    responsable_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Usuario territorial responsable
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Ruta(Base):
    """
    Representa una ruta dentro de un territorio.
    Puede tener un facilitador principal y opcionalmente uno de apoyo.
    Contiene múltiples CAC.
    """
    __tablename__ = "rutas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    territorio_id = Column(Integer, ForeignKey("territorios.id"), nullable=False)
    facilitador_principal_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Facilitador principal
    facilitador_apoyo_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Facilitador de apoyo (opcional)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CAC(Base):
    """
    Comunidad de Aprendizaje Campesino.
    Cada CAC puede tener un Técnico Social y un Técnico Productivo.
    """
    __tablename__ = "cac"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    ruta_id = Column(Integer, ForeignKey("rutas.id"), nullable=False)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    tecnico_social_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # TS asignado
    tecnico_productivo_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # TP asignado
    estatus = Column(String(20), default="OK")  # OK, VACANTE, PENDIENTE
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AsignacionPersonaCAC(Base):
    """
    Tabla de asignaciones históricas persona <-> CAC.
    Permite mantener historial de quién estuvo en qué CAC.
    """
    __tablename__ = "asignaciones_persona_cac"

    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cac_id = Column(Integer, ForeignKey("cac.id"), nullable=False)
    tipo_asignacion = Column(String(30), nullable=False)  # TECNICO_SOCIAL, TECNICO_PRODUCTIVO
    fecha_inicio = Column(DateTime(timezone=True), server_default=func.now())
    fecha_fin = Column(DateTime(timezone=True), nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ========== WORKFLOWS: CAMBIOS DE ADSCRIPCIÓN ==========

class CambioAdscripcion(Base):
    """
    Workflow para gestionar movimientos operativos:
    - Alta/Baja/Reasignación de personas a CAC, rutas o territorios
    - Control de estados: borrador -> en revisión -> autorizado -> aplicado
    """
    __tablename__ = "cambios_adscripcion"

    id = Column(Integer, primary_key=True, index=True)
    folio = Column(String(50), unique=True, nullable=False)  # Folio único
    tipo_cambio = Column(String(20), nullable=False)  # ALTA, BAJA, REASIGNACION
    objeto = Column(String(30), nullable=False)  # PERSONA_CAC, PERSONA_RUTA, PERSONA_TERRITORIO, CAC_RUTA
    
    # Entidades afectadas
    persona_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    cac_origen_id = Column(Integer, ForeignKey("cac.id"), nullable=True)
    cac_destino_id = Column(Integer, ForeignKey("cac.id"), nullable=True)
    ruta_origen_id = Column(Integer, ForeignKey("rutas.id"), nullable=True)
    ruta_destino_id = Column(Integer, ForeignKey("rutas.id"), nullable=True)
    territorio_origen_id = Column(Integer, ForeignKey("territorios.id"), nullable=True)
    territorio_destino_id = Column(Integer, ForeignKey("territorios.id"), nullable=True)
    
    # Control de workflow
    estatus = Column(String(20), default="BORRADOR")  # BORRADOR, EN_REVISION, AUTORIZADO, RECHAZADO, APLICADO, CANCELADO
    resumen = Column(Text, nullable=True)  # Descripción del cambio
    fecha_efecto = Column(DateTime, nullable=True)  # Fecha en que debe aplicarse
    fecha_limite = Column(DateTime, nullable=True)  # SLA - fecha límite
    
    # Auditoría
    propuesto_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    autorizado_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    aplicado_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    observaciones = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ========== WORKFLOWS: ACTUALIZACIONES DE ESTRUCTURA ==========

class ActualizacionEstructura(Base):
    """
    Workflow para gestionar correcciones de maestros:
    - Crear/Editar/Inactivar personas, CAC, rutas o territorios
    """
    __tablename__ = "actualizaciones_estructura"

    id = Column(Integer, primary_key=True, index=True)
    folio = Column(String(50), unique=True, nullable=False)
    tipo_objeto = Column(String(20), nullable=False)  # PERSONA, CAC, RUTA, TERRITORIO
    accion = Column(String(20), nullable=False)  # CREAR, EDITAR, INACTIVAR
    
    # Referencia al objeto afectado
    objeto_id = Column(Integer, nullable=True)  # ID del objeto (persona/CAC/ruta/territorio)
    
    # Payload con valores propuestos (JSON)
    payload_propuesto = Column(JSON, nullable=True)  # {"campo": "valor_nuevo"}
    payload_anterior = Column(JSON, nullable=True)  # {"campo": "valor_anterior"}
    
    # Control de workflow
    estatus = Column(String(20), default="EN_REVISION")  # EN_REVISION, AUTORIZADO, RECHAZADO, APLICADO, CANCELADO
    resumen = Column(Text, nullable=True)
    
    # Auditoría
    propuesto_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    autorizado_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    aplicado_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    observaciones = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ========== IMPORTACIONES (SOLO ADMIN) ==========

class Importacion(Base):
    """
    Gestión de carga de bases iniciales y republicaciones.
    Solo el rol Administrador puede subir y publicar bases.
    """
    __tablename__ = "importaciones"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(30), nullable=False)  # PERSONAL, RUTAS_CAC
    archivo_nombre = Column(String(255), nullable=False)
    archivo_path = Column(String(500), nullable=True)
    
    # Estadísticas de validación
    filas_totales = Column(Integer, default=0)
    filas_validas = Column(Integer, default=0)
    errores_criticos = Column(Integer, default=0)
    warnings = Column(Integer, default=0)
    reporte_errores_path = Column(String(500), nullable=True)  # Path al CSV de errores
    
    # Control
    estatus = Column(String(30), default="PENDIENTE")  # PENDIENTE, VALIDANDO, LISTO_PUBLICAR, PUBLICADO, ERROR
    notas = Column(Text, nullable=True)
    
    # Auditoría
    subido_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    publicado_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    fecha_publicacion = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ImportacionDetalle(Base):
    """
    Detalle de registros pendientes de resolución manual (match).
    Para personas no encontradas o ambiguas.
    """
    __tablename__ = "importacion_detalles"

    id = Column(Integer, primary_key=True, index=True)
    importacion_id = Column(Integer, ForeignKey("importaciones.id"), nullable=False)
    fila_numero = Column(Integer)
    datos_originales = Column(JSON)  # Datos del archivo
    tipo_problema = Column(String(50))  # NO_ENCONTRADO, AMBIGUO, VACANTE
    persona_id_resuelto = Column(Integer, ForeignKey("users.id"), nullable=True)  # Si se resolvió manualmente
    resuelto = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

