<template>
  <div class="notification-container">
    <!-- Botón con badge de notificaciones -->
    <button 
      @click="togglePanel"
      class="notification-button relative hover:scale-110 transition-transform"
      title="Notificaciones"
    >
      🔔
      <span 
        v-if="noLeidas > 0" 
        class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center"
      >
        {{ noLeidas > 99 ? '99+' : noLeidas }}
      </span>
    </button>

    <!-- Panel de notificaciones -->
    <div 
      v-if="showPanel" 
      class="notification-panel absolute right-0 mt-2 bg-white rounded-lg shadow-2xl border border-gray-200 z-50 w-80 max-h-96 overflow-y-auto"
    >
      <!-- Header -->
      <div class="sticky top-0 bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-t-lg">
        <div class="flex justify-between items-center">
          <h3 class="font-bold text-lg">🔔 Notificaciones</h3>
          <button 
            @click="togglePanel"
            class="text-white hover:bg-green-700 px-2 py-1 rounded"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- Contenido -->
      <div v-if="notificaciones.length === 0" class="p-8 text-center text-gray-500">
        <p class="text-sm">No hay notificaciones</p>
      </div>

      <div v-else class="divide-y divide-gray-100">
        <div 
          v-for="notif in notificaciones" 
          :key="notif.id"
          class="p-4 hover:bg-gray-50 transition-colors cursor-pointer group"
          :class="{
            'bg-blue-50 border-l-4 border-blue-400': notif.tipo === 'info',
            'bg-green-50 border-l-4 border-green-400': notif.tipo === 'success',
            'bg-yellow-50 border-l-4 border-yellow-400': notif.tipo === 'warning',
            'bg-red-50 border-l-4 border-red-400': notif.tipo === 'error',
          }"
          @click="marcarComoLeida(notif.id)"
        >
          <!-- Icono + Contenido -->
          <div class="flex gap-3">
            <!-- Icono por tipo -->
            <div class="flex-shrink-0 text-xl">
              <span v-if="notif.tipo === 'info'">ℹ️</span>
              <span v-else-if="notif.tipo === 'success'">✅</span>
              <span v-else-if="notif.tipo === 'warning'">⚠️</span>
              <span v-else-if="notif.tipo === 'error'">❌</span>
            </div>

            <!-- Texto -->
            <div class="flex-1">
              <p class="font-semibold text-sm text-gray-800">{{ notif.titulo }}</p>
              <p class="text-xs text-gray-600 mt-1">{{ notif.mensaje }}</p>
              <p class="text-xs text-gray-500 mt-2">{{ formatTime(notif.timestamp) }}</p>
            </div>

            <!-- Botón eliminar (visible en hover) -->
            <button 
              @click.stop="eliminarNotificacion(notif.id)"
              class="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity text-gray-400 hover:text-red-500"
            >
              ✕
            </button>
          </div>

          <!-- Indicador no leída -->
          <div v-if="!notif.leido" class="mt-2">
            <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
          </div>
        </div>
      </div>

      <!-- Footer con acciones -->
      <div v-if="notificaciones.length > 0" class="border-t border-gray-200 p-3 bg-gray-50 rounded-b-lg flex gap-2">
        <button 
          @click="marcarTodasLeidasClickHandler"
          class="flex-1 text-xs bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded transition"
        >
          Marcar todas como leídas
        </button>
        <button 
          @click="limpiarPanel"
          class="flex-1 text-xs bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded transition"
        >
          Limpiar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
// @ts-ignore
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const auth = useAuthStore()
const ws = ref(null)
const showPanel = ref(false)
const notificaciones = ref([])
const noLeidas = ref(0)

const connectWebSocket = () => {
  try {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = import.meta.env.VITE_API_URL.replace('https://', '').replace('http://', '')
    
    ws.value = new WebSocket(`${protocol}//${host}/notificaciones/ws`)
    
    ws.value.onopen = () => {
      console.log('✅ Conectado a notificaciones en tiempo real')
    }
    
    ws.value.onmessage = (event) => {
      try {
        const notif = JSON.parse(event.data)
        
        // Agregar notificación
        notificaciones.value.unshift(notif)
        noLeidas.value += 1
        
        // Mostrar notificación del sistema (si está permitido)
        showSystemNotification(notif)
        
        // Log
        console.log('🔔 Nueva notificación:', notif.titulo)
      } catch (e) {
        console.error('Error procesando notificación:', e)
      }
    }
    
    ws.value.onerror = (error) => {
      console.error('❌ Error WebSocket:', error)
    }
    
    ws.value.onclose = () => {
      console.log('🔴 Desconectado de notificaciones')
    }
  } catch (error) {
    console.error('Error conectando WebSocket:', error)
  }
}

const showSystemNotification = (notif) => {
  if ('Notification' in window && Notification.permission === 'granted') {
    try {
      new Notification(notif.titulo, {
        body: notif.mensaje,
        tag: `notif-${notif.id}`,
        badge: '🔔'
      })
    } catch (e) {
      console.error('Error mostrando notificación del sistema:', e)
    }
  }
}

const marcarComoLeida = async (notifId) => {
  try {
    await axios.patch(
      `${import.meta.env.VITE_API_URL}/notificaciones/${notifId}/leer`,
      {},
      { headers: { Authorization: `Bearer ${auth.token}` } }
    )
    
    const notif = notificaciones.value.find(n => n.id === notifId)
    if (notif) {
      notif.leido = true
      noLeidas.value = Math.max(0, noLeidas.value - 1)
    }
  } catch (error) {
    console.error('Error marcando como leída:', error)
  }
}

const marcarTodasLeidasClickHandler = async () => {
  for (const notif of notificaciones.value) {
    if (!notif.leido) {
      await marcarComoLeida(notif.id)
    }
  }
}

const eliminarNotificacion = async (notifId) => {
  try {
    await axios.delete(
      `${import.meta.env.VITE_API_URL}/notificaciones/${notifId}`,
      { headers: { Authorization: `Bearer ${auth.token}` } }
    )
    
    const idx = notificaciones.value.findIndex(n => n.id === notifId)
    if (idx > -1) {
      const notif = notificaciones.value[idx]
      notificaciones.value.splice(idx, 1)
      if (!notif.leido) {
        noLeidas.value = Math.max(0, noLeidas.value - 1)
      }
    }
  } catch (error) {
    console.error('Error eliminando notificación:', error)
  }
}

const limpiarPanel = async () => {
  for (const notif of notificaciones.value) {
    await eliminarNotificacion(notif.id)
  }
}

const formatTime = (timestamp) => {
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Justo ahora'
    if (diffMins < 60) return `Hace ${diffMins}m`
    
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `Hace ${diffHours}h`
    
    const diffDays = Math.floor(diffHours / 24)
    if (diffDays < 7) return `Hace ${diffDays}d`
    
    return date.toLocaleDateString('es-ES')
  } catch (e) {
    return 'Ahora'
  }
}

const togglePanel = () => {
  showPanel.value = !showPanel.value
}

onMounted(() => {
  connectWebSocket()
  
  // Solicitar permisos para notificaciones del sistema
  if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission()
  }
})

onBeforeUnmount(() => {
  if (ws.value) {
    ws.value.close()
  }
})
</script>

<style scoped>
.notification-container {
  position: relative;
}

.notification-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 4px 8px;
}

.notification-panel {
  max-width: 400px;
}

/* Scrollbar personalizado */
.notification-panel::-webkit-scrollbar {
  width: 6px;
}

.notification-panel::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.notification-panel::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.notification-panel::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
