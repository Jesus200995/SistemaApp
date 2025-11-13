# 🗺️ Diagramas & Flujos Visuales

## 1. Arquitectura General del Módulo

```
┌─────────────────────────────────────────────────────────────┐
│                     SISTEMA DE MAPAS                        │
└─────────────────────────────────────────────────────────────┘

                            Frontend Layer
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌─────────────────┐        ┌──────────────────┐           │
│  │   MapaView.vue  │◄───────┤  Auth Store      │           │
│  │   Component     │        │  (JWT Token)     │           │
│  └────────┬────────┘        └──────────────────┘           │
│           │                                                 │
│           ├─► getSembradoresMapa() [Axios GET]            │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────────────────────────┐                   │
│  │  State Management (Refs)            │                   │
│  ├─────────────────────────────────────┤                   │
│  │ sembradores: Sembrador[]            │                   │
│  │ mostrarSembradores: boolean         │                   │
│  │ contadorSembradores: computed       │                   │
│  └─────────────────────────────────────┘                   │
│           │                                                 │
│           ├─► Icon Selection ────┐                         │
│           │                      │                         │
│           ▼                      ▼                         │
│  ┌─────────────────┐    ┌──────────────────┐              │
│  │ Markers Verde   │    │ Markers Azules   │              │
│  │ (Productivo)    │    │ (Social)         │              │
│  └────────┬────────┘    └────────┬─────────┘              │
│           │                      │                         │
│           └──────┬───────────────┘                         │
│                  │                                         │
│                  ▼                                         │
│  ┌─────────────────────────────────────┐                   │
│  │  Leaflet Map                        │                   │
│  │  ├─ Tiles (OpenStreetMap)          │                   │
│  │  ├─ Markers (30+ on screen)        │                   │
│  │  ├─ Popups (interactive)           │                   │
│  │  └─ Legend (controls)              │                   │
│  └─────────────────────────────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ HTTP GET /sembradores/map
                            │ with Authorization header
                            │
┌─────────────────────────────────────────────────────────────┐
│                     Backend Layer                           │
│                     (FastAPI)                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌────────────────────────────────────────┐
        │   Authentication Middleware            │
        │   ✓ JWT Token Validation              │
        │   ✓ Extract user_id & role            │
        └────────────────────┬───────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │   Authorization Layer                  │
        │   Determine hierarchy:                 │
        │   - Admin: no filter                  │
        │   - Territorial: subordinados          │
        │   - Facilitador: técnicos             │
        │   - Técnico: propios                  │
        └────────────────────┬───────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │   Database Query                       │
        │   SELECT * FROM sembradores            │
        │   WHERE user_id IN (filtered_ids)      │
        └────────────────────┬───────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │   Response Formatting                  │
        │   {                                    │
        │     success: true,                     │
        │     total: 5,                          │
        │     items: [...]                       │
        │   }                                    │
        └────────────────────────────────────────┘
```

---

## 2. Flujo de Filtrado Jerárquico

```
┌──────────────────────┐
│   Usuario Accede     │
│   a /mapa            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────┐
│  getSembradoresMapa()        │
│  (Frontend)                  │
│  GET /sembradores/map        │
└──────────────────────────────┘
           │
           ▼ (Backend recibe)
┌──────────────────────────────┐
│ Verificar JWT Token          │
│ ✓ Válido → Extraer user_id   │
│ ✗ Inválido → 401 Error       │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  ¿Cuál es el rol del usuario?            │
└──────┬─────────────┬────────────┬────────┘
       │             │            │        
       │ admin       │ territorial│ facilitador  técnico
       │             │            │        
       ▼             ▼            ▼        ▼
   ┌────────┐  ┌────────────┐ ┌─────────┐ ┌──────┐
   │ Sin    │  │ Filtrar   │ │ Filtrar │ │Filtro│
   │filtro  │  │ por       │ │ por     │ │ por  │
   │        │  │subordin.  │ │técnicos │ │user_ │
   │Todos   │  │ directos  │ │ bajo    │ │id    │
   │        │  │           │ │supvis.  │ │      │
   └────────┘  └────────────┘ └─────────┘ └──────┘
       │             │            │        │
       └─────────────┴────────────┴────────┘
                     │
                     ▼
       ┌─────────────────────────┐
       │ Query Sembradores DB    │
       │ WHERE user_id IN (...)  │
       │ ORDER BY creado DESC    │
       └─────────────────────────┘
                     │
                     ▼
       ┌─────────────────────────┐
       │ Formatear Response      │
       │ items[] con datos       │
       │ + coordenadas (lat/lng) │
       │ + info técnico          │
       └─────────────────────────┘
                     │
                     ▼ (Frontend recibe)
       ┌─────────────────────────┐
       │ Actualizar refs:        │
       │ sembradores.value = ... │
       │ contadorSembradores++  │
       └──────────┬──────────────┘
                  │
                  ▼
       ┌─────────────────────────┐
       │ Renderizar Marcadores   │
       │ v-for per sem...        │
       │ :icon = productivo/soc. │
       │ :lat-lng = coords       │
       └──────────┬──────────────┘
                  │
                  ▼
       ┌─────────────────────────┐
       │ Usuarios ven MAPA       │
       │ con sembradores ✓       │
       └─────────────────────────┘
```

