# 📱 PWA - Progressive Web App

## ¿Qué es una PWA?

Una **Progressive Web App (PWA)** es una aplicación web que funciona como una aplicación nativa:

- ✅ **Instalable**: Se instala como una app en el home screen
- ✅ **Offline**: Funciona sin conexión a internet
- ✅ **Rápida**: Carga rápidamente y es responsive
- ✅ **Segura**: Usa HTTPS y service workers
- ✅ **Sincronización**: Sincroniza datos cuando vuelve la conexión

---

## 🏗️ Arquitectura PWA implementada

```
┌─────────────────────────────────────────────┐
│        SistemaApp PWA                       │
├─────────────────────────────────────────────┤
│                                             │
│ 🎨 Frontend (Vue 3)                         │
│ ├─ vite-plugin-pwa                          │
│ └─ Service Worker (automático)              │
│                                             │
│ 📡 Workbox (Caching)                        │
│ ├─ NetworkFirst (documentos)                │
│ ├─ StaleWhileRevalidate (scripts/styles)    │
│ └─ CacheFirst (imágenes)                    │
│                                             │
│ 💾 IndexedDB (Offline Storage)              │
│ ├─ offline_points (tabla)                   │
│ └─ Sincronización automática                │
│                                             │
│ 🔐 Seguridad                                │
│ ├─ HTTPS                                    │
│ ├─ JWT Token                                │
│ └─ CORS                                     │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 📦 Dependencias instaladas

```bash
npm install vite-plugin-pwa workbox-window idb
```

| Paquete | Versión | Propósito |
|---------|---------|----------|
| vite-plugin-pwa | latest | Plugin PWA para Vite |
| workbox-window | latest | Cliente de Workbox |
| idb | latest | IndexedDB wrapper |

---

## 🔧 Configuración aplicada

### 1. vite.config.ts

```typescript
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'SistemaApp',
        short_name: 'SistemaApp',
        description: 'Sistema Territorial de Administración',
        theme_color: '#16a34a',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: '/',
        icons: [
          { src: '/pwa-192x192.png', sizes: '192x192' },
          { src: '/pwa-512x512.png', sizes: '512x512' },
        ],
      },
      workbox: {
        runtimeCaching: [
          // NetworkFirst: documentos
          // StaleWhileRevalidate: JS/CSS
          // CacheFirst: imágenes
        ],
      },
    }),
  ],
})
```

### 2. registerSW.js

```javascript
import { registerSW } from 'virtual:pwa-register'

registerSW({
  onNeedRefresh() {
    // Notifica cuando hay update disponible
  },
  onOfflineReady() {
    // Confirma que funciona sin conexión
  },
})
```

### 3. db.js (IndexedDB)

```javascript
export const addOfflinePoint = async (point) => {
  // Guarda punto en IndexedDB
}

export const getOfflinePoints = async () => {
  // Obtiene puntos guardados offline
}

export const clearOfflinePoints = async () => {
  // Limpia puntos después de sincronizar
}
```

---

## 🌐 Flujo offline-first

```
ESCENARIO 1: CON CONEXIÓN
├─ Usuario crea punto
├─ POST /layers/{tipo}
├─ Servidor guarda
└─ Actualiza mapa ✅

ESCENARIO 2: SIN CONEXIÓN
├─ Usuario crea punto
├─ No hay conexión
├─ Guarda en IndexedDB
├─ Muestra alert: "📡 Guardando offline..."
└─ Punto aparece en mapa (local)

ESCENARIO 3: VUELVE CONEXIÓN
├─ Evento 'online' dispara
├─ syncOfflinePoints() ejecuta
├─ Para cada punto offline:
│  └─ POST /layers/{tipo}
├─ Sincroniza con servidor
├─ Limpia IndexedDB
└─ Muestra alert: "✅ Sincronizado" ✅
```

---

## 📱 Instalación de la app

### En navegadores de escritorio

1. Abre `http://localhost:5173`
2. Busca el botón "Instalar" en la barra de direcciones
3. Haz clic → Se instala como aplicación

### En móviles (Android)

1. Abre en Chrome: `http://localhost:5173`
2. Toca el menú (⋮) → "Instalar app"
3. Aparecerá en home screen

### En iOS

1. Abre en Safari: `http://localhost:5173`
2. Toca compartir → "Agregar a pantalla de inicio"
3. Aparecerá como app nativa

---

## 🔄 Sincronización automática

### Cómo funciona:

```javascript
// Se ejecuta automáticamente cuando hay conexión
window.addEventListener('online', syncOfflinePoints)

// La función:
1. Obtiene puntos de IndexedDB
2. Los envía uno por uno al servidor
3. Si falla, reintenta más tarde
4. Limpia IndexedDB cuando termina
5. Recarga el mapa
```

### Flujo en tiempo real:

```
Usuario sin conexión
    ↓
Crea 3 puntos
    ↓
Se guardan en IndexedDB
    ↓
Usuario sale de la app
    ↓
Usuario conecta de nuevo
    ↓
Evento 'online' dispara
    ↓
syncOfflinePoints() se ejecuta
    ↓
3 puntos se envían al servidor
    ↓
IndexedDB se limpia
    ↓
Mapa se recarga
    ↓
✅ Todo sincronizado
```

