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
    tipo = Column(String(50), nullable=False)  # info, warning, error, success
    rol_destino = Column(String(50))  # admin, usuario, all
    leido = Column(Boolean, default=False)
    usuario_id = Column(Integer)  # Opcional: para notificaciones personales
    created_at = Column(DateTime(timezone=True), server_default=func.now())


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
