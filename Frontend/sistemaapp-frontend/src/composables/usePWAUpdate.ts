import { ref, onMounted, onUnmounted } from 'vue'

const isUpdateAvailable = ref(false)
const registrations = ref<ServiceWorkerRegistration[]>([])
let updateInterval: ReturnType<typeof setInterval> | null = null

export function usePWAUpdate() {
  const checkForUpdates = async () => {
    if (!('serviceWorker' in navigator)) {
      console.warn('[PWA] Service Workers no soportados')
      return
    }

    try {
      const regs = await navigator.serviceWorker.getRegistrations()
      
      // Solo loguear si hay cambios o en la primera vez
      if (registrations.value.length !== regs.length) {
        console.log('[PWA] Registraciones encontradas:', regs.length)
      }
      
      registrations.value = [...regs] as ServiceWorkerRegistration[]

      if (regs.length === 0) {
        // No hay SW registrado aún, no es un error en desarrollo
        return
      }

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
        registration.update().catch(() => {
          // Silenciar errores de actualización en desarrollo
        })
      })
    } catch (error) {
      // Silenciar errores - normal en desarrollo
      console.debug('[PWA] Error verificando actualizaciones:', error)
    }
  }

  const forceUpdate = () => {
    if (navigator.serviceWorker?.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'FORCE_UPDATE',
      })
    }

    // También verificar registraciones
    registrations.value.forEach((reg) => {
      reg.update().catch(() => {})
    })
  }

  const skipWaiting = () => {
    if (navigator.serviceWorker?.controller) {
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
    if (navigator.serviceWorker?.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'CLEAR_CACHE',
      })
    }
  }

  // Escuchar mensajes del Service Worker
  const handleServiceWorkerMessage = (event: MessageEvent) => {
    if (!event.data?.type) return
    
    console.log('[PWA] Mensaje del SW:', event.data.type)

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
    if (!('serviceWorker' in navigator)) return
    
    // Verificar actualizaciones al montar
    checkForUpdates()

    // Escuchar mensajes del Service Worker
    navigator.serviceWorker.addEventListener('message', handleServiceWorkerMessage)

    // Verificar actualizaciones cada 2 minutos (reducido para menos spam en logs)
    updateInterval = setInterval(() => {
      checkForUpdates()
    }, 120000) // Cada 2 minutos
  })
  
  onUnmounted(() => {
    if (updateInterval) {
      clearInterval(updateInterval)
      updateInterval = null
    }
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.removeEventListener('message', handleServiceWorkerMessage)
    }
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
