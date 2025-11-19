<template>
  <div class="favicon-manager"></div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useFaviconAnimation } from '@/composables/useFaviconAnimation'

// Composable para manejar animaciones del favicon
const { notifyWithFavicon, updateNotificationBadge } = useFaviconAnimation()

// Listeners para notificaciones
let unsubscribeFn: (() => void) | null = null

onMounted(() => {
  // Escuchar eventos de notificación en el window
  const handleNotification = (event: CustomEvent) => {
    const { count = 1 } = event.detail
    notifyWithFavicon(count)
  }

  // También escuchar cambios en el documento cuando hay nuevas notificaciones
  window.addEventListener('notification:new', handleNotification as EventListener)

  // Permitir acceso global al composable
  ;(window as any).faviconManager = {
    notifyWithFavicon,
    updateNotificationBadge
  }

  unsubscribeFn = () => {
    window.removeEventListener('notification:new', handleNotification as EventListener)
  }
})

onUnmounted(() => {
  if (unsubscribeFn) {
    unsubscribeFn()
  }
})
</script>

<style scoped></style>
