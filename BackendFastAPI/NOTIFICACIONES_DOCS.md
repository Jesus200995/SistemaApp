# 🔔 Sistema de Notificaciones - Documentación

## ✅ Implementación completada

### 1. **Modelo Notificacion** (`models.py`)

```python
class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # info, warning, error, success
    rol_destino = Column(String(50))  # admin, usuario, all
    leido = Column(Boolean, default=False)
    usuario_id = Column(Integer)  # Opcional: para notificaciones personales
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### 2. **Rutas de Notificaciones** (`routes/notificaciones.py`)

✅ WebSocket endpoint para notificaciones en tiempo real
✅ 6 endpoints REST con autenticación JWT
✅ Sistema de broadcast a todos los clientes
✅ Gestión de conexiones

### 3. **Registro en main.py**

```python
from routes import notificaciones
app.include_router(notificaciones.router)
```

---

## 📡 Endpoints API

### WebSocket

#### **Conectar a notificaciones en tiempo real**
```
WebSocket: wss://sistemaapi.sembrandodatos.com/notificaciones/ws
```

**Cliente:**
```javascript
const ws = new WebSocket('wss://sistemaapi.sembrandodatos.com/notificaciones/ws')
ws.onmessage = (e) => {
  const notif = JSON.parse(e.data)
  console.log('🔔 Nueva notificación:', notif.titulo)
}
```

**Servidor envía:**
```json
{
  "id": 1,
  "titulo": "Nuevo punto agregado",
  "mensaje": "Se ha agregado un nuevo punto en la capa ambiental",
  "tipo": "success",
  "rol_destino": "all",
  "timestamp": "2025-11-12T14:32:15.123456"
}
```

---

### REST Endpoints

#### **1. Crear notificación**
```
POST /notificaciones/crear
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "titulo": "Nueva notificación",
  "mensaje": "Contenido de la notificación",
  "tipo": "success",
  "rol_destino": "all"
}
```

**Response:**
```json
{
  "success": true,
  "notificacion_id": 1,
  "mensaje": "Notificación creada y enviada"
}
```

---

#### **2. Obtener todas las notificaciones**
```
GET /notificaciones/
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "total": 5,
  "notificaciones": [
    {
      "id": 5,
      "titulo": "Última notificación",
      "mensaje": "Contenido...",
      "tipo": "info",
      "leido": false,
      "timestamp": "2025-11-12T14:35:00"
    },
    {
      "id": 4,
      "titulo": "Notificación anterior",
      "mensaje": "Contenido...",
      "tipo": "warning",
      "leido": true,
      "timestamp": "2025-11-12T14:30:00"
    }
  ]
}
```

---

#### **3. Marcar notificación como leída**
```
PATCH /notificaciones/{notif_id}/leer
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "success": true,
  "mensaje": "Notificación marcada como leída"
}
```

---

#### **4. Eliminar notificación**
```
DELETE /notificaciones/{notif_id}
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "success": true,
  "mensaje": "Notificación eliminada"
}
```

---

#### **5. Contar no leídas**
```
GET /notificaciones/no-leidas/count
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "no_leidas": 3
}
```

---

#### **6. Estado del sistema**
```
GET /notificaciones/status/info
```

**Response:**
```json
{
  "clientes_conectados": 5,
  "status": "✅ Sistema de notificaciones funcionando correctamente"
}
```

---

## 🎯 Tipos de notificaciones

| Tipo | Uso | Color (recomendado) |
|------|-----|---|
| **info** | Información general | 🔵 Azul |
| **success** | Operación exitosa | 🟢 Verde |
| **warning** | Advertencia | 🟡 Amarillo |
| **error** | Error o problema | 🔴 Rojo |

---

## 👥 Roles destino

| Rol | Descripción |
|-----|---|
| **all** | Todos los usuarios |
| **admin** | Solo administradores |
| **usuario** | Solo usuarios regulares |

---

## 🧪 Prueba local

### 1. **Iniciar backend**

```bash
cd BackendFastAPI
source venv/bin/activate  # Linux/Mac
python -m uvicorn main:app --reload --port 9000
```

### 2. **Obtener token JWT**

```bash
curl -X POST "http://localhost:9000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "usuario": {"id": 1, "nombre": "Admin", "rol": "admin"}
}
```

### 3. **Crear notificación**

```bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

curl -X POST "http://localhost:9000/notificaciones/crear" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Test notification",
    "mensaje": "Esta es una notificación de prueba",
    "tipo": "success",
    "rol_destino": "all"
  }'
```

### 4. **Conectar WebSocket (JavaScript)**

```javascript
const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

const ws = new WebSocket('ws://localhost:9000/notificaciones/ws')

ws.onopen = () => {
  console.log('✅ Conectado a notificaciones')
}

ws.onmessage = (event) => {
  const notif = JSON.parse(event.data)
  console.log('🔔 Nueva notificación:', notif)
  
  // Mostrar notificación al usuario
  showNotification(notif)
}

ws.onclose = () => {
  console.log('🔴 Desconectado de notificaciones')
}
```

### 5. **Obtener notificaciones**

```bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

curl -X GET "http://localhost:9000/notificaciones/" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. **Ver estado**

```bash
curl "http://localhost:9000/notificaciones/status/info"
```

