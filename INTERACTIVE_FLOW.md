# 🎬 Flujo interactivo - MapaView con Backend

## 1️⃣ Inicio de sesión

```
Usuario abre SistemaApp
        ↓
    LoginView
        ↓
Introduce email/contraseña
        ↓
POST /auth/login
        ↓
Recibe JWT token
        ↓
auth.token = "eyJ0eXAi..."
        ↓
Redirige a Dashboard ✅
```

---

## 2️⃣ Navegación a MapaView

```
Usuario está en Dashboard
        ↓
Hace clic en "Capas Temáticas"
        ↓
Router navega a MapaView
        ↓
Componente se monta
        ↓
Ejecuta onMounted() ✅
```

---

## 3️⃣ Carga inicial de capas

```
onMounted() dispara
        ↓
loadLayers() se ejecuta
        ↓
┌─ Para cada tipo de capa:
├─ GET /layers/ambiental
│  └─ Con: Authorization: Bearer <token>
│  └─ Response: {
│       "tipo": "ambiental",
│       "total": 3,
│       "items": [
│         {"id": 1, "nombre": "Bosque X", "lat": 19.43, "lng": -99.13},
│         {"id": 2, "nombre": "Bosque Y", "lat": 19.44, "lng": -99.14},
│         ...
│       ]
│     }
│
├─ GET /layers/productiva
│  └─ Response: {...}
│
├─ GET /layers/social
│  └─ Response: {...}
│
└─ GET /layers/infraestructura
   └─ Response: {...}
        ↓
dataCapas.value actualiza
        ↓
visibleCapas computed se recalcula
        ↓
Marcadores se renderizan en Leaflet
        ↓
✅ Mapa muestra puntos de 4 capas con colores
```

---

## 4️⃣ Visualización del mapa

```
┌──────────────────────────────────────────┐
│         MAPAVIEW EN NAVEGADOR            │
├──────────────────────────────────────────┤
│                                          │
│  Header: "Capas Temáticas"               │
│  [Mi ubicación]                          │
│                                          │
│  ┌──────────────┐  ┌─────────────────┐  │
│  │ Panel lateral│  │   Mapa Leaflet  │  │
│  │              │  │                 │  │
│  │ ☑ Ambiental │  │   🟢 🟢 🟢     │  │
│  │ ☑ Productiva│  │   🟠 🟠         │  │
│  │ ☑ Social    │  │   🔵             │  │
│  │ ☑ Infra     │  │   ⚪ ⚪         │  │
│  │              │  │                 │  │
│  │ Selecciona... │  │ (Clic = crear)  │  │
│  └──────────────┘  └─────────────────┘  │
│                                          │
│  Leyenda: ◦ Ambiental ◦ Productiva ...  │
│                                          │
└──────────────────────────────────────────┘

Colores:
🟢 Verde (#10b981) = Ambiental
🟠 Naranja (#f97316) = Productiva
🔵 Azul (#3b82f6) = Social
⚪ Gris (#6b7280) = Infraestructura
```

---

## 5️⃣ Usuario interactúa - Filtrado de capas

```
Usuario hace clic en checkbox
        ↓
activeLayers ref se actualiza
        ↓
visibleCapas computed se recalcula
        ↓
Filtra automáticamente qué capas mostrar
        ↓
Marcadores se muestran/ocultan en tiempo real
        ↓
✅ Panel lateral y mapa sincronizados
```

---

## 6️⃣ Usuario crea nuevo punto - Clic en mapa

