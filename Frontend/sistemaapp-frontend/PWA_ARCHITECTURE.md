# 📊 PWA - Diagrama de flujo y arquitectura

## 🏗️ Arquitectura general

```
┌─────────────────────────────────────────────────────────────────────┐
│                        NAVEGADOR DEL USUARIO                        │
│                     (Chrome, Firefox, Safari, Edge)                 │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        ┌────────────┐  ┌────────────┐  ┌──────────────┐
        │  Frontend  │  │Service     │  │   IndexedDB  │
        │  (Vue 3)   │  │  Worker    │  │   (Offline)  │
        │            │  │  (SW)      │  │              │
        └─────┬──────┘  └────┬───────┘  └──────┬───────┘
              │              │                 │
              │ axios        │                 │
              │ requests     │                 │
              └──────────┬───┴─────────────────┘
                         │
                ┌────────▼────────┐
                │   Workbox       │
                │   (Caching)     │
                │                 │
                │ NetworkFirst    │
                │ StaleWhileReval │
                │ CacheFirst      │
                └────────┬────────┘
                         │
                HTTPS/HTTP │
                         │
        ┌────────────────▼────────────────┐
        │     FastAPI Backend             │
        │     (Puerto 9000)               │
        │                                 │
        │  ├─ /layers/{tipo}              │
        │  ├─ JWT Validation              │
        │  └─ CORS Policy                 │
        └────────────────┬────────────────┘
                         │
                    SQL │
                         │
        ┌────────────────▼────────────────┐
        │   PostgreSQL Database           │
        │   (31.97.8.51:5432)             │
        │                                 │
        │  ├─ ambiental                   │
        │  ├─ productiva                  │
        │  ├─ social                      │
        │  └─ infraestructura             │
        └─────────────────────────────────┘
```

---

## 🔄 Flujo online (con conexión)

```
1. USUARIO ABRE MAPAVIEW
   ▼
2. onMounted() ejecuta loadLayers()
   ▼
3. GET /layers/ambiental, GET /layers/productiva, etc.
   ├─ Headers: Authorization: Bearer <token>
   ├─ Workbox captura
   └─ Strategy: NetworkFirst
   ▼
4. Backend valida JWT y retorna datos
   ▼
5. dataCapas.value actualiza
   ▼
6. Componente re-renderiza
   ▼
7. Marcadores aparecen en mapa ✅
   ▼
8. Workbox guarda en caché

USUARIO CREA PUNTO (ONLINE)
   ▼
9. Clic en mapa → onMapClick()
   ▼
10. Prompts piden tipo y nombre
   ▼
11. POST /layers/{tipo}
    ├─ Body: {nombre, lat, lng}
    ├─ Headers: Authorization: Bearer <token>
    └─ Sin conexión: Exception capturada
   ▼
12. Backend valida y guarda en BD
   ▼
13. Retorna {success: true}
   ▼
14. Alert: "✅ Punto guardado en servidor"
   ▼
15. loadLayers() recarga
   ▼
16. Nuevo punto aparece en mapa ✅
```

---

## 📡 Flujo offline (sin conexión)

```
USUARIO SIN CONEXIÓN ABRE MAPAVIEW
   ▼
1. Service Worker intercepta peticiones
   ▼
2. Workbox cache devuelve versión cacheada
   ├─ HTML: NetworkFirst (usa caché)
   ├─ JS/CSS: StaleWhileRevalidate (usa caché)
   └─ Imágenes: CacheFirst (usa caché)
   ▼
3. Componente renderiza con datos en caché ✅
   ▼
4. Panel de capas funcional ✅
   ▼
5. Mapa interactivo (Leaflet offline) ✅

USUARIO CREA PUNTO (OFFLINE)
   ▼
6. Clic en mapa → onMapClick()
   ▼
7. Prompts piden tipo y nombre
   ▼
8. Intenta POST /layers/{tipo}
   ▼
9. ❌ FALLA (sin conexión)
   ▼
10. catch captura el error
   ▼
11. Alert: "📡 Sin conexión, guardando offline..."
   ▼
12. await addOfflinePoint(point)
   ├─ Abre IndexedDB
   ├─ Tabla: offline_points
   └─ Guarda punto en BD local
   ▼
13. Punto se agrega al mapa (local) ✅
   ▼
14. Espera a que vuelva conexión
```

