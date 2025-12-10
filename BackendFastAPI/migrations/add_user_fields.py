"""
Migración: Agregar campos curp, territorio y telefono a la tabla users
Fecha: Diciembre 2025
"""

from sqlalchemy import text
from database import engine

def run_migration():
    """
    Agrega las columnas curp, territorio y telefono a la tabla users.
    Esta migración es idempotente (puede ejecutarse múltiples veces sin error).
    """
    
    migrations = [
        {
            "name": "curp",
            "sql": "ALTER TABLE users ADD COLUMN IF NOT EXISTS curp VARCHAR(18)",
            "description": "Agregar columna CURP (18 caracteres)"
        },
        {
            "name": "territorio",
            "sql": "ALTER TABLE users ADD COLUMN IF NOT EXISTS territorio VARCHAR(100)",
            "description": "Agregar columna territorio"
        },
        {
            "name": "telefono",
            "sql": "ALTER TABLE users ADD COLUMN IF NOT EXISTS telefono VARCHAR(20)",
            "description": "Agregar columna teléfono"
        }
    ]
    
    print("🔄 Ejecutando migraciones de usuario...")
    
    with engine.connect() as conn:
        for migration in migrations:
            try:
                conn.execute(text(migration["sql"]))
                conn.commit()
                print(f"  ✅ {migration['description']}")
            except Exception as e:
                if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                    print(f"  ⏭️  {migration['name']} ya existe, saltando...")
                else:
                    print(f"  ❌ Error en {migration['name']}: {str(e)}")
    
    print("✅ Migraciones completadas")

if __name__ == "__main__":
    run_migration()
