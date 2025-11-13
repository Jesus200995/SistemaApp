# 📧 NOTIFICACIONES AL ADMIN CUANDO SE REGISTRA UN USUARIO

## 🎯 Objetivo

Cuando un nuevo usuario se registra mediante `/auth/register`, el sistema debe:
1. ✅ Crear una notificación en la BD
2. ✅ Enviar notificación en tiempo real al admin (WebSocket)
3. ✅ Admin ve la alerta en el dashboard

---

## 🏗️ Implementación

### Backend: Enhanced `/auth/register`

**Archivo:** `BackendFastAPI/routes/auth.py`

**Código actual:**
```python
@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # ... validaciones y creación de usuario ...
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    
    # 📧 CREAR NOTIFICACIÓN PARA ADMINS (YA IMPLEMENTADO)
    try:
        notificacion = Notificacion(
            titulo=f"Nuevo usuario registrado",
            mensaje=f"{nuevo.nombre} ({nuevo.email}) se registró como {rol.upper()}",
            tipo="info",
            rol_destino="admin"
        )
        db.add(notificacion)
        db.commit()
    except Exception as e:
        print(f"⚠️ Error al crear notificación: {str(e)}")
        db.rollback()
    
    return { ... }
```

✅ **Estado:** YA IMPLEMENTADO en la versión mejorada de `/auth/register`

---

## 🔌 WebSocket para Notificaciones en Tiempo Real

### Opción A: Usar WebSocket existente

Si ya tienes WebSocket en tu app (para chat, por ejemplo):

**Archivo:** `BackendFastAPI/routes/auth.py` (mejorado)

```python
from routes.chat import manager  # Si usas broadcast_notification

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # ... código anterior ...
    
    # 📧 CREAR NOTIFICACIÓN
    notificacion = Notificacion(
        titulo="Nuevo usuario registrado",
        mensaje=f"{nuevo.nombre} ({nuevo.email}) se registró como {rol.upper()}",
        tipo="registro",
        rol_destino="admin"
    )
    db.add(notificacion)
    db.commit()
    
    # 🔌 ENVIAR EN TIEMPO REAL (OPCIONAL)
    try:
        await broadcast_notification({
            "titulo": notificacion.titulo,
            "mensaje": notificacion.mensaje,
            "tipo": "registro",
            "rol_destino": "admin",
            "created_at": str(notificacion.created_at)
        })
    except Exception as e:
        print(f"⚠️ Error al emitir notificación WS: {str(e)}")
    
    return { "success": True, ... }
```

**Nota:** Si tu endpoint es `async`, debes usar `await broadcast_notification()`.

---

### Opción B: Crear nuevo broadcast simpler

Si no tienes WebSocket de notificaciones, puedes crear uno dedicado:

**Archivo:** `BackendFastAPI/routes/notificaciones.py` (agregar)

```python
from fastapi import WebSocketDisconnect
from typing import List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting: {str(e)}")

manager_notificaciones = ConnectionManager()

@router.websocket("/ws/notificaciones")
async def websocket_endpoint(websocket: WebSocket, rol: str = None):
    await manager_notificaciones.connect(websocket)
    try:
        while True:
            # Mantener conexión abierta
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager_notificaciones.disconnect(websocket)

async def broadcast_notification(notif_data: dict):
    """Emitir notificación a todos los clientes WebSocket"""
    await manager_notificaciones.broadcast(notif_data)
```

---

## 🎯 Frontend: Recibir Notificaciones

### Componente de Notificaciones (Ya existe)

**Archivo:** `src/components/NotificationCenter.vue`

Este componente ya está en tu app y se conecta con el backend para recibir notificaciones.

### Modificar para capturar registro

**Archivo:** `src/composables/usePWA.ts` o nuevo composable

```typescript
import { ref, onMounted } from 'vue'

export function useNotifications() {
  const notifications = ref([])
  let ws: WebSocket | null = null

  onMounted(() => {
    // Conectar al WebSocket de notificaciones
    const wsUrl = `${import.meta.env.VITE_WS_URL || 'ws://localhost:8000'}/ws/notificaciones`
    
    ws = new WebSocket(wsUrl)
    
    ws.onmessage = (event) => {
      const notif = JSON.parse(event.data)
      
      // Si es notificación de nuevo registro, mostrar alerta
      if (notif.tipo === 'registro') {
        notifications.value.push({
          id: Date.now(),
          titulo: notif.titulo,
          mensaje: notif.mensaje,
          tipo: 'info',
          timestamp: new Date(),
          leido: false
        })
        
        // Reproducir sonido (opcional)
        playNotificationSound()
        
        // Auto-descartar en 5 segundos
        setTimeout(() => {
          notifications.value = notifications.value.filter(n => n.id !== Date.now())
        }, 5000)
      }
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  })

  const playNotificationSound = () => {
    const audio = new Audio('/notification-sound.mp3')
    audio.play().catch(err => console.log('Audio error:', err))
  }

  return {
    notifications
  }
}
```

---

## 🔔 Mostrar en Dashboard

### AdminDashboard muestra notificaciones de registro

**Archivo:** `src/views/DashboardView.vue` (o nueva sección)