---

## 3. Estados y Transiciones (Frontend)

```
┌─────────────────────────────────────────────────────────────┐
│                    MapaView States                          │
└─────────────────────────────────────────────────────────────┘

Initial State
───────────
  sembradores: []
  mostrarSembradores: true
  contadorSembradores: 0
  ├─ No hay marcadores
  └─ Checkbox habilitado

        │ onMounted()
        │ getSembradoresMapa()
        ▼

Loading State
───────────
  (mismo que anterior)
  └─ Esperando response API

        │ API Response 200
        │ data.items = [...]
        ▼

Data Loaded State
───────────────
  sembradores: [ {id:1...}, {id:2...}, ... ]
  contadorSembradores: N (calculated)
  mostrarSembradores: true
  ├─ Markers renderizados en mapa
  ├─ Popups disponibles (click)
  ├─ Leyenda con contador
  └─ Checkbox visible

        ↓ User clicks checkbox (toggle OFF)
        │
        ▼

Hidden State
───────────
  sembradores: [ {id:1...}, {id:2...}, ... ] ← Data NOT cleared
  contadorSembradores: N (same)
  mostrarSembradores: FALSE
  ├─ Markers desaparecen (v-if="mostrarSembradores")
  ├─ Mapa limpio
  ├─ Leyenda: Checkbox desmarcado
  └─ NO hace nueva API call

        ↓ User clicks checkbox (toggle ON)
        │
        ▼

Data Loaded State (again)
──────────────────────
  ├─ Markers reaparecen inmediatamente
  └─ Desde cache (sembradores.value)

        ↓ User clicks marker
        │
        ▼

Popup Open State
────────────────
  sembradores: [ ... ]
  popup: {open: true, data: sembrador}
  ├─ Popup visible
  ├─ Información mostrada
  └─ User puede leer datos

        ↓ User clicks fuera popup
        │
        ▼

(Back to Data Loaded State)
```

---

## 4. Estructura de Datos - Response API

```json
{
  "success": true,
  "total": 5,
  "items": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "comunidad": "La Esperanza",
      "cultivo": "Maíz",
      "lat": -33.8688,                    ← Usado para [lat, lng]
      "lng": -51.2093,                    ← Usado para [lat, lng]
      "user_id": 5,                       ← De qué técnico es
      "tecnico_nombre": "Juan Pérez",     ← Mostrado en popup
      "tecnico_rol": "tecnico_productivo",  ← Determina color ícono
      "creado_en": "2024-01-15T10:30:00"    ← Información adicional
    },
    {
      "id": 2,
      "nombre": "María González",
      "comunidad": "El Carmen",
      "cultivo": "Zapallo",
      "lat": -33.8745,
      "lng": -51.2150,
      "user_id": 6,
      "tecnico_nombre": "María González",
      "tecnico_rol": "tecnico_social",      ← Icono azul para este
      "creado_en": "2024-01-16T14:20:00"
    },
    ... (más items)
  ]
}
```

---

## 5. Componentes Visuales en el Mapa

