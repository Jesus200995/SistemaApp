<template>
  <nav class="navbar-container">
    <!-- Logo y título -->
    <div class="navbar-brand">
      <div class="logo-icon-wrapper">
        <Sprout class="logo-icon" />
      </div>
      <h1 class="navbar-title">SistemaApp</h1>
    </div>

    <!-- Centro: Enlaces de navegación (opcional) -->
    <div class="navbar-links">
      <router-link v-if="auth.user" to="/" class="nav-link">
        <Home class="link-icon" />
        <span>Inicio</span>
      </router-link>
      <router-link v-if="auth.user" to="/mapa" class="nav-link">
        <MapPin class="link-icon" />
        <span>Mapa</span>
      </router-link>
      <router-link v-if="auth.user" to="/chat" class="nav-link">
        <MessageCircle class="link-icon" />
        <span>Chat</span>
      </router-link>
      <router-link v-if="auth.user" to="/sembradores" class="nav-link">
        <Sprout class="link-icon" />
        <span>Sembradores</span>
      </router-link>
      <router-link v-if="auth.user" to="/seguimiento" class="nav-link">
        <BarChart3 class="link-icon" />
        <span>Seguimiento</span>
      </router-link>
      <router-link v-if="auth.user" to="/usuarios" class="nav-link">
        <Users class="link-icon" />
        <span>Usuarios</span>
      </router-link>
    </div>

    <!-- Derecha: Notificaciones + Usuario + Logout -->
    <div class="navbar-right">
      <!-- Campana de notificaciones -->
      <div class="notification-container">
        <button 
          @click="toggleNotifications"
          class="notification-button"
          title="Notificaciones"
        >
          <Bell class="notification-icon" />
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
            <button @click="toggleNotifications" class="close-btn">
              <X class="close-icon" />
            </button>
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
              <div class="notification-type-icon">
                <Info v-if="n.tipo === 'info'" class="type-icon" />
                <Check v-else-if="n.tipo === 'success'" class="type-icon" />
                <AlertCircle v-else-if="n.tipo === 'warning'" class="type-icon" />
                <AlertTriangle v-else-if="n.tipo === 'error'" class="type-icon" />
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
          <LogOut class="logout-icon" />
          <span>Salir</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Sprout, Home, MapPin, MessageCircle, BarChart3, Users, Bell, X, 
  Info, Check, AlertCircle, AlertTriangle, LogOut 
} from 'lucide-vue-next'
// @ts-ignore
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl, getSecureWsUrl } from '../utils/api'

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
    const wsUrl = getSecureWsUrl('/notificaciones/ws')
    
    ws.value = new WebSocket(wsUrl) as WebSocket
    
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Contenedor principal */
.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(12px);
  padding: 0.6rem 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  gap: 1rem;
  color: #e2e8f0;
  min-height: 56px;
}

/* Logo y título */
.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.logo-icon-wrapper {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.logo-icon {
  width: 24px;
  height: 24px;
  color: white;
}

.navbar-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Enlaces de navegación */
.navbar-links {
  flex: 1;
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #cbd5e1;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  border: 1px solid rgba(148, 163, 184, 0.1);
  transition: all 0.3s ease;
}

.link-icon {
  width: 18px;
  height: 18px;
  color: #10b981;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.3);
  color: #10b981;
}

.nav-link.router-link-active .link-icon {
  color: #10b981;
}

/* Sección derecha */
.navbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

/* Contenedor de notificaciones */
.notification-container {
  position: relative;
}

.notification-button {
  position: relative;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.notification-icon {
  width: 20px;
  height: 20px;
}

.notification-button:hover {
  background: rgba(16, 185, 129, 0.2);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
  transform: scale(1.05);
}

.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ef4444;
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(15, 23, 42, 0.8);
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
  margin-top: 0.75rem;
  background: rgba(15, 23, 42, 0.95);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  width: 360px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 50;
  backdrop-filter: blur(10px);
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px 12px 0 0;
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
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-icon {
  width: 18px;
  height: 18px;
}

.close-btn:hover {
  transform: scale(1.2);
}

.notification-empty {
  padding: 2rem 1rem;
  text-align: center;
  color: #64748b;
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
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  transition: all 0.2s ease;
  cursor: pointer;
}

.notification-item:hover {
  background: rgba(16, 185, 129, 0.05);
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

.notification-type-icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.type-icon {
  width: 18px;
  height: 18px;
  color: #10b981;
}

.notification-item.notif-info .type-icon {
  color: #3b82f6;
}

.notification-item.notif-warning .type-icon {
  color: #f59e0b;
}

.notification-item.notif-error .type-icon {
  color: #ef4444;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: #e2e8f0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notification-message {
  margin: 0.25rem 0 0 0;
  font-size: 0.85rem;
  color: #94a3b8;
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
  color: #64748b;
}

/* Información del usuario */
.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-left: 1rem;
  border-left: 1px solid rgba(148, 163, 184, 0.1);
}

.user-name {
  font-weight: 500;
  color: #cbd5e1;
  font-size: 0.95rem;
}

.logout-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.logout-icon {
  width: 16px;
  height: 16px;
}

.logout-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

.logout-button:active {
  transform: translateY(0);
}

/* Scrollbar personalizado */
.notification-dropdown::-webkit-scrollbar {
  width: 6px;
}

.notification-dropdown::-webkit-scrollbar-track {
  background: transparent;
}

.notification-dropdown::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 3px;
}

.notification-dropdown::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}

