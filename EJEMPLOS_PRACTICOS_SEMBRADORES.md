# 💻 Ejemplos Prácticos - SembradoresView.vue

## 🚀 Ejemplos de Uso

### 1. Crear Sembrador - Caso Normal

**Entrada del Usuario:**
```
Nombre: Juan Pérez García
Comunidad: La Esperanza
Cultivo Principal: Maíz
Teléfono: +56912345678
Latitud: -33.8688
Longitud: -51.2093
```

**Petición HTTP:**
```http
POST http://localhost:8000/sembradores/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "nombre": "Juan Pérez García",
  "comunidad": "La Esperanza",
  "cultivo_principal": "Maíz",
  "telefono": "+56912345678",
  "lat": -33.8688,
  "lng": -51.2093
}
```

**Respuesta Exitosa:**
```json
{
  "success": true,
  "id": 1,
  "nombre": "Juan Pérez García",
  "comunidad": "La Esperanza",
  "cultivo_principal": "Maíz",
  "telefono": "+56912345678",
  "lat": -33.8688,
  "lng": -51.2093,
  "user_id": 5,
  "creado_en": "2024-01-15T10:30:00.000Z",
  "message": "Sembrador registrado correctamente"
}
```

**Respuesta en UI:**
```
✅ Éxito
Sembrador registrado correctamente
[Aceptar]
```

**Formulario después:**
```
Nombre: [vacío]
Comunidad: [vacío]
Cultivo Principal: [vacío]
Teléfono: [vacío]
Latitud: [vacío]
Longitud: [vacío]
```

**Tabla se actualiza:**
```
┌─────────────────────────────────────────────┐
│ 1 │ Sembradores Registrados                 │
├─────────────────────────────────────────────┤
│ Nombre        │ Comunidad │ Cultivo │ ... │
├─────────────────────────────────────────────┤
│ Juan Pérez... │ La Esperanza │ Maíz   │ ... │
└─────────────────────────────────────────────┘
```

---

### 2. Crear Sembrador - Campo Vacío

**Intento del Usuario:**
```
Nombre: [vacío] ← Incorrecto
Comunidad: La Esperanza
Cultivo Principal: Maíz
Teléfono: +56912345678
Latitud: [vacío]
Longitud: [vacío]
```

**Código Frontend Ejecutado:**
```typescript
const crearSembrador = async () => {
  if (!form.value.nombre || !form.value.comunidad || ...) {
    // Detiene el flujo
    Swal.fire('❌ Error', 'Por favor completa todos los campos obligatorios', 'error')
    return // No hace POST
  }
  // ...
}
```

**Respuesta en UI:**
```
❌ Error
Por favor completa todos los campos obligatorios
[Aceptar]
```

**Acción:** Nada se envía al servidor

---

### 3. Crear Sembrador - Token Expirado

**Petición HTTP:**
```http
POST http://localhost:8000/sembradores/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...token_expirado
Content-Type: application/json

{...}
```

**Respuesta Backend:**
```json
{
  "detail": "Unauthorized - Token expired"
}
HTTP/1.1 401 Unauthorized
```

**Código Frontend Maneja Error:**
```typescript
catch (err: any) {
  const errorMsg = err.response?.data?.detail || 'No se pudo registrar el sembrador'
  Swal.fire('❌ Error', errorMsg, 'error')
}
```

**Respuesta en UI:**
```
❌ Error
Unauthorized - Token expired
[Aceptar]
```

**Usuario debe:** Salir (logout) y volver a hacer login

---

### 4. Listar Sembradores - Admin (Ve todo)

**Usuario:** Admin (rol: "admin")
**Token user_id:** 1

**Petición HTTP:**
```http
GET http://localhost:8000/sembradores/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...admin_token
```

**Backend Query:**
```python
# Como es admin, no aplica filtro
query = db.query(Sembrador).all()  # Todos los sembradores
```

**Respuesta:**
```json
{
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
      "creado_en": "2024-01-15T10:30:00.000Z"
    },
    {
      "id": 2,
      "nombre": "María López",
      "comunidad": "El Valle",
      "cultivo_principal": "Papa",
      "telefono": "+56987654321",
      "lat": -33.9100,
      "lng": -51.2500,
      "user_id": 6,
      "creado_en": "2024-01-14T15:20:00.000Z"
    },
    {
      "id": 3,
      "nombre": "Pedro González",
      "comunidad": "Los Campos",
      "cultivo_principal": "Trigo",
      "telefono": "+56934567890",
      "lat": -33.8500,
      "lng": -51.1800,
      "user_id": 7,
      "creado_en": "2024-01-13T09:10:00.000Z"
    }
  ]
}
```

