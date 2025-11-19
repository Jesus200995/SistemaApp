# 🔧 Configuración del Favicon - Referencia Rápida

## ¿Dónde está todo?

### Archivos del Favicon
```
/public/
├── favicon.svg              ← SVG animado (principal)
├── favicon.png              ← PNG 16x16, 32x32, 64x64
├── favicon-32.png           ← PNG 32x32
├── favicon-64.png           ← PNG 64x64
├── pwa-192x192.png          ← PNG 192x192
├── pwa-512x512.png          ← PNG 512x512
├── pwa-192x192-maskable.png ← Adaptive icon
├── pwa-512x512-maskable.png ← Adaptive icon
└── manifest.json            ← PWA manifest actualizado
```

### Código Frontend
```
/src/
├── composables/
│   └── useFaviconAnimation.ts   ← Lógica de animación
├── components/
│   └── FaviconManager.vue       ← Componente gestor
├── assets/
│   └── favicon-animations.css   ← Estilos de animación
└── App.vue                      ← Incluye FaviconManager

/index.html                       ← Referencias del favicon
```

### Scripts
```
/generate-favicon.js          ← Generador de iconos
```

## 📝 HTML (index.html)

```html
<!-- Icons -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/pwa-192x192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/pwa-512x512.png">
```

## 🎨 SVG del Favicon (public/favicon.svg)

```xml
<!-- Celular azul marino con ubicación verde pulsante -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <!-- Animaciones CSS -->
  <defs>
    <style>
      @keyframes pulse {
        0% { r: 8; opacity: 0.8; }
        50% { r: 14; opacity: 0.4; }
        100% { r: 8; opacity: 0.8; }
      }
    </style>
  </defs>
  
  <!-- Fondo azul marino -->
  <rect width="64" height="64" fill="#001a4d" rx="8"/>
  
  <!-- Cuerpo del celular -->
  <rect x="20" y="8" width="24" height="48" rx="3" fill="#001f5e" stroke="#0066cc"/>
  
  <!-- Ubicación verde pulsante -->
  <g transform="translate(32, 32)">
    <circle class="location-pulse" cx="0" cy="-12" r="3" fill="#22c55e"/>
    <path d="..." fill="#22c55e"/> <!-- Gota de ubicación -->
  </g>
</svg>
```

## 📦 Package.json - Scripts

```json
"scripts": {
  "dev": "npm run generate-favicon && vite",
  "build": "npm run generate-favicon && run-p type-check \"build-only {@}\" --",
  "generate-favicon": "node generate-favicon.js"
}
```

## 🎯 Composable (src/composables/useFaviconAnimation.ts)

```typescript
export function useFaviconAnimation() {
  return {
    notifyWithFavicon(count: number),      // Animar + badge
    updateNotificationBadge(count: number), // Solo actualizar badge
    startFaviconAnimation(),                 // Iniciar animación
    stopFaviconAnimation()                  // Detener animación
  }
}
```

## 📱 Componente (src/components/FaviconManager.vue)

```vue
<template>
  <div class="favicon-manager"></div>
</template>

<script setup lang="ts">
import { useFaviconAnimation } from '@/composables/useFaviconAnimation'

// Global access via window.faviconManager
window.faviconManager = {
  notifyWithFavicon,
  updateNotificationBadge
}
</script>
```

## 🎨 Estilos (src/assets/favicon-animations.css)

```css
@keyframes faviconPulse {
  0% { filter: drop-shadow(0 0 0px rgba(34, 197, 94, 0.8)); }
  50% { filter: drop-shadow(0 0 6px rgba(34, 197, 94, 0.4)); }
  100% { filter: drop-shadow(0 0 0px rgba(34, 197, 94, 0.8)); }
}

@keyframes faviconBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}
```

## 🚀 Flujo de Ejecución

### En Desarrollo
```
npm run dev
    ↓
npm run generate-favicon
    ↓
node generate-favicon.js (genera PNGs desde SVG)
    ↓
vite (inicia servidor)
    ↓
http://localhost:5175/
    ↓
¡Ve el favicon en la pestaña!
```

### En Build
```
npm run build
    ↓
npm run generate-favicon
    ↓
vue-tsc --build (type check)
    ↓
vite build (compilar)
    ↓
/dist/ (archivos listos para producción)
```

## 🌈 Colores Utilizados

| Elemento | Color | Código |
|----------|-------|--------|
| Fondo | Negro | #000000 |
| Celular | Azul Marino | #001f5e |
| Marco | Azul Claro | #0066cc |
| Ubicación | Verde Brillante | #22c55e |
| Pantalla | Azul Oscuro | #001a3d |

## 🔄 Cómo Regenerar los Iconos

```bash
# Manual
node generate-favicon.js

# Con npm
npm run generate-favicon

# Automático (al hacer dev o build)
npm run dev
npm run build
```

## 🧪 Testing en Navegador

1. Abre DevTools (F12)
2. Pestaña Network
3. Recarga la página
4. Busca `favicon.svg` - debe estar en 200 OK
5. Mira la pestaña - ¡debe verse el ícono!

## 🐛 Troubleshooting

| Problema | Solución |
|----------|----------|
| No se ve el favicon | Limpiar caché (Ctrl+Shift+Del) + Hard Refresh (Ctrl+Shift+R) |
| Ícono de Vue sigue apareciendo | Verificar que no hay otro favicon en index.html |
| Animación no funciona | Verificar que favicon-animations.css esté importado en main.ts |
| PNGs no se generan | Ejecutar `npm run generate-favicon` manualmente |

## ✅ Checklist de Verificación

- [x] SVG creado y animado
- [x] PNGs generados automáticamente
- [x] HTML configurado con referencias
- [x] Manifest actualizado
- [x] Componente integrado en App.vue
- [x] Estilos importados en main.ts
- [x] Servidor iniciado
- [x] Favicon visible en navegador
- [x] No hay ícono de Vue
- [x] Animación funcionando

---

**Sistema de Favicon: ✅ 100% Operativo**
