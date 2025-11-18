# 📊 Dashboard Update - Módulos Especializados

## ✅ Cambios Realizados

Se ha actualizado el archivo `DashboardView.vue` para incluir una nueva sección de **"Módulos Especializados"** con acceso directo a las funcionalidades principales del sistema.

---

## 🎨 Nueva Sección: "Módulos Especializados"

### Ubicación
Debajo de la sección "Acceso Rápido", se agregó una nueva sección con tarjetas grandes y más descriptivas.

### Botones Agregados

#### 1. **📋 Seguimiento de Campo** (Solo Técnicos)
- **Visible para:** `tecnico_productivo` y `tecnico_social`
- **Ruta:** `/seguimiento`
- **Descripción:** "Registrar visitas y avances"
- **Color:** Verde (tema principal)
- **Función:** Acceso al módulo de seguimiento de campo para registrar visitas y progresos

#### 2. **🌱 Sembradores en Mapa** (Todos)
- **Visible para:** Todos los usuarios autenticados
- **Ruta:** `/sembradores`
- **Descripción:** "Gestionar sembradores"
- **Color:** Verde claro
- **Función:** Acceso a la gestión de sembradores en mapa

#### 3. **📊 Reportes y Estadísticas** (Facilitadores, Territoriales, Admins)
- **Visible para:** `facilitador`, `territorial`, `admin`
- **Ruta:** `/estadisticas`
- **Descripción:** "Análisis general"
- **Color:** Azul
- **Función:** Acceso a reportes y análisis de datos

#### 4. **👥 Gestión de Usuarios** (Solo Admins)
- **Visible para:** `admin`
- **Ruta:** `/usuarios`
- **Descripción:** "Administrar usuarios"
- **Color:** Púrpura
- **Función:** Acceso a la gestión de usuarios del sistema

---

## 🎯 Control de Acceso por Rol

| Rol | Seguimiento | Sembradores | Reportes | Usuarios |
|-----|:----------:|:----------:|:--------:|:--------:|
| `tecnico_productivo` | ✅ | ✅ | ❌ | ❌ |
| `tecnico_social` | ✅ | ✅ | ❌ | ❌ |
| `facilitador` | ❌ | ✅ | ✅ | ❌ |
| `territorial` | ❌ | ✅ | ✅ | ❌ |
| `admin` | ❌ | ✅ | ✅ | ✅ |

---

## 🎨 Características del Diseño

### Estilos Aplicados
- ✅ **Glassmorphism:** Fondo translúcido con blur effect
- ✅ **Gradientes:** Colores diferenciados por módulo
- ✅ **Animaciones:** Entrada suave con `v-motion`
- ✅ **Efectos Hover:** 
  - Elevación (translateY)
  - Cambio de color del borde
  - Aumento de sombra
  - Animación de flecha deslizante
- ✅ **Responsive:** Adapta a mobile, tablet y desktop

### Elementos Visuales
- Icono emoji de 2rem en cada tarjeta
- Fondo gradiente con borde semitransparente
- Arrow (→) que aparece al hover
- Efecto de brillo que cruza la tarjeta

---

## 📱 Responsive Design

### Desktop (> 768px)
- Grid de 4 columnas
- Tarjetas grandes y espaciosas

### Tablet (768px)
- Grid adaptativo según contenido visible
- Tarjetas medianas

### Mobile (< 640px)
- Grid de 1 columna
- Tarjetas compactas
- Íconos más pequeños

---

## 🔄 Actualizaciones en Script

### Imports
Se agregó `Sprout` de `lucide-vue-next` para el icono de Sembradores:
```typescript
import { LogOut, User, Mail, LayoutDashboard, BarChart3, Users, Settings, MapPin, Sprout } from 'lucide-vue-next'
```

### Array de Acciones
Se reemplazó "Configuración" por "Sembradores":
```typescript
const actions = [
  { title: 'Usuarios', icon: Users, route: '/usuarios' },
  { title: 'Estadísticas', icon: BarChart3, route: '/estadisticas' },
  { title: 'Mapa', icon: MapPin, route: '/mapa' },
  { title: 'Sembradores', icon: Sprout, route: '/sembradores' },
]
```