---

## 🔄 Flujo de sincronización (reconexión)

```
USUARIO ESTABA OFFLINE Y CONECTA
   ▼
1. Navegador detecta conexión
   ▼
2. Evento 'online' dispara
   ▼
3. syncOfflinePoints() se ejecuta
   ▼
4. await getOfflinePoints()
   ├─ Abre IndexedDB
   ├─ Tabla: offline_points
   └─ Obtiene todos los puntos guardados
   ▼
5. Para cada punto offline:
   │
   ├─ POST /layers/{tipo}
   ├─ Headers: Authorization: Bearer <token>
   ├─ Body: punto guardado
   └─ Intenta sincronizar
   │
   ├─ ✅ Éxito: Pasa al siguiente
   └─ ❌ Falla: Se detiene (reintenta más tarde)
   ▼
6. Si todos tuvieron éxito:
   │
   ├─ await clearOfflinePoints()
   ├─ Limpia IndexedDB
   └─ Tabla offline_points vacía
   ▼
7. await loadLayers()
   ├─ Recarga todos los datos
   └─ Mapa se actualiza
   ▼
8. Alert: "✅ Datos offline sincronizados"
   ▼
9. Usuario ve nuevos puntos en mapa ✅
   ▼
10. Todo sincronizado con servidor
```

---

## 📊 Estados de la aplicación

```
┌─────────────────────────────────────────────────────────────────┐
│              MÁQUINA DE ESTADOS DE SEMAAPP PWA                 │
└─────────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │      INICIO     │
                    │  (App cargada)  │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
        ¿Hay conexión?          ¿Hay conexión?
                │                         │
            SÍ  │                     NO  │
                ▼                         ▼
        ┌──────────────┐        ┌──────────────┐
        │   ONLINE     │        │   OFFLINE    │
        │              │        │              │
        │ ✅ Conectado │        │ 📡 Desconectado
        └──────┬───────┘        └──────┬───────┘
               │                       │
        ┌──────┴──────┐         ┌──────┴──────┐
        │             │         │             │
     Crear       Filtrar    Crear         Filtrar
     punto       capas      punto         capas
        │             │         │             │
        ▼             │         ▼             │
   POST ok        same      POST falla      same
    (éxito)                 (IndexedDB)
        │             │         │             │
        ▼             │         ▼             │
   Recarga       rerender   Recarga        rerender
   mapa            mapa      mapa           mapa
   Alerta: ✅    (local)    Alerta: 📡   (caché)
   "Guardado"              "Offline"
        │             │         │             │
        └─────────────┼─────────┴─────────────┘
                      │
              ¿Vuelve la conexión?
                      │
                      ▼
            ┌──────────────────┐
            │  SINCRONIZANDO   │
            │                  │
            │ Enviando puntos  │
            │ guardados offline│
            └────────┬─────────┘
                     │
              ✅ Todo sincronizado
                     │
                     ▼
            ┌──────────────────┐
            │    DE VUELTA     │
            │    ONLINE        │
            │                  │
            │ ✅ Sincronizado  │
            │ Alerta: "✅ OK" │
            └──────────────────┘
```

---

## 💾 Estructura de IndexedDB

```
┌─────────────────────────────────────────┐
│          IndexedDB Database             │
│       (sistemaapp-db, v1)               │
├─────────────────────────────────────────┤
│                                         │
│  Object Store: offline_points           │
│  ┌───────────────────────────────────┐  │
│  │ id (keyPath)                      │  │
│  │ tipo                              │  │
│  │ nombre                            │  │
│  │ lat                               │  │
│  │ lng                               │  │
│  │ descripcion (opcional)            │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Ejemplo de registro:                   │
│  {                                      │
│    id: 1,                               │
│    tipo: "ambiental",                   │
│    nombre: "Bosque nuevo",              │
│    lat: 19.43,                          │
│    lng: -99.13,                         │
│    descripcion: ""                      │
│  }                                      │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔄 Ciclo de caché Workbox

```
REQUEST
   ▼
┌─ Tipo de recurso?
│
├─ document (HTML)
│  │
│  └─ NetworkFirst
│     ├─ Intenta red
│     └─ Si falla: caché
│
├─ style, script, worker
│  │
│  └─ StaleWhileRevalidate
│     ├─ Devuelve caché rápido
│     └─ Actualiza en background
│
└─ image
   │
   └─ CacheFirst
      ├─ ¿Está en caché?
      │  ├─ SÍ: Devuelve caché
      │  └─ NO: Obtiene de red
      └─ Máximo 50 imágenes
