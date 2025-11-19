# 🧪 GUÍA DE PRUEBAS - MÓDULO DE NOTIFICACIONES

## 🎯 Objetivo
Validar que el sistema de notificaciones automáticas funciona correctamente en todos los escenarios.

---

## 📋 REQUISITOS PREVIOS

### Backend
- [ ] FastAPI ejecutándose en `http://localhost:8000`
- [ ] Base de datos PostgreSQL activa
- [ ] Migraciones ejecutadas (tabla `notificaciones` debe existir)
- [ ] Variables de entorno configuradas (SECRET_KEY, JWT_SECRET, etc.)

### Frontend
- [ ] Vite dev server ejecutándose en `http://localhost:5173`
- [ ] Archivo `.env.local` con `VITE_API_URL=http://localhost:8000`
- [ ] Dependencias instaladas: `npm install`

### Usuarios de Prueba
Crear o validar estos usuarios en la BD:
- **tecnico_1**: rol = "tecnico"
- **facilitador_1**: rol = "facilitador"
- **admin_1**: rol = "admin"

---

## 🧬 ESCENARIO 1: Notificación al Crear Solicitud

### Paso 1: Preparación
```bash
# Terminal 1: Backend
cd BackendFastAPI
python main.py
# Debería mostrar: "Uvicorn running on http://127.0.0.1:8000"

# Terminal 2: Frontend
cd Frontend/sistemaapp-frontend
npm run dev
# Debería mostrar: "Local:   http://localhost:5173"
```

### Paso 2: Login con Técnico
1. Abrir `http://localhost:5173/login`
2. Email: `tecnico_1@mail.com`
3. Password: (su contraseña)
4. Debe redirigir a Dashboard

### Paso 3: Crear Solicitud
1. Click en "Solicitudes" en acceso rápido del Dashboard
2. Click en "Nueva Solicitud"
3. Llenar formulario:
   - Tipo: "Consulta técnica"
   - Descripción: "Necesito ayuda con el riego"
   - Destino: "facilitador_1"
4. Click en "Enviar"

**✅ Esperado:**
- Modal de éxito
- Se vuelve a la lista de solicitudes
- Consola backend muestra: `✅ Notificación creada para usuario [id]: [notif_id]`

### Paso 4: Verificar Notificación (Facilitador)
1. Abrir nueva pestaña del navegador
2. Ir a `http://localhost:5173/login`
3. Login como facilitador_1
4. Ir a Dashboard

**✅ Esperado:**
- Sección "Notificaciones Recientes" muestra la nueva solicitud
- Badge en campana de Navbar muestra contador (1)
- Card de notificación con:
  - Icono Clock (azul)
  - Título: "Nueva solicitud recibida"
  - Mensaje: "Has recibido una solicitud de tecnico (ID: X)."
  - Timestamp: "Hace poco"

### Paso 5: Abrir Dropdown de Notificaciones
1. Click en campana del Navbar
2. Dropdown se abre

**✅ Esperado:**
- Header con "Notificaciones"
- Card de notificación visible
- Badge desaparece (contador = 0)
- Notificación se marca como leída en BD

---

## 🧬 ESCENARIO 2: Notificación al Aprobar Solicitud

### Paso 1: Facilitador Aprueba
1. Estar en Dashboard del facilitador
2. Abrir sección de Solicitudes
3. Buscar solicitud de tecnico_1
4. Click en solicitud
5. Click en botón "Aprobar" (si existe)
   - O cambiar estado a "aprobada" en formulario

**✅ Esperado (Backend):**
- Consola muestra: `✅ Notificación de respuesta creada para usuario [tecnico_id]: [notif_id]`

### Paso 2: Verificar Notificación (Técnico)
1. Cambiar a pestaña del técnico
2. Ir a Dashboard (Si no está, hacer refresh)

**✅ Esperado:**
- Sección "Notificaciones Recientes" actualiza
- Nueva notificación con:
  - Icono CheckCircle (verde)
  - Título: "Actualización de solicitud"
  - Mensaje: "Tu solicitud ha sido aprobada."
  - Tipo: "respuesta"

### Paso 3: Verificar Badge en Navbar
- Campana del técnico muestra badge con contador 1
- Click en campana marca como leída

---

## 🧬 ESCENARIO 3: Notificación al Rechazar Solicitud

### Paso 1: Crear Nueva Solicitud (Técnico)
1. Login como tecnico_1
2. Ir a Solicitudes
3. Crear nueva solicitud → facilitador_1

### Paso 2: Rechazar Solicitud (Facilitador)
1. Login facilitador_1
2. Ir a Solicitudes
3. Abrir solicitud nueva
4. Cambiar estado a "rechazada"

**✅ Esperado (Backend):**
- Consola: `✅ Notificación de respuesta creada para usuario [tecnico_id]: [notif_id]`

### Paso 3: Verificar en Técnico
1. Pestaña del técnico
2. Ir a Dashboard

**✅ Esperado:**
- Notificación con mensaje: "Tu solicitud ha sido rechazada."
- Icono CheckCircle pero con color rojo (error)

---

## 🧬 ESCENARIO 4: Eliminar Notificaciones

### Paso 1: Abrir Dropdown
1. Click en campana del Navbar
2. Dropdown se abre

### Paso 2: Eliminar una Notificación
1. Hover sobre una notificación
2. Click en botón X (basura)
3. Notificación desaparece

**✅ Esperado:**
- Notificación se elimina del UI
- Contador se actualiza si es necesario
- En BD: notificación se marca como eliminada

---

## 🧬 ESCENARIO 5: Múltiples Notificaciones

### Paso 1: Crear Varias Solicitudes (Técnico)
1. Login tecnico_1
2. Crear 5 solicitudes diferentes a facilitador_1