```
Usuario hace clic en el mapa
        ↓
Evento @click="onMapClick" se dispara
        ↓
Se extrae: lat, lng del evento
        ↓
Primer prompt aparece:
┌─────────────────────────────────┐
│ ¿Qué tipo de capa deseas        │
│ agregar?                        │
│ (ambiental/productiva/social/.. │
│                                 │
│ [        ] [Cancelar] [Aceptar] │
└─────────────────────────────────┘
        ↓
Usuario escribe: "ambiental"
        ↓
Segundo prompt aparece:
┌─────────────────────────────────┐
│ Nombre del punto:               │
│                                 │
│ [      Nueva area verde      ]  │
│ [        ] [Cancelar] [Aceptar] │
└─────────────────────────────────┘
        ↓
Usuario escribe: "Nueva area verde"
        ↓
Validación: ¿tipo && nombre no son vacíos?
        ↓
SÍ → Continúa
        ↓
POST /layers/ambiental
Body: {
  "nombre": "Nueva area verde",
  "descripcion": "",
  "lat": 19.435,
  "lng": -99.128
}
Header: {
  "Authorization": "Bearer eyJ0eXAi...",
  "Content-Type": "application/json"
}
        ↓
Backend recibe
        ↓
✅ INSERT en tabla ambiental
        ↓
Retorna: {"success": true, "id": 123, ...}
        ↓
Frontend recibe respuesta
        ↓
Muestra alert:
┌─────────────────────┐
│ ✅ Punto agregado   │
│ correctamente       │
│     [OK]            │
└─────────────────────┘
        ↓
loadLayers() se ejecuta NUEVAMENTE
        ↓
GET a todos los endpoints
        ↓
dataCapas.value se actualiza
        ↓
✅ Nuevo marcador aparece en el mapa
```

---

## 7️⃣ Error en creación

```
Usuario hace clic en mapa
        ↓
Prompts piden tipo y nombre
        ↓
POST /layers/ambiental
        ↓
❌ Error (ej: servidor caído, token expirado)
        ↓
catch captura el error
        ↓
Muestra alert:
┌──────────────────┐
│ ❌ Error al      │
│ agregar punto    │
│      [OK]        │
└──────────────────┘
        ↓
loadLayers() NO se ejecuta
        ↓
Mapa no cambia
        ↓
Usuario puede reintentar
```

---

## 8️⃣ Interacción con marcadores

```
Usuario hace hover sobre marcador
        ↓
Marcador se destaca
        ↓
Usuario hace clic en marcador
        ↓
Popup aparece:
┌────────────────────┐
│ 🌱 Zona Ambiental  │
│ Nueva area verde   │
│        X           │
└────────────────────┘
        ↓
Usuario puede:
├─ Leer información
├─ Hacer clic fuera para cerrar
└─ Navegar el mapa sin limitaciones
```

---

## 9️⃣ Geolocalización

```
Usuario hace clic en "Mi ubicación"
        ↓
navigator.geolocation.getCurrentPosition()
        ↓
Browser solicita permiso
        ↓
Usuario autoriza
        ↓
Recibe: lat, lng
        ↓
center.value = [lat, lng]
        ↓
zoom.value = 12
        ↓
✅ Mapa se centra en ubicación del usuario
```

---

## 🔟 Ciclo de vida completo

```
┌─────────────────────────────────────────────────────┐
│               COMPONENTE MAPAVIEW                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Componente se crea                              │
│                                                     │
│  2. onMounted() se ejecuta                          │
│     ↓                                               │
│     loadLayers()                                    │
│     ↓                                               │
│     GET /layers/* → Carga datos                     │
│                                                     │
│  3. Componente renderiza                           │
│     ↓                                               │
│     Muestra mapa con marcadores                     │
│                                                     │
│  4. Usuario interactúa                             │
│     ├─ Filtra capas (activa/desactiva)             │
│     ├─ Hace clic en marcadores (muestra popups)    │
│     ├─ Hace clic en "Mi ubicación"                 │
│     └─ Hace clic en el mapa (crea nuevos puntos)   │
│                                                     │
│  5. Si hace clic en el mapa:                       │
│     ↓                                               │
│     onMapClick()                                    │
│     ↓                                               │
│     Solicita tipo y nombre                         │
│     ↓                                               │
│     POST /layers/{tipo} → Crea punto               │
│     ↓                                               │
│     loadLayers() → Recarga datos                   │
│                                                    │
│  6. Componente se desmonta                         │
│     ↓                                               │
│     Recursos se limpian                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Diagrama de estados

```
┌─────────────────┐
│   INICIAL       │ (Componente creado)
│ (sin datos)     │
└────────┬────────┘
         │
         │ onMounted()
         ↓
