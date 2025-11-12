# 🧪 Testing API de Capas Temáticas

## 1️⃣ Iniciar el servidor

```bash
cd BackendFastAPI
python main.py
```

Debería ver:
```
INFO:     Uvicorn running on http://0.0.0.0:9000
```

---

## 2️⃣ Obtener token (Autenticación)

Primero registra un usuario o usa credenciales existentes:

```bash
curl -X POST "http://localhost:9000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@ejemplo.com",
    "password": "password123"
  }'
```

Guarda el `access_token` que recibes:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 3️⃣ Testing de Capas

### 🟢 Crear punto ambiental

```bash
curl -X POST "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer <TU_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Bosque de Chapultepec",
    "descripcion": "Área verde protegida en CDMX",
    "lat": 19.4267,
    "lng": -99.1776
  }'
```

**Respuesta esperada:**
```json
{
  "success": true,
  "id": 1,
  "tipo": "ambiental",
  "message": "Punto creado exitosamente en la capa ambiental"
}
```

---

### 🟢 Crear punto productivo

```bash
curl -X POST "http://localhost:9000/layers/productiva" \
  -H "Authorization: Bearer <TU_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Parcela Ejidal Los Reyes",
    "descripcion": "Zona de cultivo de maíz y frijol",
    "lat": 19.35,
    "lng": -99.20
  }'
```

---

### 🟢 Crear punto social

```bash
curl -X POST "http://localhost:9000/layers/social" \
  -H "Authorization: Bearer <TU_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Centro Comunitario Benito Juárez",
    "descripcion": "Espacio cultural y de reunión",
    "lat": 19.42,
    "lng": -99.15
  }'
```

---

### 🟢 Crear punto infraestructura

```bash
curl -X POST "http://localhost:9000/layers/infraestructura" \
  -H "Authorization: Bearer <TU_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Estación Metro Blanca",
    "descripcion": "Acceso a transporte público",
    "lat": 19.40,
    "lng": -99.18
  }'
```

---

### 📖 Obtener todos los puntos de una capa

```bash
curl -X GET "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer <TU_TOKEN>"
```

**Respuesta:**
```json
{
  "tipo": "ambiental",
  "total": 1,
  "items": [
    {
      "id": 1,
      "nombre": "Bosque de Chapultepec",
      "descripcion": "Área verde protegida en CDMX",
      "lat": 19.4267,
      "lng": -99.1776,
      "created_at": "2025-11-12T10:30:00"
    }
  ]
}
```

---

### 📖 Obtener un punto específico

```bash
curl -X GET "http://localhost:9000/layers/ambiental/1" \
  -H "Authorization: Bearer <TU_TOKEN>"
```

---

### ✏️ Actualizar un punto

```bash
curl -X PUT "http://localhost:9000/layers/ambiental/1" \
  -H "Authorization: Bearer <TU_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Bosque de Chapultepec - Restaurado",
    "descripcion": "Área verde protegida y en restauración"
  }'
```

---

### 🗑️ Eliminar un punto

```bash
curl -X DELETE "http://localhost:9000/layers/ambiental/1" \
  -H "Authorization: Bearer <TU_TOKEN>"
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Punto 1 eliminado exitosamente"
}
```

---

## 🧬 Script de Testing Completo

```bash
#!/bin/bash

# Guarda el token
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 1. Crear punto ambiental
echo "✅ Creando punto ambiental..."
curl -X POST "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Bosque de Chapultepec",
    "descripcion": "Área verde protegida",
    "lat": 19.4267,
    "lng": -99.1776
  }' | jq .

# 2. Listar capas ambientales
echo -e "\n✅ Listando capas ambientales..."
curl -X GET "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 3. Crear punto productivo
echo -e "\n✅ Creando punto productivo..."
curl -X POST "http://localhost:9000/layers/productiva" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Parcela Ejidal Los Reyes",
    "descripcion": "Zona de cultivo",
    "lat": 19.35,
    "lng": -99.20
  }' | jq .

# 4. Actualizar punto
echo -e "\n✅ Actualizando punto..."
curl -X PUT "http://localhost:9000/layers/ambiental/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Bosque Chapultepec - Actualizado"
  }' | jq .

# 5. Obtener un punto específico
echo -e "\n✅ Obteniendo punto específico..."
curl -X GET "http://localhost:9000/layers/ambiental/1" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

Guarda como `test_layers.sh` y ejecuta:
```bash
chmod +x test_layers.sh
./test_layers.sh
```

---

## 📋 Checklist

- ✅ Modelos creados en `models.py`
- ✅ Rutas creadas en `routes/layers.py`
- ✅ Main.py actualizado con import y router
- ✅ Servidor iniciado en puerto 9000
- ✅ Token JWT obtenido
- ✅ GET /layers/{tipo} funcionando
- ✅ POST /layers/{tipo} funcionando
- ✅ PUT /layers/{tipo}/{id} funcionando
- ✅ DELETE /layers/{tipo}/{id} funcionando
- ✅ CORS configurado correctamente
- ✅ Autenticación validando tokens

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'layers'"
**Solución:** Asegúrate de que `routes/layers.py` existe y main.py tiene `from routes import layers`

### Error: "Token inválido"
**Solución:** Usa un token válido. Obtén uno nuevo en `/auth/login`

### Error: "Tipo de capa no válido"
**Solución:** Usa solo: `ambiental`, `productiva`, `social`, `infraestructura`

### Error: "Faltan campos requeridos"
**Solución:** Asegúrate de enviar `nombre`, `lat`, `lng` en el body

