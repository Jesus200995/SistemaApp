# 📋 Módulo de Solicitudes - Documentación Técnica

## 🎯 Descripción General

El módulo de Solicitudes permite a los usuarios crear, listar y gestionar solicitudes dentro del sistema. Las solicitudes pueden ser de diferentes tipos y dirigidas a usuarios específicos según su rol.

---

## 📊 Estructura de la Tabla

```sql
CREATE TABLE solicitudes (
  id SERIAL PRIMARY KEY,
  tipo VARCHAR(50) NOT NULL,
  descripcion TEXT,
  usuario_id INT REFERENCES users(id) ON DELETE CASCADE,
  destino_id INT REFERENCES users(id) ON DELETE SET NULL,
  estado VARCHAR(20) DEFAULT 'pendiente',
  fecha TIMESTAMP DEFAULT NOW()
);
```

### Campos
- **id**: Identificador único (auto-incremento)
- **tipo**: Tipo de solicitud (string hasta 50 caracteres)
- **descripcion**: Descripción detallada de la solicitud
- **usuario_id**: ID del usuario que crea la solicitud (FK → users.id)
- **destino_id**: ID del usuario destinatario (FK → users.id, NULL al eliminar usuario)
- **estado**: Estado de la solicitud (`pendiente`, `aprobada`, `rechazada`)
- **fecha**: Timestamp de creación (automático)

---

## 🧩 Modelo SQLAlchemy

**Archivo**: `BackendFastAPI/models.py`

```python
class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50))
    descripcion = Column(Text)
    usuario_id = Column(Integer, ForeignKey("users.id"))
    destino_id = Column(Integer, ForeignKey("users.id"))
    estado = Column(String(20), default="pendiente")
    fecha = Column(DateTime(timezone=True), server_default=func.now())
```

---

## 🔌 Endpoints API

### 1️⃣ Crear Solicitud (POST)

**Endpoint**: `POST /solicitudes/`

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "tipo": "permiso_ausencia",
  "descripcion": "Solicito permiso para ausentarme el 20 de noviembre",
  "destino_id": 5
}
```

**Response (201)**:
```json
{
  "success": true,
  "solicitud_id": 42
}
```

**Error (401)**:
```json
{
  "detail": "Token inválido"
}
```

---

### 2️⃣ Listar Solicitudes (GET)

**Endpoint**: `GET /solicitudes/`

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Query Parameters**: Ninguno

**Response (200)**:
```json
[
  {
    "id": 1,
    "tipo": "permiso_ausencia",
    "descripcion": "Solicito permiso...",
    "usuario_id": 3,
    "destino_id": 5,
    "estado": "pendiente",
    "fecha": "2025-11-18T10:30:00"
  },
  {
    "id": 2,
    "tipo": "cambio_zona",
    "descripcion": "Solicito cambio de zona...",
    "usuario_id": 3,
    "destino_id": 5,
    "estado": "aprobada",
    "fecha": "2025-11-17T14:20:00"
  }
]
```

**Filtrado por Rol** (automático):
- **admin**: Ve todas las solicitudes
- **territorial/facilitador**: Ve solo las solicitudes dirigidas a ellos (`destino_id == user_id`)
- **tecnico**: Ve solo las que creó (`usuario_id == user_id`)

**Error (401)**:
```json
{
  "detail": "Token inválido"
}
```

---

### 3️⃣ Actualizar Estado (PUT)

**Endpoint**: `PUT /solicitudes/{id}/estado`

**URL Parameters**:
- `id`: ID de la solicitud (integer)

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "estado": "aprobada"
}
```

**Response (200)**:
```json
{
  "success": true,
  "estado": "aprobada"
}
```

**Error (404)**:
```json
{
  "detail": "Solicitud no encontrada"
}
```

**Error (401)**:
```json
{
  "detail": "Token inválido"
}
```

---

## 🔐 Control de Acceso (RBAC)

### Creación de Solicitud
- **Quién puede**: Cualquier usuario autenticado
- **Campo obligatorio**: JWT token válido (proporciona `usuario_id`)

### Listado de Solicitudes
- **admin**: Ve todas las solicitudes del sistema
- **territorial**: Ve solo las solicitudes dirigidas a él
- **facilitador**: Ve solo las solicitudes dirigidas a él
- **tecnico**: Ve solo las que él creó

### Actualización de Estado
- **Quién puede**: Cualquier usuario autenticado
- **Validación**: Se verifica que el usuario actualice solo solicitudes válidas

---

## 📝 Estados de Solicitud

| Estado | Descripción |
|--------|-------------|
| `pendiente` | Solicitud recién creada, esperando respuesta |
| `aprobada` | Solicitud ha sido aprobada por el destinatario |
| `rechazada` | Solicitud ha sido rechazada por el destinatario |

---

## 🔄 Integración en main.py

```python
from routes import solicitudes

# En la sección de include_router
app.include_router(solicitudes.router)
```

---

## 📂 Archivos Modificados

1. **`BackendFastAPI/models.py`**
   - Agregada clase `Solicitud` al final del archivo
   - Líneas agregadas: ~10

2. **`BackendFastAPI/routes/solicitudes.py`** (NUEVO)
   - Creado nuevo archivo con 3 endpoints
   - Total: ~80 líneas de código

3. **`BackendFastAPI/main.py`**
   - Importación de `solicitudes` en línea de imports
   - Agregado `app.include_router(solicitudes.router)` en sección de rutas
   - Líneas modificadas: 2

---

## ✅ Verificación

### Modelo
- ✅ Clase `Solicitud` creada en `models.py`
- ✅ Tabla `solicitudes` definida con ORM
- ✅ Todas las columnas mapeadas correctamente

### Rutas
- ✅ Endpoint POST `/solicitudes/` funcional
- ✅ Endpoint GET `/solicitudes/` funcional
- ✅ Endpoint PUT `/solicitudes/{id}/estado` funcional
- ✅ Autenticación JWT implementada en todos

### Integración
- ✅ Router importado en `main.py`
- ✅ Router registrado con `include_router`
- ✅ CORS configurado para nuevos endpoints

---

## 🧪 Ejemplo de Uso (cURL)

### 1. Crear Solicitud
```bash
curl -X POST http://localhost:8000/solicitudes/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "permiso_ausencia",
    "descripcion": "Permiso para ausentarme",
    "destino_id": 5
  }'
```

### 2. Listar Solicitudes
```bash
curl -X GET http://localhost:8000/solicitudes/ \
  -H "Authorization: Bearer <token>"
```

### 3. Actualizar Estado
```bash
curl -X PUT http://localhost:8000/solicitudes/42/estado \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"estado": "aprobada"}'
```

---

## 🚀 Próximos Pasos Opcionales

1. **Frontend Component**
   - Vista para crear solicitudes
   - Vista para listar solicitudes
   - Vista para aprobar/rechazar solicitudes

2. **Notificaciones**
   - Notificar al destinatario cuando recibe una solicitud
   - Notificar al creador cuando su solicitud es procesada

3. **Validaciones Adicionales**
   - Validar tipos de solicitud permitidos
   - Validar que el usuario destino existe
   - Validar permisos según rol

4. **Campos Adicionales**
   - `motivo_rechazo`: Razón del rechazo
   - `fecha_procesamiento`: Cuándo fue procesada
   - `procesado_por`: Quién procesó la solicitud

---

## 📞 Soporte

Para más información sobre los endpoints, consulta la documentación interactiva:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