```
Mapa de Leaflet
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   🌍 [zoom controls]                                        │
│                                                              │
│   ┌─ Punto A                                               │
│   │  🌱 Sembrador Productivo (verde)                       │
│   │    ├─ ID: 1                                            │
│   │    ├─ Técnico: Juan                                    │
│   │    └─ Comunidad: La Esperanza                          │
│   │                                                         │
│   ├─ Punto B                                               │
│   │  👥 Sembrador Social (azul)                            │
│   │    ├─ ID: 2                                            │
│   │    ├─ Técnico: María                                   │
│   │    └─ Comunidad: El Carmen                             │
│   │                                                         │
│   │                                                         │
│   │         [Pan around map]                               │
│   │                                                         │
│   │                                                         │
│   └─ [Zoom in/out]                                         │
│                                                              │
│   ┌────────────────────── Leyenda ──────────────┐          │
│   │                                             │          │
│   │ ● Ambiental     [capas temáticas]         │          │
│   │ ● Productiva                              │          │
│   │ ● Social                                  │          │
│   │ ● Infraestructura                         │          │
│   │ ─────────────────────────────────────────  │          │
│   │ 🌱 Sembrador Productivo                   │          │
│   │ 👥 Sembrador Social                       │          │
│   │ ─────────────────────────────────────────  │          │
│   │ ☑ Mostrar sembradores (5)  [clickeable]  │          │
│   │                                             │          │
│   └─────────────────────────────────────────────┘          │
│                                                              │
└──────────────────────────────────────────────────────────────┘

Cuando haces click en 🌱 o 👥:

┌─────────────────────────────┐
│ 🌱 Sembrador Productivo    │
├─────────────────────────────┤
│ Nombre: Juan Pérez          │
│ Comunidad: La Esperanza     │
│ Cultivo: Maíz               │
│ Técnico: Juan Pérez         │
│ Ubicación: -33.87, -51.21   │
└─────────────────────────────┘
```

---

## 6. Flujo de Filtrado por Rol - Ejemplo Concreto

```
Base de datos (12 sembradores):
├─ Sembrador 1 (user_id=5, tecnico_productivo)
├─ Sembrador 2 (user_id=5, tecnico_productivo)
├─ Sembrador 3 (user_id=5, tecnico_productivo)
├─ Sembrador 4 (user_id=6, tecnico_social)
├─ Sembrador 5 (user_id=6, tecnico_social)
├─ Sembrador 6 (user_id=7, tecnico_productivo)
├─ Sembrador 7 (user_id=7, tecnico_productivo)
├─ Sembrador 8 (user_id=8, tecnico_social)
├─ Sembrador 9 (user_id=9, tecnico_productivo)
├─ Sembrador 10 (user_id=9, tecnico_productivo)
├─ Sembrador 11 (user_id=10, tecnico_social)
└─ Sembrador 12 (user_id=10, tecnico_social)

Jerarquía de usuarios:
    Admin (id=1)
    ├─ Territorial (id=2)
    │  ├─ Facilitador A (id=3)
    │  │  ├─ Técnico Juan (id=5) → Sembradores: 1,2,3
    │  │  └─ Técnico María (id=6) → Sembradores: 4,5
    │  │
    │  └─ Facilitador B (id=4)
    │     └─ Técnico Pedro (id=7) → Sembradores: 6,7
    │
    ├─ Territorial (id=11) [diferente]
    │  └─ Facilitador (id=12)
    │     ├─ Técnico (id=8) → Sembradores: 8
    │     ├─ Técnico (id=9) → Sembradores: 9,10
    │     └─ Técnico (id=10) → Sembradores: 11,12

Resultados por rol:
───────────────────

1️⃣ Admin (id=1) abre mapa
   → Ve: [1,2,3,4,5,6,7,8,9,10,11,12]  (12 total)
   → Tooltip: "Mostrar sembradores (12)"

2️⃣ Territorial-1 (id=2) abre mapa
   → Subordinados: Facilitador A (3), Facilitador B (4)
   → Ve: [1,2,3,4,5,6,7]  (7 total)
   → Tooltip: "Mostrar sembradores (7)"

3️⃣ Facilitador A (id=3) abre mapa
   → Técnicos: Juan (5), María (6)
   → Ve: [1,2,3,4,5]  (5 total)
   → Tooltip: "Mostrar sembradores (5)"

4️⃣ Técnico Juan (id=5) abre mapa
   → Solo propios (user_id=5)
   → Ve: [1,2,3]  (3 total)
   → Tooltip: "Mostrar sembradores (3)"

5️⃣ Técnico Pedro (id=7) abre mapa
   → Solo propios (user_id=7)
   → Ve: [6,7]  (2 total)
   → Tooltip: "Mostrar sembradores (2)"

6️⃣ Territorial-2 (id=11) abre mapa
   → Subordinados: Facilitador (12)
   → Ve: [8,9,10,11,12]  (5 total)
   → Tooltip: "Mostrar sembradores (5)"

7️⃣ Técnico (id=8) sin sembradores abre mapa
   → Solo propios: ninguno
   → Ve: []  (0 total)
   → Tooltip: "Mostrar sembradores (0)"
```

