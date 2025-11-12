# 🗺️ Guía de Integración - MapaView con Backend API

## Estado actual ✅

El frontend MapaView.vue ahora está **100% integrado** con el backend API de capas temáticas.

---

## Cambios realizados

### 1. **Importaciones agregadas**
```typescript
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
```

### 2. **Nueva función `loadLayers()`**
Reemplazó la función anterior que generaba datos ficticios. Ahora:
- Hace peticiones HTTP GET a cada endpoint de capas
- Obtiene datos reales de la base de datos
- Convierte coordenadas lat/lng en formato [lat, lng] para Leaflet
- Incluye manejo de errores

```typescript
const loadLayers = async () => {
  try {
    for (const c of capas) {
      const { data } = await axios.get(
        `${import.meta.env.VITE_API_URL}/layers/${c.value}`,
        {
          headers: { Authorization: `Bearer ${auth.token}` },
        }
      )
      dataCapas.value[c.value] = data.items.map(p => ({
        id: p.id,
        nombre: p.nombre,
        latlng: [p.lat, p.lng],
      }))
    }
  } catch (err) {
    console.error('Error al cargar capas:', err)
  }
}
```

### 3. **Nueva función `onMapClick()`**
Permite crear nuevos puntos directamente desde el mapa:
- Al hacer clic en el mapa, pide confirmación del tipo de capa
- Solicita nombre del punto
- Envía POST al backend
- Recarga todas las capas después de crear

```typescript
const onMapClick = async (event) => {
  const { lat, lng } = event.latlng
  const tipo = prompt("¿Qué tipo de capa deseas agregar? 
                       (ambiental/productiva/social/infraestructura)")
  const nombre = prompt("Nombre del punto:")
  if (tipo && nombre) {
    try {
      await axios.post(
        `${import.meta.env.VITE_API_URL}/layers/${tipo}`,
        {
          nombre,
          descripcion: "",
          lat,
          lng
        },
        {
          headers: { Authorization: `Bearer ${auth.token}` }
        }
      )
      alert("✅ Punto agregado correctamente")
      loadLayers()
    } catch {
      alert("❌ Error al agregar punto")
    }
  }
}
```

### 4. **Evento de clic en el mapa**
El mapa ahora escucha clics del usuario:
```vue
<l-map
  ref="map"
  v-model:zoom="zoom"
  :center="center"
  style="height: 100%; width: 100%;"
  @click="onMapClick"
>
```

---

## Flujo completo

```
┌─────────────────────────────────┐
│  1. Usuario abre MapaView       │
│  (onMounted se ejecuta)         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  2. loadLayers() se ejecuta     │
│  - Para cada capa (ambiental,   │
│    productiva, social, infra)   │
│  - GET /layers/{tipo}           │
│  - Con JWT Token                │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  3. Datos retornados            │
│  {                              │
│    "tipo": "ambiental",         │
│    "total": 5,                  │
│    "items": [...]               │
│  }                              │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  4. Marcadores renderizados     │
│  - Cada punto es un marker      │
│  - Con popup con nombre         │
│  - Color según tipo de capa     │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  5. Usuario hace clic en mapa   │
│  - onMapClick() se ejecuta      │
│  - Pide tipo y nombre           │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  6. POST /layers/{tipo}         │
│  {                              │
│    "nombre": "...",             │
│    "lat": 19.45,                │
│    "lng": -99.15                │
│  }                              │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  7. Backend guarda en DB        │
│  y retorna {success}            │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  8. loadLayers() se ejecuta     │
│  nuevamente para recargar       │
└─────────────────────────────────┘
```

---

## Requisitos previos

### Backend
✅ FastAPI corriendo en puerto 9000
✅ PostgreSQL accesible
✅ Tablas de capas creadas (ambiental, productiva, social, infraestructura)
✅ CORS configurado para `http://localhost:5173`

### Frontend
✅ Vue 3 + Vite
✅ axios instalado (`npm install axios`)
✅ Vue Leaflet instalado
✅ Store de autenticación configurado
✅ `.env` con `VITE_API_URL` correcto

### Autenticación
✅ Usuario debe estar logueado
✅ Token JWT debe estar en `auth.token`
✅ Token debe ser válido y no expirado

---

## Testing local

### 1. Asegúrate de que el backend esté corriendo

```bash
cd BackendFastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 9000
```

### 2. Obtén un token JWT

```bash
curl -X POST "http://localhost:9000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"usuario@example.com","password":"password123"}'
```

Respuesta:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Crea algunos datos iniciales

```bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# Crear punto ambiental
curl -X POST "http://localhost:9000/layers/ambiental" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Bosque Nacional",
    "descripcion": "Bosque protegido",
    "lat": 19.4326,
    "lng": -99.1332
  }'

# Crear punto productivo
curl -X POST "http://localhost:9000/layers/productiva" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Parcela de maíz",
    "descripcion": "Área de cultivo",
    "lat": 19.45,
    "lng": -99.15
  }'

# Crear punto social
curl -X POST "http://localhost:9000/layers/social" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Centro comunitario",
    "descripcion": "Centro social del pueblo",
    "lat": 19.42,
    "lng": -99.12
  }'

# Crear punto de infraestructura
curl -X POST "http://localhost:9000/layers/infraestructura" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carretera principal",
    "descripcion": "Ruta federal",
    "lat": 19.40,
    "lng": -99.18
  }'
```

### 4. Inicia el frontend

```bash
cd Frontend/sistemaapp-frontend
npm run dev
```

Abre `http://localhost:5173` en el navegador

### 5. Verifica que los datos aparezcan en el mapa

- Deberías ver marcadores de 4 colores:
  - 🟢 Verde (Ambiental)
  - 🟠 Naranja (Productiva)
  - 🔵 Azul (Social)
  - ⚪ Gris (Infraestructura)

### 6. Prueba crear un nuevo punto

- Haz clic en el mapa
- Introduce `ambiental` (o el tipo que quieras)
- Introduce un nombre
- El punto debe aparecer inmediatamente en el mapa

---

## Variables de entorno

### Frontend (`.env`)
```env
VITE_API_URL=http://localhost:9000
```

Para producción:
```env
VITE_API_URL=https://sistemaapi.sembrandodatos.com
```

### Backend (`.env` en BackendFastAPI/)
```env
DATABASE_URL=postgresql://usuario:password@31.97.8.51:5432/SistemaApp
SECRET_KEY=tu_secret_key_muy_seguro
API_HOST=0.0.0.0
API_PORT=9000
```

---

## Manejo de errores

### Error: "401 Unauthorized"
**Causa**: Token inválido o expirado
**Solución**: 
- Vuelve a hacer login
- Verifica que `auth.token` no sea null

### Error: "400 Bad Request"
**Causa**: Campo requerido faltante o tipo de capa inválido
**Solución**:
- Verifica que `nombre`, `lat`, `lng` no sean vacíos
- Verifica que `tipo` sea uno de: `ambiental`, `productiva`, `social`, `infraestructura`

### Error: "Network Error"
**Causa**: Backend no está accesible
**Solución**:
- Verifica que FastAPI esté corriendo
- Comprueba `VITE_API_URL` en `.env`
- Verifica CORS en main.py

### Error: "No markers appear on map"
**Causa**: Posiblemente no hay datos o la respuesta tiene formato diferente
**Solución**:
- Abre la consola (F12)
- Busca errores en la red (Network tab)
- Verifica la respuesta de `GET /layers/ambiental`

---

## Próximos pasos

### 1. Mejorar UX para crear puntos
```typescript
// Podríamos hacer un modal en lugar de prompts
const showCreateDialog = ref(false)
const newPointData = ref({ tipo: '', nombre: '', lat: 0, lng: 0 })
```

### 2. Agregar edición de puntos
```typescript
const onMarkerRightClick = async (event, punto) => {
  // Permitir editar nombre/descripción
}
```

### 3. Agregar búsqueda/filtro
```typescript
const searchTerm = ref('')
const filteredCapas = computed(() => {
  // Filtrar por nombre
})
```

### 4. Agregar eliminación de puntos
```typescript
const onMarkerDelete = async (id, tipo) => {
  // DELETE /layers/{tipo}/{id}
}
```

### 5. Agregar actualización de puntos
```typescript
const onPointUpdate = async (id, tipo, data) => {
  // PUT /layers/{tipo}/{id}
}
```

---

## Documentación relacionada

- 📖 [API Docs](../BackendFastAPI/LAYERS_API_DOCS.md)
- 🧪 [Testing Guide](../BackendFastAPI/TESTING_GUIDE.md)
- 🏗️ [Architecture](../BackendFastAPI/ARCHITECTURE.md)
- 📝 [README](../BackendFastAPI/README_LAYERS.md)

---

## Contacto & Soporte

Para problemas o sugerencias:
1. Revisa los logs del backend (`uvicorn.log`)
2. Abre la consola del navegador (F12 → Console)
3. Ejecuta los comandos de testing en TESTING_GUIDE.md

