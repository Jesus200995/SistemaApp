import { ref, onMounted, onUnmounted } from 'vue'

const isUpdateAvailable = ref(false)
const registrations = ref<ServiceWorkerRegistration[]>([])

export function usePWAUpdate() {
  const checkForUpdates = () => {
    if (!('serviceWorker' in navigator)) {
      console.warn('[PWA] Service Workers no soportados')
      return
    }

    navigator.serviceWorker.getRegistrations().then((regs) => {
      console.log('[PWA] Registraciones encontradas:', regs.length)
      registrations.value = [...regs] as ServiceWorkerRegistration[]

      regs.forEach((registration) => {
        // Verificar actualizaciones periódicamente
        registration.addEventListener('updatefound', () => {
          console.log('[PWA] Actualización encontrada')
          const newWorker = registration.installing

          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'activated') {
                console.log('[PWA] Nuevo Service Worker activado')
                isUpdateAvailable.value = true

                // Notificar al modal
                if (window.__updateModal) {
                  window.__updateModal.show({
                    title: '✨ Nueva Versión Disponible',
                    message: 'Se está descargando la actualización...',
                    infoText: 'La app se actualizará automáticamente',
                    showButton: false,
                  })
                }

                // Auto-reload después de 3 segundos
                setTimeout(() => {
                  window.location.reload()
                }, 3000)
              }
            })
          }
        })

        // Verificar actualizaciones manualmente
        registration.update()
      })
    })
  }

  const forceUpdate = () => {
    if (navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'FORCE_UPDATE',
      })
    }

    // También verificar registraciones
    registrations.value.forEach((reg) => {
      reg.update()
    })
  }

  const skipWaiting = () => {
    if (navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'SKIP_WAITING',
      })
    }

    // Recargar después de un breve momento
    setTimeout(() => {
      window.location.reload()
    }, 500)
  }

  const clearCache = () => {
    if (navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'CLEAR_CACHE',
      })
    }
  }

  // Escuchar mensajes del Service Worker
  const handleServiceWorkerMessage = (event: any) => {
    console.log('[PWA] Mensaje del SW:', event.data)

    if (event.data.type === 'UPDATE_AVAILABLE') {
      console.log('[PWA] Actualización disponible')
      isUpdateAvailable.value = true

      // Mostrar modal
      if (window.__updateModal) {
        window.__updateModal.show({
          title: '✨ Nueva Versión',
          message: 'Se está descargando...',
          infoText: 'Actualizando automáticamente',
          showButton: false,
        })
      }
    }

    if (event.data.type === 'SW_ACTIVATED') {
      console.log('[PWA] Service Worker activado:', event.data.version)

      // Mostrar modal de éxito
      if (window.__updateModal) {
        window.__updateModal.show({
          title: '✅ App Actualizada',
          message: 'La aplicación se ha actualizado correctamente',
          infoText: 'Se recargará en 2 segundos...',
          showButton: false,
        })

        // Auto-reload
        setTimeout(() => {
          window.location.reload()
        }, 2000)
      }
    }
  }

  onMounted(() => {
    // Verificar actualizaciones al montar
    checkForUpdates()

    // Escuchar mensajes del Service Worker
    navigator.serviceWorker.addEventListener('message', handleServiceWorkerMessage)

    // Verificar actualizaciones cada minuto
    const updateInterval = setInterval(() => {
      console.log('[PWA] Verificando actualizaciones automáticas...')
      checkForUpdates()
    }, 60000) // Cada minuto

    // Cleanup
    onUnmounted(() => {
      clearInterval(updateInterval)
      navigator.serviceWorker.removeEventListener('message', handleServiceWorkerMessage)
    })
  })

  return {
    isUpdateAvailable,
    checkForUpdates,
    forceUpdate,
    skipWaiting,
    clearCache,
  }
}

// Interfaz global para el modal
declare global {
  interface Window {
    __updateModal?: {
      show: (config: any) => void
      hide: () => void
    }
  }
}
