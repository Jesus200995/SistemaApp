// Registro de Service Worker para PWA
// Solo registrar en producción o si está disponible

const registerServiceWorker = async () => {
  // Verificar si el navegador soporta Service Workers
  if (!('serviceWorker' in navigator)) {
    console.log('⚠️ Service Workers no soportados en este navegador')
    return
  }

  // Solo registrar en producción (HTTPS) o localhost
  const isLocalhost = Boolean(
    window.location.hostname === 'localhost' ||
    window.location.hostname === '[::1]' ||
    window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/)
  )

  const isProduction = window.location.protocol === 'https:'

  if (!isProduction && !isLocalhost) {
    console.log('⚠️ PWA solo funciona en HTTPS o localhost')
    return
  }

  try {
    // Intentar importar el registro de PWA de Vite
    const { registerSW } = await import('virtual:pwa-register')
    
    const updateSW = registerSW({
      immediate: true,
      onNeedRefresh() {
        console.log('🔄 Nueva versión disponible')
        // Actualizar automáticamente sin preguntar
        updateSW(true)
      },
      onOfflineReady() {
        console.log('📡 App lista para funcionar sin conexión')
      },
      onRegistered(registration) {
        console.log('✅ Service Worker registrado correctamente')
        // Verificar actualizaciones cada hora
        if (registration) {
          setInterval(() => {
            registration.update()
          }, 60 * 60 * 1000)
        }
      },
      onRegisterError(error) {
        console.warn('⚠️ Error registrando Service Worker:', error)
      }
    })
  } catch (error) {
    // Si falla el registro de PWA de Vite, usar registro manual
    console.warn('⚠️ PWA plugin no disponible, usando fallback:', error.message)
    
    try {
      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/',
        updateViaCache: 'none'
      })
      console.log('✅ Service Worker registrado (fallback):', registration.scope)
    } catch (swError) {
      console.warn('⚠️ No se pudo registrar Service Worker:', swError.message)
    }
  }
}

// Ejecutar cuando la página esté lista
if (document.readyState === 'complete') {
  registerServiceWorker()
} else {
  window.addEventListener('load', registerServiceWorker)
}