┌─────────────────┐
│   CARGANDO      │ (loadLayers ejecutándose)
│ (peticiones)    │
└────────┬────────┘
         │
         │ Respuestas recibidas
         ↓
┌─────────────────┐
│   LISTO         │ (Datos cargados, mapa mostrado)
│ (marcadores)    │
└────────┬────────┘
         │
         │ Usuario interactúa
         ├─ Filtra capas
         ├─ Visualiza popups
         ├─ Geolocación
         └─ Crea puntos
         │
         ├─ Si crea punto:
         │  ↓
         │  ┌──────────────────┐
         │  │ CREANDO PUNTO    │
         │  │ (POST enviando)  │
         │  └────────┬─────────┘
         │           │
         │           ├─ ✅ Éxito → loadLayers() → vuelve a LISTO
         │           └─ ❌ Error → muestra alert → sigue en LISTO
         │
         └─ Si no crea:
            └─ Sigue en LISTO

┌─────────────────┐
│   DESMONTADO    │ (Componente destruido)
│ (limpio)        │
└─────────────────┘
```

---

## 🔐 Flujo de seguridad

```
1. Usuario hace login
   ↓
   Backend genera JWT
   ↓
   Frontend guarda en auth.store.token
   ↓

2. Cada petición a /layers
   ↓
   Frontend prepara headers:
   {
     "Authorization": "Bearer <token>"
   }
   ↓
   Envía petición con headers
   ↓

3. Backend recibe petición
   ↓
   Extrae token del header
   ↓
   Valida: ¿token válido?
   ├─ SÍ → Procesa la petición → Retorna datos
   └─ NO → Retorna 401 Unauthorized
   ↓

4. Frontend recibe respuesta
   ├─ 200 OK → Muestra datos/confirmación
   └─ 401 Unauthorized → Pide re-login
```

---

## 📝 Resumen de endpoints utilizados

| Método | Endpoint | Datos | Respuesta | Evento |
|--------|----------|-------|----------|--------|
| GET | `/layers/{tipo}` | Token | `{tipo, total, items}` | onMounted |
| GET | `/layers/{tipo}` | Token | `{tipo, total, items}` | Después de crear |
| POST | `/layers/{tipo}` | Punto data + Token | `{success, id}` | Al crear |

---

## 🎯 Casos de uso cubiertos

- ✅ Ver todas las capas en el mapa
- ✅ Filtrar capas (mostrar/ocultar)
- ✅ Ver información de puntos (popups)
- ✅ Crear nuevos puntos interactivamente
- ✅ Autenticación JWT en todas las peticiones
- ✅ Manejo de errores
- ✅ Geolocalización del usuario
- ✅ Responsive en mobile/desktop

---

## 🚀 ¿Cómo probar cada flujo?

### Flujo 1: Carga inicial
1. Abre MapaView
2. Abre DevTools (F12) → Network
3. Deberías ver 4 peticiones GET a `/layers/*`
4. Todos con status 200 ✅

### Flujo 2: Filtrado de capas
1. En el panel lateral, desactiva "Ambiental"
2. Los marcadores verdes desaparecen
3. Vuelve a activarla
4. Los marcadores reaparecen ✅

### Flujo 3: Crear punto
1. Haz clic en el mapa
2. Escribe: `ambiental`
3. Escribe: `Mi nuevo punto`
4. Verifica alerta de éxito ✅
5. Punto aparece en el mapa ✅

### Flujo 4: Seguridad
1. Abre DevTools → Network
2. Busca cualquier petición GET/POST
3. Expande el header
4. Verifica presencia de `Authorization: Bearer ...` ✅

