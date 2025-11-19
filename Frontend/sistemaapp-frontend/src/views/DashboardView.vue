<template>
  <div class="dashboard-container">
    <!-- Header moderno -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">
            <LayoutDashboard class="logo-svg" />
          </div>
          <div class="logo-text">
            <h1 class="app-title">SistemaApp</h1>
            <p class="app-subtitle">Panel de Control</p>
          </div>
        </div>
        <button @click="logout" class="logout-btn">
          <LogOut class="logout-icon" />
          <span class="logout-text">Salir</span>
        </button>
      </div>
    </header>

    <!-- Contenido principal -->
    <main class="dashboard-main">
      <div class="dashboard-content">
        <!-- Tarjeta de perfil -->
        <div
          v-motion
          :initial="{ opacity: 0, scale: 0.8, y: 50 }"
          :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 200, duration: 700 } }"
          class="profile-card"
        >
          <!-- Avatar con glow -->
          <div class="avatar-wrapper">
            <div class="avatar-glow"></div>
            <img
              src="https://ui-avatars.com/api/?name=Usuario&background=10b981&color=fff&size=200&bold=true&rounded=true"
              alt="avatar"
              class="avatar-image"
            />
          </div>

          <!-- Bienvenida -->
          <div class="welcome-section">
            <div class="welcome-icon-wrapper">
              <Smile class="welcome-icon" />
            </div>
            <h2 class="welcome-title">¡Bienvenido!</h2>
            <p class="user-name">{{ auth.user?.nombre || 'Usuario' }}</p>
          </div>

          <!-- Información -->
          <div class="info-box">
            <div class="info-item">
              <User class="info-icon" />
              <div class="info-text">
                <span class="info-label">Rol</span>
                <span class="info-value">{{ auth.user?.rol || 'N/A' }}</span>
              </div>
            </div>
            <div class="divider"></div>
            <div class="info-item">
              <Mail class="info-icon" />
              <div class="info-text">
                <span class="info-label">Correo</span>
                <span class="info-value">{{ auth.user?.email || 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Sección de acciones -->
        <div class="actions-section">
          <h3 class="section-title">Acceso Rápido</h3>
          
          <div class="actions-grid">
            <div
              v-for="(action, index) in actions"
              :key="action.title"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 500 + index * 100, duration: 500 } }"
              @click="goTo(action.route)"
              class="action-card"
            >
              <div class="action-icon-wrapper">
                <component :is="action.icon" class="action-icon" />
              </div>
              <span class="action-title">{{ action.title }}</span>
            </div>
          </div>
        </div>

        <!-- Sección de notificaciones recientes -->
        <div
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 950, duration: 500 } }"
          class="notifications-section"
        >
          <div class="notifications-header">
            <h3 class="section-title">Notificaciones Recientes</h3>
            <div class="notifications-badge">
              {{ unreadNotifications }}
            </div>
          </div>

          <div v-if="notificaciones.length === 0" class="notifications-empty">
            <Bell :size="32" class="empty-icon" />
            <p>Sin notificaciones nuevas</p>
          </div>

          <div v-else class="notifications-list">
            <div 
              v-for="notif in notificaciones.slice(0, 5)"
              :key="notif.id"
              class="notification-card"
              :class="{ 'notif-unread': !notif.leido }"
              :style="{ borderLeftColor: getNotificationColor(notif.tipo) }"
            >
              <div 
                class="notif-icon"
                :style="{ background: getNotificationColor(notif.tipo) }"
              >
                <component :is="getNotificationIcon(notif.tipo)" :size="18" color="white" />
              </div>
              <div class="notif-content">
                <p class="notif-title">{{ notif.titulo }}</p>
                <p class="notif-message">{{ notif.mensaje }}</p>
                <p class="notif-time">{{ formatTime(notif.timestamp) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Sección de módulos especializados -->
        <div class="specialized-section">
          <h3 class="section-title">Módulos Especializados</h3>
          
          <div class="specialized-grid">
            <!-- Seguimiento de Campo - Solo técnicos -->
            <router-link
              v-if="auth.user?.rol && (auth.user.rol.includes('tecnico'))"
              to="/seguimiento"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 600, duration: 500 } }"
              class="specialized-card specialized-seguimiento"
            >
              <div class="specialized-icon-wrapper">
                <Clipboard class="specialized-icon-lucide" />
              </div>
              <h4 class="specialized-title">Seguimiento de Campo</h4>
              <p class="specialized-desc">Registrar visitas y avances</p>
              <div class="card-arrow">→</div>
            </router-link>

            <!-- Sembradores - Todos los roles -->
            <router-link
              to="/sembradores"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 700, duration: 500 } }"
              class="specialized-card specialized-sembradores"
            >
              <div class="specialized-icon-wrapper">
                <Sprout class="specialized-icon-lucide" />
              </div>
              <h4 class="specialized-title">Sembradores en Mapa</h4>
              <p class="specialized-desc">Gestionar sembradores</p>
              <div class="card-arrow">→</div>
            </router-link>

            <!-- Reportes - Facilitadores, Territoriales, Admins -->
            <router-link
              v-if="auth.user?.rol && ['facilitador', 'territorial', 'admin'].includes(auth.user.rol)"
              to="/estadisticas"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 800, duration: 500 } }"
              class="specialized-card specialized-reportes"
            >
              <div class="specialized-icon-wrapper">
                <BarChart3 class="specialized-icon-lucide" />
              </div>
              <h4 class="specialized-title">Reportes y Estadísticas</h4>
              <p class="specialized-desc">Análisis general</p>
              <div class="card-arrow">→</div>
            </router-link>

            <!-- Solicitudes Jerárquicas - Todos los roles -->
            <router-link
              to="/solicitudes"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 850, duration: 500 } }"
              class="specialized-card specialized-solicitudes"
            >
              <div class="specialized-icon-wrapper">
                <FileText class="specialized-icon-lucide" />
              </div>
              <h4 class="specialized-title">Solicitudes</h4>
              <p class="specialized-desc">Gestionar solicitudes jerárquicas</p>
              <div class="card-arrow">→</div>
            </router-link>

            <!-- Gestión de Usuarios - Solo admins -->
            <router-link
              v-if="auth.user?.rol === 'admin'"
              to="/usuarios"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 900, duration: 500 } }"
              class="specialized-card specialized-usuarios"
            >
              <div class="specialized-icon-wrapper">
                <Users class="specialized-icon-lucide" />
              </div>
              <h4 class="specialized-title">Gestión de Usuarios</h4>
              <p class="specialized-desc">Administrar usuarios</p>
              <div class="card-arrow">→</div>
            </router-link>

            <!-- Panel de Administración Global - Solo admins -->
            <router-link
              v-if="auth.user?.rol === 'admin'"
              to="/admin-panel"
              v-motion
              :initial="{ opacity: 0, y: 30 }"
              :enter="{ opacity: 1, y: 0, transition: { delay: 950, duration: 500 } }"
              class="specialized-card specialized-admin"
            >
              <div class="specialized-icon-wrapper">
                <Settings class="specialized-icon-lucide" />
              </div>
              <h4 class="specialized-title">Panel Global</h4>
              <p class="specialized-desc">Control centralizado del sistema</p>
              <div class="card-arrow">→</div>
            </router-link>
          </div>
        </div>

        <!-- Stats -->
        <div
          v-motion
          :initial="{ opacity: 0 }"
          :enter="{ opacity: 1, transition: { delay: 800, duration: 600 } }"
          class="stats-grid"
        >
          <div class="stat-card stat-online">
            <div class="stat-icon"><Check class="stat-lucide" /></div>
            <p class="stat-text">Conectado</p>
          </div>
          <div class="stat-card stat-secure">
            <div class="stat-icon"><Shield class="stat-lucide" /></div>
            <p class="stat-text">Seguro</p>
          </div>
          <div class="stat-card stat-active">
            <div class="stat-icon"><Zap class="stat-lucide" /></div>
            <p class="stat-text">Activo</p>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer
      v-motion
      :initial="{ opacity: 0 }"
      :enter="{ opacity: 1, transition: { delay: 1000, duration: 600 } }"
      class="dashboard-footer"
    >
      <p>© 2025 <span class="footer-highlight">SistemaApp</span>. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, onUnmounted } from 'vue'
