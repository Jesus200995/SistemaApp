import { registerSW } from 'virtual:pwa-register'

// Solo registrar el SW si estamos en un entorno que lo soporta
const updateSW = registerSW({
  immediate: true,
  onNeedRefresh() {
    console.log('🔄 Nueva versión disponible')
    // Actualizar automáticamente sin preguntar en desarrollo
    if (import.meta.env.DEV) {
      window.location.reload()
    } else if (confirm('🔄 Hay una nueva versión disponible. ¿Actualizar ahora?')) {
      updateSW(true)
    }
  },
  onOfflineReady() {
    console.log('📡 App lista para funcionar sin conexión')
  },
  onRegistered(registration) {
    console.log('✅ Service Worker registrado correctamente')
  },
  onRegisterError(error) {
    // En desarrollo, los errores de SW son normales debido a HMR
    if (import.meta.env.DEV) {
      console.debug('⚠️ SW no registrado (normal en desarrollo):', error?.message || error)
    } else {
      console.error('❌ Error al registrar SW:', error)
    }
  },
})
