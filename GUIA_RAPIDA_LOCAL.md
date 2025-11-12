# 🎯 GUÍA RÁPIDA - Hacer Funcionar Sistema Localmente

## ⚡ En 5 Minutos - Inicia Todo

### Paso 1: Preparar Base de Datos

```bash
# Crear base de datos PostgreSQL (si no existe)
# Option A: Si tienes PostgreSQL local
psql -U postgres -c "CREATE DATABASE sistema;"

# Option B: Si usas la VPS (31.97.8.51:5432)
# Ya debe estar creada - solo verifica conexión:
psql -h 31.97.8.51 -U admin -d sistema -c "SELECT 1"
```

### Paso 2: Configurar Backend

```bash
# 1. Navega al Backend
cd c:\Users\Admin_1\Music\SISTEMA\SistemaApp\Backend

# 2. Crea/activa entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instala dependencias
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose bcrypt python-multipart python-dotenv broadcaster python-socketio

# 4. Crea .env en Backend/
cat > .env << 'EOF'
DATABASE_URL=postgresql://admin:password@31.97.8.51:5432/sistema
JWT_SECRET=tu_secreto_jwt_seguro_aqui_123456
ENVIRONMENT=development
DEBUG=True
EOF

# 5. Inicia servidor
uvicorn main:app --reload --port 9000
```

✅ Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:9000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Paso 3: Configurar Frontend

```bash
# 1. Navega a Frontend
cd Frontend\sistemaapp-frontend

# 2. Instala dependencias
npm install

# 3. Crea .env en Frontend/sistemaapp-frontend/
cat > .env.local << 'EOF'
VITE_API_URL=http://localhost:9000
EOF

# 4. Inicia dev server
npm run dev
```

✅ Deberías ver:
```
  VITE v4.x.x  dev server running at:
  ➜  Local:   http://localhost:5173/
```

---

## 🌐 Paso 4: Acceder a la Aplicación

1. **Abrir navegador** → `http://localhost:5173`

2. **Si es primera vez:**
   - Ir a Login
   - O registrarse si hay ruta de signup
   - Usar credenciales de prueba

3. **Deberías ver:**
   - ✅ Navbar en la parte superior con:
     - Logo "🌱 SistemaApp"
     - Links (Home, Mapa, Chat, etc.)
     - Ícono de campana 🔔
     - Tu nombre de usuario
     - Botón "Logout"

---

## 🧪 Paso 5: Probar Notificaciones

### Opción A: Usando PowerShell

```powershell
# 1. Obtén un token válido del backend
$loginResponse = Invoke-WebRequest -Uri "http://localhost:9000/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"email":"admin@sistema.com","password":"password"}'

$token = ($loginResponse.Content | ConvertFrom-Json).access_token

# 2. Envía una notificación de prueba
$headers = @{"Authorization" = "Bearer $token"}
$body = @{
    "titulo" = "¡Hola!"
    "mensaje" = "Notificación de prueba"
    "tipo" = "info"
    "rol_destino" = "admin"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:9000/notificaciones/crear" `
  -Method POST `
  -Headers $headers `
  -ContentType "application/json" `
  -Body $body
```

✅ **Resultado esperado:**
- La notificación aparece en el navbar (badge rojo con +1)
- Puedes verla en el dropdown

### Opción B: Usando cURL (Git Bash)

```bash
# Token de prueba (reemplaza con uno válido)
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Enviar notificación
curl -X POST http://localhost:9000/notificaciones/crear \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Prueba",
    "mensaje": "¿Funciona?",
    "tipo": "success",
    "rol_destino": "admin"
  }'
```

---

## 🧠 Flujo Completo de Notificaciones

```
┌────────────────────────────────────────────────────────────┐
│                 USUARIO EN NAVBAR                           │
│         (Ve ícono 🔔 con badge contador)                  │
└────────────────────┬───────────────────────────────────────┘
                     │ WebSocket conectado
                     ▼
         /notificaciones/ws (localhost:9000)
                     │
        ┌────────────┴────────────┐
        │                         │
   RECIBE                    ENVIA
   notificación          (si se conecta)
        │                         │
        ▼                         ▼
  Badge aumenta          Heartbeat/ping
  Lista actualiza        Connection ACK
  (últimas 20)
        │
        ▼
┌────────────────────────────────────────────────────────────┐
│              DROPDOWN PANEL ABIERTO                         │
│  • Título: "¡Hola!"                                        │
│  • Mensaje: "Notificación de prueba"                       │
│  • Tipo: info (azul)                                       │
│  • Timestamp: "Hace 5s"                                    │
└────────────────────────────────────────────────────────────┘
```

---

## ❌ Troubleshooting

### Error: "No puedo conectar a la base de datos"

```bash
# Verificar conexión a PostgreSQL
psql -h 31.97.8.51 -U admin -d sistema -c "SELECT 1;"

# Si da error, revisar credenciales en .env
# DATABASE_URL=postgresql://USER:PASS@HOST:PORT/DATABASE
```

### Error: "Puerto 9000 ya está en uso"

```bash
# Encontrar y matar proceso
netstat -ano | findstr :9000
taskkill /PID <PID> /F

# O usar puerto diferente
uvicorn main:app --reload --port 9001
```

