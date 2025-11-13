# 📋 CRUD de Sembradores - Documentación Completa

## 🎯 Resumen

Se ha implementado un sistema completo de CRUD para **Sembradores** con soporte de jerarquía de usuarios. Los sembradores son personas que siembran cultivos en diferentes comunidades.

---

## 📦 Estructura de Datos

### Tabla: `sembradores`

```python
class Sembrador(Base):
    __tablename__ = "sembradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))  # Nombre del sembrador
    comunidad = Column(String(100))  # Comunidad donde siembra
    cultivo_principal = Column(String(100))  # Ej: Maíz, Papa, etc.
    telefono = Column(String(30))  # Contacto
    lat = Column(Float)  # Latitud
    lng = Column(Float)  # Longitud
    user_id = Column(Integer, ForeignKey("users.id"))  # Usuario propietario
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
```

---

## 🔗 Endpoints Implementados

### 1️⃣ POST - Crear Sembrador

**URL:** `POST /sembradores/`

**Autenticación:** Bearer Token (JWT)

**Body:**
```json
{
  "nombre": "Juan Pérez",
  "comunidad": "La Esperanza",
  "cultivo_principal": "Maíz",
  "telefono": "+56912345678",
  "lat": -33.8688,
  "lng": -51.2093
}
```

**Response (201 - Success):**
```json
{
  "success": true,
  "id": 1,
  "nombre": "Juan Pérez",
  "message": "Sembrador creado exitosamente"
}
```

**Response (400 - Error):**
```json
{
  "detail": "El nombre es obligatorio"
}
```

---

### 2️⃣ GET - Listar Sembradores

**URL:** `GET /sembradores/`

**Autenticación:** Bearer Token (JWT)

**Response (200 - Success):**
```json
{
  "total": 2,
  "items": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "comunidad": "La Esperanza",
      "cultivo_principal": "Maíz",
      "telefono": "+56912345678",
      "lat": -33.8688,
      "lng": -51.2093,
      "user_id": 5,
      "creado_en": "2025-11-13T10:30:00+00:00"
    },
    {
      "id": 2,
      "nombre": "María García",
      "comunidad": "Nueva vida",
      "cultivo_principal": "Papa",
      "telefono": "+56987654321",
      "lat": -33.9156,
      "lng": -51.3259,
      "user_id": 5,
      "creado_en": "2025-11-13T11:00:00+00:00"
    }
  ]
}
```

**Filtrado según rol:**
- **Admin:** Ve TODOS los sembradores
- **Territorial:** Ve sembradores de subordinados directos
- **Facilitador:** Ve sembradores de técnicos subordinados
- **Técnico:** Ve solo sus propios sembradores

---

### 3️⃣ GET - Obtener Sembrador Específico

**URL:** `GET /sembradores/{id}`

**Autenticación:** Bearer Token (JWT)

**Parameters:**
- `id` (integer, required): ID del sembrador