// @ts-ignore
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { LogOut, User, Mail, LayoutDashboard, BarChart3, Users, Settings, MapPin, Sprout, FileText, Smile, Clipboard, Check, Shield, Zap, Bell, Clock, CheckCircle, AlertCircle, Info } from 'lucide-vue-next'
import axios from 'axios'

const auth = useAuthStore()
const router = useRouter()
const notificaciones = ref<any[]>([])
const ws = ref<WebSocket | null>(null)

onMounted(() => {
  auth.fetchProfile()
  getNotificaciones()
  connectWebSocket()
})

onUnmounted(() => {
  if (ws.value) {
    ws.value.close()
  }
})

const connectWebSocket = () => {
  try {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const host = apiUrl.replace(/^(https?:\/\/)/, '').replace(/\/$/, '')
    
    const wsUrl = `${protocol}//${host}/notificaciones/ws`
    console.log('🔌 Conectando WebSocket:', wsUrl)
    
    ws.value = new WebSocket(wsUrl)

    ws.value.onopen = () => {
      console.log('✅ WebSocket conectado en Dashboard')
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
          console.log('🔔 Nueva notificación en Dashboard:', notif)
        }
      } catch (error) {
        console.error('Error procesando WebSocket:', error)
      }
    }

    ws.value.onerror = (error) => {
      console.error('❌ Error WebSocket:', error)
    }

    ws.value.onclose = () => {
      console.log('🔌 Desconectado de WebSocket')
    }
  } catch (error) {
    console.error('Error conectando WebSocket:', error)
  }
}