---

## 🎨 Frontend - Integración con Vue

### **NotificationCenter.vue** (Componente recomendado)

```vue
<template>
  <div class="notification-container">
    <!-- Badge con contador -->
    <button class="notification-button" @click="togglePanel">
      🔔
      <span v-if="noLeidas > 0" class="badge">{{ noLeidas }}</span>
    </button>

    <!-- Panel de notificaciones -->
    <div v-if="showPanel" class="notification-panel">
      <h3>Notificaciones</h3>
      
      <div v-if="notificaciones.length === 0" class="empty">
        Sin notificaciones
      </div>
      
      <div v-else class="notification-list">
        <div 
          v-for="notif in notificaciones" 
          :key="notif.id"
          class="notification-item"
          :class="[notif.tipo, { 'no-leida': !notif.leido }]"
        >
          <div class="notification-header">
            <span class="notification-title">{{ notif.titulo }}</span>
            <button @click="marcarComoLeida(notif.id)" class="close-btn">✕</button>
          </div>
          <p class="notification-message">{{ notif.mensaje }}</p>
          <span class="notification-time">{{ formatTime(notif.timestamp) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const auth = useAuthStore()
const ws = ref(null)
const showPanel = ref(false)
const notificaciones = ref([])
const noLeidas = ref(0)

const connectWebSocket = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = import.meta.env.VITE_API_URL.replace('https://', '').replace('http://', '')
  
  ws.value = new WebSocket(`${protocol}//${host}/notificaciones/ws`)
  
  ws.value.onmessage = (event) => {
    const notif = JSON.parse(event.data)
    notificaciones.value.unshift(notif)
    noLeidas.value += 1
    
    // Mostrar notificación de sistema
    if (Notification.permission === 'granted') {
      new Notification(notif.titulo, {
        body: notif.mensaje,
        tag: notif.id
      })
    }
  }
}

const marcarComoLeida = async (notifId) => {
  try {
    await axios.patch(
      `${import.meta.env.VITE_API_URL}/notificaciones/${notifId}/leer`,
      {},
      { headers: { Authorization: `Bearer ${auth.token}` } }
    )
    
    const notif = notificaciones.value.find(n => n.id === notifId)
    if (notif) notif.leido = true
    noLeidas.value = Math.max(0, noLeidas.value - 1)
  } catch (error) {
    console.error('Error marcando como leída:', error)
  }
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
}

const togglePanel = () => {
  showPanel.value = !showPanel.value
}

onMounted(() => {
  connectWebSocket()
  // Solicitar permisos para notificaciones del sistema
  if ('Notification' in window) {
    Notification.requestPermission()
  }
})

onBeforeUnmount(() => {
  if (ws.value) ws.value.close()
})
</script>

<style scoped>
.notification-container {
  position: relative;
}

.notification-button {
  position: relative;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.badge {
  position: absolute;
  top: -5px;
  right: -8px;
  background: #dc2626;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.notification-panel {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 350px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
}

.notification-item {
  padding: 12px;
  border-bottom: 1px solid #f3f4f6;
  border-left: 4px solid #3b82f6;
}

.notification-item.success {
  border-left-color: #10b981;
}

.notification-item.warning {
  border-left-color: #f59e0b;
}

.notification-item.error {
  border-left-color: #ef4444;
}

.notification-item.no-leida {
  background: #f0f9ff;
}

.notification-title {
  font-weight: bold;
  color: #1f2937;
}

.notification-message {
  font-size: 14px;
  color: #6b7280;
  margin: 4px 0;
}

.notification-time {
  font-size: 12px;
  color: #9ca3af;
}
</style>
```

---

## 🚀 Ejemplo de uso completo

### Backend - Crear notificación cuando se agrega un punto

```python
# En routes/layers.py
from routes.notificaciones import broadcast_notification

@router.post("/layers/ambiental")
async def crear_punto_ambiental(data: dict, db: Session = Depends(get_db)):
    # ... crear punto ...
    
    # Enviar notificación
    await broadcast_notification({
        "id": 1,
        "titulo": "Nuevo punto ambiental",
        "mensaje": f"Se agregó: {data.get('nombre')}",
        "tipo": "success",
        "rol_destino": "all",
        "timestamp": datetime.now().isoformat()
    })
    
    return {"success": True}
```

---

## 🔐 Seguridad

✅ **Todos los endpoints REST requieren JWT**
✅ **WebSocket solo recibe, no valida (broadcast solo)**
✅ **Validación de datos en entrada**
✅ **Manejo de excepciones robusto**

---

## 📊 Base de datos

Las notificaciones se guardan en PostgreSQL:

```sql
SELECT * FROM notificaciones 
ORDER BY created_at DESC;
```

---

## ✨ Características implementadas

| Característica | Estado |
|---|---|
| WebSocket broadcasting | ✅ |
| REST API CRUD | ✅ |
| Autenticación JWT | ✅ |
| Tipos de notificaciones | ✅ |
| Roles destino | ✅ |
| Marcar como leída | ✅ |
| Contador de no leídas | ✅ |
| Estado del sistema | ✅ |
| Persistencia BD | ✅ |

---

**✅ Sistema de notificaciones completamente implementado.** 🎉

