"""
Migración: Agregar campos curp, territorio y telefono a la tabla users
          Agregar campos curp y territorio a la tabla sembradores
Fecha: Diciembre 2025
"""

from sqlalchemy import text
from database import engine

def run_migration():
    """
    Agrega las columnas curp, territorio y telefono a la tabla users.
    Agrega las columnas curp y territorio a la tabla sembradores.
    Esta migración es idempotente (puede ejecutarse múltiples veces sin error).
    """
    
    migrations = [
        # Migraciones para tabla users
        {
            "name": "users.curp",
            "sql": "ALTER TABLE users ADD COLUMN IF NOT EXISTS curp VARCHAR(18)",
            "description": "Agregar columna CURP a users (18 caracteres)"
        },
        {
            "name": "users.territorio",
            "sql": "ALTER TABLE users ADD COLUMN IF NOT EXISTS territorio VARCHAR(100)",
            "description": "Agregar columna territorio a users"
        },
        {
            "name": "users.telefono",
            "sql": "ALTER TABLE users ADD COLUMN IF NOT EXISTS telefono VARCHAR(20)",
            "description": "Agregar columna teléfono a users"
        },
        # Migraciones para tabla sembradores
        {
            "name": "sembradores.curp",
            "sql": "ALTER TABLE sembradores ADD COLUMN IF NOT EXISTS curp VARCHAR(18)",
            "description": "Agregar columna CURP a sembradores (18 caracteres)"
        },
        {
            "name": "sembradores.territorio",
            "sql": "ALTER TABLE sembradores ADD COLUMN IF NOT EXISTS territorio VARCHAR(100)",
            "description": "Agregar columna territorio a sembradores"
        }
    ]
    
    print("🔄 Ejecutando migraciones...")
    
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