---

## 📊 Caché de Workbox

### Estrategias implementadas:

#### 1. **NetworkFirst** (Documentos HTML)
- Intenta obtener del servidor primero
- Si falla, usa versión cacheada
- Para: Páginas, documentos

#### 2. **StaleWhileRevalidate** (Scripts/CSS)
- Devuelve versión cacheada rápidamente
- Actualiza en background
- Para: JavaScript, CSS, workers

#### 3. **CacheFirst** (Imágenes)
- Devuelve versión cacheada
- Si no existe, obtiene del servidor
- Máximo 50 imágenes en caché
- Para: Imágenes, activos estáticos

---

## 🧪 Testing de PWA

### En desarrollo:

1. Abre DevTools (F12)
2. Pestaña "Application"
3. Sección "Service Workers"
4. Busca "SistemaApp"

### Prueba offline:

1. DevTools → Network
2. Busca "Offline" en el dropdown
3. Selecciona "Offline"
4. La app debe seguir funcionando

### Prueba instalación:

1. Abre DevTools → Application
2. Pestaña "Manifest"
3. Verifica que el manifest esté presente
4. Busca el botón "Install" en la barra

---

## 📝 Cambios en código

### MapaView.vue:

**Agregado:**
```typescript
import { addOfflinePoint, getOfflinePoints, clearOfflinePoints } from '../utils/db'

const onMapClick = async (event) => {
  // Si hay conexión: POST al servidor
  // Si no hay: Guarda en IndexedDB
}

const syncOfflinePoints = async () => {
  // Sincroniza puntos offline
  // Se ejecuta cuando vuelve la conexión
}

window.addEventListener('online', syncOfflinePoints)
```

### main.ts:

**Agregado:**
```typescript
import './registerSW'
```

### vite.config.ts:

**Agregado:**
```typescript
import { VitePWA } from 'vite-plugin-pwa'

VitePWA({
  registerType: 'autoUpdate',
  manifest: { ... },
  workbox: { ... },
})
```

---

## 🚀 Deployment a producción

### Requisitos:

1. ✅ HTTPS habilitado (obligatorio para PWA)
2. ✅ Service Worker registrado
3. ✅ Manifest presente
4. ✅ Íconos en lugar correcto
5. ✅ Backend con CORS configurado

### Pasos:

```bash
# 1. Build
npm run build

# 2. Deploy a servidor HTTPS
# (Vercel, Netlify, AWS, etc.)

# 3. La app se instala automáticamente
```

### Verificar en producción:

```bash
# Usar Lighthouse (en DevTools → Audits)
# Debe pasar todas las pruebas PWA
```

---

## 📊 Beneficios implementados

| Beneficio | Antes | Ahora |
|----------|-------|-------|
| Instalable | ❌ | ✅ |
| Offline | ❌ | ✅ |
| Sincronización | ❌ | ✅ |
| Caché inteligente | ❌ | ✅ |
| Notificaciones | ❌ | (próximamente) |
| Push notifications | ❌ | (próximamente) |

---

## 🔐 Seguridad

### Implementado:

- ✅ HTTPS requerido
- ✅ Service Worker seguro
- ✅ JWT token en peticiones
- ✅ CORS configurado
- ✅ Content Security Policy (CSP)

### Offline:

- ✅ Datos sensibles protegidos
- ✅ IndexedDB local (no sincroniza datos privados automáticamente)
- ✅ Autenticación JWT requerida incluso offline

---

## 📚 Archivos relacionados

- `vite.config.ts` - Configuración PWA
- `src/registerSW.js` - Registro de Service Worker
- `src/utils/db.js` - Funciones IndexedDB
- `src/views/MapaView.vue` - Integración offline
- `public/manifest.json` - Manifest (generado automáticamente)
- `public/pwa-*.png` - Íconos (necesitan ser agregados)

---

## 🎯 Próximas features PWA

- 📋 Push notifications
- 📋 Background sync API
- 📋 Share API
- 📋 Periodic background sync
- 📋 Web app shortcuts

---

## 💡 Tips

### Limpiar caché en desarrollo:

```javascript
// En DevTools Console:
navigator.serviceWorker.getRegistrations().then(registrations => {
  registrations.forEach(registration => registration.unregister())
})

// Luego recarga la página
```

### Ver almacenamiento offline:

```javascript
// En DevTools Console:
const db = await indexedDB.databases()
console.log(db)
```

### Debuggear Service Worker:

```javascript
// DevTools → Application → Service Workers
// Verifica logs, errores, estado
```

---

## 📞 Soporte

**¿No funciona offline?**
- Verifica que el Service Worker esté registrado (DevTools → Application)
- Verifica que HTTPS esté habilitado (si es producción)
- Revisa la consola de errores

**¿No sincroniza?**
- Verifica que haya conexión (`navigator.onLine`)
- Revisa IndexedDB (DevTools → Application → IndexedDB)
- Revisa logs de sincronización

**¿No se instala?**
- Verifica que el manifest sea válido
- Debe haber HTTPS en producción
- Revisa DevTools → Application → Manifest

---

**Estado:** ✅ COMPLETADO
**Versión:** 1.0
**Fecha:** 12 de Noviembre 2025