**Response (200 - Success):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "comunidad": "La Esperanza",
  "cultivo_principal": "Maíz",
  "telefono": "+56912345678",
  "lat": -33.8688,
  "lng": -51.2093,
  "user_id": 5,
  "creado_en": "2025-11-13T10:30:00+00:00"
}
```

**Response (404 - Not Found):**
```json
{
  "detail": "Sembrador no encontrado"
}
```

**Response (403 - Forbidden):**
```json
{
  "detail": "No tienes permiso para ver este sembrador"
}
```

---

### 4️⃣ PUT - Actualizar Sembrador

**URL:** `PUT /sembradores/{id}`

**Autenticación:** Bearer Token (JWT)

**Body:** (todos los campos son opcionales)
```json
{
  "nombre": "Juan Carlos Pérez",
  "comunidad": "La Esperanza Nueva",
  "cultivo_principal": "Maíz y Papa",
  "telefono": "+56912345679",
  "lat": -33.8700,
  "lng": -51.2100
}
```

**Response (200 - Success):**
```json
{
  "success": true,
  "message": "Sembrador 1 actualizado exitosamente",
  "sembrador": {
    "id": 1,
    "nombre": "Juan Carlos Pérez",
    "comunidad": "La Esperanza Nueva",
    "cultivo_principal": "Maíz y Papa",
    "telefono": "+56912345679",
    "lat": -33.8700,
    "lng": -51.2100,
    "user_id": 5
  }
}
```

**Response (403 - Forbidden):**
```json
{
  "detail": "No tienes permiso para actualizar este sembrador"
}
```

---

### 5️⃣ DELETE - Eliminar Sembrador

**URL:** `DELETE /sembradores/{id}`

**Autenticación:** Bearer Token (JWT)

**Parameters:**
- `id` (integer, required): ID del sembrador

**Response (200 - Success):**
```json
{
  "success": true,
  "message": "Sembrador 1 eliminado exitosamente"
}
```

**Response (403 - Forbidden):**
```json
{
  "detail": "No tienes permiso para eliminar este sembrador"
}
```

---

## 🔐 Seguridad y Jerarquía

### Matriz de Acceso

| Rol | Crear | Listar | Ver Detalles | Actualizar | Eliminar |
|-----|-------|--------|--------------|-----------|----------|
| Admin | ✅ | ✅ Todos | ✅ Todos | ✅ Cualquiera | ✅ Cualquiera |
| Territorial | ✅ | ✅ Subordinados | ✅ Subordinados | ✅ Propios | ✅ Propios |
| Facilitador | ✅ | ✅ Técnicos | ✅ Técnicos | ✅ Propios | ✅ Propios |
| Técnico | ✅ | ✅ Propios | ✅ Propios | ✅ Propios | ✅ Propios |

### Filtrado Jerárquico

```python
# Admin: Ve todo
if rol == "admin":
    query = query  # Sin filtro

# Territorial: Ve subordinados directos
elif rol == "territorial":
    sub_ids = [u.id for u in db.query(User).filter(User.superior_id == user_id)]
    query = query.filter(Sembrador.user_id.in_(sub_ids))

# Facilitador: Ve técnicos subordinados (ambos tipos)
elif rol == "facilitador":
    sub_ids = [u.id for u in db.query(User).filter(
        User.superior_id == user_id,
        User.rol.like("tecnico%")  # Cubre tecnico_productivo y tecnico_social
    )]
    query = query.filter(Sembrador.user_id.in_(sub_ids))

# Técnico/Otro: Ve solo propios
else:
    query = query.filter(Sembrador.user_id == user_id)
```

---

## 📊 Casos de Uso

### Caso 1: Técnico crea y listar sus sembradores
```bash
# 1. Login como técnico
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "tecnico@test.com", "password": "123456"}'
# Response: {"token": "eyJhbGc..."}

# 2. Crear sembrador
curl -X POST http://localhost:8000/sembradores/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "comunidad": "La Esperanza",
    "cultivo_principal": "Maíz",
    "telefono": "+56912345678",
    "lat": -33.8688,
    "lng": -51.2093
  }'

# 3. Listar sus sembradores
curl -X GET http://localhost:8000/sembradores/ \
  -H "Authorization: Bearer {token}"
# Response: {"total": 1, "items": [...]}
```

### Caso 2: Facilitador ve sembradores de sus técnicos
```bash
# 1. Login como facilitador
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "facilitador@test.com", "password": "123456"}'

# 2. Listar sembradores (filtra por técnicos subordinados)
curl -X GET http://localhost:8000/sembradores/ \
  -H "Authorization: Bearer {token_facilitador}"
# Retorna: sembradores creados por sus técnicos subordinados
```

### Caso 3: Admin ve todos los sembradores
```bash
# Admin ve TODOS los sembradores sin restricción
curl -X GET http://localhost:8000/sembradores/ \
  -H "Authorization: Bearer {token_admin}"
# Retorna: Todos los sembradores de la plataforma
```

---

## ✅ Tests Recomendados

### Test 1: Crear Sembrador
```bash
POST /sembradores/
Authorization: Bearer {token_tecnico}

Body:
{
  "nombre": "Carlos López",
  "comunidad": "Santa Rosa",
  "cultivo_principal": "Papa",
  "telefono": "+56912345678",
  "lat": -33.8688,
  "lng": -51.2093
}

