<template>
  <nav class="navbar-container">
    <!-- Logo y título -->
    <div class="navbar-brand">
      <h1 class="navbar-title">🌱 SistemaApp</h1>
    </div>

    <!-- Centro: Enlaces de navegación (opcional) -->
    <div class="navbar-links">
      <router-link v-if="auth.user" to="/" class="nav-link">Inicio</router-link>
      <router-link v-if="auth.user" to="/mapa" class="nav-link">🗺️ Mapa</router-link>
      <router-link v-if="auth.user" to="/chat" class="nav-link">💬 Chat</router-link>
      <router-link v-if="auth.user" to="/sembradores" class="nav-link">🌱 Sembradores</router-link>
      <router-link v-if="auth.user" to="/usuarios" class="nav-link">👥 Usuarios</router-link>
    </div>

    <!-- Derecha: Notificaciones + Usuario + Logout -->
    <div class="navbar-right">
      <!-- 🔔 Campana de notificaciones -->
      <div class="notification-container">
        <button 
          @click="toggleNotifications"
          class="notification-button"
          title="Notificaciones"
        >
          🔔
          <span 
            v-if="unreadCount > 0" 
            class="notification-badge"
          >
            {{ unreadCount > 99 ? '99+' : unreadCount }}
          </span>
        </button>

        <!-- Dropdown de notificaciones -->
        <div 
          v-if="showNotifications" 
          class="notification-dropdown"
        >
          <div class="notification-header">
            <h3>Notificaciones</h3>
            <button @click="toggleNotifications" class="close-btn">✕</button>
          </div>

          <div v-if="notificaciones.length === 0" class="notification-empty">
            Sin notificaciones
          </div>

          <div v-else class="notification-list">
            <div 
              v-for="n in notificaciones" 
              :key="n.id"
              class="notification-item"
              :class="`notif-${n.tipo}`"
            >
              <div class="notification-icon">
                <span v-if="n.tipo === 'info'">ℹ️</span>
                <span v-else-if="n.tipo === 'success'">✅</span>
                <span v-else-if="n.tipo === 'warning'">⚠️</span>
                <span v-else-if="n.tipo === 'error'">❌</span>
              </div>
              <div class="notification-content">
                <p class="notification-title">{{ n.titulo }}</p>
                <p class="notification-message">{{ n.mensaje }}</p>
                <p class="notification-time">{{ formatTime(n.timestamp) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Usuario y logout -->
      <div class="user-info">
        <span class="user-name">{{ auth.user?.nombre || 'Usuario' }}</span>
        <button 
          @click="logout"
          class="logout-button"
          title="Cerrar sesión"
        >
          Salir
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
// @ts-ignore
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const ws = ref<WebSocket | null>(null)
const unreadCount = ref<number>(0)
const notificaciones = ref<any[]>([])
const showNotifications = ref<boolean>(false)

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) {
    unreadCount.value = 0
  }
}

const logout = () => {
  auth.logout()
  router.push('/login')
}

const formatTime = (timestamp: any) => {
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Justo ahora'
    if (diffMins < 60) return `Hace ${diffMins}m`
    
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `Hace ${diffHours}h`
    
    return date.toLocaleDateString('es-ES')
  } catch (e) {
    return 'Ahora'
  }
}

const connectWebSocket = () => {
  try {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = import.meta.env.VITE_API_URL.replace('https://', '').replace('http://', '')
    
    ws.value = new WebSocket(`${protocol}//${host}/notificaciones/ws`) as WebSocket
    
    ws.value.onopen = () => {
      console.log('✅ Conectado a notificaciones en navbar')
    }
    
    ws.value.onmessage = (event: Event) => {
      try {
        const messageEvent = event as MessageEvent
        const data = JSON.parse(messageEvent.data)
        notificaciones.value.unshift(data)
        unreadCount.value++
        
        // Limitar a últimas 20 notificaciones
        if (notificaciones.value.length > 20) {
          notificaciones.value.pop()
        }
      } catch (e) {
        console.error('Error procesando notificación:', e)
      }
    }
    
    ws.value.onerror = (error: Event) => {
      console.error('❌ Error WebSocket:', error)
    }
    
    ws.value.onclose = () => {
      console.log('🔴 Desconectado de notificaciones')
    }
  } catch (error) {
    console.error('Error conectando WebSocket:', error)
  }
}

onMounted(() => {
  connectWebSocket()
})

onBeforeUnmount(() => {
  if (ws.value) {
    ws.value.close()
  }
})
</script>

<style scoped>
/* Contenedor principal */
.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
  padding: 1rem 2rem;
  border-bottom: 2px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  gap: 2rem;
}

/* Logo y título */
.navbar-brand {
  flex-shrink: 0;
}

.navbar-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #059669;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Enlaces de navegación */
.navbar-links {
  flex: 1;
  display: flex;
  gap: 2rem;
  justify-content: center;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: #374151;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  transition: all 0.3s ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: #dcfce7;
  color: #059669;
}

/* Sección derecha */
.navbar-right {
  display: flex;
  align-items: center;
  gap: 2rem;
}

/* Contenedor de notificaciones */
.notification-container {
  position: relative;
}

.notification-button {
  position: relative;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: all 0.3s ease;
}

.notification-button:hover {
  background-color: #f3f4f6;
  transform: scale(1.1);
}

.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #ef4444;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(239, 68, 68, 0);
  }
}

/* Dropdown de notificaciones */
.notification-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 360px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 50;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-bottom: 1px solid #e5e7eb;
  border-radius: 0.5rem 0.5rem 0 0;
}

.notification-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  transform: scale(1.2);
}

.notification-empty {
  padding: 2rem 1rem;
  text-align: center;
  color: #9ca3af;
  font-size: 0.9rem;
}

.notification-list {
  max-height: 320px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f3f4f6;
  transition: all 0.2s ease;
  cursor: pointer;
}

.notification-item:hover {
  background-color: #f9fafb;
}

.notification-item.notif-info {
  border-left: 3px solid #3b82f6;
}

.notification-item.notif-success {
  border-left: 3px solid #10b981;
}

.notification-item.notif-warning {
  border-left: 3px solid #f59e0b;
}

.notification-item.notif-error {
  border-left: 3px solid #ef4444;
}

.notification-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notification-message {
  margin: 0.25rem 0 0 0;
  font-size: 0.85rem;
  color: #6b7280;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
}

.notification-time {
  margin: 0.5rem 0 0 0;
  font-size: 0.75rem;
  color: #9ca3af;
}

/* Información del usuario */
.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-left: 1rem;
  border-left: 1px solid #e5e7eb;
}

.user-name {
  font-weight: 500;
  color: #374151;
  font-size: 0.95rem;
}

.logout-button {
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.logout-button:hover {
  background-color: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

/* Scrollbar personalizado */
.notification-dropdown::-webkit-scrollbar {
  width: 6px;
}

.notification-dropdown::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.notification-dropdown::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.notification-dropdown::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Responsive */
@media (max-width: 768px) {
  .navbar-container {
    padding: 1rem;
    gap: 1rem;
  }

  .navbar-links {
    display: none;
  }

  .navbar-title {
    font-size: 1.2rem;
  }

  .notification-dropdown {
    width: 300px;
  }

  .user-info {
    gap: 0.5rem;
    padding-left: 0.5rem;
    border-left: none;
  }

  .user-name {
    display: none;
  }

  .logout-button {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
}
</style>