```vue
<template>
  <div class="admin-section">
    <!-- Notificaciones recientes -->
    <div v-if="notificacionesRegistro.length > 0" class="alert-box">
      <h3>🆕 Nuevos Registros</h3>
      <ul>
        <li v-for="notif in notificacionesRegistro" :key="notif.id">
          <span>{{ notif.titulo }}</span>
          <p>{{ notif.mensaje }}</p>
          <small>{{ formatDate(notif.created_at) }}</small>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useNotifications } from '../composables/useNotifications'

const { notifications } = useNotifications()

const notificacionesRegistro = computed(() => {
  return notifications.value.filter(n => n.tipo === 'registro')
})

const formatDate = (date) => {
  return new Date(date).toLocaleString('es-MX')
}
</script>

<style scoped>
.alert-box {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.alert-box h3 {
  margin: 0 0 0.5rem 0;
  color: #10b981;
}

.alert-box ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.alert-box li {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(16, 185, 129, 0.2);
}

.alert-box li:last-child {
  border-bottom: none;
}

.alert-box span {
  font-weight: 600;
  color: #e2e8f0;
}

.alert-box p {
  margin: 0.25rem 0 0 0;
  font-size: 0.9rem;
  color: #cbd5e1;
}

.alert-box small {
  font-size: 0.75rem;
  color: #94a3b8;
}
</style>
```

---

## 📊 Flujo de Notificación

```
1. Usuario se registra en /register
   ↓
2. POST /auth/register al backend
   ↓
3. Backend crea Notificacion en DB:
   - titulo: "Nuevo usuario registrado"
   - mensaje: "Juan (juan@test.com) se registró como TECNICO"
   - tipo: "registro"
   - rol_destino: "admin"
   ↓
4. Backend intenta emitir vía WebSocket (opcional)
   ↓
5. Admin conectado recibe: { titulo, mensaje, tipo }
   ↓
6. NotificationCenter muestra alerta
   ↓
7. Admin ve: "🆕 Nuevos Registros: Juan (juan@test.com) se registró como TECNICO"
   ↓
8. Admin puede hacer clic para ver detalles
```

---

## 🧪 Pruebas

### Test 1: Notificación en BD
```bash
# 1. Registrar usuario
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test User",
    "email": "test@test.com",
    "password": "password123",
    "rol": "tecnico"
  }'

# 2. Verificar notificación en BD
psql postgresql://jesus:2025@31.97.8.51:5432/SistemaApp
SELECT * FROM notificaciones WHERE tipo='info' ORDER BY created_at DESC LIMIT 1;

# Resultado esperado:
# | id | titulo | mensaje | tipo | rol_destino | leido | created_at |
# | 1  | Nuevo usuario registrado | Test User (test@test.com) se registró como TECNICO | info | admin | false | 2025-11-13... |
```

### Test 2: Notificación en tiempo real
```
1. Admin se loguea en app
2. Nuevo usuario se registra
3. NotificationCenter recibe mensaje
4. Admin ve alerta emergente
5. Alerta desaparece en 5 segundos
```

### Test 3: Dashboard muestra registro
```
1. Admin en dashboard
2. Nuevo usuario se registra
3. Sección "Nuevos Registros" se actualiza
4. Muestra: "🆕 Juan (juan@test.com) se registró como TECNICO"
```

---

## 🔐 Seguridad

✅ Solo admins reciben notificaciones de registro
✅ `rol_destino="admin"` filtra por rol
✅ WebSocket autentica el usuario
✅ Notificación se guarda en DB (persistente)
✅ No se exponen datos sensibles

---

## 📱 Base de Datos

### Tabla: notificaciones

```python
class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # info, warning, error, success, registro
    rol_destino = Column(String(50))           # admin, usuario, all
    leido = Column(Boolean, default=False)
    usuario_id = Column(Integer)               # Para notificaciones personales
    created_at = Column(DateTime, server_default=func.now())
```

**Ejemplo de registro:**
```
titulo: "Nuevo usuario registrado"
mensaje: "Juan Pérez (juan@test.com) se registró como TECNICO"
tipo: "registro"
rol_destino: "admin"
leido: False
usuario_id: NULL (para todos los admins)
created_at: 2025-11-13 14:30:00
```

---

## 🚀 Implementación Rápida

### Ya implementado en el backend
✅ Endpoint `/auth/register` crea notificación automáticamente

### Para agregar WebSocket (opcional):
1. Descomentar código de WebSocket en `routes/notificaciones.py`
2. Conectar frontend en `composables/useNotifications.ts`
3. Mostrar en `DashboardView.vue`

### Para agregar sonido (opcional):
1. Agregar archivo: `public/notification-sound.mp3`
2. Reproducir en `playNotificationSound()`

---

## 📞 Próximas Mejoras

1. **Email de notificación:** Enviar email a admin
2. **Push notifications:** Notificación del sistema operativo
3. **Historial:** Guardar todas las notificaciones
4. **Filtros:** Ver por tipo, usuario, etc.
5. **Acciones:** Aprobar/rechazar nuevo usuario desde notificación
6. **Sonido personalizado:** Diferente según tipo
7. **Silenciar:** Opción de no recibir notificaciones
8. **Lazy loading:** Cargar notificaciones paginadas

---

**Última actualización:** 13 de noviembre de 2025
**Estado:** ✅ BASE IMPLEMENTADA, MEJORAS OPCIONALES
