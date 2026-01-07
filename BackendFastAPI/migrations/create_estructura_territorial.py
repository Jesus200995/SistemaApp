"""
Migración: Crear tablas para Estructura Territorial - Sembrando Vida
Módulo 1: Personal Operativo y Estructura Territorial

Tablas nuevas:
- territorios
- rutas  
- cac
- asignaciones_persona_cac
- cambios_adscripcion
- actualizaciones_estructura
- importaciones
- importacion_detalles

Columnas nuevas en users:
- perfil_operativo
- territorio_id
- correo_contacto
- updated_at
"""

from sqlalchemy import text
from database import engine, SessionLocal

def run_migration():
    """Ejecuta la migración para crear tablas de estructura territorial"""
    
    with engine.connect() as conn:
        # ========== TERRITORIOS ==========
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS territorios (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                estado_region VARCHAR(100),
                responsable_id INTEGER REFERENCES users(id),
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE
            );
        """))
        
        # ========== RUTAS ==========
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS rutas (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                territorio_id INTEGER NOT NULL REFERENCES territorios(id),
                facilitador_principal_id INTEGER REFERENCES users(id),
                facilitador_apoyo_id INTEGER REFERENCES users(id),
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE
            );
        """))
        
        # ========== CAC ==========
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS cac (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(150) NOT NULL,
                ruta_id INTEGER NOT NULL REFERENCES rutas(id),
                latitud DOUBLE PRECISION,
                longitud DOUBLE PRECISION,
                tecnico_social_id INTEGER REFERENCES users(id),
                tecnico_productivo_id INTEGER REFERENCES users(id),
                estatus VARCHAR(20) DEFAULT 'OK',
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE
            );
        """))
        
        # ========== ASIGNACIONES PERSONA-CAC ==========
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS asignaciones_persona_cac (
                id SERIAL PRIMARY KEY,
                persona_id INTEGER NOT NULL REFERENCES users(id),
                cac_id INTEGER NOT NULL REFERENCES cac(id),
                tipo_asignacion VARCHAR(30) NOT NULL,
                fecha_inicio TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                fecha_fin TIMESTAMP WITH TIME ZONE,
                activo BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """))
        
        # ========== CAMBIOS DE ADSCRIPCIÓN ==========
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS cambios_adscripcion (
                id SERIAL PRIMARY KEY,
                folio VARCHAR(50) UNIQUE NOT NULL,
                tipo_cambio VARCHAR(20) NOT NULL,
                objeto VARCHAR(30) NOT NULL,
                persona_id INTEGER REFERENCES users(id),
                cac_origen_id INTEGER REFERENCES cac(id),
                cac_destino_id INTEGER REFERENCES cac(id),
                ruta_origen_id INTEGER REFERENCES rutas(id),
                ruta_destino_id INTEGER REFERENCES rutas(id),
                territorio_origen_id INTEGER REFERENCES territorios(id),
                territorio_destino_id INTEGER REFERENCES territorios(id),
                estatus VARCHAR(20) DEFAULT 'BORRADOR',
                resumen TEXT,
                fecha_efecto TIMESTAMP,
                fecha_limite TIMESTAMP,
                propuesto_por_id INTEGER NOT NULL REFERENCES users(id),
                autorizado_por_id INTEGER REFERENCES users(id),
                aplicado_por_id INTEGER REFERENCES users(id),
                observaciones TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE
            );
        """))
        
        # ========== ACTUALIZACIONES DE ESTRUCTURA ==========
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS actualizaciones_estructura (
                id SERIAL PRIMARY KEY,
                folio VARCHAR(50) UNIQUE NOT NULL,
                tipo_objeto VARCHAR(20) NOT NULL,
                accion VARCHAR(20) NOT NULL,
                objeto_id INTEGER,
                payload_propuesto JSONB,
                payload_anterior JSONB,
                estatus VARCHAR(20) DEFAULT 'EN_REVISION',
                resumen TEXT,
                propuesto_por_id INTEGER NOT NULL REFERENCES users(id),
                autorizado_por_id INTEGER REFERENCES users(id),
                aplicado_por_id INTEGER REFERENCES users(id),
                observaciones TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE
            );
        """))
        
        # ========== IMPORTACIONES ==========
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS importaciones (
                id SERIAL PRIMARY KEY,
                tipo VARCHAR(30) NOT NULL,
                archivo_nombre VARCHAR(255) NOT NULL,
                archivo_path VARCHAR(500),
                filas_totales INTEGER DEFAULT 0,
                filas_validas INTEGER DEFAULT 0,
                errores_criticos INTEGER DEFAULT 0,
                warnings INTEGER DEFAULT 0,
                reporte_errores_path VARCHAR(500),
                estatus VARCHAR(30) DEFAULT 'PENDIENTE',
                notas TEXT,
                subido_por_id INTEGER NOT NULL REFERENCES users(id),
                publicado_por_id INTEGER REFERENCES users(id),
                fecha_publicacion TIMESTAMP,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE
            );
        """))
        
        # ========== IMPORTACION DETALLES ==========
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS importacion_detalles (
                id SERIAL PRIMARY KEY,
                importacion_id INTEGER NOT NULL REFERENCES importaciones(id),
                fila_numero INTEGER,
                datos_originales JSONB,
                tipo_problema VARCHAR(50),
                persona_id_resuelto INTEGER REFERENCES users(id),
                resuelto BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """))
        
        # ========== COLUMNAS NUEVAS EN USERS ==========
        # Verificar y agregar columnas si no existen
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS perfil_operativo VARCHAR(50);
            """))
        except:
            pass
        
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS territorio_id INTEGER REFERENCES territorios(id);
            """))
        except:
            pass
        
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS correo_contacto VARCHAR(100);
            """))
        except:
            pass
        
        try:
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE;
            """))
        except:
            pass
        
        # ========== ÍNDICES ==========
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_rutas_territorio ON rutas(territorio_id);
            CREATE INDEX IF NOT EXISTS idx_cac_ruta ON cac(ruta_id);
            CREATE INDEX IF NOT EXISTS idx_cac_ts ON cac(tecnico_social_id);
            CREATE INDEX IF NOT EXISTS idx_cac_tp ON cac(tecnico_productivo_id);
            CREATE INDEX IF NOT EXISTS idx_cambios_estatus ON cambios_adscripcion(estatus);
            CREATE INDEX IF NOT EXISTS idx_actualizaciones_estatus ON actualizaciones_estructura(estatus);
            CREATE INDEX IF NOT EXISTS idx_users_territorio ON users(territorio_id);
            CREATE INDEX IF NOT EXISTS idx_users_curp ON users(curp);
        """))
        
        conn.commit()
        
        print("✅ Migración de estructura territorial completada exitosamente")


if __name__ == "__main__":
    run_migration()
