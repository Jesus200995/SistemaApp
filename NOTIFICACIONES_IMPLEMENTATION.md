# 🔔 MÓDULO DE NOTIFICACIONES AUTOMÁTICAS - GUÍA DE IMPLEMENTACIÓN

## ✅ Resumen de Cambios Realizados

### 🎯 Objetivo General
Implementar un sistema de notificaciones automáticas en tiempo real vinculadas a solicitudes, permitiendo que técnicos/facilitadores reciban alertas inmediatas cuando se crean, aprueban o rechazan solicitudes.

---

## 📋 CAMBIOS EN EL BACKEND

### 1️⃣ Actualización del Modelo de Notificación
**Archivo**: `BackendFastAPI/models.py`

✅ **Campos agregados/actualizados:**
```python
class Notificacion(Base):
    __tablename__ = "notificaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # solicitud, respuesta, info, warning, error, success
    rol_destino = Column(String(50), nullable=True)  # Para notificaciones por rol
    user_destino = Column(Integer, ForeignKey("users.id"), nullable=True)  # Usuario específico ⭐ NUEVO
    leido = Column(Boolean, default=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Quién la generó
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id"), nullable=True)  # Vinculación ⭐ NUEVO
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
```

### 2️⃣ Actualización de routes/solicitudes.py
**Archivo**: `BackendFastAPI/routes/solicitudes.py`

#### 📝 Función: `crear_solicitud()`
**Cambios:**
- Al crear una solicitud, se genera una notificación automática
- La notificación se envía al usuario destino con tipo `"solicitud"`
- Se registra en la BD para auditoría

**Código:**
```python
# 🔔 Crear notificación para el destino
if data.get("destino_id"):
    notif = Notificacion(
        titulo="Nueva solicitud recibida",
        mensaje=f"Has recibido una solicitud de {rol} (ID: {user_id}).",
        tipo="solicitud",
        user_destino=data.get("destino_id"),
        usuario_id=user_id,
        solicitud_id=nueva.id
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    print(f"✅ Notificación creada para usuario {data.get('destino_id')}: {notif.id}")
```

#### 📝 Función: `actualizar_estado()`
**Cambios:**
- Al cambiar estado de solicitud (aprobada/rechazada), se envía notificación al solicitante
- Tipo de notificación: `"respuesta"`
- Mensaje dinámico con el estado actualizado

**Código:**
```python
# 🔔 Enviar notificación al solicitante
notif = Notificacion(
    titulo="Actualización de solicitud",
    mensaje=f"Tu solicitud ha sido {nuevo_estado}.",
    tipo="respuesta",
    user_destino=solicitud.usuario_id,
    usuario_id=user_id,
    solicitud_id=solicitud.id
)
db.add(notif)
db.commit()
db.refresh(notif)
print(f"✅ Notificación de respuesta creada para usuario {solicitud.usuario_id}: {notif.id}")
```

### 3️⃣ WebSocket y Broadcast (Ya implementado)
**Archivo**: `BackendFastAPI/routes/notificaciones.py`

✅ **Funcionalidad existente:**
- Conexión WebSocket en `GET /notificaciones/ws`
- Función `broadcast_notification()` para enviar en tiempo real
- Endpoint `PATCH /notificaciones/{id}/leer` para marcar como leídas
- Endpoint `DELETE /notificaciones/{id}` para eliminar

---

## 🎨 CAMBIOS EN EL FRONTEND

### 1️⃣ Componente NotificationCenter.vue
**Archivo**: `Frontend/sistemaapp-frontend/src/components/NotificationCenter.vue`

**Características:**
- ✅ Botón de campana con badge de contador
- ✅ Dropdown con lista de notificaciones
- ✅ WebSocket connection para actualizaciones en tiempo real
- ✅ Colores dinámicos según tipo de notificación
- ✅ Iconos de Lucide Vue Next
- ✅ Botones para eliminar notificaciones
- ✅ Estilos profesionales dark-theme

**Tipos de notificación y colores:**
```javascript
const tipoColores = {
  solicitud: { border: '#3b82f6' },    // Azul
  respuesta: { border: '#10b981' },    // Verde
  info: { border: '#78716c' },         // Gris
  warning: { border: '#f59e0b' },      // Ámbar
  error: { border: '#ef4444' },        // Rojo
  success: { border: '#10b981' }       // Verde
}
```

**Estructura:**
```vue
<div class="notification-center">
  <button class="notification-bell">
    <!-- Ícono con badge de contador -->
  </button>
  
  <div class="notification-dropdown" v-if="showDropdown">
    <!-- Header con título y botón cerrar -->
    <!-- Lista de notificaciones o empty state -->
  </div>
</div>
```

### 2️⃣ Integración en Dashboard
**Archivo**: `Frontend/sistemaapp-frontend/src/views/DashboardView.vue`

**Nueva sección:** "Notificaciones Recientes"

