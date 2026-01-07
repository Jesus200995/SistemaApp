# 📋 MÓDULO 1: Personal Operativo y Estructura Territorial

## Descripción General

Este módulo implementa la gestión de la estructura territorial y el personal operativo según la especificación "Sembrando Vida - Módulo 1". Incluye la jerarquía completa de Territorio → Ruta → CAC, los flujos de trabajo para cambios de adscripción y actualizaciones de estructura, así como el sistema de importaciones de bases.

---

## 🏗️ Arquitectura

### Jerarquía de Roles

```
ADMINISTRADOR
    ↓
TERRITORIAL (Responsable de Territorio)
    ↓
FACILITADOR (Principal/Apoyo de Ruta)
    ↓
TÉCNICO (Social/Productivo asignado a CAC)
```

### Estructura Territorial

```
Territorio (Responsable: Territorial)
    └── Rutas (Facilitador Principal + Apoyo)
            └── CAC (Técnico Social + Técnico Productivo)
```

---

## 📁 Archivos Creados/Modificados

### Backend (FastAPI)

| Archivo | Descripción |
|---------|-------------|
| `BackendFastAPI/models.py` | Modelos SQLAlchemy actualizados con Territorio, Ruta, CAC, CambioAdscripcion, ActualizacionEstructura, Importacion |
| `BackendFastAPI/routes/estructura.py` | Endpoints para gestión de estructura territorial y directorio |
| `BackendFastAPI/routes/workflows.py` | Endpoints para flujos de cambios de adscripción y actualizaciones |
| `BackendFastAPI/routes/importaciones.py` | Endpoints para importación de bases (solo Admin) |
| `BackendFastAPI/migrations/create_estructura_territorial.py` | Script de migración para nuevas tablas |
| `BackendFastAPI/main.py` | Actualizado con nuevos routers |

### Frontend (Vue 3)

| Archivo | Descripción |
|---------|-------------|
| `src/views/EstructuraTerritorialView.vue` | Vista de 3 columnas para Territorio → Ruta → CAC |
| `src/views/CambiosAdscripcionView.vue` | Bandeja de workflows para cambios de personal |
| `src/views/ImportacionesView.vue` | Gestión de importaciones (solo Admin) |
| `src/views/DirectorioView.vue` | Directorio de personal con filtros y búsqueda |
| `src/router/index.ts` | Rutas actualizadas con nuevas vistas |
| `src/components/DesktopSidebar.vue` | Navegación lateral actualizada |

---

## 🔌 Endpoints API

### Estructura Territorial (`/estructura`)

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/territorios` | Lista territorios | Admin, Territorial |
| POST | `/territorios` | Crear territorio | Admin |
| PUT | `/territorios/{id}` | Actualizar territorio | Admin |
| GET | `/rutas` | Lista rutas | Admin, Territorial, Facilitador |
| POST | `/rutas` | Crear ruta | Admin, Territorial |
| PUT | `/rutas/{id}` | Actualizar ruta | Admin, Territorial |
| GET | `/cac` | Lista CAC | Todos |
| POST | `/cac` | Crear CAC | Admin, Territorial |
| PUT | `/cac/{id}` | Actualizar CAC | Admin, Territorial |
| GET | `/directorio` | Directorio de personal | Todos |
| GET | `/buscar-curp` | Búsqueda global por CURP | Admin, Territorial |

### Workflows (`/workflows`)

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/cambios-adscripcion` | Lista cambios pendientes | Admin, Territorial |
| POST | `/cambios-adscripcion` | Crear propuesta de cambio | Admin, Territorial |
| POST | `/cambios-adscripcion/{id}/enviar-revision` | Enviar a revisión | Territorial |
| POST | `/cambios-adscripcion/{id}/accion` | Autorizar/Rechazar/Aplicar | Admin |
| GET | `/actualizaciones-estructura` | Lista actualizaciones | Admin |
| POST | `/actualizaciones-estructura` | Crear actualización | Territorial |
| GET | `/dashboard-operativo` | Dashboard con KPIs | Admin |

### Importaciones (`/importaciones`)

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| GET | `/` | Lista importaciones | Admin |
| POST | `/subir` | Subir archivo CSV/Excel | Admin |
| POST | `/{id}/validar` | Validar importación | Admin |
| GET | `/{id}/detalles-pendientes` | Registros pendientes de resolución | Admin |
| POST | `/{id}/resolver-match` | Resolver coincidencia manual | Admin |
| POST | `/{id}/publicar` | Publicar importación | Admin |

---

## 🗄️ Modelos de Base de Datos

### Nuevas Tablas