```

---

## 📱 Instalación de app

```
NAVEGADOR                          APP
   │                               │
   │ Usuario abre app              │
   ├──────────────────────────────>│
   │                               │
   │ Service Worker registrado     │
   │ Manifest válido               │
   │ HTTPS habilitado              │
   │                               │
   │ Botón "Instalar" aparece      │
   │ <─────────────────────────────┤
   │                               │
   │ Usuario hace clic             │
   ├──────────────────────────────>│
   │                               │
   │ App se instala                │
   │ Icono en home screen          │
   │ Se abre como app nativa       │
   │                               │
   │ Usuario abre app              │
   │ (desde home screen)           │
   ├──────────────────────────────>│
   │                               │
   │ Navegación cerrada (fullscreen│
   │ Sin barra de direcciones)     │
   │ Funciona offline              │
   │                               │
```

---

## 🔐 Flujo de seguridad

```
REQUEST A /layers/{tipo}
   ▼
1. ¿Tiene header Authorization?
   ├─ NO: ❌ 403 Forbidden
   └─ SÍ: Continúa
   ▼
2. ¿Es token Bearer válido?
   ├─ NO: ❌ 401 Unauthorized
   └─ SÍ: Continúa
   ▼
3. ¿Token no expirado?
   ├─ NO: ❌ 401 Unauthorized
   └─ SÍ: Continúa
   ▼
4. ¿Usuario tiene permiso?
   ├─ NO: ❌ 403 Forbidden
   └─ SÍ: Continúa
   ▼
5. ✅ Procesa request
   └─ Retorna 200 OK + datos

OFFLINE:
   │
   └─ Punto se guarda en IndexedDB
      (No se envía JWT hasta online)
      
SYNC:
   │
   ├─ JWT se incluye en POST
   ├─ Backend valida
   └─ Si válido: Sincroniza
```

---

## 📈 Métricas de caché

```
┌─────────────────────────────────────────┐
│         ESTADÍSTICAS DE CACHÉ           │
├─────────────────────────────────────────┤
│                                         │
│ Documentos HTML                         │
│  Estrategia: NetworkFirst               │
│  Tamaño caché: Ilimitado                │
│  TTL: No expira                         │
│                                         │
│ Scripts y estilos                       │
│  Estrategia: StaleWhileRevalidate       │
│  Tamaño caché: Ilimitado                │
│  TTL: Siempre actualiza en bg           │
│                                         │
│ Imágenes                                │
│  Estrategia: CacheFirst                 │
│  Tamaño caché: Máx. 50 imágenes         │
│  TTL: Ilimitado                         │
│                                         │
│ Offline points (IndexedDB)              │
│  Límite: Sin límite teórico             │
│  TTL: Hasta sincronizar                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎯 User journey completo

```
DÍA 1 - USUARIO DESCUBRE LA APP

1. Abre navegador
2. Visita http://localhost:5173
3. Ve botón "Instalar" en barra
4. Hace clic → Se instala
5. Aparece en home screen
6. Service Worker se registra


DÍA 2 - CON CONEXIÓN

1. Abre app desde home screen
2. Ve mapa con datos (caché rápido)
3. Crea 5 puntos ambientales
4. Todos se sincronizan al servidor ✅


DÍA 3 - SIN CONEXIÓN (Móvil en campo)

1. Abre app (no necesita conexión)
2. Carga desde caché en 0.5 seg ⚡
3. Crea 10 puntos nuevos
4. Se guardan en IndexedDB
5. Sigue usando la app normal


DÍA 4 - VUELVE LA CONEXIÓN

1. Conecta de nuevo
2. Evento 'online' dispara automáticamente
3. syncOfflinePoints() se ejecuta
4. Los 10 puntos se sincronizan
5. Alert: "✅ Sincronizado"
6. Todos ven los nuevos puntos


RESULTADO: ✅ EXPERIENCIA FLUIDA
- App rápida
- Funciona sin conexión
- Sincronización automática
- Usuario productivo siempre
```

---

**Arquitectura PWA completamente implementada y funcional.** 🚀