### Error: "WebSocket connection failed"

```typescript
// En DevTools (F12) → Console
// Verificar que ve conexión a:
console.log('Conectando a:', `ws://localhost:9000/notificaciones/ws`)

// Si dice "wss://", verifica VITE_API_URL en .env.local
// No debe incluir https:// para local
```

### Navbar no aparece en pantalla

1. Revisar que `HomeView.vue` importa `Navbar.vue`:
   ```typescript
   import Navbar from '../components/Navbar.vue'
   ```

2. Verificar que está en el template:
   ```vue
   <template>
     <div class="home-container">
       <Navbar />
       ...
     </div>
   </template>
   ```

3. Verificar en DevTools (F12) que Navbar está en el DOM

### Notificación no aparece

```bash
# 1. Verificar que el usuario está logueado
# (Debería ver su nombre en navbar)

# 2. Verificar JWT token en localStorage:
# F12 → Application → Local Storage → http://localhost:5173
# Debe haber entrada "token" o "auth_token"

# 3. Verificar que rol_destino coincide
# Si enviaste rol_destino="admin", pero eres "usuario", no aparecerá

# 4. Ver logs del backend
# Terminal donde corre uvicorn debe mostrar requests
```

---

## 📋 Checklist Antes de Usar

```bash
# ✅ Verificar archivo .env en Backend
[ -f Backend/.env ] && echo "✅ .env existe" || echo "❌ Falta .env"

# ✅ Verificar archivo .env en Frontend
[ -f Frontend/sistemaapp-frontend/.env.local ] && echo "✅ .env.local existe" || echo "❌ Falta .env.local"

# ✅ Verificar node_modules instalados
[ -d Frontend/sistemaapp-frontend/node_modules ] && echo "✅ Deps instaladas" || echo "❌ Falta npm install"

# ✅ Verificar venv backend
[ -d Backend/venv ] && echo "✅ venv existe" || echo "❌ Falta venv"

# ✅ Verificar conexión DB
psql -h 31.97.8.51 -U admin -d sistema -c "SELECT COUNT(*) FROM users;" 2>/dev/null && echo "✅ DB accesible" || echo "❌ DB no accesible"
```

---

## 🚀 Comandos Finales (Copy-Paste Ready)

### Terminal 1 - Backend

```powershell
# PowerShell - Backend
cd "c:\Users\Admin_1\Music\SISTEMA\SistemaApp\Backend"
.\venv\Scripts\activate
uvicorn main:app --reload --port 9000
```

### Terminal 2 - Frontend

```powershell
# PowerShell - Frontend
cd "c:\Users\Admin_1\Music\SISTEMA\SistemaApp\Frontend\sistemaapp-frontend"
npm run dev
```

### Terminal 3 - Testing (Opcional)

```powershell
# PowerShell - Test
# Copiar y ejecutar para enviar notificación de prueba
$token = "YOUR_JWT_TOKEN_HERE"
$headers = @{"Authorization" = "Bearer $token"; "Content-Type" = "application/json"}
$body = @{"titulo"="Test";"mensaje"="¡Funciona!";"tipo"="success";"rol_destino"="admin"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:9000/notificaciones/crear" -Method POST -Headers $headers -Body $body -ContentType "application/json"
```

---

## 🎯 Indicadores de Éxito

✅ **Frontend carga en 2s**
```
VITE v4.x running at:
Local: http://localhost:5173/
```

✅ **Backend acepta requests**
```
INFO:     Application startup complete
GET /auth/login - "200 OK"
```

✅ **Ves el Navbar**
- Logo "🌱 SistemaApp" arriba
- Ícono 🔔 a la derecha
- Tu nombre en la esquina superior derecha

✅ **Notificación llega en tiempo real**
- Badge contador aumenta
- Aparece en dropdown sin refresh

✅ **WebSocket conectado**
- F12 → Network → WS
- Una conexión a `ws://localhost:9000/notificaciones/ws`
- Estado: "Connected"

---

## 📞 Resumen Rápido

| Componente | URL/Puerto | Status |
|-----------|-----------|--------|
| Frontend | localhost:5173 | npm run dev |
| Backend | localhost:9000 | uvicorn main:app |
| Database | 31.97.8.51:5432 | PostgreSQL |
| WebSocket | ws://localhost:9000/notificaciones/ws | Auto-conectado |

---

```
╔═════════════════════════════════════════╗
║  ✅ TODO LISTO PARA FUNCIONAR EN LOCAL  ║
║                                         ║
║  1. Terminal 1: Backend (uvicorn)      ║
║  2. Terminal 2: Frontend (npm)         ║
║  3. Browser: http://localhost:5173     ║
║  4. ¡Ver Navbar con notificaciones! 🔔║
║                                         ║
╚═════════════════════════════════════════╝
```

---

**¿Preguntas o problemas? Revisar:**
- Backend logs (Terminal 1)
- Browser Console (F12)
- Network tab (F12 → Network)
- NOTIFICACIONES_DOCS.md (Backend API)
- NOTIFICACIONES_FRONTEND_GUIDE.md (Frontend)
