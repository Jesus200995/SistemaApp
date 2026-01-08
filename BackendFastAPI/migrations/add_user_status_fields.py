"""
Migración: Agregar campos de estatus laboral y seguimiento a usuarios
Fecha: 2026-01-08
Descripción: Agrega campos para trackear el estatus laboral, fechas de alta/baja,
             y la última acción realizada sobre el usuario.
"""

from sqlalchemy import text
from database import engine


def migrate():
    """
    Agrega los campos de estatus laboral a la tabla users:
    - estatus_laboral: ACTIVO, BAJA, SUSPENDIDO, PENDIENTE_ALTA
    - fecha_alta: Fecha cuando fue dado de alta
    - fecha_baja: Fecha cuando fue dado de baja
    - fecha_ultima_accion: Última acción (alta/baja/reasignación)
    - motivo_ultima_accion: Justificación de la última acción
    - tipo_ultima_accion: ALTA, BAJA, REASIGNACION
    """
    
    with engine.connect() as conn:
        # Verificar y agregar columna estatus_laboral
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS estatus_laboral VARCHAR(30) DEFAULT 'ACTIVO'
            """))
            print("✅ Columna 'estatus_laboral' agregada/verificada")
        except Exception as e:
            print(f"⚠️ Error con estatus_laboral: {e}")
        
        # Verificar y agregar columna fecha_alta
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS fecha_alta TIMESTAMP WITH TIME ZONE
            """))
            print("✅ Columna 'fecha_alta' agregada/verificada")
        except Exception as e:
            print(f"⚠️ Error con fecha_alta: {e}")
        
        # Verificar y agregar columna fecha_baja
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS fecha_baja TIMESTAMP WITH TIME ZONE
            """))
            print("✅ Columna 'fecha_baja' agregada/verificada")
        except Exception as e:
            print(f"⚠️ Error con fecha_baja: {e}")
        
        # Verificar y agregar columna fecha_ultima_accion
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS fecha_ultima_accion TIMESTAMP WITH TIME ZONE
            """))
            print("✅ Columna 'fecha_ultima_accion' agregada/verificada")
        except Exception as e:
            print(f"⚠️ Error con fecha_ultima_accion: {e}")
        
        # Verificar y agregar columna motivo_ultima_accion
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS motivo_ultima_accion TEXT
            """))
            print("✅ Columna 'motivo_ultima_accion' agregada/verificada")
        except Exception as e:
            print(f"⚠️ Error con motivo_ultima_accion: {e}")
        
        # Verificar y agregar columna tipo_ultima_accion
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS tipo_ultima_accion VARCHAR(30)
            """))
            print("✅ Columna 'tipo_ultima_accion' agregada/verificada")
        except Exception as e:
            print(f"⚠️ Error con tipo_ultima_accion: {e}")
        
        # Actualizar usuarios activos existentes con estatus_laboral = 'ACTIVO'
        try:
            conn.execute(text("""
                UPDATE users 
                SET estatus_laboral = 'ACTIVO' 
                WHERE activo = true AND (estatus_laboral IS NULL OR estatus_laboral = '')
            """))
            print("✅ Usuarios activos actualizados con estatus_laboral = 'ACTIVO'")
        except Exception as e:
            print(f"⚠️ Error actualizando usuarios activos: {e}")
        
        # Actualizar usuarios inactivos existentes con estatus_laboral = 'BAJA'
        try:
            conn.execute(text("""
                UPDATE users 
                SET estatus_laboral = 'BAJA' 
                WHERE activo = false AND (estatus_laboral IS NULL OR estatus_laboral = '')
            """))
            print("✅ Usuarios inactivos actualizados con estatus_laboral = 'BAJA'")
        except Exception as e:
            print(f"⚠️ Error actualizando usuarios inactivos: {e}")
        
        conn.commit()
        print("\n✅ Migración de campos de estatus completada exitosamente")


if __name__ == "__main__":
    print("🚀 Iniciando migración de campos de estatus laboral...")
    migrate()
    print("✅ Migración completada")
