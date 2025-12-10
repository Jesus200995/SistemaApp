"""
Script para crear TODAS las tablas del modelo en la base de datos.
Ejecutar: python migrations/create_all_tables.py
"""
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, Base
from models import User, Notificacion, Sembrador, Seguimiento, Solicitud

def create_all_tables():
    """Crear todas las tablas si no existen"""
    try:
        # Importar todos los modelos para que se registren
        print("📊 Creando tablas en la base de datos...")
        
        # Crear todas las tablas que no existan
        Base.metadata.create_all(bind=engine)
        
        print("✅ Todas las tablas creadas exitosamente")
        print("   - users")
        print("   - notificaciones")
        print("   - sembradores")
        print("   - seguimientos")
        print("   - solicitudes")
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_all_tables()