const getNotificaciones = async () => {
  try {
    const token = localStorage.getItem('token') || auth.token
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/notificaciones`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    notificaciones.value = (response.data || []).reverse()
    console.log('✅ Notificaciones cargadas en Dashboard:', notificaciones.value.length)
  } catch (error) {
    console.error('❌ Error cargando notificaciones:', error)
  }
}

const unreadNotifications = computed(() => {
  return notificaciones.value.filter(n => !n.leido).length
})

const getNotificationColor = (tipo: string): string => {
  const colores: Record<string, string> = {
    solicitud: '#3b82f6',
    respuesta: '#10b981',
    info: '#78716c',
    warning: '#f59e0b',
    error: '#ef4444',
    success: '#10b981'
  }
  return colores[tipo] || '#78716c'
}

const getNotificationIcon = (tipo: string) => {
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

const formatTime = (timestamp: string): string => {
  try {
    const date = new Date(timestamp)
    const ahora = new Date()
    const diff = ahora.getTime() - date.getTime()
    const minutos = Math.floor(diff / 60000)
    const horas = Math.floor(diff / 3600000)

    if (minutos < 1) return 'Hace poco'
    if (minutos < 60) return `Hace ${minutos}m`
    if (horas < 24) return `Hace ${horas}h`
    return date.toLocaleDateString('es-CO')
  } catch {
    return 'Ahora'
  }
}

const actions = [
  { title: 'Usuarios', icon: Users, route: '/usuarios' },
  { title: 'Estadísticas', icon: BarChart3, route: '/estadisticas' },
  { title: 'Solicitudes', icon: FileText, route: '/solicitudes' },
  { title: 'Mapa', icon: MapPin, route: '/mapa' },
  { title: 'Sembradores', icon: Sprout, route: '/sembradores' },
]

const goTo = (route: string) => {
  if (route === '/usuarios' || route === '/estadisticas' || route === '/mapa' || route === '/sembradores' || route === '/solicitudes') {
    router.push(route)
  } else {
    alert(`👉 Próximamente: ${route}`)
  }
}

const logout = () => {
  auth.logout()
  window.location.href = '/login'
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-container {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  color: #fff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding-top: 56px;
}

/* ========== HEADER ========== */
.dashboard-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 9999;
  backdrop-filter: blur(12px);
  background: rgba(15, 23, 42, 0.95);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding: 0.6rem 0;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  width: 100%;
  min-height: 56px;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  height: 56px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  min-width: 0;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
  flex-shrink: 0;
}

.logo-svg {
  width: 24px;
  height: 24px;
  color: white;
}

.logo-text h1 {
  font-size: 1.1rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.logo-text p {
  font-size: 0.6rem;
  color: #94a3b8;
  margin: 0.1rem 0 0 0;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  padding: 0.4rem 0.6rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  font-size: 0.7rem;
  flex-shrink: 0;
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

.logout-btn:active {
  transform: translateY(0);
}

.logout-icon {
  width: 14px;
  height: 14px;
}

.logout-text {
  font-size: 0.7rem;
}

@media (max-width: 768px) {
  .logout-text {
    display: none;
  }

  .logout-btn {
    padding: 0.5rem;
  }

  .logo-icon {
    width: 40px;
    height: 40px;
  }

  .logo-text h1 {
    font-size: 1.25rem;
  }
}

/* ========== MAIN CONTENT ========== */
.dashboard-main {
  flex: 1;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 1rem 0.5rem;
  overflow-y: auto;
}

.dashboard-content {
  width: 100%;
  max-width: 900px;
}

/* ========== PROFILE CARD ========== */
.profile-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 20px;
  padding: 1rem 0.8rem;
  backdrop-filter: blur(10px);
  text-align: center;
  margin-bottom: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.profile-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: 0 12px 48px rgba(16, 185, 129, 0.1);
}

.avatar-wrapper {
  position: relative;
  width: 90px;
  height: 90px;
  margin: 0 auto 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-glow {
  position: absolute;
  inset: -10px;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  border-radius: 50%;
  opacity: 0.2;
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 0.4; }
}

.avatar-image {
  position: relative;
  width: 75px;
  height: 75px;
  border-radius: 50%;
  border: 3px solid #10b981;
  object-fit: cover;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
}

.welcome-section {
  margin-bottom: 0.75rem;
}

.welcome-icon-wrapper {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(34, 197, 94, 0.15));
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.5rem;
  transition: all 0.3s ease;
}

.welcome-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
  transition: transform 0.3s ease;
}

.profile-card:hover .welcome-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(34, 197, 94, 0.25));
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
  transform: scale(1.05);
}

.profile-card:hover .welcome-icon {
  transform: scale(1.15);
}

.welcome-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #e2e8f0;
}

.user-name {
  font-size: 1.3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.75rem;
}

.info-box {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 14px;
  padding: 0.7rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.info-icon {
  width: 18px;
  height: 18px;
  color: #10b981;
  flex-shrink: 0;
}

.info-text {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.info-label {
  font-size: 0.6rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 0.8rem;
  font-weight: 600;
  color: #e2e8f0;
  word-break: break-all;
}

.divider {
  height: 1px;
  background: rgba(148, 163, 184, 0.1);
}

/* ========== ACTIONS SECTION ========== */
.actions-section {
  margin-bottom: 1rem;
}

.section-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.8rem;
  color: #cbd5e1;
  text-align: center;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
  gap: 0.6rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .actions-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }
}

.action-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 14px;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  text-decoration: none;
  color: inherit;
}

.action-card:hover {
  transform: translateY(-6px);
  border-color: rgba(16, 185, 129, 0.5);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
  box-shadow: 0 12px 24px rgba(16, 185, 129, 0.2);
}

.action-card:active {
  transform: translateY(-2px);
}

.action-icon-wrapper {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  transition: all 0.3s ease;
}

.action-card:hover .action-icon-wrapper {
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
}

.action-icon {
  width: 20px;
  height: 20px;
  color: white;
}

.action-title {
  font-size: 0.7rem;
  font-weight: 600;
  color: #cbd5e1;
  text-align: center;
  transition: color 0.3s ease;
}

.action-card:hover .action-title {
  color: #10b981;
}

/* ========== SPECIALIZED MODULES SECTION ========== */
.specialized-section {
  margin-bottom: 1rem;
}

.specialized-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .specialized-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.6rem;
  }
}

@media (max-width: 480px) {
  .specialized-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}

.specialized-card {
  position: relative;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 1.2rem 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.6rem;
  text-decoration: none;
  color: inherit;
  overflow: hidden;
}

.specialized-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
  z-index: 0;
}

.specialized-card:hover::before {
  left: 100%;
}

.specialized-card:hover {
  transform: translateY(-8px);
  border-color: rgba(16, 185, 129, 0.4);
  box-shadow: 0 16px 32px rgba(16, 185, 129, 0.15);
}

.specialized-card:active {
  transform: translateY(-2px);
}

.specialized-icon-wrapper {
  position: relative;
  z-index: 1;
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.specialized-icon {
  font-size: 2rem;
  transition: transform 0.3s ease;
}

.specialized-icon-lucide {
  width: 32px;
  height: 32px;
  color: white;
  transition: transform 0.3s ease;
}

.specialized-card:hover .specialized-icon-lucide {
  transform: scale(1.2);
}

/* Variantes de color por tarjeta */
.specialized-seguimiento .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(34, 197, 94, 0.15));
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.specialized-seguimiento:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(34, 197, 94, 0.25));
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.specialized-sembradores .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(16, 185, 129, 0.15));
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.specialized-sembradores:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.3), rgba(16, 185, 129, 0.25));
  box-shadow: 0 8px 16px rgba(34, 197, 94, 0.3);
}

.specialized-reportes .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.15));
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.specialized-reportes:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(37, 99, 235, 0.25));
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
}

.specialized-usuarios .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(139, 92, 246, 0.15));
  border: 1px solid rgba(168, 85, 247, 0.3);
}

.specialized-usuarios:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(139, 92, 246, 0.25));
  box-shadow: 0 8px 16px rgba(168, 85, 247, 0.3);
}

.specialized-admin .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.15));
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.specialized-admin:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.3), rgba(220, 38, 38, 0.25));
  box-shadow: 0 8px 16px rgba(239, 68, 68, 0.3);
}

.specialized-solicitudes .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.15));
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.specialized-solicitudes:hover .specialized-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(5, 150, 105, 0.25));
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.specialized-title {
  position: relative;
  z-index: 1;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  color: #e2e8f0;
  transition: color 0.3s ease;
}

.specialized-card:hover .specialized-title {
  color: #10b981;
}

.specialized-desc {
  position: relative;
  z-index: 1;
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0;
  transition: color 0.3s ease;
}

.specialized-card:hover .specialized-desc {
  color: #cbd5e1;
}

.card-arrow {
  position: absolute;
  bottom: 1rem;
  right: 1.5rem;
  font-size: 1.25rem;
  color: #10b981;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s ease;
  z-index: 1;
}

.specialized-card:hover .card-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* ========== STATS GRID ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 0.6rem;
  margin-bottom: 1rem;
}

.stat-card {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 0.8rem 0.6rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(16, 185, 129, 0.3);
}

.stat-icon {
  font-size: 1.4rem;
  margin-bottom: 0.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-lucide {
  width: 20px;
  height: 20px;
  color: inherit;
}

.stat-text {
  font-size: 0.6rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.stat-online {
  border-left: 3px solid #10b981;
}

.stat-secure {
  border-left: 3px solid #3b82f6;
}

.stat-active {
  border-left: 3px solid #a855f7;
}

/* ========== NOTIFICATIONS SECTION ========== */
.notifications-section {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.4), rgba(30, 41, 59, 0.2));
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 14px;
  padding: 1.2rem 0.8rem;
  margin-bottom: 1rem;
  backdrop-filter: blur(10px);
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.notifications-badge {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  min-width: 28px;
}

.notifications-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem 1rem;
  color: #cbd5e1;
  text-align: center;
}

.empty-icon {
  color: #94a3b8;
  margin-bottom: 0.8rem;
  opacity: 0.6;
  width: 28px;
  height: 28px;
}

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  max-height: 300px;
  overflow-y: auto;
}

.notification-card {
  display: flex;
  gap: 0.75rem;
  padding: 0.8rem;
  background: rgba(30, 41, 59, 0.4);
  border-radius: 10px;
  border-left: 3px solid;
  transition: all 0.3s ease;
}

.notification-card.notif-unread {
  background: rgba(16, 185, 129, 0.05);
}

.notification-card:hover {
  background: rgba(30, 41, 59, 0.6);
  transform: translateX(4px);
}

.notif-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: 0.9;
}

.notif-content {
  flex: 1;
  min-width: 0;
}

.notif-title {
  color: #f1f5f9;
  font-weight: 600;
  font-size: 0.85rem;
  margin: 0 0 0.2rem 0;
  word-break: break-word;
}

.notif-message {
  color: #cbd5e1;
  font-size: 0.8rem;
  margin: 0 0 0.4rem 0;
  line-height: 1.3;
  word-break: break-word;
}

.notif-time {
  color: #94a3b8;
  font-size: 0.7rem;
  margin: 0;
}

/* ========== FOOTER ========== */
.dashboard-footer {
  text-align: center;
  padding: 0.8rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(10px);
  font-size: 0.7rem;
  color: #94a3b8;
}

.footer-highlight {
  color: #10b981;
  font-weight: 600;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .dashboard-main {
    padding: 0.8rem 0.4rem;
  }

  .profile-card {
    padding: 0.9rem 0.7rem;
  }
}

@media (max-width: 768px) {
  .dashboard-main {
    padding: 0.8rem 0.4rem;
  }

  .profile-card {
    padding: 0.9rem 0.7rem;
    margin-bottom: 0.8rem;
  }

  .avatar-wrapper {
    width: 80px;
    height: 80px;
    margin-bottom: 0.6rem;
  }

  .avatar-image {
    width: 65px;
    height: 65px;
  }

  .welcome-title {
    font-size: 1.1rem;
  }

  .user-name {
    font-size: 1.2rem;
  }

  .info-box {
    padding: 0.6rem;
  }

  .actions-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .specialized-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .dashboard-main {
    padding: 0.6rem 0.3rem;
  }

  .profile-card {
    padding: 0.8rem 0.6rem;
    margin-bottom: 0.7rem;
    border-radius: 16px;
  }

  .avatar-wrapper {
    width: 75px;
    height: 75px;
    margin-bottom: 0.5rem;
  }

  .avatar-image {
    width: 60px;
    height: 60px;
    border: 2px solid #10b981;
  }

  .welcome-title {
    font-size: 1rem;
  }

  .user-name {
    font-size: 1.1rem;
  }

  .info-box {
    padding: 0.5rem;
    gap: 0.5rem;
  }

  .info-item {
    gap: 0.6rem;
  }

  .section-title {
    font-size: 0.9rem;
    margin-bottom: 0.7rem;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }

  .action-card {
    padding: 0.6rem;
    gap: 0.3rem;
  }

  .action-icon-wrapper {
    width: 36px;
    height: 36px;
  }

  .action-icon {
    width: 18px;
    height: 18px;
  }

  .action-title {
    font-size: 0.65rem;
  }

  .specialized-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .specialized-card {
    padding: 1rem 0.8rem;
    gap: 0.5rem;
  }

  .specialized-icon-wrapper {
    width: 48px;
    height: 48px;
  }

  .specialized-title {
    font-size: 0.9rem;
  }

  .specialized-desc {
    font-size: 0.65rem;
  }

  .card-arrow {
    font-size: 1rem;
    bottom: 0.7rem;
    right: 0.8rem;
  }

  .stats-grid {
    gap: 0.5rem;
  }

  .stat-card {
    padding: 0.7rem 0.5rem;
  }

  .stat-lucide {
    width: 18px;
    height: 18px;
  }

  .stat-text {
    font-size: 0.55rem;
  }

  .notifications-section {
    padding: 1rem 0.7rem;
    margin-bottom: 0.8rem;
  }

  .notifications-header {
    margin-bottom: 0.8rem;
  }

  .notifications-badge {
    width: 26px;
    height: 26px;
    font-size: 0.75rem;
  }

  .notification-card {
    padding: 0.7rem;
    gap: 0.6rem;
  }

  .notif-icon {
    width: 32px;
    height: 32px;
  }

  .notif-title {
    font-size: 0.8rem;
  }

  .notif-message {
    font-size: 0.75rem;
  }

  .notif-time {
    font-size: 0.65rem;
  }

  .dashboard-footer {
    padding: 0.6rem;
    font-size: 0.65rem;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding-top: 56px;
    min-height: 100vh;
  }

  .dashboard-header {
    padding: 0;
    min-height: 56px;
  }

  .header-content {
    padding: 0 0.6rem;
    gap: 0.5rem;
    height: 56px;
  }

  .logo-section {
    gap: 0.4rem;
    flex: 1;
    min-width: 0;
  }

  .logo-icon {
    width: 32px;
    height: 32px;
    flex-shrink: 0;
  }

  .logo-svg {
    width: 18px;
    height: 18px;
  }

  .logo-text h1 {
    font-size: 0.95rem;
  }

  .logo-text p {
    font-size: 0.55rem;
  }

  .logout-btn {
    padding: 0.35rem 0.4rem;
    font-size: 0.65rem;
    flex-shrink: 0;
  }

  .logout-icon {
    width: 12px;
    height: 12px;
  }

  .dashboard-main {
    padding: 0.5rem 0.3rem;
    margin-top: 0;
  }

  .profile-card {
    padding: 0.7rem 0.5rem;
    margin-bottom: 0.6rem;
  }

  .avatar-wrapper {
    width: 70px;
    height: 70px;
    margin-bottom: 0.4rem;
  }

  .avatar-image {
    width: 55px;
    height: 55px;
    border: 2px solid #10b981;
  }

  .welcome-icon-wrapper {
    width: 40px;
    height: 40px;
    margin-bottom: 0.3rem;
  }

  .welcome-icon {
    width: 20px;
    height: 20px;
  }

  .welcome-title {
    font-size: 0.95rem;
  }

  .user-name {
    font-size: 1rem;
  }

  .info-box {
    padding: 0.4rem;
    gap: 0.4rem;
  }

  .info-item {
    gap: 0.5rem;
  }

  .info-icon {
    width: 16px;
    height: 16px;
  }

  .info-label {
    font-size: 0.55rem;
  }

  .info-value {
    font-size: 0.75rem;
  }

  .actions-section {
    margin-bottom: 0.8rem;
  }

  .section-title {
    font-size: 0.85rem;
    margin-bottom: 0.6rem;
  }

  .actions-grid {
    gap: 0.4rem;
  }

  .action-card {
    padding: 0.5rem;
    gap: 0.25rem;
  }

  .action-icon-wrapper {
    width: 32px;
    height: 32px;
  }

  .action-icon {
    width: 16px;
    height: 16px;
  }

  .action-title {
    font-size: 0.6rem;
  }

  .specialized-grid {
    gap: 0.4rem;
  }

  .specialized-card {
    padding: 0.8rem 0.6rem;
    gap: 0.4rem;
  }

  .specialized-icon-wrapper {
    width: 44px;
    height: 44px;
  }

  .specialized-icon-lucide {
    width: 24px;
    height: 24px;
  }

  .specialized-title {
    font-size: 0.85rem;
  }

  .specialized-desc {
    font-size: 0.6rem;
  }

  .card-arrow {
    font-size: 0.95rem;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.4rem;
  }

  .stat-card {
    padding: 0.6rem 0.4rem;
    border-radius: 10px;
  }

  .stat-icon {
    margin-bottom: 0.15rem;
  }

  .stat-lucide {
    width: 16px;
    height: 16px;
  }

  .stat-text {
    font-size: 0.5rem;
  }

  .notifications-section {
    padding: 0.8rem 0.6rem;
    border-radius: 12px;
    margin-bottom: 0.6rem;
  }

  .notifications-header {
    margin-bottom: 0.6rem;
  }

  .notifications-badge {
    width: 24px;
    height: 24px;
    font-size: 0.7rem;
  }

  .empty-icon {
    width: 24px;
    height: 24px;
    margin-bottom: 0.6rem;
  }

  .notifications-list {
    max-height: 250px;
    gap: 0.5rem;
  }

  .notification-card {
    padding: 0.6rem;
    border-radius: 8px;
  }

  .notif-icon {
    width: 30px;
    height: 30px;
  }

  .notif-title {
    font-size: 0.75rem;
  }

  .notif-message {
    font-size: 0.7rem;
    margin-bottom: 0.3rem;
  }

  .notif-time {
    font-size: 0.6rem;
  }

  .dashboard-footer {
    padding: 0.5rem;
    font-size: 0.6rem;
  }
}

@media (max-width: 360px) {
  .dashboard-container {
    padding-top: 50px;
  }

  .dashboard-header {
    padding: 0;
    min-height: 50px;
  }

  .header-content {
    padding: 0 0.4rem;
    gap: 0.2rem;
    height: 50px;
  }

  .logo-section {
    gap: 0.3rem;
  }

  .logo-icon {
    width: 28px;
    height: 28px;
  }

  .logo-text h1 {
    font-size: 0.8rem;
    font-weight: 700;
  }

  .logo-text p {
    font-size: 0.5rem;
  }

  .logout-btn {
    padding: 0.3rem 0.3rem;
    font-size: 0.6rem;
  }

  .logout-icon {
    width: 10px;
    height: 10px;
  }

  .profile-card {
    padding: 0.6rem 0.4rem;
  }

  .avatar-wrapper {
    width: 65px;
    height: 65px;
    margin-bottom: 0.3rem;
  }

  .avatar-image {
    width: 50px;
    height: 50px;
  }

  .welcome-title {
    font-size: 0.9rem;
  }

  .user-name {
    font-size: 0.95rem;
  }

  .action-card {
    padding: 0.4rem;
  }

  .action-icon-wrapper {
    width: 28px;
    height: 28px;
  }

  .action-icon {
    width: 14px;
    height: 14px;
  }

  .action-title {
    font-size: 0.55rem;
  }

  .specialized-card {
    padding: 0.7rem 0.5rem;
  }

  .specialized-icon-wrapper {
    width: 40px;
    height: 40px;
  }

  .specialized-title {
    font-size: 0.8rem;
  }

  .specialized-desc {
    font-size: 0.55rem;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .stat-card {
    padding: 0.5rem 0.3rem;
  }

  .notifications-section {
    padding: 0.7rem 0.5rem;
  }

  .notification-card {
    gap: 0.5rem;
  }
}

/* ========== ANIMACIONES ========== */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}
</style>
