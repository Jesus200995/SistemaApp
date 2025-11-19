# 🌿 Animación de Carga en LoginView

## Descripción
Se agregó una animación de carga con una flor verde girando que aparece cuando el usuario presiona el botón "Iniciar Sesión". La animación se muestra durante 1.5 segundos y luego se desvanece para acceder al dashboard.

## Cambios Realizados

### Template (Nueva Animación)
```vue
<!-- Animación de carga con flor girando -->
<transition name="fade-loading">
  <div v-if="isLoading" class="loading-overlay">
    <div class="loading-container">
      <svg class="rotating-flower" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <!-- Tallo -->
        <line x1="100" y1="100" x2="100" y2="30" stroke="#22C55E" stroke-width="3" stroke-linecap="round"/>
        
        <!-- Pétalos de flor (8 pétalos) -->
        <circle cx="100" cy="30" r="12" fill="#10B981" class="petal" style="transform-origin: 100px 100px"/>
        <!-- ... más pétalos ... -->
        
        <!-- Centro de la flor -->
        <circle cx="100" cy="100" r="16" fill="#FCD34D"/>
      </svg>
      <p class="loading-text">Cargando...</p>
    </div>
  </div>
</transition>
```

### Script
```typescript
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  try {
    const ok = await auth.login(email.value, password.value)
    if (ok) {
      // Esperar 1.5 segundos para que la animación sea visible
      await new Promise(resolve => setTimeout(resolve, 1500))
      router.push('/dashboard')
    }
  } finally {
    isLoading.value = false
  }
}
```

### CSS Estilos Principales

#### Overlay de Carga
- **Posición**: Fixed, cubre toda la pantalla
- **Fondo**: Rgba oscuro con backdrop blur (4px)
- **Z-index**: 9999 (por encima de todo)

#### SVG Flor Girando
```css
.rotating-flower {
  width: 80px;
  height: 80px;
  animation: rotate-flower 3s linear infinite;
}

@keyframes rotate-flower {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

#### Texto "Cargando..."
```css
.loading-text {
  color: #22C55E;
  font-size: 1.125rem;
  font-weight: 500;
  letter-spacing: 1px;
  animation: pulse-text 1.5s ease-in-out infinite;
}

@keyframes pulse-text {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

#### Transición de Fade
```css
.fade-loading-enter-active,
.fade-loading-leave-active {
  transition: opacity 0.3s ease;
}

.fade-loading-enter-from,
.fade-loading-leave-to {
  opacity: 0;
}
```

### Responsividad
La animación se ajusta en todos los breakpoints:
- **Desktop (>1024px)**: 80px de flor
- **Tablet (768px)**: 65px de flor
- **Mobile (640px)**: 60px de flor
- **Small Mobile (480px)**: 55px de flor
- **Tiny (320px)**: 50px de flor

## Características

✅ **Flor Verde Girando**: Animación suave de 3 segundos en rotación continua
✅ **Texto Pulsante**: "Cargando..." con efecto de fade in/out
✅ **Overlay Oscuro**: Fondo semi-transparente que bloquea interacción
✅ **Transición Suave**: Fade in/out de 0.3 segundos
✅ **Duración Total**: 1.5 segundos visible antes de navegar
✅ **Completamente Responsiva**: Se ajusta a todos los tamaños de pantalla
✅ **Sin Errores**: Validado sin errores de sintaxis

## Flujo de Login

1. Usuario ingresa credenciales
2. Usuario presiona "Iniciar Sesión"
3. `isLoading.value = true` → Aparece animación
4. Se envía solicitud de login
5. Se espera 1.5 segundos
6. Si login es exitoso, navega a `/dashboard`
7. `isLoading.value = false` → Desaparece animación

## Colores Utilizados

- **Flor**: Verde oscuro (#10B981)
- **Tallo**: Verde claro (#22C55E)
- **Centro**: Amarillo (#FCD34D)
- **Fondo Overlay**: Negro semi-transparente (rgba(15, 23, 42, 0.95))
- **Texto**: Verde (#22C55E)

## Animaciones Aplicadas

### Rotate Flower (3 segundos)
- Rotación continua de 0° a 360°
- Timing: linear para rotación uniforme
- Infinita

### Pulse Text (1.5 segundos)
- Fade in/out continuo
- Timing: ease-in-out para efecto suave
- Infinita

### Fade Loading (0.3 segundos)
- Entrada y salida del overlay
- Transición suave de opacidad
- Vue transition component

## Archivo Modificado
- `LoginView.vue`: +150 líneas de código (template, script, CSS)

## Próximos Pasos
- Probar en navegador en diferentes dispositivos
- Ajustar duración de la animación si es necesario
- Considerar agregar animación similar en RegisterView si lo requiere
