# 🏛️ DIAGRAMA DE JERARQUIZACIÓN IMPLEMENTADA

**Documento de referencia visual para la arquitectura de roles y permisos**

---

## 📊 ESTRUCTURA JERÁRQUICA

```
┌─────────────────────────────────────────────────────────────────┐
│                     SISTEMA DE ADMINISTRACIÓN                   │
│                   (Jerarquía de 5 Niveles)                      │
└─────────────────────────────────────────────────────────────────┘

                         NIVEL 0: ADMIN
                    (Coordinador Nacional)
                              │
                              │ Crea
                              ▼
        ┌─────────────────────────────────────────┐
        │   NIVEL 1: TERRITORIAL                  │
        │   (Responsable Regional)                │
        │   - Ve: Todos los subordinados          │
        │   - Puede: Crear Facilitadores          │
        └─────────────────────────────────────────┘
                              │
                              │ Crea
                              ▼
        ┌─────────────────────────────────────────┐
        │   NIVEL 2: FACILITADOR                  │
        │   (Coordinador Local)                   │
        │   - Ve: Sus técnicos                    │
        │   - Puede: Crear Técnicos               │
        └─────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    │ Crea              │ Crea
                    ▼                   ▼
    ┌───────────────────────────┐   ┌────────────────────────────┐
    │ NIVEL 3: TÉCNICO          │   │ NIVEL 3: TÉCNICO           │
    │ PRODUCTIVO                │   │ SOCIAL                     │
    │ (Técnico de Campo)        │   │ (Técnico Social)           │
    │                           │   │                            │
    │ - Ve: Sembradores propios │   │ - Ve: Sembradores propios  │
    │ - Puede: Crear            │   │ - Puede: Crear             │
    │   Seguimientos productivos│   │   Seguimientos sociales    │
    │ - Acceso: Capas           │   │ - Acceso: Capas            │
    │   Productivas             │   │   Sociales                 │
    │ - NO ve capas sociales    │   │ - NO ve capas productivas  │
    └───────────────────────────┘   └────────────────────────────┘
```

---

## 🔐 MATRIZ DE PERMISOS COMPLETA

### Operaciones por Rol

```
┌──────────────┬────────┬───────┬─────────┬──────────────┬───────────┐
│ Operación    │ Admin  │ Terr  │ Facil   │ Tec. Prod    │ Tec. Soc  │
├──────────────┼────────┼───────┼─────────┼──────────────┼───────────┤
│ Ver Todo     │   ✅   │  ❌   │  ❌     │     ❌       │    ❌     │
│ Ver Subordin │   ✅   │  ✅   │  ✅     │     ❌       │    ❌     │
│ Ver Propios  │   ✅   │  ✅   │  ✅     │     ✅       │    ✅     │
│ Crear Terr   │   ✅   │  ❌   │  ❌     │     ❌       │    ❌     │
│ Crear Facil  │   ❌   │  ✅   │  ❌     │     ❌       │    ❌     │
│ Crear Téc    │   ❌   │  ❌   │  ✅     │     ❌       │    ❌     │
│ Crear Semb   │   ✅   │  ✅   │  ✅     │     ✅       │    ✅     │
│ Editar Propio│   ✅   │  ✅   │  ✅     │     ✅       │    ✅     │
│ Editar Otros │   ✅   │  ❌   │  ❌     │     ❌       │    ❌     │
│ Eliminar Pro │   ✅   │  ✅   │  ✅     │     ✅       │    ✅     │
│ Eliminar Otr │   ✅   │  ❌   │  ❌     │     ❌       │    ❌     │
│ Ver Reportes │   ✅   │  ✅   │  ✅     │     ❌       │    ❌     │
│ Crear Solici │   ✅   │  ✅   │  ✅     │     ✅       │    ✅     │
│ Aprobar Soli │   ✅   │  ✅   │  ✅     │     ❌       │    ❌     │
└──────────────┴────────┴───────┴─────────┴──────────────┴───────────┘
```

