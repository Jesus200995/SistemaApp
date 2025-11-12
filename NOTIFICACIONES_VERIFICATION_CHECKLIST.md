# ✅ Checklist de Verificación - Sistema de Notificaciones

## 🔍 Verificación Backend

### 1. Modelos
- [ ] `models.py` contiene `class Notificacion`
- [ ] Tabla: `notificaciones`
- [ ] Columnas: id, titulo, mensaje, tipo, rol_destino, leido, usuario_id, created_at
- [ ] Sin errores de Python

**Verificar:**
```bash
python -c "from models import Notificacion; print('✅ Modelo OK')"
```

### 2. Rutas de Notificaciones
- [ ] Archivo `routes/notificaciones.py` existe
- [ ] Contiene WebSocket endpoint
- [ ] Contiene 6 endpoints REST
- [ ] Sin errores de importación

**Verificar:**
```bash
python -c "from routes import notificaciones; print('✅ Rutas OK')"
```

### 3. Registro en main.py
- [ ] Import: `from routes import notificaciones`
- [ ] Include router: `app.include_router(notificaciones.router)`
- [ ] Sin errores de sintaxis

**Verificar:**
```bash
python -m uvicorn main:app --reload
# Deberías ver: Uvicorn running on http://127.0.0.1:9000
```

---

## 🔍 Verificación Frontend

### 1. Componente
- [ ] `src/components/NotificationCenter.vue` existe
- [ ] Contiene template, script setup, styles
- [ ] Importa useAuthStore
- [ ] Sin errores de TypeScript

**Verificar:**
```bash
npm run build 2>&1 | grep -i "error"
# No debería mostrar errores
```

### 2. Dependencias
- [ ] axios instalado
- [ ] vue@3 instalado

**Verificar:**
```bash
npm ls axios vue
```

---

## 🧪 Testing

### Test 1: Backend corriendo

```bash
curl http://localhost:9000/notificaciones/status/info
```

**Esperado:**
```json
{
  "clientes_conectados": 0,
  "status": "✅ Sistema de notificaciones funcionando correctamente"
}
```

### Test 2: WebSocket conectando

Abre DevTools (F12) → Network → WS filter

Abre app en http://localhost:5173

**Deberías ver:**
```
ws://localhost:9000/notificaciones/ws    101 Web Socket Protocol Handshake
```

### Test 3: Obtener token

```bash
curl -X POST http://localhost:9000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

**Esperado:**
```json
{
  "access_token": "eyJ0eXAi...",
  "token_type": "bearer"
}
```

### Test 4: Crear notificación

```bash
TOKEN="eyJ0eXAi..."

curl -X POST http://localhost:9000/notificaciones/crear \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Test Notification",
    "mensaje": "Esta es una prueba",
    "tipo": "success",
    "rol_destino": "all"
  }'
```

**Esperado:**
```json
{
  "success": true,
  "notificacion_id": 1,
  "mensaje": "Notificación creada y enviada"
}
```

### Test 5: Verificar en frontend

Abre http://localhost:5173 en navegador

**Deberías ver:**
- 🔔 Icono de notificación en navbar
- Badge rojo con número "1"
- Al hacer clic, se abre panel
- Panel muestra notificación con:
  - ✅ Icono verde (success)
  - Título: "Test Notification"
  - Mensaje: "Esta es una prueba"
  - Timestamp: "Justo ahora"

---

## 📋 Estructura de carpetas

```
Backend/
├── routes/
│   ├── auth.py
│   ├── chat.py
│   ├── layers.py
│   ├── notificaciones.py ✅ NEW
│   └── users.py
├── models.py ✅ UPDATED (+ Notificacion)
├── main.py ✅ UPDATED (+ notificaciones import)
├── database.py
├── NOTIFICACIONES_DOCS.md ✅ NEW
└── ...

Frontend/
├── src/
│   ├── components/
│   │   └── NotificationCenter.vue ✅ NEW
│   ├── views/
│   ├── router/
│   └── ...
├── NOTIFICACIONES_FRONTEND_GUIDE.md ✅ NEW
└── ...

Root/
└── SISTEMA_NOTIFICACIONES_SUMMARY.md ✅ NEW
```

---

## 🔐 Verificar Seguridad

### JWT requerido en endpoints

```bash
# Sin token (debería fallar)
curl -X POST http://localhost:9000/notificaciones/crear \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Test"}'

# Esperado: 403 Forbidden o 401 Unauthorized
```

### CORS configurado

```bash
# Desde frontend
fetch('http://localhost:9000/notificaciones/')
# No debería tener error de CORS
```

---

## 🎯 Integración en App.vue

- [ ] Importar `NotificationCenter` en App.vue
- [ ] Agregar `<NotificationCenter />` en navbar
- [ ] Probar en navegador

**Verificar:**
```vue
<template>
  <nav>
    <NotificationCenter />
  </nav>
</template>

<script setup>
import NotificationCenter from './components/NotificationCenter.vue'
</script>
```

---

## 📊 Logs esperados

### Backend (uvicorn)
```
INFO:     Uvicorn running on http://127.0.0.1:9000
INFO:     Application startup complete
```

### Frontend (vite)
```
✅ Conectado a notificaciones en tiempo real
🔔 Nueva notificación: Test Notification
```

### Console (DevTools)
```
✅ Conectado a notificaciones en tiempo real
📤 Mensaje enviado
← Mensaje recibido
```

---

## ✨ Funcionalidades a verificar

- [ ] WebSocket conecta automáticamente
- [ ] Badge se actualiza con contador
- [ ] Panel abre/cierra con clic
- [ ] Notificación muestra tipo correcto
- [ ] Timestamp es relativo (Hace 1m, etc)
- [ ] Marcar como leída funciona
- [ ] Eliminar notificación funciona
- [ ] Notificación del sistema aparece (si permitido)

---

## 🐛 Troubleshooting

Si algo no funciona:

### Backend error: "No module named 'notificaciones'"
```bash
# Verificar que archivo existe
ls -la routes/notificaciones.py

# Reinstalar dependencias
pip install -r requirements.txt
```

### Frontend error: "Cannot find module NotificationCenter"
```bash
# Verificar path
ls -la src/components/NotificationCenter.vue

# Npm install
npm install
```

### WebSocket connection refused
```bash
# Verificar que backend está corriendo
curl http://localhost:9000/

# Verificar puerto
lsof -i :9000
```

### JWT token inválido
```bash
# Verificar SECRET_KEY en .env
cat .env | grep JWT_SECRET

# Generar nuevo token
curl -X POST http://localhost:9000/auth/login ...
```

---

## ✅ Checklist final

- [ ] Backend: Modelos, rutas, main.py
- [ ] Frontend: Componente, documentación
- [ ] Testing: WebSocket, REST, JWT
- [ ] Integración: NotificationCenter en App.vue
- [ ] Documentación: 3 archivos (backend, frontend, summary)
- [ ] Sin errores de Python/TypeScript
- [ ] Logs correctos en console

---

**Si todo está ✅, el sistema está listo para producción.** 🚀

