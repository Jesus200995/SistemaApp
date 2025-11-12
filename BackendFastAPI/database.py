from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Variables del entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurar el motor de conexión a PostgreSQL
engine = create_engine(DATABASE_URL)

# Crear la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de modelos
Base = declarative_base()

# ✅ Esta es la función que falta
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