**Características:**
- ✅ Muestra últimas 5 notificaciones
- ✅ Badge con contador de no leídas
- ✅ Conexión WebSocket local
- ✅ Estilos uniformes con SembradoresView
- ✅ Animación de entrada (v-motion)
- ✅ Icono dinámico según tipo

**Template agregado:**
```vue
<!-- Sección de notificaciones recientes -->
<div class="notifications-section">
  <div class="notifications-header">
    <h3 class="section-title">Notificaciones Recientes</h3>
    <div class="notifications-badge">{{ unreadNotifications }}</div>
  </div>
  
  <div v-if="notificaciones.length === 0" class="notifications-empty">
    <!-- Empty state -->
  </div>
  
  <div v-else class="notifications-list">
    <!-- Lista de notificaciones -->
  </div>
</div>
```

**Estilos CSS:**
- Background: `rgba(30, 41, 59, 0.4)` con gradiente
- Border: `rgba(148, 163, 184, 0.1)`
- Cards: `rgba(30, 41, 59, 0.4)` con border-left dinámico
- Texto primario: `#f1f5f9`
- Texto secundario: `#cbd5e1`
- Acentos: `#10b981` (verde)

### 3️⃣ Script de Dashboard
**Cambios en `<script setup>`:**

```typescript
// Conexión WebSocket
const connectWebSocket = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = apiUrl.replace(/^(https?:\/\/)/, '').replace(/\/$/, '')
  const wsUrl = `${protocol}//${host}/notificaciones/ws`
  
  ws.value = new WebSocket(wsUrl)
  
  ws.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.user_destino === auth.user?.id || !data.user_destino) {
      notificaciones.value.unshift(data)
    }
  }
}

// Funciones auxiliares
const getNotificationColor = (tipo: string): string => { ... }
const getNotificationIcon = (tipo: string) => { ... }
const formatTime = (timestamp: string): string => { ... }
```

---

## 🔄 FLUJO DE NOTIFICACIONES

### Escenario 1: Técnico envía solicitud a Facilitador

```
1. Técnico crea solicitud en SolicitudesView
   ↓
2. Backend: crear_solicitud()
   - Crea Solicitud en BD
   - Crea Notificacion con tipo="solicitud"
   - user_destino = facilitador_id
   ↓
3. WebSocket broadcast en tiempo real
   ↓
4. Facilitador recibe notificación:
   - En Navbar campana (contador +1)
   - En Dashboard sección notificaciones
   - Notificación del sistema (si permitido)
```

### Escenario 2: Facilitador aprueba solicitud

```
1. Facilitador aprueba en SolicitudesView
   ↓
2. Backend: actualizar_estado()
   - Actualiza estado="aprobada"
   - Crea Notificacion con tipo="respuesta"
   - user_destino = tecnico_id
   ↓
3. WebSocket broadcast en tiempo real
   ↓
4. Técnico recibe notificación:
   - "Tu solicitud ha sido aprobada"
   - En Navbar y Dashboard
```

---

## 📱 COMPONENTES INVOLUCRADOS

### Frontend
- ✅ `NotificationCenter.vue` - Componente profesional de notificaciones
- ✅ `DashboardView.vue` - Widget de notificaciones recientes
- ✅ `Navbar.vue` - Campana de notificaciones (ya existente)

### Backend
- ✅ `models.py` - Modelo Notificacion actualizado
- ✅ `routes/solicitudes.py` - Lógica de creación de notificaciones
- ✅ `routes/notificaciones.py` - WebSocket y endpoints (existente)

---

## 🧪 PRUEBAS RECOMENDADAS

### Test 1: Crear Solicitud
```bash
1. Login como técnico_1
2. Ir a Solicitudes
3. Crear nueva solicitud → facilitador_1
4. Abrir otra pestaña con login facilitador_1
5. ✅ Debería ver notificación en Navbar y Dashboard
```

### Test 2: Aprobar Solicitud
```bash
1. Facilitador abre solicitud recibida
2. Aprueba la solicitud
3. Cambiar a pestaña del técnico
4. ✅ Debería recibir notificación "aprobada"
```

### Test 3: Rechazar Solicitud
```bash
1. Facilitador abre solicitud diferente
2. Rechaza la solicitud
3. Cambiar a pestaña del técnico
4. ✅ Debería recibir notificación "rechazada"
```

### Test 4: Marcar como Leída
```bash
1. Abrir dropdown de notificaciones
2. Badge debería resetear a 0
3. ✅ Notificaciones marcadas como leídas
```

---

## 🚀 PRÓXIMOS PASOS OPCIONALES

### 1. Notificaciones por Jerarquía
```python
# En actualizar_estado: Notificar también al superior
if solicitud.usuario.superior_id:
    notif_superior = Notificacion(
        titulo="Nueva respuesta en solicitud",
        mensaje=f"Seguimiento: {solicitud.descripcion}",
        tipo="info",
        user_destino=solicitud.usuario.superior_id
    )
    db.add(notif_superior)