**Tabla en Frontend:**
```
┌─────────────────────────────────────────────────────┐
│ 3 │ Sembradores Registrados                         │
├─────────────────────────────────────────────────────┤
│ Nombre    │ Comunidad     │ Cultivo │ Tel │ ... │ │
├─────────────────────────────────────────────────────┤
│ Juan P... │ La Esperanza  │ Maíz    │ ... │ ... │ │
│ María L..│ El Valle      │ Papa    │ ... │ ... │ │
│ Pedro G..│ Los Campos    │ Trigo   │ ... │ ... │ │
└─────────────────────────────────────────────────────┘
```

---

### 5. Listar Sembradores - Técnico (Solo suyo)

**Usuario:** Técnico Productivo
**Token user_id:** 5
**Sus sembradores:** Solo id 1 (user_id=5)

**Petición HTTP:**
```http
GET http://localhost:8000/sembradores/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...tecnico_token
```

**Backend Query:**
```python
# Como es técnico, filtra por user_id
query = db.query(Sembrador).filter(Sembrador.user_id == 5).all()
```

**Respuesta:**
```json
{
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
      "creado_en": "2024-01-15T10:30:00.000Z"
    }
  ]
}
```

**Tabla en Frontend:**
```
┌─────────────────────────────────────────────┐
│ 1 │ Sembradores Registrados                 │
├─────────────────────────────────────────────┤
│ Nombre    │ Comunidad     │ Cultivo │ ... │ │
├─────────────────────────────────────────────┤
│ Juan P... │ La Esperanza  │ Maíz    │ ... │ │
└─────────────────────────────────────────────┘
```

---

### 6. Eliminar Sembrador - Exitoso

**Usuario:** Técnico (id 5), elimina su propio sembrador (id 1)

**Click en botón 🗑️**

**Modal de Confirmación:**
```
⚠️ Confirmar eliminación
¿Estás seguro de que deseas eliminar este sembrador?

[Cancelar] [Sí, eliminar]
```

**Usuario clickea "Sí, eliminar"**

**Petición HTTP:**
```http
DELETE http://localhost:8000/sembradores/1 HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...tecnico_token
```

**Backend Valida:**
```python
# Obtiene el sembrador
sembrador = db.query(Sembrador).filter(Sembrador.id == 1).first()

# Valida propiedad
if sembrador.user_id != current_user.id:  # 5 == 5
    raise HTTPException(status_code=403, detail="No tienes permiso")

# Procede a eliminar
db.delete(sembrador)
db.commit()
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Sembrador eliminado correctamente"
}
```

**Frontend Recibe Respuesta:**
```typescript
if (result.isConfirmed) {
  try {
    await axios.delete(`${apiUrl}/sembradores/1`, {...})
    Swal.fire('✅ Eliminado', 'Sembrador eliminado correctamente', 'success')
    await getSembradores()  // Recarga lista
  } catch (err) {...}
}
```

**Notificación en UI:**
```
✅ Eliminado
Sembrador eliminado correctamente
[Aceptar]
```

**Tabla se actualiza:**
```
┌─────────────────────────────────────────────┐
│ 0 │ Sembradores Registrados                 │
├─────────────────────────────────────────────┤
│                                             │
│    Sin sembradores aún                      │
│    Registra el primer sembrador...          │
│                                             │
└─────────────────────────────────────────────┘
```

---

### 7. Eliminar Sembrador - Sin Permiso

**Usuario:** Técnico (id 5), intenta eliminar de otro (id 2, user_id=6)

**Petición HTTP:**
```http
DELETE http://localhost:8000/sembradores/2 HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...tecnico_5_token
```

**Backend Valida:**
```python
sembrador = db.query(Sembrador).filter(Sembrador.id == 2).first()
# sembrador.user_id = 6

if sembrador.user_id != current_user.id:  # 6 != 5
    raise HTTPException(
        status_code=403,
        detail="No tienes permiso para eliminar este sembrador"
    )
```