```sql
-- Territorios
CREATE TABLE territorios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    clave VARCHAR(20) UNIQUE NOT NULL,
    responsable_id INTEGER REFERENCES users(id),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);

-- Rutas
CREATE TABLE rutas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    clave VARCHAR(20) UNIQUE NOT NULL,
    territorio_id INTEGER REFERENCES territorios(id) NOT NULL,
    facilitador_principal_id INTEGER REFERENCES users(id),
    facilitador_apoyo_id INTEGER REFERENCES users(id),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- CAC (Comunidades de Aprendizaje Campesino)
CREATE TABLE cac (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    clave VARCHAR(20) UNIQUE NOT NULL,
    ruta_id INTEGER REFERENCES rutas(id) NOT NULL,
    tecnico_social_id INTEGER REFERENCES users(id),
    tecnico_productivo_id INTEGER REFERENCES users(id),
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Cambios de Adscripción
CREATE TABLE cambios_adscripcion (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    persona_id INTEGER REFERENCES users(id) NOT NULL,
    datos_antes JSONB,
    datos_despues JSONB,
    motivo TEXT,
    estatus VARCHAR(20) DEFAULT 'BORRADOR',
    solicitante_id INTEGER REFERENCES users(id) NOT NULL,
    autorizador_id INTEGER REFERENCES users(id),
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_autorizacion TIMESTAMP,
    fecha_aplicacion TIMESTAMP
);

-- Actualizaciones de Estructura
CREATE TABLE actualizaciones_estructura (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    entidad_tipo VARCHAR(20) NOT NULL,
    entidad_id INTEGER NOT NULL,
    datos_antes JSONB,
    datos_despues JSONB,
    motivo TEXT,
    estatus VARCHAR(20) DEFAULT 'BORRADOR',
    solicitante_id INTEGER REFERENCES users(id) NOT NULL,
    autorizador_id INTEGER REFERENCES users(id),
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Importaciones
CREATE TABLE importaciones (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL,
    archivo_nombre VARCHAR(255) NOT NULL,
    archivo_path VARCHAR(500),
    filas_totales INTEGER DEFAULT 0,
    filas_validas INTEGER DEFAULT 0,
    errores_criticos INTEGER DEFAULT 0,
    warnings INTEGER DEFAULT 0,
    estatus VARCHAR(20) DEFAULT 'PENDIENTE',
    usuario_id INTEGER REFERENCES users(id) NOT NULL,
    notas TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    publicado_at TIMESTAMP
);
```

### Columnas Añadidas a users

```sql
ALTER TABLE users ADD COLUMN perfil_operativo VARCHAR(30);
ALTER TABLE users ADD COLUMN territorio_id INTEGER REFERENCES territorios(id);
ALTER TABLE users ADD COLUMN correo_contacto VARCHAR(100);
ALTER TABLE users ADD COLUMN updated_at TIMESTAMP;
```

---

## 🎨 Vistas Frontend

### EstructuraTerritorialView

- **Layout:** 3 columnas (Territorios | Rutas | CAC)
- **Funcionalidades:**
  - Navegación jerárquica con drill-down
  - KPIs por cada nivel
  - Filtros de vacantes y sin coordenadas
  - CRUD modals para cada entidad
  - Indicadores visuales de completitud

### DirectorioView

- **Layout:** Tabla/Cards con filtros
- **Funcionalidades:**
  - Búsqueda por nombre, CURP, correo
  - Filtros por rol, perfil, territorio, ruta
  - Vista de tabla y tarjetas
  - Exportación a CSV
  - Modal de detalle con historial

### CambiosAdscripcionView

- **Layout:** Tabla de workflows con acciones
- **Funcionalidades:**
  - Filtros por estatus
  - Badges de estado coloridos
  - Acciones contextuales (enviar, autorizar, rechazar, aplicar)
  - Modal de detalle con comparador antes/después

### ImportacionesView

- **Layout:** Formulario de upload + historial
- **Funcionalidades:**
  - Drag & drop de archivos CSV/Excel
  - Validación asíncrona
  - Resolución manual de matches ambiguos
  - Publicación con resumen

---

## 🔐 Permisos por Rol

| Funcionalidad | Admin | Territorial | Facilitador | Técnico |
|---------------|-------|-------------|-------------|---------|
| Ver estructura | ✅ | ✅ (su territorio) | ❌ | ❌ |
| Editar estructura | ✅ | ❌ | ❌ | ❌ |
| Ver directorio | ✅ | ✅ (su territorio) | ✅ (su ruta) | ✅ (su CAC) |
| Crear cambios | ✅ | ✅ | ❌ | ❌ |
| Autorizar cambios | ✅ | ❌ | ❌ | ❌ |
| Importaciones | ✅ | ❌ | ❌ | ❌ |

---

## 🚀 Despliegue

### 1. Ejecutar migración

```bash
cd BackendFastAPI
python migrations/create_estructura_territorial.py
```

### 2. Reiniciar backend

```bash
uvicorn main:app --reload
```

### 3. Compilar frontend

```bash
cd Frontend/sistemaapp-frontend
npm run build
```

---

## 📊 Flujos de Trabajo

### Cambio de Adscripción

```
[BORRADOR] → Enviar a Revisión → [EN_REVISION] → Autorizar → [AUTORIZADO] → Aplicar → [APLICADO]
                                              → Rechazar → [RECHAZADO]
```

### Importación de Base

```
[PENDIENTE] → Validar → [LISTO_PUBLICAR] → Publicar → [PUBLICADO]
                      → Resolver matches manuales → Publicar
```

---

## 📝 Notas de Implementación

1. **Scope automático:** Los endpoints filtran automáticamente según el rol del usuario
2. **Historial:** Todas las asignaciones de técnicos a CAC se registran en `asignaciones_persona_cac`
3. **CURP único:** La búsqueda por CURP permite encontrar personal entre territorios (solo Admin/Territorial)
4. **Validación CSV:** Los archivos importados validan estructura, CURPs duplicados y coincidencias ambiguas
5. **Coordenadas opcionales:** Los CAC pueden no tener coordenadas, se marcan con indicador visual

---

## 🔗 Referencias

- Documento de especificación: `Frontend/sistemaapp-frontend/logo/Especificacion_Maquetacion_Front_Modulo1_v2.pdf`
- Modelos base: `BackendFastAPI/models.py`
- Configuración API: `BackendFastAPI/main.py`