**Leyenda:**
- ✅ = Permitido
- ❌ = No permitido
- Terr = Territorial
- Facil = Facilitador
- Tec. Prod = Técnico Productivo
- Tec. Soc = Técnico Social

---

## 📱 VISIBILIDAD EN INTERFAZ (Dashboard + Navbar)

### Dashboard - Módulos Especializados

```
┌─────────────────────────────────────────────────────┐
│              DASHBOARD - Módulos Especializados     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ✅ Seguimiento de Campo              [Ver módulo] │
│     Visible para: Técnico Productivo, Técnico Social│
│                  (No visible para otros)            │
│                                                      │
│  ✅ Sembradores en Mapa               [Ver módulo] │
│     Visible para: TODOS               <-- Público  │
│                                                      │
│  ✅ Reportes y Estadísticas           [Ver módulo] │
│     Visible para: Admin, Territorial, Facilitador  │
│                  (No visible para Técnicos)        │
│                                                      │
│  ✅ Solicitudes Jerárquicas           [Ver módulo] │
│     Visible para: TODOS               <-- Público  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Navbar - Opciones de Navegación

```
┌──────────────────────────────────────────────────────┐
│   NAVBAR - Enlaces Principales                      │
├──────────────────────────────────────────────────────┤
│                                                       │
│  Visible para TODOS:                                 │
│  • Inicio (Home)                                     │
│  • Mapa                                              │
│  • Chat                                              │
│  • Sembradores                                       │
│                                                       │
│  Visible SOLO para Técnicos:                         │
│  • Seguimiento                                       │
│                                                       │
│  Visible para Admin, Territorial, Facilitador:       │
│  • Usuarios                                          │
│                                                       │
└──────────────────────────────────────────────────────┘
```

---

## 🗺️ FLUJO DE ACCESO A SEMBRADORES

```
┌──────────────┐
│ Usuario      │
│ autenticado  │
└────────┬─────┘
         │
         │ Solicita: GET /sembradores/
         │
         ▼
┌──────────────────────────────────┐
│ Backend obtiene JWT Token        │
│ Extrae: user_id, rol             │
└────────┬─────────────────────────┘
         │
         ├─── rol = "admin"?
         │       ├─ SÍ → Devuelve TODO ✅
         │       └─ NO → Sigue verificando
         │
         ├─── rol = "territorial"?
         │       ├─ SÍ → Filtra por subordinados directos ✅
         │       └─ NO → Sigue verificando
         │
         ├─── rol = "facilitador"?
         │       ├─ SÍ → Filtra por técnicos subordinados ✅
         │       └─ NO → Sigue verificando
         │
         ├─── rol contiene "tecnico"?
         │       ├─ SÍ → Devuelve solo propios ✅
         │       └─ NO → Error 403 ❌
         │
         ▼
    Frontend recibe solo datos permitidos
    y los muestra en tabla/mapa ✅
