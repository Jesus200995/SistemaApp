# 🗺️ API de Capas Temáticas - Documentación

## Descripción
Endpoints para gestionar capas temáticas del mapa: Ambiental, Productiva, Social e Infraestructura.

## Base URL
```
http://localhost:9000/layers
```

## Autenticación
Todos los endpoints requieren un **JWT Token** en el header:
```
Authorization: Bearer <token>
```

---

## 📍 Endpoints

### 1️⃣ Obtener todas las capas de un tipo

**GET** `/layers/{tipo}`

Obtiene todos los puntos de una capa específica.

**Parámetros:**
- `tipo` (string): `ambiental`, `productiva`, `social`, `infraestructura`

**Ejemplo de request:**
```bash
curl -X GET "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer <token>"
```

**Respuesta exitosa (200):**
```json
{
  "tipo": "ambiental",
  "total": 2,
  "items": [
    {
      "id": 1,
      "nombre": "Bosque de Chapultepec",
      "descripcion": "Área verde protegida en CDMX",
      "lat": 19.4267,
      "lng": -99.1776,
      "created_at": "2025-11-12T10:30:00"
    },
    {
      "id": 2,
      "nombre": "Xochimilco",
      "descripcion": "Zona ecológica con chinampas",
      "lat": 19.2565,
      "lng": -99.0906,
      "created_at": "2025-11-12T10:35:00"
    }
  ]
}
```

---

### 2️⃣ Crear un nuevo punto

**POST** `/layers/{tipo}`

Crea un nuevo punto en una capa específica.

**Body esperado:**
```json
{
  "nombre": "Nombre del punto",
  "descripcion": "Descripción detallada",
  "lat": 19.4326,
  "lng": -99.1332
}
```

**Ejemplo de request:**
```bash
curl -X POST "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Vivero Forestal",
    "descripcion": "Centro de reproducción de plantas nativas",
    "lat": 19.35,
    "lng": -99.15
  }'
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "id": 3,
  "tipo": "ambiental",
  "message": "Punto creado exitosamente en la capa ambiental"
}
```

---

### 3️⃣ Obtener un punto específico

**GET** `/layers/{tipo}/{id}`

Obtiene un punto específico de una capa.

**Parámetros:**
- `tipo` (string): `ambiental`, `productiva`, `social`, `infraestructura`
- `id` (integer): ID del punto

**Ejemplo de request:**
```bash
curl -X GET "http://localhost:9000/layers/ambiental/1" \
  -H "Authorization: Bearer <token>"
```

**Respuesta exitosa (200):**
```json
{
  "id": 1,
  "nombre": "Bosque de Chapultepec",
  "descripcion": "Área verde protegida en CDMX",
  "lat": 19.4267,
  "lng": -99.1776,
  "created_at": "2025-11-12T10:30:00"
}
```

---

### 4️⃣ Actualizar un punto

**PUT** `/layers/{tipo}/{id}`

Actualiza un punto específico de una capa.

**Body esperado:**
```json
{
  "nombre": "Nuevo nombre (opcional)",
  "descripcion": "Nueva descripción (opcional)",
  "lat": 19.4267,
  "lng": -99.1776
}
```

**Ejemplo de request:**
```bash
curl -X PUT "http://localhost:9000/layers/ambiental/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Bosque de Chapultepec Actualizado",
    "descripcion": "Área verde protegida y restaurada en CDMX"
  }'
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Punto 1 actualizado exitosamente",
  "item": {
    "id": 1,
    "nombre": "Bosque de Chapultepec Actualizado",
    "descripcion": "Área verde protegida y restaurada en CDMX",
    "lat": 19.4267,
    "lng": -99.1776
  }
}
```

---

### 5️⃣ Eliminar un punto

**DELETE** `/layers/{tipo}/{id}`

Elimina un punto específico de una capa.

**Parámetros:**
- `tipo` (string): `ambiental`, `productiva`, `social`, `infraestructura`
- `id` (integer): ID del punto a eliminar

**Ejemplo de request:**
```bash
curl -X DELETE "http://localhost:9000/layers/ambiental/1" \
  -H "Authorization: Bearer <token>"
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Punto 1 eliminado exitosamente"
}
```

---

## 🔴 Códigos de Error

| Código | Mensaje | Descripción |
|--------|---------|------------|
| 400 | Tipo de capa no válido | El tipo de capa no existe |
| 400 | Faltan campos requeridos | Faltan nombre, lat, o lng |
| 401 | Token inválido | El JWT token no es válido |
| 404 | Punto no encontrado | El ID del punto no existe |
| 500 | Error al crear punto | Error general del servidor |

---

## 📦 Tipos de capas válidos

```
- ambiental       → Áreas verdes, bosques, zonas ecológicas
- productiva      → Parcelas, tierras cultivables, zonas agrícolas
- social          → Centros comunitarios, espacios culturales
- infraestructura → Rutas, puentes, servicios públicos
```

---

## 🔐 Ejemplo de autenticación

Primero obten el token en `/auth/login`:

```bash
curl -X POST "http://localhost:9000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@ejemplo.com",
    "password": "password123"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Luego usa ese token en los endpoints de capas:

```bash
curl -X GET "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 📊 Casos de uso

### Cargar todas las capas para el mapa
```bash
curl -X GET "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer <token>"
curl -X GET "http://localhost:9000/layers/productiva" \
  -H "Authorization: Bearer <token>"
curl -X GET "http://localhost:9000/layers/social" \
  -H "Authorization: Bearer <token>"
curl -X GET "http://localhost:9000/layers/infraestructura" \
  -H "Authorization: Bearer <token>"
```

### Crear múltiples puntos
```bash
for i in {1..5}; do
  curl -X POST "http://localhost:9000/layers/ambiental" \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d "{
      \"nombre\": \"Punto Verde $i\",
      \"descripcion\": \"Descripción del punto $i\",
      \"lat\": $((194000 + RANDOM % 1000))/10000,
      \"lng\": $((991000 + RANDOM % 1000))/10000
    }"
done
```

---

## ✅ Consideraciones

- Todos los puntos requieren **lat** (latitud) y **lng** (longitud) válidas
- El campo **descripcion** es opcional
- Los puntos incluyen **created_at** automáticamente
- Solo usuarios autenticados pueden acceder
- Las coordenadas son números decimales: `-99.1776`, `19.4267`

