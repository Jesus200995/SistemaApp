import { ref, onMounted } from 'vue'

export function usePWA() {
  const isInstallable = ref(false)
  const isInstalled = ref(false)
  const deferredPrompt = ref<any>(null)
  const swRegistration = ref<ServiceWorkerRegistration | null>(null)

  onMounted(async () => {
    // Detectar si la app ya está instalada
    if (window.matchMedia('(display-mode: standalone)').matches) {
      isInstalled.value = true
    }

    // Escuchar el evento beforeinstallprompt
    window.addEventListener('beforeinstallprompt', (e: Event) => {
      e.preventDefault()
      deferredPrompt.value = e
      isInstallable.value = true
    })

    // Escuchar cuando se instala
    window.addEventListener('appinstalled', () => {
      isInstalled.value = true
      isInstallable.value = false
      deferredPrompt.value = null
    })

    // Obtener registro existente del SW (gestionado por vite-plugin-pwa)
    // NO registrar manualmente - usar el registro de registerSW.js
    if ('serviceWorker' in navigator) {
      try {
        const registrations = await navigator.serviceWorker.getRegistrations()
        if (registrations.length > 0) {
          swRegistration.value = registrations[0]
          console.log('✅ Service Worker activo encontrado')
        }
      } catch (error) {
        console.warn('⚠️ No se pudo obtener el SW:', error)
      }
    }
  })

  // Función para instalar PWA
  const installApp = async () => {
    if (!deferredPrompt.value) {
      console.log('PWA no disponible para instalar')
      return
    }

    try {
      deferredPrompt.value.prompt()
      const { outcome } = await deferredPrompt.value.userChoice
      
      if (outcome === 'accepted') {
        console.log('✅ App instalada exitosamente')
        isInstalled.value = true
      } else {
        console.log('❌ Instalación cancelada')
      }
      
      deferredPrompt.value = null
    } catch (error) {
      console.error('Error durante instalación:', error)
    }
  }

  // Función para actualizar Service Worker
  const updateServiceWorker = async () => {
    if (!swRegistration.value) return

    try {
      const registration = await swRegistration.value.update()
      if (registration.waiting) {
        // Nueva versión disponible
        registration.waiting.postMessage({ type: 'SKIP_WAITING' })
        window.location.reload()
      }
    } catch (error) {
      console.error('Error actualizando SW:', error)
    }
  }

  // Función para sincronizar datos en background
  const syncNotifications = async () => {
    if (!swRegistration.value) return

    try {
      // Enviar mensaje al Service Worker
      swRegistration.value.active?.postMessage({ type: 'SYNC_NOTIFICATIONS' })
      console.log('✅ Sincronización programada')
    } catch (error) {
      console.error('Error programando sincronización:', error)
    }
  }

  // Función para solicitar notificaciones
  const requestNotificationPermission = async () => {
    if (!('Notification' in window)) {
      console.log('El navegador no soporta notificaciones')
      return false
    }

    if (Notification.permission === 'granted') {
      return true
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission()
      return permission === 'granted'
    }

    return false
  }

  // Función para mostrar notificación
  const showNotification = (title: string, options?: NotificationOptions) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, options)
    }
  }

  // Función para limpiar caché
  const clearCache = async () => {
    if ('caches' in window) {
      const cacheNames = await caches.keys()
      await Promise.all(cacheNames.map((name) => caches.delete(name)))
      console.log('✅ Caché limpiado')
    }
  }

  // Verificar estado online/offline
  const isOnline = ref(navigator.onLine)
  
  window.addEventListener('online', () => {
    isOnline.value = true
    console.log('✅ De vuelta online')
  })
  
  window.addEventListener('offline', () => {
    isOnline.value = false
    console.log('⚠️ Sin conexión')
  })

  return {
    isInstallable,
    isInstalled,
    isOnline,
    installApp,
    updateServiceWorker,
    syncNotifications,
    requestNotificationPermission,
    showNotification,
    clearCache,
  }
}