### Control de Acceso
Cada botón utiliza `v-if` para mostrar/ocultar según el rol del usuario:
- `auth.user?.rol.includes('tecnico')` - Para técnicos
- `['facilitador', 'territorial', 'admin'].includes(auth.user?.rol)` - Para gestores
- `auth.user?.rol === 'admin'` - Solo admin

---

## 📋 Código Agregado

### Template
```vue
<!-- Sección de módulos especializados -->
<div class="specialized-section">
  <h3 class="section-title">Módulos Especializados</h3>
  
  <div class="specialized-grid">
    <!-- Seguimiento de Campo - Solo técnicos -->
    <router-link
      v-if="auth.user?.rol && (auth.user.rol.includes('tecnico'))"
      to="/seguimiento"
      v-motion
      :initial="{ opacity: 0, y: 30 }"
      :enter="{ opacity: 1, y: 0, transition: { delay: 600, duration: 500 } }"
      class="specialized-card specialized-seguimiento"
    >
      <div class="specialized-icon-wrapper">
        <span class="specialized-icon">📋</span>
      </div>
      <h4 class="specialized-title">Seguimiento de Campo</h4>
      <p class="specialized-desc">Registrar visitas y avances</p>
      <div class="card-arrow">→</div>
    </router-link>
    <!-- ... más tarjetas ... -->
  </div>
</div>
```

### Estilos CSS
Se agregaron estilos para:
- `.specialized-section` - Contenedor de la sección
- `.specialized-grid` - Grid responsivo
- `.specialized-card` - Tarjeta base
- `.specialized-*` (variantes) - Estilos por color para cada módulo
- `.card-arrow` - Animación de flecha

---

## ✨ Animaciones Implementadas

### Entrada de Tarjetas
Cada tarjeta entra con:
- Opacidad: 0 → 1
- Posición Y: 30px → 0
- Duración: 500ms
- Delay escalonado: 600ms, 700ms, 800ms, 900ms

### Hover Effects
- **Elevación:** `translateY(-8px)`
- **Brillo:** Animación de gradiente horizontal
- **Sombra:** Aumento de `box-shadow`
- **Icono:** Escala `1.2`
- **Flecha:** Opacidad y traslación

---

## 🔗 Rutas Verificadas

Todas las rutas están registradas en `src/router/index.ts`:
- ✅ `/seguimiento` → SeguimientoView.vue
- ✅ `/sembradores` → SembradoresView.vue
- ✅ `/estadisticas` → EstadisticasView.vue
- ✅ `/usuarios` → UsuariosView.vue

---

## 🧪 Testing

### Para Técnico Productivo
1. Login con rol `tecnico_productivo`
2. En Dashboard, verás:
   - ✅ Seguimiento de Campo
   - ✅ Sembradores en Mapa
   - ❌ Reportes y Estadísticas (oculto)
   - ❌ Gestión de Usuarios (oculto)

### Para Facilitador
1. Login con rol `facilitador`
2. En Dashboard, verás:
   - ❌ Seguimiento de Campo (oculto)
   - ✅ Sembradores en Mapa
   - ✅ Reportes y Estadísticas
   - ❌ Gestión de Usuarios (oculto)

### Para Admin
1. Login con rol `admin`
2. En Dashboard, verás:
   - ❌ Seguimiento de Campo (oculto)
   - ✅ Sembradores en Mapa
   - ✅ Reportes y Estadísticas
   - ✅ Gestión de Usuarios

---

## 📝 Notas Técnicas

- **Componente:** Vue 3 SFC con `<script setup>`
- **Animaciones:** Utilizan la librería `v-motion`
- **Routing:** `vue-router` con `<router-link>`
- **Iconos:** Lucide Vue Next
- **Auth:** Pinia store `useAuthStore`
- **Responsive:** Media queries CSS nativas

---

## ✅ Estado de Implementación

- ✅ Tarjetas agregadas al template
- ✅ Estilos CSS completos
- ✅ Animaciones implementadas
- ✅ Control de acceso por rol
- ✅ Responsive design
- ✅ Sin errores de compilación
- ✅ Integración con rutas existentes

---

**Última actualización:** 18 de noviembre de 2025
**Archivo modificado:** `src/views/DashboardView.vue`