**Respuesta HTTP:**
```json
{
  "detail": "No tienes permiso para eliminar este sembrador"
}
HTTP/1.1 403 Forbidden
```

**Frontend Maneja Error:**
```typescript
catch (err: any) {
  Swal.fire('❌ Error', 'No se pudo eliminar el sembrador', 'error')
}
```

**Notificación en UI:**
```
❌ Error
No se pudo eliminar el sembrador
[Aceptar]
```

---

### 8. Estado Vacío - Primera Vez

**Usuario:** Nuevo técnico sin sembradores aún

**Petición HTTP:**
```http
GET http://localhost:8000/sembradores/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...new_tecnico_token
```

**Backend Query:**
```python
query = db.query(Sembrador).filter(Sembrador.user_id == 99).all()
# Retorna lista vacía: []
```

**Respuesta:**
```json
{
  "items": []
}
```

**Frontend Detecta:**
```typescript
if (sembradores.length === 0) {
  // Muestra empty state
}
```

**Vista Rendered:**
```
┌──────────────────────────────────┐
│ 0 │ Sembradores Registrados      │
├──────────────────────────────────┤
│                                  │
│       🌱                         │
│                                  │
│   Sin sembradores aún            │
│   Registra el primer sembrador   │
│                                  │
└──────────────────────────────────┘
```

---

## 📊 Matrices de Filtrado

### Ejemplo: Facilitador Obtiene Lista

**Usuario:** Facilitador (id 3)
**Subordinados Técnicos:** IDs 4, 5, 6 (todos con `rol LIKE "tecnico%"`)

**Backend Query:**
```python
# Obtiene los IDs de técnicos subordinados
facilitador = db.query(User).filter(User.id == 3).first()
tecnicos = db.query(User).filter(
    User.superior_id == 3,
    User.rol.like("tecnico%")  # Tanto productivo como social
).all()  # [User(id=4), User(id=5), User(id=6)]

tecnico_ids = [t.id for t in tecnicos]  # [4, 5, 6]

# Obtiene sembradores de esos técnicos
sembradores = db.query(Sembrador).filter(
    Sembrador.user_id.in_(tecnico_ids)
).all()
```

**Sembradores en BD:**
```
id | nombre    | user_id
---|-----------|--------
1  | Juan      | 4  ✅ Es técnico de facilitador 3
2  | María     | 5  ✅ Es técnico de facilitador 3
3  | Pedro     | 6  ✅ Es técnico de facilitador 3
4  | Carlos    | 7  ❌ No es subordinado de 3
5  | Ana       | 3  ❌ Es él mismo
```

**Resultado:** Sembradores [1, 2, 3] (Juan, María, Pedro)

---

### Ejemplo: Territorial Obtiene Lista

**Usuario:** Territorial (id 2)
**Subordinados Directos:** IDs 3 (Facilitador), que tiene técnicos 4, 5, 6

**Backend Query:**
```python
# Obtiene subordinados directos
territorial = db.query(User).filter(User.id == 2).first()
subordinados = db.query(User).filter(
    User.superior_id == 2
).all()  # [User(id=3), ...]

subordinado_ids = [s.id for s in subordinados]  # [3, ...]

# Obtiene sembradores de esos subordinados
sembradores = db.query(Sembrador).filter(
    Sembrador.user_id.in_(subordinado_ids)
).all()
```

**Resultado:** Sembradores solo de usuario_id 3 (Facilitador)

---

## 🎬 Flujos de Pantalla

### Flujo 1: Primera Vez

```
┌──────────────────────────┐
│ LOGIN                    │
│ username/password        │
└──────────────────────────┘
            ↓
┌──────────────────────────┐
│ DASHBOARD                │
│ Welcome back!            │
└──────────────────────────┘
            ↓
    User clicks 🌱 Sembradores
            ↓
┌──────────────────────────┐
│ SEMBRADORES VIEW         │
│ ┌────────────────────┐   │
│ │ Formulario Vacío   │   │
│ └────────────────────┘   │
│ ┌────────────────────┐   │
│ │ Sin sembradores    │   │
│ │ (empty state)      │   │
│ └────────────────────┘   │
└──────────────────────────┘
            ↓
    User fills form & clicks Save
            ↓
┌──────────────────────────┐
│ ✅ Éxito                 │
│ Sembrador registrado     │
└──────────────────────────┘
            ↓
┌──────────────────────────┐
│ SEMBRADORES VIEW         │
│ ┌────────────────────┐   │
│ │ Formulario Limpio  │   │
│ └────────────────────┘   │
│ ┌────────────────────┐   │
│ │ Tabla con 1 item   │   │
│ │ ┌──────────────┐   │   │
│ │ │ Juan | ... |   │   │
│ │ └──────────────┘   │   │
│ └────────────────────┘   │
└──────────────────────────┘
```