### Paso 2: Verificar Dashboard del Facilitador
1. Login facilitador_1
2. Ir a Dashboard

**✅ Esperado:**
- Sección "Notificaciones Recientes" muestra máximo 5
- Badge muestra contador 5
- Todas con icono Clock (azul)

### Paso 3: Abrir Dropdown
1. Click en campana
2. Dropdown muestra las 5 notificaciones
3. Scroll si es necesario

**✅ Esperado:**
- Lista scrolleable
- Todas las notificaciones visibles
- Estilos consistentes

---

## 🧬 ESCENARIO 6: Persistencia Después de Recargar

### Paso 1: Crear Notificación
1. Login tecnico_1
2. Crear solicitud → facilitador_1

### Paso 2: Recargar Página (Facilitador)
1. Login facilitador_1
2. Ir a Dashboard
3. Press F5 (Recargar)

**✅ Esperado:**
- Notificación se mantiene visible
- WebSocket reconecta automáticamente
- Contador se recalcula

---

## 🧬 ESCENARIO 7: Conexión WebSocket

### Paso 1: Abrir DevTools del Navegador
1. Presionar F12
2. Tab "Network" → Filter "WS"

### Paso 2: Ir a Dashboard
1. Dashboard debe conectar a WebSocket

**✅ Esperado:**
- Una conexión WebSocket `/notificaciones/ws` conectada
- Estado: (101 Switching Protocols)

### Paso 3: Crear Notificación
1. Desde otra pestaña, crear solicitud

**✅ Esperado:**
- En WebSocket se ve un mensaje entrante
- Notificación aparece inmediatamente sin recargar

---

## 🐛 TROUBLESHOOTING

### Problema: No aparecen notificaciones en Dashboard

**Causas posibles:**
1. WebSocket no conectó
2. user_destino no coincide con auth.user.id
3. Notificaciones no se crearon en BD

**Solución:**
```javascript
// En DevTools Console
console.log(auth.user?.id)  // Debe mostrar un número
// Verificar en Network → WS → Messages
```

### Problema: Badge no se actualiza

**Causas posibles:**
1. Notificaciones no se marcan como leídas
2. Computed property no se recalcula

**Solución:**
- Abrir y cerrar dropdown manual
- Recargar página

### Problema: Error "WebSocket connection failed"

**Causas posibles:**
1. Backend no está corriendo
2. VITE_API_URL incorrecto
3. CORS no configurado

**Solución:**
```bash
# Verificar backend
curl http://localhost:8000/docs

# Verificar URL en .env.local
VITE_API_URL=http://localhost:8000
```

### Problema: Notificaciones en Backend crean pero no llegan

**Causas posibles:**
1. broadcast_notification() no ejecuta
2. Clientes WebSocket desconectados

**Solución:**
```python
# En Backend: Verificar broadcast
print(f"Clientes conectados: {len(active_connections)}")
await broadcast_notification(data)
```

---

## 📊 CHECKLIST DE VALIDACIÓN

### Backend
- [ ] Base de datos: tabla `notificaciones` existe
- [ ] Routes: `/solicitudes/` crea notificaciones
- [ ] Routes: `/solicitudes/{id}/estado` crea notificaciones
- [ ] WebSocket: `/notificaciones/ws` conecta clientes
- [ ] Endpoints: PATCH `/notificaciones/{id}/leer` funciona
- [ ] Endpoints: DELETE `/notificaciones/{id}` funciona

### Frontend - Navbar
- [ ] Campana visible en navbar
- [ ] Badge aparece cuando hay notificaciones
- [ ] Contador se actualiza
- [ ] Dropdown muestra notificaciones
- [ ] Estilos dark-theme consistentes

### Frontend - Dashboard
- [ ] Sección "Notificaciones Recientes" visible
- [ ] Muestra máximo 5 notificaciones
- [ ] Icons dinámicos según tipo
- [ ] Colores según tipo (azul, verde, etc)
- [ ] Timestamp formateado ("Hace poco", "Hace 5m", etc)
- [ ] Badge con contador actualiza

### Funcionalidad
- [ ] Crear solicitud → notificación al destino
- [ ] Aprobar solicitud → notificación al solicitante
- [ ] Rechazar solicitud → notificación al solicitante
- [ ] Notificaciones persisten en BD
- [ ] WebSocket entrega en tiempo real
- [ ] Marcar como leída funciona
- [ ] Eliminar notificación funciona
- [ ] Múltiples notificaciones se muestran

### Performance
- [ ] Dashboard carga rápido
- [ ] Notificaciones aparecen <500ms
- [ ] Sin lag en UI
- [ ] WebSocket se reconecta automáticamente

---

## 🎥 VIDEO DE DEMO RECOMENDADO

Captura los siguientes escenarios:

1. Login tecnico_1 → Crear solicitud → Notificación en facilitador_1 (0:00-0:30)
2. Facilitador aprueba → Notificación en tecnico_1 (0:30-1:00)
3. Abrir dropdown, marcar como leída (1:00-1:15)
4. Dashboard con múltiples notificaciones (1:15-1:30)

**Duración total:** ~90 segundos

---

## 📞 CONTACTO Y SOPORTE

Si encuentras problemas:

1. Verificar logs del backend:
   ```bash
   # Terminal donde corre FastAPI
   # Debe mostrar: ✅ Notificación creada para usuario...
   ```

2. Verificar Console del navegador (F12 → Console):
   ```javascript
   // Buscar mensajes como:
   // "🔔 Nueva notificación en Dashboard: ..."
   ```

3. Verificar BD directamente:
   ```sql
   SELECT * FROM notificaciones ORDER BY created_at DESC LIMIT 5;
   ```

---

**Estado:** ✅ Listo para pruebas

**Última actualización:** 19 de Noviembre, 2025
