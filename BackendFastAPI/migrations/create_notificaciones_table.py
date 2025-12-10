"""
Script para crear la tabla notificaciones en la base de datos.
Ejecutar: python migrations/create_notificaciones_table.py
"""
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine
from models import Base, Notificacion

def create_table():
    """Crear la tabla notificaciones si no existe"""
    try:
        # Crear solo la tabla notificaciones
        Notificacion.__table__.create(engine, checkfirst=True)
        print("✅ Tabla 'notificaciones' creada exitosamente")
    except Exception as e:
        print(f"❌ Error creando tabla: {e}")

if __name__ == "__main__":
    create_table()