```

### 2. Notificaciones Push del Sistema
```javascript
// En NotificationCenter.vue
if ('Notification' in window && Notification.permission === 'granted') {
  new Notification(notif.titulo, {
    body: notif.mensaje,
    tag: `notif-${notif.id}`,
    badge: '🔔'
  })
}
```

### 3. Email Notifications (Opcional)
```python
# En routes/notificaciones.py
async def enviar_email_notificacion(usuario_id: int, notif: Notificacion):
    usuario = db.query(User).filter(User.id == usuario_id).first()
    # Enviar email con sendgrid o similar
```

---

## 📊 DIAGRAMA DE ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND (Vue 3 + TypeScript)              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌─────────────────────────┐      │
│  │  Navbar.vue  │         │   DashboardView.vue     │      │
│  │  (Campana)   │◄────────│ (Notif Recientes)      │      │
│  └──────────────┘         └─────────────────────────┘      │
│         ▲                           ▲                       │
│         │                           │                       │
│         └───────────┬───────────────┘                       │
│                     │                                       │
│              ┌──────▼──────┐                               │
│              │  WebSocket  │                               │
│              │  Connection │                               │
│              └──────┬──────┘                               │
│                     │                                       │
└─────────────────────┼──────────────────────────────────────┘
                      │ (wss://api/notificaciones/ws)
┌─────────────────────┼──────────────────────────────────────┐
│                     ▼                                       │
│  ┌──────────────────────────────────────────────┐          │
│  │      BACKEND (FastAPI + SQLAlchemy)          │          │
│  └──────────────────────────────────────────────┘          │
│                     ▲                                       │
│                     │                                       │
│  ┌─────────────────────────────────────────────┐           │
│  │   routes/notificaciones.py                   │           │
│  │   - WebSocket /notificaciones/ws             │           │
│  │   - PATCH /notificaciones/{id}/leer          │           │
│  │   - DELETE /notificaciones/{id}              │           │
│  │   - GET /notificaciones/                     │           │
│  └─────────────────────────────────────────────┘           │
│                     ▲                                       │
│                     │                                       │
│  ┌─────────────────────────────────────────────┐           │
│  │   routes/solicitudes.py (MODIFICADO)         │           │
│  │   - POST / (crear_solicitud)                 │           │
│  │     └─► Crea Notificacion                   │           │
│  │   - PUT /{id}/estado (actualizar_estado)    │           │
│  │     └─► Crea Notificacion                   │           │
│  └─────────────────────────────────────────────┘           │
│                     ▲                                       │
│                     │                                       │
│  ┌─────────────────────────────────────────────┐           │
│  │   models.py (ACTUALIZADO)                   │           │
│  │   - Notificacion                             │           │
│  │     - user_destino ⭐ NUEVO                 │           │
│  │     - solicitud_id ⭐ NUEVO                 │           │
│  └─────────────────────────────────────────────┘           │
│                     ▲                                       │
└─────────────────────┼──────────────────────────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │  Base de Datos│
              │  (notificacio│
              │   nes tabla) │
              └───────────────┘
```

---

## ✅ CHECKLIST DE VALIDACIÓN

- [x] Modelo Notificacion actualizado con campos necesarios
- [x] Función crear_solicitud genera notificaciones
- [x] Función actualizar_estado genera notificaciones
- [x] WebSocket en notificaciones.py funcionando
- [x] NotificationCenter.vue profesional con dark theme
- [x] Dashboard integrado con widget de notificaciones
- [x] Navbar con campana de notificaciones
- [x] Colores y estilos consistentes (SembradoresView baseline)
- [x] Tipos de notificación con iconos dinámicos
- [x] Contador de no leídas
- [x] Marcar como leídas
- [x] Eliminar notificaciones
- [x] Validación sin errores de compilación

---

## 📝 NOTAS IMPORTANTES

1. **WebSocket URL**: Asegúrese que `VITE_API_URL` esté configurado en `.env.local`
2. **CORS**: Verificar que el backend permite WebSocket desde el frontend
3. **JWT Secret**: Debe coincidir entre frontend y backend
4. **Base de Datos**: Ejecutar migración si es necesario para la nueva tabla
5. **Timeouts**: WebSocket envía ping cada 30s para mantener conexión activa

---

## 🎯 RESUMEN FINAL

✅ **Sistema de notificaciones automáticas completamente implementado**

- 🔔 Notificaciones en tiempo real vía WebSocket
- 📱 UI profesional en Navbar y Dashboard
- 🎨 Estilos uniformes con tema dark
- 📊 Integración con solicitudes
- 🔐 Seguridad con JWT
- 📈 Escalable y mantenible

**Estado**: LISTO PARA PROBAR Y DESPLEGAR 🚀