/* Responsive */
@media (max-width: 1024px) {
  .navbar-container {
    padding: 0.5rem 0.8rem;
    gap: 0.8rem;
  }

  .logo-icon-wrapper {
    width: 36px;
    height: 36px;
  }

  .logo-icon {
    width: 18px;
    height: 18px;
  }

  .navbar-title {
    font-size: 1.1rem;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0.5rem 0.6rem;
    gap: 0.6rem;
  }

  .navbar-links {
    display: none;
  }

  .navbar-title {
    font-size: 0.95rem;
  }

  .logo-icon-wrapper {
    width: 32px;
    height: 32px;
  }

  .logo-icon {
    width: 16px;
    height: 16px;
  }

  .notification-dropdown {
    width: 280px;
    max-height: 350px;
  }

  .user-info {
    gap: 0.4rem;
    padding-left: 0.4rem;
    border-left: none;
  }

  .user-name {
    display: none;
  }

  .logout-button {
    padding: 0.4rem 0.6rem;
    font-size: 0.75rem;
  }

  .logout-button span {
    display: none;
  }

  .notification-button {
    width: 36px;
    height: 36px;
  }

  .notification-icon {
    width: 16px;
    height: 16px;
  }
}

@media (max-width: 480px) {
  .navbar-container {
    padding: 0.4rem 0.5rem;
    min-height: 48px;
    gap: 0.4rem;
  }

  .navbar-brand {
    gap: 0.4rem;
  }

  .logo-icon-wrapper {
    width: 28px;
    height: 28px;
  }

  .logo-icon {
    width: 14px;
    height: 14px;
  }

  .navbar-title {
    font-size: 0.9rem;
  }

  .notification-button {
    width: 32px;
    height: 32px;
  }

  .notification-icon {
    width: 14px;
    height: 14px;
  }

  .logout-button {
    padding: 0.35rem 0.5rem;
    font-size: 0.7rem;
  }

  .notification-dropdown {
    width: 240px;
    max-height: 300px;
    right: -20px;
    margin-top: 0.5rem;
  }

  .notification-header {
    padding: 0.75rem;
  }

  .notification-item {
    padding: 0.6rem 0.75rem;
    gap: 0.5rem;
  }

  .notification-type-icon {
    width: 28px;
    height: 28px;
  }

  .type-icon {
    width: 14px;
    height: 14px;
  }

  .notification-title {
    font-size: 0.8rem;
  }

  .notification-message {
    font-size: 0.75rem;
  }

  .notification-time {
    font-size: 0.65rem;
  }
}

@media (max-width: 320px) {
  .navbar-container {
    padding: 0.3rem 0.4rem;
    min-height: 44px;
  }

  .navbar-title {
    font-size: 0.8rem;
  }

  .notification-button {
    width: 28px;
    height: 28px;
  }

  .notification-dropdown {
    width: 200px;
  }
}
</style>
