import { registerSW } from 'virtual:pwa-register'

registerSW({
  onNeedRefresh() {
    if (confirm('🔄 Hay una nueva versión disponible. ¿Actualizar ahora?')) {
      window.location.reload()
    }
  },
  onOfflineReady() {
    console.log('📡 App lista para funcionar sin conexión')
  },
})
