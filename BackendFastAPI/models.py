from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, func, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(String, nullable=False)
    activo = Column(Boolean, default=True)
    superior_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 🔑 Jerarquía
    created_at = Column(DateTime(timezone=True), server_default=func.now())


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
    comunidad = Column(String(100))
    cultivo_principal = Column(String(100))
    telefono = Column(String(30))
    lat = Column(Float)
    lng = Column(Float)
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
