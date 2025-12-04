<template>
  <div class="notification-center">
    <!-- Botón de campana profesional -->
    <div class="relative">
      <button 
        @click="toggleDropdown" 
        class="notification-bell"
      >
        <Bell :size="24" />
        <span 
          v-if="unreadCount > 0" 
          class="notification-badge"
        >
          {{ unreadCount > 9 ? '9+' : unreadCount }}
        </span>
      </button>

      <!-- Dropdown con notificaciones -->
      <div 
        v-if="showDropdown" 
        class="notification-dropdown"
      >
        <!-- Header -->
        <div class="notification-header">
          <h3>Notificaciones</h3>
          <button @click="showDropdown = false" class="close-btn">
            <X :size="20" />
          </button>
        </div>

        <!-- Lista -->
        <div class="notification-list">
          <div v-if="notificaciones.length === 0" class="empty-state">
            <Bell :size="32" />
            <p>Sin notificaciones</p>
          </div>

          <div 
            v-for="notif in notificaciones" 
            :key="notif.id"
            class="notification-item"
            :class="{ leida: notif.leido }"
            :style="{ borderLeftColor: getColorScheme(notif.tipo).border }"
          >
            <!-- Ícono -->
            <div 
              class="notification-icon"
              :style="{ background: getColorScheme(notif.tipo).border }"
            >
              <component 
                :is="getIconComponent(notif.tipo)" 
                :size="18" 
                color="white"
              />
            </div>

            <!-- Contenido -->
            <div class="notification-content">
              <p class="notification-title">{{ notif.titulo }}</p>
              <p class="notification-message">{{ notif.mensaje }}</p>
              <p class="notification-time">{{ formatearFecha(notif.timestamp) }}</p>
            </div>

            <!-- Botón eliminar -->
            <button 
              @click="eliminarNotificacion(notif.id)"
              class="delete-btn"
            >
              <Trash2 :size="16" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Overlay -->
    <div 
      v-if="showDropdown"
      @click="showDropdown = false"
      class="notification-overlay"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
// @ts-ignore
import { useAuthStore } from '../stores/auth'
import { Bell, X, CheckCircle, AlertCircle, Clock, Trash2, Info } from 'lucide-vue-next'
import axios from 'axios'

const auth = useAuthStore()
const ws = ref<WebSocket | null>(null)
const notificaciones = ref<any[]>([])
const showDropdown = ref(false)

const tipoColores = {
  solicitud: { bg: '#1e3a8a', border: '#3b82f6', text: '#93c5fd' },
  respuesta: { bg: '#065f46', border: '#10b981', text: '#86efac' },
  info: { bg: '#44403c', border: '#78716c', text: '#d7d5d0' },
  warning: { bg: '#78350f', border: '#f59e0b', text: '#fcd34d' },
  error: { bg: '#7f1d1d', border: '#ef4444', text: '#fca5a5' },
  success: { bg: '#064e3b', border: '#10b981', text: '#86efac' }
}

const unreadCount = computed(() => notificaciones.value.filter(n => !n.leido).length)

const toggleDropdown = async () => {
  showDropdown.value = !showDropdown.value
  
  if (showDropdown.value) {
    // Marcar todas las no leídas como leídas al abrir
    const noLeidas = notificaciones.value.filter(n => !n.leido)
    for (const notif of noLeidas) {
      await marcarComoLeida(notif.id)
    }
  }
}

const marcarComoLeida = async (id: number) => {
  try {
    const token = localStorage.getItem('token') || auth.token
    await axios.patch(
      `${import.meta.env.VITE_API_URL}/notificaciones/${id}/leer`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    )
    const notif = notificaciones.value.find(n => n.id === id)
    if (notif) notif.leido = true
  } catch (error) {
    console.error('Error marcando como leída:', error)
  }
}