---

## 7. Selector de Íconos - Decision Tree

```
¿Qué ícono mostrar?
│
├─ Verificar: sembrador.tecnico_rol
│
├─ Contiene "social" (case-insensitive)?
│  │
│  ├─ "tecnico_social" → Ícono AZUL 👥
│  ├─ "tecnico_social_v2" → Ícono AZUL 👥
│  ├─ "SOCIAL" → Ícono AZUL 👥
│  │
│  └─ SI → Retorna: sembradorSocialIcon
│
└─ Sino → Ícono VERDE 🌱
   │
   ├─ "tecnico_productivo" → Ícono VERDE 🌱
   ├─ "tecnico_productivo_v2" → Ícono VERDE 🌱
   ├─ "PRODUCTIVO" → Ícono VERDE 🌱
   ├─ Null/undefined → Ícono VERDE 🌱
   │
   └─ Retorna: sembradorProductivoIcon

Implementación:
───────────────
const getIconSembrador = (s) => {
  if (s.tecnico_rol?.toLowerCase().includes('social')) {
    return sembradorSocialIcon  // Azul
  }
  return sembradorProductivoIcon  // Verde (default)
}
```

---

## 8. Ciclo de Vida del Componente

```
Creation
───────
  new MapaView()

        ↓

Setup Phase
──────────
  const sembradores = ref([])
  const mostrarSembradores = ref(true)
  const contadorSembradores = computed(...)
  const getSembradoresMapa = async () => { ... }
  const getIconSembrador = (s) => { ... }

        ↓

Template Compiled
────────────────
  Vue compila el template de MapaView
  Registra event listeners
  Prepara directivas (v-for, v-if, v-model)

        ↓

onMounted Hook
──────────────
  loadLayers()          // Capas temáticas existentes
  getSembradoresMapa()  // Carga sembradores del backend

        │ API Request
        │ GET /sembradores/map
        ▼

Data Available
──────────────
  sembradores.value = [array de objetos]
  contadorSembradores = computed actualiza → N
  Template reactivamente re-renderiza

        ▼

Rendering Complete
──────────────────
  <l-marker v-for="s in sembradores...">
  Leaflet renderiza marcadores
  Leyenda actualizada con contador
  Checkbox habilitado

        ▼

User Interaction (ongoing)
──────────────────────────
  ├─ Click marca → popup
  ├─ Click leyenda → legend action
  ├─ Click checkbox → toggle mostrarSembradores
  ├─ Zoom/pan → mapa interactivo
  └─ Close popup → vuelve a estado anterior

        ▼

Unmounted (when leaving page)
────────────────────────────
  API requests se limpian
  Event listeners se detachen
  Componente se destruye
```

---

## 9. Caso de Error - Error Handling Flow

```
getSembradoresMapa() called
        │
        ▼
Try to Fetch API
        │
        ├─ Network Error
        │  ├─ Backend no responde
        │  └─ catch (error)
        │     └─ console.error("Error cargando sembradores:", error)
        │        └─ sembradores.value = []  (vacío)
        │
        ├─ 401 Unauthorized
        │  ├─ Token inválido/expirado
        │  └─ Backend devuelve: {"detail": "Usuario no encontrado"}
        │     └─ catch (error)
        │        └─ Frontend: mostrará (0) sembradores
        │
        ├─ 400 Bad Request
        │  ├─ Error base de datos
        │  └─ Backend devuelve: {"detail": "Error: [mensaje]"}
        │     └─ Frontend: mostrará (0) sembradores
        │
        └─ 200 OK
           ├─ Response: {success: true, items: [...]}
           └─ sembradores.value = items
              └─ Renderiza marcadores ✓

En todos los casos:
- No se interrumpe la UI
- Usuario ve página pero sin marcadores (o con los anteriores)
- DevTools Console muestra el error (para debug)
- No se expone datos sensibles al usuario final
```

