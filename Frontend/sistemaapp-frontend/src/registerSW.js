// Registro simple de PWA - Solo en producción
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/sw.js', { scope: '/' })
      .then((registration) => {
        console.log('✅ Service Worker registrado:', registration.scope)
        
        // Verificar actualizaciones
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                console.log('🔄 Nueva versión disponible')
              }
            })
          }
        })
      })
      .catch((error) => {
        console.warn('⚠️ Service Worker no registrado:', error.message)
      })
  })
} else {
  console.log('📱 PWA: Modo desarrollo o SW no soportado')
}
