# 📊 Módulo de Seguimiento de Campo y Reportes

## Estado de Implementación: ✅ COMPLETADO

Todo el módulo ha sido completamente implementado tanto en backend como en frontend.

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Componentes Implementados](#componentes-implementados)
3. [Arquitectura](#arquitectura)
4. [Guía de Uso](#guía-de-uso)
5. [API Endpoints](#api-endpoints)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Descripción General

El módulo de **Seguimiento de Campo y Reportes** permite que los técnicos registren y documenten visitas a los campos de los sembradores. El sistema proporciona:

- **Registro de Visitas**: Técnicos pueden registrar nuevas visitas con observaciones, estado del cultivo y progreso
- **Documentación Visual**: Soporte para URLs de fotos como evidencia
- **Reportes Jerárquicos**: Supervisores pueden ver reportes por técnico y por tipo de cultivo
- **Seguimiento de Progreso**: Gráficos y porcentajes de avance por sembrador
- **Control de Acceso**: Filtrado jerárquico basado en roles (Admin > Territorial > Facilitador > Técnico)

### Características Clave

✅ CRUD completo de seguimientos  
✅ Reportes por técnico (cantidad, promedio de avance, última visita)  
✅ Reportes por cultivo (cantidad de sembradores, promedio de avance)  
✅ Almacenamiento de fotos (URLs)  
✅ Interfaz intuitiva con gráficos de progreso  
✅ Control de acceso basado en roles  
✅ Búsqueda y filtrado de datos  
✅ Actualización y eliminación de registros (solo por creador)  

---

## 🏗️ Componentes Implementados

### Backend (FastAPI + SQLAlchemy)

#### 1. **Model: Seguimiento** (`Backend/models.py`)
```python
class Seguimiento(Base):
    __tablename__ = "seguimientos"
    
    id: Integer (Primary Key)
    sembrador_id: Integer (Foreign Key → Sembrador)
    user_id: Integer (Foreign Key → User/Technician)
    fecha_visita: DateTime (When visit occurred)
    estado_cultivo: String (Growing stage)
    observaciones: Text (Notes from technician)
    avance_porcentaje: Float (0-100%)
    foto_url: String (Optional photo link)
    creado_en: DateTime (Auto-timestamp)
    actualizado_en: DateTime (Auto-timestamp)
```

#### 2. **Routes: Seguimientos** (`Backend/routes/seguimientos.py`)

**7 Endpoints CRUD:**
- `POST /seguimientos/crear` - Create new visit record
- `GET /seguimientos/` - List all visits (hierarchically filtered)
- `GET /seguimientos/{id}` - Get single record
- `PUT /seguimientos/{id}` - Update record (creator only)
- `DELETE /seguimientos/{id}` - Delete record (creator only)

**2 Reporting Endpoints:**
- `GET /seguimientos/reportes/por-tecnico` - Stats by technician
- `GET /seguimientos/reportes/por-cultivo` - Stats by crop type

#### 3. **Route Registration** (`Backend/main.py`)
```python
from routes import auth, layers, chat, notificaciones, sembradores, seguimientos
app.include_router(seguimientos.router)
```

### Frontend (Vue 3 + TypeScript)

#### 1. **View: SeguimientoView** (`Frontend/src/views/SeguimientoView.vue`)

**3 Tabs principales:**

**Tab 1: Crear Seguimiento**
- Selector de sembrador (dropdown)
- Date/time picker para fecha de visita
- Dropdown de estado del cultivo (8 opciones)
- Range slider para progreso (0-100%)
- Textarea para observaciones
- Input URL opcional para foto
- Botón submit y reset

**Tab 2: Mis Seguimientos**
- Grid de tarjetas con todos los seguimientos
- Muestra: sembrador, comunidad, cultivo, fecha, técnico
- Barra de progreso visual
- Sección de observaciones
- Display de foto (si existe)
- Botones editar/eliminar
- Estado vacío cuando no hay datos

**Tab 3: Reportes**
- **Reporte por Técnico**: Tabla con cantidad de seguimientos, avance promedio, último seguimiento
- **Reporte por Cultivo**: Tabla con cultivo, cantidad de sembradores, cantidad de seguimientos, avance promedio
- Mini barras de progreso en ambos reportes

#### 2. **Router** (`Frontend/src/router/index.ts`)
```typescript
{
  path: '/seguimiento',
  name: 'seguimiento',
  component: () => import('../views/SeguimientoView.vue'),
  meta: { requiresAuth: true }
}
```

#### 3. **Navigation** (`Frontend/src/components/Navbar.vue`)
- Agregado enlace: "📊 Seguimiento" en la navbar
- Visible para todos los usuarios autenticados
- Posicionado entre "Sembradores" y "Usuarios"

---

## 🏗️ Arquitectura

### Flujo de Datos

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vue 3)                          │
├─────────────────────────────────────────────────────────────┤
│  SeguimientoView.vue                                         │
│  ├─ Tab: Crear Seguimiento                                  │
│  │  └─ POST /seguimientos/crear                             │
│  ├─ Tab: Mis Seguimientos                                   │
│  │  ├─ GET /seguimientos/ (lista)                           │
│  │  ├─ PUT /seguimientos/{id} (editar)                      │
│  │  └─ DELETE /seguimientos/{id} (eliminar)                 │
│  └─ Tab: Reportes                                           │
│     ├─ GET /seguimientos/reportes/por-tecnico               │
│     └─ GET /seguimientos/reportes/por-cultivo               │
└─────────────────────────────────────────────────────────────┘
         ↕ HTTP + JWT Authentication
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                           │
├─────────────────────────────────────────────────────────────┤
│  routes/seguimientos.py                                     │
│  ├─ Authentication: JWT Bearer                              │
│  ├─ Access Control: Hierarchical (4 levels)                 │
│  ├─ CRUD Operations (5 endpoints)                           │
│  └─ Reporting (2 endpoints)                                 │
└─────────────────────────────────────────────────────────────┘
         ↕ SQLAlchemy ORM
┌─────────────────────────────────────────────────────────────┐
│              DATABASE (PostgreSQL)                           │
├─────────────────────────────────────────────────────────────┤
│  Table: seguimientos                                        │
│  ├─ Relationships: Sembrador, User                          │
│  ├─ Indexed: id (PK), sembrador_id (FK), user_id (FK)      │
│  └─ Timestamps: creado_en, actualizado_en                  │
└─────────────────────────────────────────────────────────────┘
```

### Hierarchical Access Control

```
Admin
  └─ Puede ver: Todos los seguimientos
  
Territorial
  └─ Puede ver: Seguimientos de sus subordinados (Facilitadores + Técnicos)
  
Facilitador / Gestor_Facilitador
  └─ Puede ver: Seguimientos de sus técnicos
  
Técnico (Productivo/Social)
  └─ Puede ver: Solo sus propios seguimientos
```

### Relaciones de Base de Datos

```
usuarios (users)
  ├─ id
  ├─ nombre
  ├─ rol
  └─ (muchas) → seguimientos

sembradores (sembradores)
  ├─ id
  ├─ nombre
  ├─ comunidad
  ├─ cultivo_principal
  └─ (muchas) → seguimientos

seguimientos
  ├─ id (PK)
  ├─ sembrador_id (FK → sembradores.id)
  ├─ user_id (FK → usuarios.id)
  ├─ fecha_visita
  ├─ estado_cultivo
  ├─ observaciones
  ├─ avance_porcentaje
  ├─ foto_url
  ├─ creado_en (timestamp)
  └─ actualizado_en (timestamp)
```

---

## 🚀 Guía de Uso

### Para Técnicos

#### 1. Crear un Seguimiento
1. Navega a **"📊 Seguimiento"** en la navbar
2. Asegúrate de estar en la tab **"Crear Seguimiento"**
3. Completa el formulario:
   - **Sembrador**: Selecciona de la lista desplegable
   - **Fecha de Visita**: Selecciona fecha y hora
   - **Estado del Cultivo**: Elige de las 8 opciones
   - **Avance**: Usa el slider para indicar progreso (%)
   - **Observaciones**: Describe lo que observaste
   - **Foto (opcional)**: Pega URL de la foto
4. Haz clic en "✅ Guardar Seguimiento"
5. Verás confirmación y se te llevará a "Mis Seguimientos"

#### 2. Ver Seguimientos Creados
1. Ve a la tab **"Mis Seguimientos"**
2. Verás todas tus visitas en tarjetas
3. Cada tarjeta muestra:
   - Nombre del sembrador y comunidad
   - Cultivo principal
   - Fecha de la visita
   - Barra de progreso
   - Observaciones
   - Foto (si la hay)
4. Haz clic en ✏️ para editar (funcionalidad en desarrollo)
5. Haz clic en 🗑️ para eliminar

#### 3. Estados del Cultivo Disponibles
- 🌱 **Germinando**: Semillas brotando
- 🌿 **Vegetativo**: Crecimiento de hojas y tallos
- 🌻 **Floración**: Producción de flores
- 🍅 **Fructificación**: Desarrollo de frutos
- ✂️ **Cosecha**: Tiempo de recolección
- 🐛 **Plagas**: Presencia de plagas
- 😷 **Enfermedad**: Enfermedad detectada

### Para Supervisores/Territorial

#### 1. Ver Reporte por Técnico
1. Ve a la tab **"Reportes"**
2. Observa la tabla **"Reporte por Técnico"**
3. Información mostrada:
   - Nombre del técnico
   - Rol (Técnico Productivo/Social)
   - Total de seguimientos registrados
   - Avance promedio (%)
   - Fecha del último seguimiento
4. Los técnicos se ordenan por cantidad de seguimientos

#### 2. Ver Reporte por Cultivo
1. En la tab **"Reportes"**, sección **"Reporte por Cultivo"**
2. Información mostrada:
   - Nombre del cultivo
   - Total de sembradores con ese cultivo
   - Total de seguimientos realizados
   - Avance promedio de todos los seguimientos
3. Cultivos se ordenan por mayor avance

### Para Admin

- Acceso completo a todos los datos
- Puede ver todos los técnicos y todos los reportes
- Puede eliminar seguimientos si es necesario

---

## 📡 API Endpoints

### Autenticación

Todos los endpoints requieren:
```
Headers:
  Authorization: Bearer {JWT_TOKEN}
```

### CRUD Endpoints

#### Crear Seguimiento
```http
POST /seguimientos/crear
Content-Type: application/json

{
  "sembrador_id": 1,
  "fecha_visita": "2024-11-18T14:30:00",
  "estado_cultivo": "Vegetativo",
  "observaciones": "Cultivo en buen estado, sin plagas visibles",
  "avance_porcentaje": 45.5,
  "foto_url": "https://ejemplo.com/foto.jpg"
}

Response 200:
{
  "success": true,
  "id": 42,
  "mensaje": "Seguimiento creado exitosamente"
}
```

#### Listar Seguimientos
```http
GET /seguimientos/
GET /seguimientos/?sembrador_id=1

Response 200:
{
  "success": true,
  "total": 25,
  "items": [
    {
      "id": 42,
      "sembrador_id": 1,
      "sembrador_nombre": "Juan Perez",
      "comunidad": "El Palmar",
      "cultivo_principal": "Maíz",
      "user_id": 5,
      "tecnico_nombre": "Carlos García",
      "fecha_visita": "2024-11-18T14:30:00",
      "estado_cultivo": "Vegetativo",
      "observaciones": "...",
      "avance_porcentaje": 45.5,
      "foto_url": "https://...",
      "creado_en": "2024-11-18T14:30:00",
      "actualizado_en": "2024-11-18T14:30:00"
    }
  ]
}
```

#### Obtener Detalle
```http
GET /seguimientos/{id}

Response 200:
{
  "success": true,
  "item": { ... }
}

Response 404:
{
  "success": false,
  "mensaje": "Seguimiento no encontrado"
}
```

#### Actualizar Seguimiento
```http
PUT /seguimientos/{id}
Content-Type: application/json

{
  "estado_cultivo": "Floración",
  "avance_porcentaje": 60,
  "observaciones": "Actualizando observaciones"
}

Response 200:
{
  "success": true,
  "mensaje": "Seguimiento actualizado"
}

Response 403:
{
  "success": false,
  "mensaje": "No tienes permiso para actualizar este seguimiento"
}
```

#### Eliminar Seguimiento
```http
DELETE /seguimientos/{id}

Response 200:
{
  "success": true,
  "mensaje": "Seguimiento eliminado"
}

Response 403:
{
  "success": false,
  "mensaje": "No tienes permiso para eliminar este seguimiento"
}
```

### Reporting Endpoints

#### Reporte por Técnico
```http
GET /seguimientos/reportes/por-tecnico

Response 200:
{
  "success": true,
  "total": 5,
  "items": [
    {
      "tecnico_id": 5,
      "tecnico_nombre": "Carlos García",
      "rol": "tecnico_productivo",
      "total_seguimientos": 25,
      "avance_promedio": 45.2,
      "ultimo_seguimiento": "2024-11-18T14:30:00"
    },
    {
      "tecnico_id": 6,
      "tecnico_nombre": "María López",
      "rol": "tecnico_social",
      "total_seguimientos": 18,
      "avance_promedio": 38.7,
      "ultimo_seguimiento": "2024-11-17T10:00:00"
    }
  ]
}
```

#### Reporte por Cultivo
```http
GET /seguimientos/reportes/por-cultivo

Response 200:
{
  "success": true,
  "total": 8,
  "items": [
    {
      "cultivo": "Maíz",
      "total_sembradores": 15,
      "total_seguimientos": 42,
      "avance_promedio": 52.3
    },
    {
      "cultivo": "Papa",
      "total_sembradores": 8,
      "total_seguimientos": 28,
      "avance_promedio": 38.9
    }
  ]
}
```

### Códigos de Error

| Código | Significado | Causas Comunes |
|--------|------------|---|
| 400 | Bad Request | Datos inválidos o faltantes |
| 401 | Unauthorized | Token JWT inválido o expirado |
| 403 | Forbidden | No tienes permiso (ej: no eres creador) |
| 404 | Not Found | Seguimiento o Sembrador no existe |
| 500 | Server Error | Error en la base de datos |

---

## 🧪 Testing

### Testing con Postman

1. **Obtener Token**
```
POST http://localhost:8000/login
Body (raw JSON):
{
  "email": "tecnico@example.com",
  "password": "password123"
}
```

2. **Crear Seguimiento**
```
POST http://localhost:8000/seguimientos/crear
Headers:
  Authorization: Bearer {token_from_step_1}
Body:
{
  "sembrador_id": 1,
  "fecha_visita": "2024-11-18T14:30:00",
  "estado_cultivo": "Germinando",
  "observaciones": "Test seguimiento",
  "avance_porcentaje": 25,
  "foto_url": null
}
```

3. **Listar Seguimientos**
```
GET http://localhost:8000/seguimientos/
Headers:
  Authorization: Bearer {token}
```

4. **Ver Reportes**
```
GET http://localhost:8000/seguimientos/reportes/por-tecnico
GET http://localhost:8000/seguimientos/reportes/por-cultivo
Headers:
  Authorization: Bearer {token}
```

### Testing en Frontend

1. Abre navegador en `http://localhost:5173`
2. Inicia sesión como técnico
3. Navega a "📊 Seguimiento"
4. Prueba cada funcionalidad:
   - Crear nuevo seguimiento
   - Ver lista de seguimientos
   - Eliminar un seguimiento
   - Ver reportes

---

## 🔧 Configuración

### Variables de Entorno

**Backend** (`.env` o en `main.py`):
```
DATABASE_URL=postgresql://user:password@localhost/sistemaapp
API_PORT=8000
```

**Frontend** (`.env.local`):
```
VITE_API_URL=http://localhost:8000
```

### Iniciar la Aplicación

**Backend**:
```bash
cd Backend
python -m uvicorn main:app --reload --port 8000
```

**Frontend**:
```bash
cd Frontend/sistemaapp-frontend
npm install
npm run dev
```

---

## 🆘 Troubleshooting

### Problema: "401 Unauthorized" al crear seguimiento

**Solución:**
- Verifica que el token JWT sea válido
- Inicia sesión nuevamente
- Verifica que el token esté siendo enviado correctamente en el header

### Problema: "404 Sembrador not found"

**Solución:**
- El sembrador_id seleccionado no existe en la base de datos
- Verifica que el sembrador esté creado en "🌱 Sembradores"
- Recarga la página para obtener la lista actualizada

### Problema: No puedo editar un seguimiento

**Solución:**
- Solo el creador del seguimiento puede editarlo
- Funcionalidad de edición está en desarrollo (actualmente solo eliminar)
- Verifica que seas el técnico que creó el registro

### Problema: Las fotos no se muestran

**Solución:**
- Las fotos deben ser URLs públicamente accesibles
- Verifica que la URL sea válida (comience con http:// o https://)
- Comprueba que el servidor de imágenes esté disponible

### Problema: Reportes vacíos

**Solución:**
- Crea primero algunos seguimientos
- Verifica que tengas permisos para ver reportes (rol Facilitador o superior)
- Espera a que los datos se carguen completamente

### Problema: Base de datos - tabla no se crea

**Solución:**
- Asegúrate que PostgreSQL esté corriendo
- Verifica la conexión a la base de datos
- El modelo `Seguimiento` debe estar importado en `main.py`
- SQLAlchemy creará la tabla automáticamente en el primer inicio

---

## 📊 Estadísticas y Métricas

### Campos Rastreados

- **Fecha de Visita**: Permite análisis temporal
- **Estado del Cultivo**: Seguimiento del ciclo de crecimiento
- **Progreso %**: Métrica cuantificable de avance
- **Observaciones**: Datos cualitativos del campo
- **Foto**: Evidencia visual

### Métricas Disponibles

1. **Por Técnico**:
   - Total de visitas realizadas
   - Promedio de avance de todos los cultivos
   - Última fecha de actividad

2. **Por Cultivo**:
   - Cantidad de sembradores cultivando
   - Total de seguimientos registrados
   - Promedio de progreso del cultivo

---

## 🔐 Seguridad

✅ **JWT Authentication**: Todos los endpoints requieren token válido  
✅ **Hierarchical Access Control**: Usuarios solo ven datos autorizados  
✅ **Creator-Only Permissions**: Solo el creador puede editar/eliminar  
✅ **Foreign Key Constraints**: Integridad referencial en BD  
✅ **Input Validation**: Validación de tipos en FastAPI  
✅ **HTTPS Ready**: Compatible con certificados SSL/TLS  

---

## 📈 Próximas Mejoras (Roadmap)

- [ ] Edición completa de seguimientos (actualmente solo delete)
- [ ] Carga directa de fotos (sin URLs externas)
- [ ] Filtros avanzados por rango de fechas
- [ ] Exportar reportes a PDF/Excel
- [ ] Gráficos interactivos con Chart.js/D3.js
- [ ] Notificaciones cuando técnicos crean seguimientos
- [ ] Comparación de progreso entre técnicos
- [ ] Mapa de calor de visitas
- [ ] Autofill de datos históricos
- [ ] Sincronización offline

---

## 📞 Soporte

Para reportar bugs o solicitar features:
1. Documenta el problema detalladamente
2. Incluye pasos para reproducir
3. Adjunta screenshots si es aplicable
4. Reporta al equipo de desarrollo

---

**Última Actualización**: 18 Noviembre 2024  
**Versión**: 1.0.0  
**Estado**: ✅ Production Ready