---

## 10. Performance Timeline

```
Timeline de Carga:
────────────────

0ms     ├─ Usuario navega a /mapa
        │
50ms    ├─ MapaView.vue carga
        │  └─ Script setup ejecuta
        │
100ms   ├─ Template compila
        │  └─ Leaflet inicializa
        │
150ms   ├─ onMounted hook
        │  ├─ loadLayers() inicia
        │  └─ getSembradoresMapa() inicia
        │
200ms   ├─ loadLayers() completa (+capas temáticas)
        │
250ms   ├─ API request enviado
        │  └─ GET /sembradores/map con token
        │
300ms   ├─ [Backend processing]
        │  ├─ Validar JWT
        │  ├─ Filtrar por rol (BD query)
        │  └─ Formatear response
        │
350ms   ├─ [Network latency]
        │
400ms   ├─ API response recibida
        │  └─ JSON parsed
        │
450ms   ├─ Frontend actualiza refs
        │  ├─ sembradores.value = items
        │  └─ contadorSembradores recalcula
        │
500ms   ├─ Markers renderizados
        │  ├─ Leaflet dibuja 5 marcadores (en ejemplo)
        │  └─ Popups disponibles
        │
550ms   ├─ Leyenda actualiza
        │  └─ Contador muestra "Mostrar sembradores (5)"
        │
600ms   ├─ UI totalmente interactiva ✓
        │  └─ Usuario puede:
        │     ├─ Click marcadores
        │     ├─ Toggle checkbox
        │     ├─ Pan/zoom
        │     └─ Leer popups
        │
        └─ Total carga: ~600ms (bueno)

Performance por operación:
──────────────────────────
Operación               | Tiempo
────────────────────────|────────
Toggle checkbox         | 0-50ms
Abrir popup            | 50-100ms
Zoom mapa              | 0-200ms (depende GPU)
Pan mapa               | 0-200ms
Cargar 100 sembradores | 300-600ms
API latency (10 items) | 50-150ms
```

---

## 11. Interacciones Usuario

```
Usuario en Mapa
───────────────

Acción 1: Ver marcadores
    Usuario abre página /mapa
    └─ Automáticamente se cargan sembradores
    └─ Marcadores aparecen en mapa

Acción 2: Inspeccionar sembrador
    Usuario hace click en marcador 🌱
    └─ Popup abre en ubicación
    └─ Muestra 5 campos de información
    └─ Usuario lee datos
    └─ Usuario hace click fuera para cerrar

Acción 3: Filtrar por tipo
    Usuario ve checkbox "Mostrar sembradores"
    └─ Puede hacer click para desmarcar
    └─ Todos marcadores desaparecen
    └─ Mapa se ve limpio
    └─ Contador sigue igual: "(5)"
    └─ Click nuevamente para mostrar

Acción 4: Navegar mapa
    Usuario usa controles de zoom/pan
    └─ Scroll up/down = zoom
    └─ Click+drag = pan
    └─ Doble click = zoom center
    └─ Marcadores se adaptan

Acción 5: Cambiar usuario (login diferente)
    Usuario hace logout → login como otro rol
    └─ Navega a /mapa nuevamente
    └─ API filtra datos según nuevo rol
    └─ Ve menos (o más) sembradores
    └─ Marcadores diferentes

Acción 6: Crear nuevo sembrador (en SembradoresView)
    Usuario crea sembrador
    └─ Vuelve a /mapa
    └─ Nuevo marcador NO aparece automáticamente
    └─ Necesita F5 para recargar
    └─ O: Implementar websockets para real-time

Acción 7: Dispositivo móvil
    Usuario abre en tablet/phone
    └─ Mapa ocupa pantalla
    └─ Tap en marcador abre popup
    └─ Legends más compacta
    └─ Checkbox aún funciona
    └─ Todo responsive
```

---

**Fin de Diagramas & Flujos Visuales**

*Estos diagramas son de referencia para entender la arquitectura y flujos del módulo.*

