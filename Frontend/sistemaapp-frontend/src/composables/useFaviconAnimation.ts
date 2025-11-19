/**
 * Composable para animar el favicon cuando hay notificaciones
 */

import { ref, watch } from 'vue'

export function useFaviconAnimation() {
  const isAnimating = ref(false)
  const notificationCount = ref(0)

  /**
   * Inicia la animación del favicon
   */
  const startFaviconAnimation = () => {
    if (isAnimating.value) return

    isAnimating.value = true
    const originalTitle = document.title

    // Crear efecto visual en el título
    let flashCount = 0
    const flashInterval = setInterval(() => {
      flashCount++
      if (flashCount % 2 === 0) {
        document.title = `🔔 ${originalTitle}`
      } else {
        document.title = originalTitle
      }

      if (flashCount >= 6) {
        clearInterval(flashInterval)
        document.title = originalTitle
        isAnimating.value = false
      }
    }, 500)

    // Agregar clase de animación a body
    document.body.classList.add('favicon-notification')
    setTimeout(() => {
      document.body.classList.remove('favicon-notification')
    }, 1800)
  }

  /**
   * Detiene la animación del favicon
   */
  const stopFaviconAnimation = () => {
    isAnimating.value = false
    document.title = document.title.replace('🔔 ', '')
    document.body.classList.remove('favicon-notification')
  }

  /**
   * Actualiza el contador de notificaciones en el favicon
   */
  const updateNotificationBadge = (count: number) => {
    notificationCount.value = count
    if (count > 0) {
      document.title = `(${count}) SistemaApp - Panel de Control`
    } else {
      document.title = 'SistemaApp - Panel de Control'
    }
  }

  /**
   * Reproduce sonido de notificación y anima el favicon
   */
  const notifyWithFavicon = (count: number = 1) => {
    updateNotificationBadge(count)
    startFaviconAnimation()

    // Reproducir sonido si está disponible
    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
      const oscillator = audioContext.createOscillator()
      const gain = audioContext.createGain()

      oscillator.connect(gain)
      gain.connect(audioContext.destination)

      oscillator.frequency.value = 800
      gain.gain.setValueAtTime(0.3, audioContext.currentTime)
      gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1)

      oscillator.start(audioContext.currentTime)
      oscillator.stop(audioContext.currentTime + 0.1)
    } catch (e) {
      // Silenciosamente ignorar si no hay soporte de audio
    }
  }

  return {
    isAnimating,
    notificationCount,
    startFaviconAnimation,
    stopFaviconAnimation,
    updateNotificationBadge,
    notifyWithFavicon
  }
}