const eliminarNotificacion = async (id: number) => {
  try {
    const token = localStorage.getItem('token') || auth.token
    await axios.delete(
      `${import.meta.env.VITE_API_URL}/notificaciones/${id}`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    notificaciones.value = notificaciones.value.filter(n => n.id !== id)
  } catch (error) {
    console.error('Error eliminando notificación:', error)
  }
}

const getColorScheme = (tipo: string) => {
  return tipoColores[tipo as keyof typeof tipoColores] || tipoColores.info
}

const getIconComponent = (tipo: string) => {
  switch (tipo) {
    case 'solicitud':
      return Clock
    case 'respuesta':
      return CheckCircle
    case 'warning':
    case 'error':
      return AlertCircle
    case 'info':
      return Info
    default:
      return Bell
  }
}

const formatearFecha = (fecha: string) => {
  const date = new Date(fecha)
  const ahora = new Date()
  const diff = ahora.getTime() - date.getTime()
  const minutos = Math.floor(diff / 60000)
  const horas = Math.floor(diff / 3600000)

  if (minutos < 1) return 'Hace poco'
  if (minutos < 60) return `Hace ${minutos}m`
  if (horas < 24) return `Hace ${horas}h`
  return date.toLocaleDateString('es-CO')
}

const getNotificaciones = async () => {
  try {
    const token = localStorage.getItem('token') || auth.token
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/notificaciones`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    notificaciones.value = (response.data || []).reverse()
    console.log('✅ Notificaciones cargadas:', notificaciones.value.length)
  } catch (error) {
    console.error('❌ Error cargando notificaciones:', error)
  }
}

onMounted(() => {
  // Cargar notificaciones persistidas de la BD
  getNotificaciones()
  
  // Conectar WebSocket
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  
  // Si la API es relativa (/api), usar el host actual
  let wsUrl: string
  if (apiUrl.startsWith('/')) {
    wsUrl = `${protocol}//${window.location.host}${apiUrl}/notificaciones/ws`
  } else {
    const host = apiUrl.replace(/^(https?:\/\/)/, '').replace(/\/$/, '')
    wsUrl = `${protocol}//${host}/notificaciones/ws`
  }
  console.log('🔌 Conectando WebSocket:', wsUrl)
  
  ws.value = new WebSocket(wsUrl)

  ws.value.onopen = () => {
    console.log('✅ WebSocket conectado')
    setInterval(() => {
      if (ws.value?.readyState === WebSocket.OPEN) {
        ws.value?.send('ping')
      }
    }, 30000)
  }

  ws.value.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      
      if (data.user_destino === auth.user?.id || !data.user_destino) {
        const notif = {
          ...data,
          leido: false,
          timestamp: data.timestamp || new Date().toISOString()
        }
        notificaciones.value.unshift(notif)
        console.log('🔔 Nueva notificación:', notif)
      }
    } catch (error) {
      console.error('Error procesando WebSocket:', error)
    }
  }

  ws.value.onerror = (error) => {
    console.error('❌ Error WebSocket:', error)
  }

  ws.value.onclose = () => {
    console.log('� Desconectado')
  }
})

onUnmounted(() => {
  if (ws.value) {
    ws.value.close()
  }
})
</script>

<style scoped>
.notification-center {
  position: relative;
}

.notification-bell {
  position: relative;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  padding: 0.625rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-bell:hover {
  background: rgba(30, 41, 59, 0.8);
  border-color: rgba(148, 163, 184, 0.4);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
}

.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
  border: 2px solid rgba(15, 23, 42, 0.9);
}

.notification-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 400px;
  max-height: 600px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  z-index: 1000;
  margin-top: 0.5rem;
  display: flex;
  flex-direction: column;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  background: rgba(30, 41, 59, 0.5);
}

.notification-header h3 {
  color: #f1f5f9;
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #cbd5e1;
  cursor: pointer;
  transition: color 0.2s;
  padding: 0;
}

.close-btn:hover {
  color: #f1f5f9;
}

.notification-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  min-height: 100px;
}

.notification-list::-webkit-scrollbar {
  width: 6px;
}

.notification-list::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.5);
  border-radius: 3px;
}

.notification-list::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 3px;
}

.notification-list::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  color: #cbd5e1;
  text-align: center;
}

.empty-state svg {
  margin-bottom: 1rem;
  opacity: 0.5;
}

.notification-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(30, 41, 59, 0.4);
  margin-bottom: 0.5rem;
  border-radius: 8px;
  border-left: 3px solid;
  transition: all 0.2s ease;
}

.notification-item:not(.leida) {
  background: rgba(16, 185, 129, 0.05);
}

.notification-item.leida {
  background: rgba(241, 245, 249, 0.05);
  opacity: 0.9;
}

.notification-item:hover {
  background: rgba(30, 41, 59, 0.7);
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: 0.9;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  color: #f1f5f9;
  font-weight: 600;
  font-size: 0.95rem;
  margin: 0 0 0.25rem 0;
  word-break: break-word;
}

.notification-message {
  color: #cbd5e1;
  font-size: 0.875rem;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
  word-break: break-word;
}

.notification-time {
  color: #94a3b8;
  font-size: 0.75rem;
  margin: 0;
}

.delete-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 0.25rem;
  transition: all 0.2s;
  flex-shrink: 0;
}

.delete-btn:hover {
  color: #ef4444;
}

.notification-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
}

@media (max-width: 640px) {
  .notification-dropdown {
    width: 320px;
    max-height: 400px;
  }

  .notification-item {
    padding: 0.75rem;
  }

  .notification-title {
    font-size: 0.875rem;
  }

  .notification-message {
    font-size: 0.8rem;
  }
}
</style>