### Flujo 2: Eliminar

```
┌──────────────────────────┐
│ SEMBRADORES VIEW         │
│ Tabla con 3 items        │
│ ┌──────────────────────┐ │
│ │ Juan  │ ... │ 🗑️    │ │
│ │ María │ ... │ 🗑️    │ │
│ │ Pedro │ ... │ 🗑️    │ │
│ └──────────────────────┘ │
└──────────────────────────┘
            ↓
    Click 🗑️ en María
            ↓
┌──────────────────────────┐
│ ⚠️ Confirmar eliminación │
│ ¿Estás seguro?           │
│ [Cancelar] [Sí, eliminar]│
└──────────────────────────┘
            ↓
    Click "Sí, eliminar"
            ↓
        DELETE /api/...
            ↓
┌──────────────────────────┐
│ ✅ Eliminado             │
│ Sembrador eliminado      │
└──────────────────────────┘
            ↓
┌──────────────────────────┐
│ SEMBRADORES VIEW         │
│ Tabla con 2 items        │
│ ┌──────────────────────┐ │
│ │ Juan  │ ... │ 🗑️    │ │
│ │ Pedro │ ... │ 🗑️    │ │
│ └──────────────────────┘ │
└──────────────────────────┘
```

---

## 🧮 Casos de Borde

### Caso 1: Campos de Geolocalización Vacíos

**Formulario:**
```
Nombre: Juan Pérez ✓
Comunidad: La Esperanza ✓
Cultivo Principal: Maíz ✓
Teléfono: +56912345678 ✓
Latitud: [vacío] ← OK (no obligatorio)
Longitud: [vacío] ← OK (no obligatorio)
```

**Petición:**
```json
{
  "nombre": "Juan Pérez",
  "comunidad": "La Esperanza",
  "cultivo_principal": "Maíz",
  "telefono": "+56912345678",
  "lat": null,
  "lng": null
}
```

**Backend Acepta:**
```python
sembrador = Sembrador(
    nombre="Juan Pérez",
    comunidad="La Esperanza",
    cultivo_principal="Maíz",
    telefono="+56912345678",
    lat=None,  # ✅ Válido
    lng=None,  # ✅ Válido
    user_id=5
)
db.add(sembrador)
```

**Tabla Muestra:**
```
Latitud: N/A
Longitud: N/A
```

---

### Caso 2: Números de Geolocalización Inválidos

**Formulario:**
```
Latitud: "no es número" ← TypeError
```

**HTML5 Validation:**
```html
<input type="number" v-model="form.lat" />
<!-- Input number rechaza no-números -->
```

**Resultado:** Browser no permite enviar

---

### Caso 3: Teléfono con Caracteres Especiales

**Formulario:**
```
Teléfono: +56-912-345-678
```

**Enviado:**
```json
{
  "telefono": "+56-912-345-678"
}
```

**Backend Acepta:** Campo string, sin validación de formato

**Tabla Muestra:**
```
Teléfono: +56-912-345-678
```

**Si clickea:** `tel:+56-912-345-678` (puede fallar en algunos navegadores)

---

### Caso 4: Nombre Muy Largo

**Formulario:**
```
Nombre: "Juan Pérez García López González Rodríguez Fernández Torres..." (500 caracteres)
```

**HTML Valida:**
```
minlength="2" ✓ (cumple)
maxlength no especificado (pero BD tiene VARCHAR(255))
```

**Backend Maneja:**
```python
nombre = "Juan Pérez García López González Rodríguez Fernández Torres... (500 caracteres)"
# SQLAlchemy trunca automáticamente a 255 caracteres
```

---

## 🔄 Ciclo Completo de Vida

### Semana 1: Técnico Crea Sembradores

