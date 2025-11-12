# 💬 Chat en Tiempo Real - Guía de Integración

## ✅ Verificación rápida

### Backend - Pasos completados:

✅ **Dependencias instaladas:**
```bash
pip install broadcaster[postgresql] python-socketio
```

✅ **Archivo creado:** `routes/chat.py`
- WebSocket endpoint: `/chat/ws`
- Gestión de conexiones: `connect_user()`, `disconnect_user()`
- Broadcasting: `broadcast_message()`
- Endpoint de estado: `/chat/status`

✅ **Registro en main.py:**
```python
from routes import auth, layers, chat
app.include_router(chat.router)
```

---

## 🎨 Frontend - Integración completada

✅ **Vista creada:** `src/views/ChatView.vue`
- Header con estado de conexión
- Contenedor de mensajes scrollable
- Input con validación
- Indicador de escritura
- Estilos responsivos y modernos

✅ **Ruta registrada en router:**
```typescript
{
  path: '/chat',
  name: 'chat',
  component: () => import('../views/ChatView.vue'),
  meta: { requiresAuth: true },
}
```

---

## 🚀 Cómo probar localmente

### 1. **Iniciar el backend**

```bash
cd BackendFastAPI
source venv/bin/activate  # Linux/Mac
# o en Windows: venv\Scripts\activate

python -m uvicorn main:app --reload --port 9000
```

**Esperado:**
```
INFO:     Uvicorn running on http://127.0.0.1:9000
✅ API corriendo correctamente
```

### 2. **Iniciar el frontend**

En otra terminal:

```bash
cd Frontend/sistemaapp-frontend
npm run dev
```

**Esperado:**
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:5173/
```

### 3. **Abrir la aplicación**

1. Abre `http://localhost:5173` en el navegador
2. Haz login
3. Navega a `/chat` (URL o menú)

### 4. **Probar WebSocket**

**Abre 2 pestañas diferentes:**

**Pestaña 1:**
- URL: `http://localhost:5173/chat`
- Usuario 1: Login como "usuario1"

**Pestaña 2:**
- URL: `http://localhost:5173/chat`
- Usuario 2: Login como "usuario2" (en navegador diferente o incógnito)

**Prueba:**
1. En pestaña 1, escribe: "Hola desde usuario 1"
2. Presiona Enter
3. **Ambas pestañas recibirán el mensaje** ✅
4. En pestaña 2, responde
5. Ambas ven la respuesta ✅

---

## 📊 Verificar en DevTools

### 1. **Conexión WebSocket**

Abre DevTools (F12) → Network tab

Busca request con tipo **websocket**:
```
wss://localhost:9000/chat/ws
```

**Estado:** `101 Web Socket Protocol Handshake` ✅

### 2. **Mensajes en WebSocket**

En DevTools → Network → Clic en WebSocket → Messages tab

**Deberías ver:**
```
► {"type": "message", "sender": "Usuario1", "text": "Hola", "time": "14:32"}
← {"type": "message", "sender": "Usuario1", "text": "Hola", "time": "14:32"}
```

### 3. **Console logs**

```
✅ Conectado al chat en tiempo real
📤 Mensaje enviado
← Mensaje recibido
🔴 Desconectado del chat (al cerrar)
```

---

## 🔧 Configuración por entorno

### Desarrollo (localhost)

**Frontend .env:**
```env
VITE_API_URL=http://localhost:9000
```

**ChatView.vue detecta automáticamente:**
```javascript
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
// ws://localhost:9000/chat/ws
```

### Producción (VPS)

**Frontend .env:**
```env
VITE_API_URL=https://sistemaapi.sembrandodatos.com
```

**ChatView.vue usa:**
```javascript
// wss://sistemaapi.sembrandodatos.com/chat/ws
```

---

## 📝 Características implementadas

| Característica | Estado | Descripción |
|---|---|---|
| WebSocket endpoint | ✅ | `/chat/ws` en puerto 9000 |
| Broadcasting | ✅ | Mensajes a todos los clientes |
| Gestión de conexiones | ✅ | Connect/disconnect automático |
| Reconexión | ✅ | Se intenta reconectar automáticamente |
| Indicador de estado | ✅ | Muestra conectado/desconectado |
| Hora del mensaje | ✅ | Timestamp automático |
| Indicador de escritura | ✅ | Muestra quién está escribiendo |
| Mensajes propios/ajenos | ✅ | Diferente estilo visual |
| Scroll automático | ✅ | Auto-scroll al llegar nuevo mensaje |
| Responsive design | ✅ | Funciona en móvil/tablet |

---

## 🎯 Estructura de mensajes

### Mensaje de chat:
```json
{
  "type": "message",
  "sender": "Juan Pérez",
  "text": "Hola equipo, ¿cómo están?",
  "time": "14:32:15"
}
```

### Indicador de escritura:
```json
{
  "type": "typing",
  "sender": "María García"
}
```

---

## 🔒 Seguridad

### Autenticación:
- ✅ Solo usuarios logueados pueden acceder a `/chat`
- ✅ Meta `requiresAuth: true` en router
- ✅ Redirige a login si no hay token

### WebSocket:
- ✅ Se conecta desde usuario autenticado
- ✅ Nombre se obtiene de `auth.user.nombre`
- ✅ Validación en frontend antes de enviar

---

## 🐛 Troubleshooting

### "No puedo conectar al chat"

**Problema:** `WebSocket connection failed`

**Soluciones:**
1. Verifica que backend está corriendo (puerto 9000)
2. Verifica que VITE_API_URL es correcto
3. Abre DevTools → Network → busca WebSocket
4. Mira el estado de conexión (debe ser 101)

### "No veo los mensajes del otro usuario"

**Problema:** Solo veo mis propios mensajes

**Soluciones:**
1. Abre 2 pestañas diferentes (o incógnito)
2. Verifica que ambos están logueados
3. Verifica que ambos en `/chat`
4. Abre DevTools → Console en ambas pestañas
5. Debería haber logs de conexión exitosa

### "El chat desconecta constantemente"

**Problema:** Conexión inestable

**Causas:**
- Backend reiniciando
- Problema de red
- Proxy/firewall bloqueando WebSocket

**Soluciones:**
1. Verifica logs del backend
2. Aumenta timeout en proxy (si aplica)
3. Usa `wss://` en producción (WebSocket Secure)

---

## 📈 Monitoreo en producción

### Ver conexiones activas:

En el backend, endpoint:
```bash
GET https://sistemaapi.sembrandodatos.com/chat/status
```

**Response:**
```json
{
  "connected_users": 5,
  "status": "✅ Chat funcionando correctamente"
}
```

### Logs del backend:

```bash
uvicorn main:app --log-level debug
```

**Deberías ver:**
```
✅ Cliente conectado. Total: 1
✅ Cliente conectado. Total: 2
📤 Mensaje enviado: "Hola"
🔴 Cliente desconectado. Total: 1
```

---

## 🚀 Próximos pasos (opcional)

1. **Persistencia de mensajes:**
   - Guardar en PostgreSQL
   - Cargar historial al conectar

2. **Notificaciones:**
   - Push notification cuando nuevo mensaje
   - Sound alert (configurable)

3. **Salas de chat:**
   - Chat por equipo/proyecto
   - Canales temáticos

4. **Emojis y rich text:**
   - Soporte para emojis
   - Markdown básico
   - Menciones @usuario

5. **Archivos:**
   - Compartir archivos en chat
   - Imágenes inline

---

**✅ Chat en tiempo real completamente integrado.** 🎉

Ahora puedes hacer clic en el menú "Chat" o navegar a `/chat` para probar la funcionalidad en tiempo real.