```

---

## 🔒 FILTRADO POR ESPECIALIDAD (Técnicos)

```
┌────────────────────────────────────────────────┐
│   TÉCNICO_PRODUCTIVO                           │
├────────────────────────────────────────────────┤
│                                                 │
│  Dashboard:                                     │
│  ✅ Ve botón "Seguimiento de Campo"            │
│  ✅ Ve módulo "Sembradores en Mapa"            │
│  ❌ NO ve "Reportes y Estadísticas"            │
│                                                 │
│  Sembradores:                                   │
│  ✅ Ve solo sus sembradores                    │
│  ✅ Puede crear seguimientos productivos       │
│  ❌ NO puede crear seguimientos sociales       │
│                                                 │
│  Mapa - Capas temáticas:                       │
│  ✅ Ve capa "Ambiental"                        │
│  ✅ Ve capa "Productiva"                       │
│  ❌ NO ve capa "Social"                        │
│  ✅ Ve capa "Infraestructura"                  │
│                                                 │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│   TÉCNICO_SOCIAL                               │
├────────────────────────────────────────────────┤
│                                                 │
│  Dashboard:                                     │
│  ✅ Ve botón "Seguimiento de Campo"            │
│  ✅ Ve módulo "Sembradores en Mapa"            │
│  ❌ NO ve "Reportes y Estadísticas"            │
│                                                 │
│  Sembradores:                                   │
│  ✅ Ve solo sus sembradores                    │
│  ✅ Puede crear seguimientos sociales          │
│  ❌ NO puede crear seguimientos productivos    │
│                                                 │
│  Mapa - Capas temáticas:                       │
│  ✅ Ve capa "Ambiental"                        │
│  ✅ Ve capa "Social"                           │
│  ❌ NO ve capa "Productiva"                    │
│  ✅ Ve capa "Infraestructura"                  │
│                                                 │
└────────────────────────────────────────────────┘
```

---

## 📊 NIVELES DE VALIDACIÓN

### 4 Capas de Defensa (Defense in Depth)

```
┌─────────────────────────────────────────────┐
│   CAPA 1: FRONTEND (Navbar/Rutas)           │
│   ─────────────────────────────────────────│
│   • Valida si usuario está autenticado      │
│   • Muestra/oculta opciones de menú         │
│   • Previene acceso directo a URLs          │
│   • UX mejorado: menos confusión            │
│                                             │
│   Tecnología: Vue Router + localStorage     │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│   CAPA 2: FRONTEND (Componentes)            │
│   ─────────────────────────────────────────│
│   • Valida rol antes de cargar datos        │
│   • Muestra mensajes de error claros        │
│   • Redirige si acceso denegado             │
│   • Previene llamadas innecesarias a API    │
│                                             │
│   Tecnología: Vue Components + SweetAlert   │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│   CAPA 3: BACKEND (API)                     │
│   ─────────────────────────────────────────│
│   • Valida token JWT                        │
│   • Verifica expiration del token           │
│   • Extrae y valida rol del usuario         │
│   • Filtra datos según jerarquía            │
│   • Rechaza operaciones no permitidas       │
│   • Retorna 403 Forbidden si denegado       │
│                                             │
│   Tecnología: FastAPI + JWT + SQLAlchemy    │
└──────────────┬──────────────────────────────┘
               │
┌──────────────▼──────────────────────────────┐
│   CAPA 4: BASE DE DATOS                     │
│   ─────────────────────────────────────────│
│   • Constraints de integridad               │
│   • Foreign keys con ON DELETE              │
│   • Validación de tipos de datos            │
│   • Auditoría de cambios                    │
│                                             │
│   Tecnología: PostgreSQL + SQLAlchemy ORM   │
└─────────────────────────────────────────────┘
```

---

## 🎯 CASOS DE USO - EJEMPLO PRÁCTICO

### Caso 1: Admin ve todo

```
Admin (ID: 1)
    │
    ├─ Dashboard
    │   └─ Ve todas las opciones ✅
    │
    ├─ Sembradores
    │   └─ Ve TODOS (1000+ registros) ✅
    │       ├─ Del territorial A ✅
    │       ├─ Del territorial B ✅
    │       └─ Del territorial C ✅
    │
    ├─ Usuarios
    │   └─ Ve TODOS (500+ usuarios) ✅
    │       ├─ Todos los territoriales ✅
    │       ├─ Todos los facilitadores ✅
    │       ├─ Todos los técnicos ✅
    │       └─ Todos los sembradores ✅
    │
    ├─ Reportes
    │   └─ Ve estadísticas globales ✅
    │
    └─ Puede
        ├─ Crear Territoriales ✅
        ├─ Editar cualquiera ✅
        ├─ Eliminar cualquiera ✅
        └─ Aprobar todas las solicitudes ✅