```
Lun: Juan crea 3 sembradores
    - Sembrador 1: Juan (user_id 5)
    - Sembrador 2: María (user_id 5)
    - Sembrador 3: Pedro (user_id 5)

Mar: María crea 2 sembradores
    - Sembrador 4: Carlos (user_id 6)
    - Sembrador 5: Ana (user_id 6)
```

### Semana 2: Facilitador Revisa

```
Facilitador (user_id 3) accede a /sembradores
Backend retorna: [1, 2, 3, 4, 5] (todos sus subordinados)
Tabla muestra 5 sembradores
```

### Semana 3: Territorial Revisa

```
Territorial (user_id 2) accede a /sembradores
Backend retorna: [1, 2, 3, 4, 5] (subordinados directos)
Tabla muestra 5 sembradores
```

### Semana 4: Admin Revisa

```
Admin (user_id 1) accede a /sembradores
Backend retorna: TODOS los sembradores del sistema
Tabla muestra cientos de sembradores
```

---

## 📱 Responsive en Acción

### Desktop (1920x1080)

```
┌─────────────────────────────────────────────────┐
│ Header: 🌱 Sembradores                          │
├─────────────────────────────────────────────────┤
│ ┌──────────────────┬──────────────────┐         │
│ │ Nombre           │ Comunidad        │         │
│ ├──────────────────┼──────────────────┤         │
│ │ Cultivo          │ Teléfono         │         │
│ ├──────────────────┼──────────────────┤         │
│ │ Latitud          │ Longitud         │         │
│ └──────────────────┴──────────────────┘         │
│ [Guardar Sembrador]                             │
├─────────────────────────────────────────────────┤
│ Tabla (6 columnas):                             │
│ ┌────┬────┬────┬────┬────┬────┐                │
│ │ N  │ C  │ Cu │ Te │ Ub │ Ac │                │
│ ├────┼────┼────┼────┼────┼────┤                │
│ │...│...│...│...│...│... │                │
│ └────┴────┴────┴────┴────┴────┘                │
└─────────────────────────────────────────────────┘
```

### Tablet (768x1024)

```
┌───────────────────────────────┐
│ Header: 🌱 Sembradores        │
├───────────────────────────────┤
│ ┌─────────────────────────┐   │
│ │ Nombre                  │   │
│ ├─────────────────────────┤   │
│ │ Comunidad               │   │
│ ├─────────────────────────┤   │
│ │ Cultivo Principal       │   │
│ ├─────────────────────────┤   │
│ │ Teléfono                │   │
│ ├─────────────────────────┤   │
│ │ Latitud                 │   │
│ ├─────────────────────────┤   │
│ │ Longitud                │   │
│ └─────────────────────────┘   │
│ [Guardar]                     │
├───────────────────────────────┤
│ Tabla (scrollable):           │
│ ┌─────────────────────────┐   │
│ │ N │ C │ Cu │ Te │ ... │   │
│ ├─────────────────────────┤   │
│ │ ...(scroll horizontal)  │   │
│ └─────────────────────────┘   │
└───────────────────────────────┘
```

### Mobile (375x667)

```
┌─────────────────────┐
│ 🌱 Sembradores      │
├─────────────────────┤
│ ┌───────────────┐   │
│ │ Nombre        │   │
│ ├───────────────┤   │
│ │ Comunidad     │   │
│ ├───────────────┤   │
│ │ Cultivo       │   │
│ ├───────────────┤   │
│ │ Teléfono      │   │
│ ├───────────────┤   │
│ │ Latitud       │   │
│ ├───────────────┤   │
│ │ Longitud      │   │
│ └───────────────┘   │
│ [Guardar]           │
├─────────────────────┤
│ Tabla (scroll):     │
│ N | C | Cu | Te... │
│ ────────────────    │
│ Juan | La E | Maíz  │
│ (scroll →)          │
└─────────────────────┘
```

---

## ✅ Resumen

Este documento proporciona ejemplos prácticos y reales de cómo funciona SembradoresView.vue en diferentes escenarios:

1. ✅ Operaciones normales (crear, listar, eliminar)
2. ✅ Casos de error (token expirado, campos vacíos, sin permiso)
3. ✅ Filtrado jerárquico por rol
4. ✅ Casos de borde (campos vacíos, caracteres especiales)
5. ✅ Ciclos de vida completos
6. ✅ Responsive design en diferentes dispositivos

Todos los ejemplos usan datos reales y están basados en la implementación actual.

