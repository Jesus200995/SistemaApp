# 🎨 Favicon Animado - Guía de Implementación

## Descripción

Se ha implementado un nuevo sistema de favicon personalizado que muestra:
- **Celular azul marino oscuro** (#001f5e) con pantalla
- **Ícono de ubicación verde** (#22c55e) en el centro
- **Animación de pulso** en la ubicación (2 segundos)
- **Animación en las pestañas del navegador** cuando hay notificaciones

## Archivos Creados

### 1. **public/favicon.svg** ✨
SVG animado del favicon con:
- Cuerpo del celular con borde azul marino
- Pantalla oscura con efecto de notch
- Ícono de ubicación verde con animación de pulso
- Pulso decorativo alrededor del ícono

### 2. **generate-favicon.js** 🔧
Script que genera automáticamente los iconos en diferentes tamaños:
- favicon.png (16x16, 32x32, 64x64)
- pwa-192x192.png y pwa-512x512.png
- Variantes maskable para PWA

### 3. **src/composables/useFaviconAnimation.ts** 🎯
Composable Vue 3 que proporciona funciones para:
- `notifyWithFavicon(count)` - Animar favicon con contador
- `updateNotificationBadge(count)` - Actualizar badge de notificaciones
- `startFaviconAnimation()` - Iniciar animación
- `stopFaviconAnimation()` - Detener animación

### 4. **src/components/FaviconManager.vue** 📋
Componente Vue que:
- Gestiona eventos de notificaciones
- Integra animaciones del favicon
- Proporciona interfaz global para acceso desde cualquier parte

### 5. **src/assets/favicon-animations.css** 💫
Estilos CSS con animaciones:
- `faviconPulse` - Pulso de brillo
- `faviconRotate` - Rotación
- `faviconBounce` - Rebote

## Cómo Usar

### Opción 1: Usar desde el Composable
```typescript
import { useFaviconAnimation } from '@/composables/useFaviconAnimation'

export default {
  setup() {
    const { notifyWithFavicon, updateNotificationBadge } = useFaviconAnimation()
    
    // Mostrar 3 notificaciones con animación
    notifyWithFavicon(3)
    
    // Actualizar badge silenciosamente
    updateNotificationBadge(5)
  }
}
```

### Opción 2: Usar desde cualquier parte (window)
```javascript
// En cualquier componente o script
window.faviconManager.notifyWithFavicon(2)
window.faviconManager.updateNotificationBadge(5)
```

### Opción 3: Disparar evento personalizado
```javascript
// Desde componentes o servicios
window.dispatchEvent(new CustomEvent('notification:new', {
  detail: { count: 1 }
}))
```

## Configuración de Build

El archivo `package.json` ha sido actualizado para:
- Ejecutar `generate-favicon` antes de `dev` y `build`
- Instalar dependencia `sharp@0.33` para procesamiento de imágenes

```json
"scripts": {
  "dev": "npm run generate-favicon && vite",
  "build": "npm run generate-favicon && run-p type-check \"build-only {@}\" --"
}
```

## Integración en index.html

Se agregaron referencias al favicon SVG con soporte multi-navegador:

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="192x192" href="/pwa-192x192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/pwa-512x512.png">
```

## Características de Animación

### Pulso de Ubicación
La ubicación verde tiene un efecto de pulso continuo:
- Radio inicial: 8px
- Radio máximo: 14px
- Duración: 2 segundos
- Transparencia: 0.8 → 0.4 → 0.8

### Animación al Recibir Notificaciones
Cuando se recibe una notificación:
1. Se actualiza el título con badge numérico (ej: "(3) SistemaApp...")
2. Se agrega efecto de rebote al body
3. Se produce sonido de notificación (Web Audio API)
4. Se parpadea el ícono en el título por 3 segundos

## Compatibilidad

✅ Chrome/Chromium 90+
✅ Firefox 88+
✅ Safari 15+
✅ Edge 90+
✅ Opera 76+

## Solución de Problemas

### El favicon no aparece
1. Limpiar caché del navegador (Ctrl+Shift+Del)
2. Hard refresh (Ctrl+Shift+R en Chrome)
3. Verificar que `public/favicon.svg` existe

### Las animaciones no funcionan
1. Verificar soporte CSS animations en navegador
2. Revisar que `favicon-animations.css` esté importado en `main.ts`
3. Abrir DevTools y revisar aplicación de estilos

### PWA no muestra los iconos correctamente
1. Ejecutar `npm run generate-favicon` manualmente
2. Limpiar caché de Service Worker
3. Verificar que los archivos PNG existen en `public/`

## Notas Técnicas

- El SVG es escalable a cualquier tamaño
- Las animaciones CSS funcionan sin necesidad de JavaScript
- Compatible con PWA y app installed
- Soporta iconos maskable para adaptive icons en Android 12+
- El sistema de notificaciones es completamente opcional - el favicon se muestra correctamente incluso sin usarlo

## Próximas Mejoras

- [ ] Integrar con NotificationCenter.vue
- [ ] Agregar sonidos de notificación personalizados
- [ ] Implementar diferentes animaciones por tipo de notificación
- [ ] Agregar contador de notificaciones no leídas
- [ ] Crear variantes del favicon para diferentes estados
