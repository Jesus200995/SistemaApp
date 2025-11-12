# 🔔 Notificaciones - Guía de Integración Frontend

## ✅ Componente CreatedCreated

**Ruta:** `src/components/NotificationCenter.vue`

### Características:
- ✅ WebSocket en tiempo real
- ✅ Badge con contador de no leídas
- ✅ Panel desplegable con notificaciones
- ✅ Colores por tipo (info, success, warning, error)
- ✅ Marcar como leída con 1 clic
- ✅ Eliminar notificaciones
- ✅ Notificaciones del sistema
- ✅ Timestamps relativos (hace 5m, hace 1h, etc)
- ✅ Responsive design

---

## 📦 Integración en App.vue

Abre tu `src/App.vue` y agrega el componente en el navbar:

```vue
<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar">
      <div class="flex items-center justify-between p-4">
        <h1>SistemaApp</h1>
        
        <div class="flex items-center gap-4">
          <!-- 🔔 AGREGAR AQUÍ -->
          <NotificationCenter />
          
          <!-- Usuario + Logout -->
          <div class="user-menu">
            <span>{{ user.nombre }}</span>
            <button @click="logout">Salir</button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido -->
    <router-view />
  </div>
</template>

<script setup>
// @ts-ignore
import NotificationCenter from './components/NotificationCenter.vue'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const user = auth.user

const logout = () => {
  auth.logout()
  // redirigir a login
}
</script>
```

---

## 🎯 Cómo usar en el backend

### Ejemplo: Enviar notificación cuando se crea un punto

**En `routes/layers.py`:**

```python
from routes.notificaciones import broadcast_notification
from datetime import datetime

@router.post("/layers/ambiental")
async def crear_punto_ambiental(
    data: dict,
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    db: Session = Depends(get_db)
):
    # ... validar, crear punto ...
    
    # 🔔 Enviar notificación a todos
    await broadcast_notification({
        "id": ambiental.id,
        "titulo": "🌳 Nuevo punto ambiental agregado",
        "mensaje": f"Se agregó: {ambiental.nombre}",
        "tipo": "success",
        "rol_destino": "all",
        "timestamp": datetime.now().isoformat()
    })
    
    return {"success": True, "punto": ambiental.id}
```

### Ejemplo: Notificación de error

```python
try:
    # ... operación riesgosa ...
except Exception as e:
    await broadcast_notification({
        "id": 1,
        "titulo": "❌ Error al procesar datos",
        "mensaje": str(e),
        "tipo": "error",
        "rol_destino": "admin",
        "timestamp": datetime.now().isoformat()
    })
    raise HTTPException(status_code=400, detail=str(e))
```

---

## 🚀 Casos de uso comunes

### 1. **Notificar cuando un usuario se registra**

```python
# En auth.py
from routes.notificaciones import broadcast_notification

@router.post("/register")
async def register(data: dict, db: Session = Depends(get_db)):
    # ... crear usuario ...
    
    await broadcast_notification({
        "titulo": "👤 Nuevo usuario registrado",
        "mensaje": f"{new_user.nombre} ({new_user.email})",
        "tipo": "info",
        "rol_destino": "admin",
        "timestamp": datetime.now().isoformat()
    })
    
    return {"success": True}
```

### 2. **Notificar cambio en datos**

```python
# Cuando alguien modifica un punto
await broadcast_notification({
    "titulo": "✏️ Punto actualizado",
    "mensaje": f"El punto '{punto.nombre}' fue actualizado",
    "tipo": "warning",
    "rol_destino": "all",
    "timestamp": datetime.now().isoformat()
})
```

### 3. **Notificación de sistema**

```python
# Mantenimiento programado
await broadcast_notification({
    "titulo": "🔧 Mantenimiento programado",
    "mensaje": "El sistema estará en mantenimiento el 15/11 de 2-3 AM",
    "tipo": "warning",
    "rol_destino": "all",
    "timestamp": datetime.now().isoformat()
})
```

---

## 🧪 Testing

### Test local

#### 1. **Iniciar backend**
```bash
cd BackendFastAPI
python -m uvicorn main:app --reload --port 9000
```

#### 2. **Iniciar frontend**
```bash
cd Frontend/sistemaapp-frontend
npm run dev
```

#### 3. **Abrir 2 navegadores**

**Browser 1:**
- URL: `http://localhost:5173`
- Login con usuario admin

**Browser 2:**
- URL: `http://localhost:5173`
- Login con usuario diferente

#### 4. **Crear notificación con curl**

```bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

curl -X POST "http://localhost:9000/notificaciones/crear" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "🧪 Test Notification",
    "mensaje": "Esta es una notificación de prueba",
    "tipo": "success",
    "rol_destino": "all"
  }'
```

#### 5. **Verificar en ambos navegadores**

Deberías ver:
- 🔔 Badge actualizado en ambos
- Notificación aparece en ambos panels
- Timestamp relativo correcto

---

## 🎨 Personalización

### Cambiar colores

Edita `NotificationCenter.vue` en la sección de clases:

```vue
<!-- Para tipo 'success' -->
'bg-green-50 border-l-4 border-green-400': notif.tipo === 'success',

<!-- Cambiar a otro color -->
'bg-emerald-50 border-l-4 border-emerald-500': notif.tipo === 'success',
```

### Cambiar position del panel

```vue
<!-- Actual: top right -->
<div class="notification-panel absolute right-0 mt-2">

<!-- Opción: top left -->
<div class="notification-panel absolute left-0 mt-2">

<!-- Opción: bottom right -->
<div class="notification-panel absolute right-0 mb-2 bottom-full">
```

### Limitar cantidad de notificaciones

```javascript
const connectWebSocket = () => {
  ws.value.onmessage = (event) => {
    const notif = JSON.parse(event.data)
    notificaciones.value.unshift(notif)
    
    // Mantener solo últimas 50 notificaciones
    if (notificaciones.value.length > 50) {
      notificaciones.value.pop()
    }
    
    noLeidas.value += 1
  }
}
```

---

## 🔊 Audio y animaciones

### Agregar sonido

```javascript
const playSound = () => {
  const audio = new Audio('/notification.mp3')
  audio.play().catch(e => console.log('No se pudo reproducir sonido'))
}

const showSystemNotification = (notif) => {
  playSound()  // ← Agregar esto
  
  if ('Notification' in window) {
    new Notification(notif.titulo, {
      body: notif.mensaje
    })
  }
}
```

### Agregar animación (Tailwind)

```vue
<div 
  @enter="enterAnimation"
  v-for="notif in notificaciones"
  class="animate-slideIn"
>
  <!-- contenido -->
</div>

<style>
@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.animate-slideIn {
  animation: slideIn 0.3s ease-out;
}
</style>
```

---

## 🔐 Permisos necesarios

El componente solicita permiso para notificaciones del sistema:

```javascript
if ('Notification' in window && Notification.permission === 'default') {
  Notification.requestPermission()
}
```

El usuario verá un popup:
```
Este sitio quiere mostrar notificaciones
[Permitir] [Bloquear]
```

---

## 📊 Estado actual

| Característica | Estado |
|---|---|
| WebSocket real-time | ✅ |
| Badge contador | ✅ |
| Panel desplegable | ✅ |
| Marcar como leída | ✅ |
| Eliminar | ✅ |
| Notificaciones sistema | ✅ |
| Timestamps relativos | ✅ |
| Colores por tipo | ✅ |
| Responsive | ✅ |

---

## 🐛 Troubleshooting

### "No veo el badge de notificaciones"

**Problema:** Badge no aparece

**Soluciones:**
1. Verifica que WebSocket está conectado
2. Abre DevTools → Console
3. Busca "✅ Conectado a notificaciones"
4. Si no aparece, verifica que backend está corriendo

### "Las notificaciones no aparecen en tiempo real"

**Problema:** Notificaciones no llegan en vivo

**Soluciones:**
1. Verifica que backend está corriendo en puerto 9000
2. Verifica `VITE_API_URL` en `.env`
3. Abre DevTools → Network → WS filter
4. Debería haber conexión a `/notificaciones/ws`

### "Permiso de notificaciones bloqueado"

**Problema:** No aparece popup de permiso

**Causas:**
- Usuario lo bloqueó antes
- Navegador tiene bloqueado

**Soluciones:**
1. Chrome: Icono 🔒 en barra de URL
2. Firefox: Preferences → Privacy → Permissions
3. Safari: Preferences → Websites → Notifications

---

## 📈 Próximas mejoras

1. **Persistencia:** Guardar notificaciones en localStorage
2. **Categorías:** Agrupar por tipo
3. **Filtros:** Mostrar solo no leídas
4. **Notificaciones de desktop:** Integrar Desktop API
5. **Email:** Enviar resumen por email
6. **Preferencias:** Notificaciones por rol

---

**✅ Sistema de notificaciones completamente integrado en frontend.** 🎉

Para usar: Simplemente importa `<NotificationCenter />` en tu navbar y está listo.