Esperado: Status 200, id generado
```

### Test 2: Listar Sembradores (Técnico)
```bash
GET /sembradores/
Authorization: Bearer {token_tecnico}

Esperado: Solo sembradores creados por este técnico
```

### Test 3: Listar Sembradores (Facilitador)
```bash
GET /sembradores/
Authorization: Bearer {token_facilitador}

Esperado: Sembradores de técnicos subordinados
```

### Test 4: Listar Sembradores (Admin)
```bash
GET /sembradores/
Authorization: Bearer {token_admin}

Esperado: TODOS los sembradores
```

### Test 5: Técnico no puede ver otro técnico
```bash
GET /sembradores/2
Authorization: Bearer {token_tecnico_1}

Esperado: 403 Forbidden (si sembrador pertenece a otro técnico)
```

### Test 6: Actualizar Sembrador (Propietario)
```bash
PUT /sembradores/1
Authorization: Bearer {token_tecnico_1}

Body:
{
  "nombre": "Carlos López Actualizado",
  "telefono": "+56912345679"
}

Esperado: 200 Success
```

### Test 7: Actualizar Sembrador (No propietario)
```bash
PUT /sembradores/1
Authorization: Bearer {token_tecnico_2}

Esperado: 403 Forbidden
```

### Test 8: Eliminar Sembrador
```bash
DELETE /sembradores/1
Authorization: Bearer {token_tecnico_1}

Esperado: 200 Success
```

---

## 📱 Integración con Frontend (Próxima Fase)

### Estructura de Componentes Recomendada

```
Frontend/
├── src/
│   ├── views/
│   │   └── SembradoresView.vue  (NEW)
│   ├── components/
│   │   ├── SembradoresList.vue  (NEW)
│   │   ├── SembradoresForm.vue  (NEW)
│   │   └── SembradoresMap.vue   (NEW)
│   ├── stores/
│   │   └── sembradores.ts       (NEW)
│   └── services/
│       └── sembradoresService.ts (NEW)
```

### API Service Example

```typescript
// services/sembradoresService.ts
export const sembradoresService = {
  async crear(data) {
    return fetch(`${API_URL}/sembradores/`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: JSON.stringify(data)
    })
  },
  
  async listar() {
    return fetch(`${API_URL}/sembradores/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
  },
  
  async obtener(id) {
    return fetch(`${API_URL}/sembradores/${id}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
  },
  
  async actualizar(id, data) {
    return fetch(`${API_URL}/sembradores/${id}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` },
      body: JSON.stringify(data)
    })
  },
  
  async eliminar(id) {
    return fetch(`${API_URL}/sembradores/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })
  }
}
```

---

## 🗄️ Migración de BD

Para crear la tabla en PostgreSQL:

```sql
CREATE TABLE sembradores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    comunidad VARCHAR(100),
    cultivo_principal VARCHAR(100),
    telefono VARCHAR(30),
    lat FLOAT,
    lng FLOAT,
    user_id INTEGER REFERENCES users(id),
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sembradores_user_id ON sembradores(user_id);
CREATE INDEX idx_sembradores_comunidad ON sembradores(comunidad);
```

O usar Alembic (recomendado):

```bash
alembic revision --autogenerate -m "Add Sembrador model"
alembic upgrade head
```

---

## ✨ Características Implementadas

✅ CRUD completo (Create, Read, Update, Delete)
✅ Jerarquía de usuarios (admin, territorial, facilitador, técnico)
✅ Validación de permisos en cada operación
✅ Geolocalización (lat/lng)
✅ Información de contacto (teléfono)
✅ Timestamps automáticos
✅ Asociación automática a usuario actual
✅ Filtrado por jerarquía en listados
✅ Manejo robusto de errores

---

## 📈 Próximas Fases

1. **Frontend** - Crear vista de sembradores con formulario y mapa
2. **Reportes** - Generar reportes de sembradores por región/comunidad
3. **Analytics** - Seguimiento de cultivos y producción
4. **Mobile** - App móvil para captura de datos en campo
5. **Export** - Exportar datos a Excel/PDF

---

**Fecha de Creación:** 13 de noviembre de 2025
**Status:** ✅ Implementado y Listo para Usar
**Última Actualización:** 13 de noviembre de 2025