```

### Caso 2: Territorial ve subordinados

```
Territorial (ID: 5, responsable de Región Sur)
    │
    ├─ Dashboard
    │   └─ Ve: Sembradores, Usuarios, Reportes ✅
    │
    ├─ Sembradores
    │   └─ Ve solo de sus subordinados ✅
    │       ├─ Facilitador F1 (ID: 8)
    │       │   ├─ Técnico T1 (ID: 12) → Sembradores: 50 ✅
    │       │   └─ Técnico T2 (ID: 13) → Sembradores: 30 ✅
    │       │
    │       └─ Facilitador F2 (ID: 9)
    │           ├─ Técnico T3 (ID: 14) → Sembradores: 45 ✅
    │           └─ Técnico T4 (ID: 15) → Sembradores: 25 ✅
    │
    ├─ Usuarios
    │   └─ Ve: Sus Facilitadores (F1, F2) ✅
    │       NO ve técnicos (backend filtra) ✅
    │
    ├─ Reportes
    │   └─ Ve estadísticas de su región ✅
    │
    ├─ Puede
    │   ├─ Crear Facilitadores ✅
    │   ├─ Editar propios datos ✅
    │   ├─ Eliminar propias solicitudes ✅
    │   └─ Aprobar solicitudes de subordinados ✅
    │
    └─ NO puede
        ├─ Ver la región de otro Territorial ❌
        ├─ Crear Territoriales ❌
        ├─ Crear Técnicos ❌
        └─ Ver reportes globales ❌
```

### Caso 3: Técnico ve solo propios

```
Técnico Productivo (ID: 12, Juan)
    │
    ├─ Dashboard
    │   └─ Ve: Seguimiento, Sembradores, Solicitudes ✅
    │
    ├─ Sembradores
    │   └─ Ve SOLO sus sembradores (50) ✅
    │       ├─ Sembrador 1 (Juan creó)
    │       ├─ Sembrador 2 (Juan creó)
    │       └─ ... 50 más ...
    │       NO ve sembradores de T2 ❌
    │
    ├─ Seguimiento de Campo
    │   └─ Ve solo sus seguimientos ✅
    │       ├─ Seguimiento 1 (productivo) ✅
    │       ├─ Seguimiento 2 (productivo) ✅
    │       └─ NO ve seguimientos sociales ❌
    │
    ├─ Mapa
    │   └─ Ve sus sembradores en capa "Productiva" ✅
    │       NO ve capa "Social" ❌
    │
    ├─ Reportes
    │   └─ NO ve opción ❌
    │       Si intenta acceder: Error 403 ❌
    │
    ├─ Usuarios
    │   └─ NO ve opción ❌
    │
    └─ Puede
        ├─ Crear sembradores (propios) ✅
        ├─ Crear seguimientos productivos ✅
        ├─ Editar propios ✅
        ├─ Eliminar propios ✅
        └─ Crear solicitudes ✅
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

Verificación de que cada componente cumple:

- ✅ **SembradoresView.vue**
  - Backend filtra por jerarquía
  - Frontend confía en backend
  - CRUD validado en API

- ✅ **UsuariosView.vue**
  - Solo puede crear rol subordinado
  - Botón solo visible si puede crear
  - Fallback local + backend

- ✅ **DashboardView.vue**
  - Seguimiento visible solo técnicos
  - Reportes visible solo superiores
  - Sembradores visible todos

- ✅ **Navbar.vue**
  - Seguimiento solo técnicos
  - Usuarios solo superiores
  - Otros disponibles todos

- ✅ **EstadisticasView.vue**
  - Validación en onMounted
  - Error claro si denegado
  - Redirección a dashboard

- ✅ **MapaView.vue**
  - Capas filtradas por rol
  - Sembradores filtrados por jerarquía
  - Backend respeta especialidad

- ✅ **SeguimientoView.vue**
  - Especialización productivo/social
  - Filtrado jerárquico

- ✅ **Router**
  - Middleware de autenticación
  - Protección de rutas
  - Redirección correcta

---

## 📞 REFERENCIAS

**Documentos relacionados:**
- `AUDITORIA_JERARQUIZACION_FRONTEND.md` - Auditoría detallada
- `RESUMEN_CORRECCIONES_AUDITORIA.md` - Cambios implementados
- `DIAGRAMAS_ROLES_TECNICOS.md` - Diagramas técnicos
- `Sistema de administración.pdf` - Especificación original

---

**Última actualización:** 10 de diciembre de 2025  
**Estado:** ✅ IMPLEMENTADO Y AUDITADO
