import { registerSW } from 'virtual:pwa-register'

// Función para limpiar todo el caché
const clearAllCaches = async () => {
  if ('caches' in window) {
    const cacheNames = await caches.keys()
    await Promise.all(cacheNames.map(name => caches.delete(name)))
    console.log('🗑️ Todos los cachés limpiados')
  }
}

// Solo registrar el SW si estamos en un entorno que lo soporta
const updateSW = registerSW({
  immediate: true,
  async onNeedRefresh() {
    console.log('🔄 Nueva versión disponible - Actualizando automáticamente...')
    // Limpiar todos los cachés antes de actualizar
    await clearAllCaches()
    // Actualizar automáticamente SIN preguntar
    updateSW(true)
    // Recargar la página después de un breve delay
    setTimeout(() => {
      window.location.reload()
    }, 500)
  },
  onOfflineReady() {
    console.log('📡 App lista para funcionar sin conexión')
  },
  onRegistered(registration) {
    console.log('✅ Service Worker registrado correctamente')
    // Verificar actualizaciones cada 30 segundos
    setInterval(() => {
      registration.update()
    }, 30000)
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

// Exportar función para limpiar caché manualmente si se necesita
export { clearAllCaches }
