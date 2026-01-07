"""
Migración: Agregar columna destino_id a cambios_adscripcion
Fecha: 2026-01-07
"""

from sqlalchemy import text
from database import engine

def run_migration():
    """Agregar columna destino_id para solicitudes dirigidas a un usuario específico"""
    with engine.connect() as conn:
        # Agregar columna destino_id
        try:
            conn.execute(text("""
                ALTER TABLE cambios_adscripcion 
                ADD COLUMN IF NOT EXISTS destino_id INTEGER REFERENCES users(id)
            """))
            conn.commit()
            print("✅ Columna destino_id agregada a cambios_adscripcion")
        except Exception as e:
            print(f"⚠️ Error o columna ya existe: {e}")
        
        print("✅ Migración completada")

if __name__ == "__main__":
    run_migration()
