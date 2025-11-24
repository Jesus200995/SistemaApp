<template>
  <div class="dashboard-container">
    <!-- Header moderno -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">
            <!-- Icono SVG personalizado: Carpeta con ubicación -->
            <svg viewBox="0 0 64 64" width="48" height="48" class="custom-logo-svg" xmlns="http://www.w3.org/2000/svg">
              <!-- Carpeta outline -->
              <g id="folder">
                <!-- Línea superior de la carpeta (pestaña) -->
                <path d="M 12 16 L 24 10 L 48 10 L 48 16" 
                      stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                <!-- Cuerpo de la carpeta -->
                <rect x="8" y="16" width="48" height="28" rx="3" 
                      stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              </g>
              
              <!-- Pin de ubicación en el centro con outline -->
              <g transform="translate(32, 32)">
                <!-- Pin shape outline -->
                <path d="M 0 -8 C -4.4 -8 -8 -4.4 -8 0 C -8 4 -3.6 8 0 13 C 3.6 8 8 4 8 0 C 8 -4.4 4.4 -8 0 -8 Z" 
                      stroke="#10b981" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                <!-- Círculo en la punta del pin -->
                <circle cx="0" cy="0" r="2.5" fill="#10b981" stroke="none"/>
              </g>
              
              <!-- Pequeños detalles de líneas dentro de la carpeta -->
              <line x1="16" y1="26" x2="48" y2="26" stroke="white" stroke-width="1.5" opacity="0.4" stroke-linecap="round"/>
              <line x1="16" y1="34" x2="40" y2="34" stroke="white" stroke-width="1.5" opacity="0.4" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="logo-text">
            <h1 class="app-title">Sistema de Administración</h1>
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
        <!-- Etiqueta de perfil -->
        <div class="profile-label">Mi Perfil</div>

        <!-- Tarjeta de perfil -->
        <div
          v-motion
          :initial="{ opacity: 0, scale: 0.8, y: 50 }"
          :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 200, duration: 700 } }"
          class="profile-card"
        >
          <!-- Avatar neon circle con iniciales -->
          <div class="profile-header">
            <div class="avatar-initials">
              {{ getInitials(auth.user?.nombre || 'U') }}
            </div>

            <!-- Información del usuario -->
            <div class="user-info-section">
              <h2 class="user-full-name">{{ auth.user?.nombre || 'Usuario' }}</h2>
              <div class="role-badge">{{ formatRole(auth.user?.rol || 'N/A') }}</div>
              <p class="user-email">{{ auth.user?.email || 'N/A' }}</p>
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

// Obtener iniciales del usuario (máximo 2 caracteres)
const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map((word) => word.charAt(0))
    .slice(0, 2)
    .join('')
    .toUpperCase()
}

// Formatear el rol correctamente (convertir a palabras legibles)
const formatRole = (role: string): string => {
  const roleMap: { [key: string]: string } = {
    admin: 'Administrador',
    territorial: 'Territorial',
    coordinador: 'Coordinador',
    sembrador: 'Sembrador',
    usuario: 'Usuario',
  }
  return roleMap[role?.toLowerCase()] || role
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
  width: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  color: #fff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  padding-top: 56px;
  box-sizing: border-box;
  position: relative;
  height: 100vh;
  will-change: scroll-position;
}

/* ========== HEADER ========== */
.dashboard-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 9999;
  backdrop-filter: blur(12px);
  background: linear-gradient(90deg, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.92) 100%);
  border-bottom: 2px solid rgba(16, 185, 129, 0.2);
  padding: 0;
  box-shadow: 0 8px 40px rgba(16, 185, 129, 0.15);
  width: 100%;
  height: 56px;
  animation: header-slide-down 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-sizing: border-box;
}

@keyframes header-slide-down {
  from {
    transform: translateY(-60px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.header-content {
  max-width: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  height: 56px;
  box-sizing: border-box;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 0;
  padding-left: 0.5rem;
}

.logo-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  padding: 4px;
}

.custom-logo-svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.logo-text h1 {
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: -0.5px;
  background: linear-gradient(90deg, #ffffff 0%, #10b981 25%, #ffffff 50%, #10b981 75%, #ffffff 100%);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  font-family: 'Segoe UI', 'Trebuchet MS', sans-serif;
  animation: gradient-flow 4s ease-in-out infinite;
}

@keyframes gradient-flow {
  0% {
    background-position: 0% center;
  }
  50% {
    background-position: 100% center;
  }
  100% {
    background-position: 0% center;
  }
}

.logo-text p {
  font-size: 0.7rem;
  color: #6ee7b7;
  margin: 0.05rem 0 0 0;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-family: 'Segoe UI', sans-serif;
  animation: subtitle-fade-in 1s ease-out 0.2s forwards;
  opacity: 0;
}

@keyframes subtitle-fade-in {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  font-size: 0.7rem;
  flex-shrink: 0;
  font-family: 'Segoe UI', sans-serif;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  margin-right: 0.5rem;
}

.logout-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(239, 68, 68, 0.5);
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

.logout-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
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
  padding: 0;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  width: 100%;
  min-height: calc(100vh - 56px);
  box-sizing: border-box;
}

.dashboard-content {
  width: 100%;
  max-width: 900px;
  padding: 1.5rem 0.5rem 3rem 0.5rem;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

/* ========== PROFILE LABEL ========== */
.profile-label {
  display: inline-block;
  background: linear-gradient(90deg, #10b981 0%, #84cc16 100%);
  color: #0f172a;
  padding: 0.35rem 1rem;
  border-radius: 6px 6px 0 0;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-align: center;
  margin-bottom: 0;
  margin-left: 0.5rem;
  text-transform: none;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
}

/* ========== PROFILE CARD ========== */
.profile-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 20px;
  padding: 1rem 0.8rem;
  backdrop-filter: blur(10px);
  text-align: left;
  margin-bottom: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  margin-top: -2px;
}

.profile-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: 0 12px 48px rgba(16, 185, 129, 0.1);
}

/* ===== NEW PROFILE HEADER LAYOUT ===== */
.profile-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.2rem;
}

.avatar-initials {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2.5px solid #84cc16;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  font-weight: 700;
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
  background: transparent;
  box-shadow: 
    inset 0 0 10px rgba(132, 204, 22, 0.2),
    0 0 15px rgba(132, 204, 22, 0.3);
}

.user-info-section {
  flex: 1;
}

.user-full-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 0.3rem;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.8rem;
  border: 1.5px solid #84cc16;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #84cc16;
  margin-bottom: 0.3rem;
}

.user-email {
  font-size: 0.85rem;
  color: #cbd5e1;
  font-style: italic;
  margin: 0;
}

/* ===== OLD STYLES (keeping for reference/removal) ===== */
.avatar-wrapper {
  display: none;
}

.avatar-glow {
  display: none;
}

.avatar-image {
  display: none;
}

.welcome-section {
  display: none;
}

.welcome-icon-wrapper {
  display: none;
}

.welcome-icon {
  display: none;
}

.welcome-title {
  display: none;
}

.user-name {
  display: none;
}

.info-box {
  display: none;
}

.info-item {
  display: none;
}

.info-icon {
  display: none;
}

.info-text {
  display: none;
}

.info-label {
  display: none;
}

.info-value {
  display: none;
}

.divider {
  display: none;
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
  background: transparent;
  border: 2px solid rgba(132, 204, 22, 0.3);
  border-radius: 20px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  color: inherit;
}

.action-card:hover {
  transform: translateY(-8px);
  border-color: #84cc16;
  background: rgba(132, 204, 22, 0.08);
  box-shadow: 0 12px 32px rgba(132, 204, 22, 0.25), inset 0 0 20px rgba(132, 204, 22, 0.1);
}

.action-card:active {
  transform: translateY(-4px);
}

.action-icon-wrapper {
  width: 48px;
  height: 48px;
  background: transparent;
  border: 2.5px solid #84cc16;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 15px rgba(132, 204, 22, 0.4);
  transition: all 0.3s ease;
}

.action-card:hover .action-icon-wrapper {
  transform: scale(1.15) rotate(5deg);
  box-shadow: 0 0 25px rgba(132, 204, 22, 0.6);
  background: rgba(132, 204, 22, 0.1);
}

.action-icon {
  width: 24px;
  height: 24px;
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
}

.action-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #e2e8f0;
  text-align: center;
  transition: color 0.3s ease;
  letter-spacing: 0.5px;
}

.action-card:hover .action-title {
  color: #84cc16;
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
  background: rgba(132, 204, 22, 0.08);
  border: 2px solid rgba(132, 204, 22, 0.3);
  border-radius: 20px;
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
  backdrop-filter: blur(10px);
}

.specialized-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(132, 204, 22, 0.1), transparent);
  transition: left 0.5s ease;
  z-index: 0;
}

.specialized-card:hover::before {
  left: 100%;
}

.specialized-card:hover {
  transform: translateY(-8px);
  border-color: #84cc16;
  background: rgba(132, 204, 22, 0.15);
  box-shadow: 0 16px 40px rgba(132, 204, 22, 0.25), inset 0 0 20px rgba(132, 204, 22, 0.1);
}

.specialized-card:active {
  transform: translateY(-4px);
}

.specialized-icon-wrapper {
  position: relative;
  z-index: 1;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  background: transparent;
  border: 2.5px solid #84cc16;
  box-shadow: 0 0 15px rgba(132, 204, 22, 0.4);
}

.specialized-icon {
  font-size: 2rem;
  transition: transform 0.3s ease;
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
}

.specialized-icon-lucide {
  width: 28px;
  height: 28px;
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
  transition: transform 0.3s ease;
}

.specialized-card:hover .specialized-icon-wrapper {
  transform: scale(1.15) rotate(5deg);
  box-shadow: 0 0 25px rgba(132, 204, 22, 0.6);
  background: rgba(132, 204, 22, 0.1);
}

.specialized-card:hover .specialized-icon-lucide {
  transform: scale(1.2);
}

/* Variantes de color por tarjeta - todas usan verde neon ahora */
.specialized-seguimiento .specialized-icon-wrapper {
  border-color: #84cc16;
  box-shadow: 0 0 15px rgba(132, 204, 22, 0.4);
}

.specialized-seguimiento .specialized-icon,
.specialized-seguimiento .specialized-icon-lucide {
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
}

.specialized-seguimiento:hover .specialized-icon-wrapper {
  box-shadow: 0 0 25px rgba(132, 204, 22, 0.6);
  background: rgba(132, 204, 22, 0.1);
}

.specialized-sembradores .specialized-icon-wrapper {
  border-color: #84cc16;
  box-shadow: 0 0 15px rgba(132, 204, 22, 0.4);
}

.specialized-sembradores .specialized-icon,
.specialized-sembradores .specialized-icon-lucide {
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
}

.specialized-sembradores:hover .specialized-icon-wrapper {
  box-shadow: 0 0 25px rgba(132, 204, 22, 0.6);
  background: rgba(132, 204, 22, 0.1);
}

.specialized-reportes .specialized-icon-wrapper {
  border-color: #84cc16;
  box-shadow: 0 0 15px rgba(132, 204, 22, 0.4);
}

.specialized-reportes .specialized-icon,
.specialized-reportes .specialized-icon-lucide {
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
}

.specialized-reportes:hover .specialized-icon-wrapper {
  box-shadow: 0 0 25px rgba(132, 204, 22, 0.6);
  background: rgba(132, 204, 22, 0.1);
}

.specialized-usuarios .specialized-icon-wrapper {
  border-color: #84cc16;
  box-shadow: 0 0 15px rgba(132, 204, 22, 0.4);
}

.specialized-usuarios .specialized-icon,
.specialized-usuarios .specialized-icon-lucide {
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
}

.specialized-usuarios:hover .specialized-icon-wrapper {
  box-shadow: 0 0 25px rgba(132, 204, 22, 0.6);
  background: rgba(132, 204, 22, 0.1);
}

.specialized-admin .specialized-icon-wrapper {
  border-color: #84cc16;
  box-shadow: 0 0 15px rgba(132, 204, 22, 0.4);
}

.specialized-admin .specialized-icon,
.specialized-admin .specialized-icon-lucide {
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
}

.specialized-admin:hover .specialized-icon-wrapper {
  box-shadow: 0 0 25px rgba(132, 204, 22, 0.6);
  background: rgba(132, 204, 22, 0.1);
}

.specialized-solicitudes .specialized-icon-wrapper {
  border-color: #84cc16;
  box-shadow: 0 0 15px rgba(132, 204, 22, 0.4);
}

.specialized-solicitudes .specialized-icon,
.specialized-solicitudes .specialized-icon-lucide {
  color: #84cc16;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.6);
}

.specialized-solicitudes:hover .specialized-icon-wrapper {
  box-shadow: 0 0 25px rgba(132, 204, 22, 0.6);
  background: rgba(132, 204, 22, 0.1);
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
    padding: 0;
  }

  .profile-card {
    padding: 0.9rem 0.7rem;
  }
}

@media (max-width: 768px) {
  .dashboard-main {
    padding: 0;
  }

  .profile-label {
    font-size: 0.65rem;
    padding: 0.3rem 0.9rem;
  }

  .profile-card {
    padding: 0.9rem 0.7rem;
    margin-bottom: 0.8rem;
  }

  .profile-header {
    gap: 0.8rem;
  }

  .avatar-initials {
    width: 55px;
    height: 55px;
    font-size: 1.3rem;
  }

  .user-full-name {
    font-size: 1.1rem;
  }

  .role-badge {
    font-size: 0.8rem;
    padding: 0.2rem 0.7rem;
  }

  .user-email {
    font-size: 0.8rem;
  }

  .action-card {
    padding: 0.9rem;
  }

  .action-icon-wrapper {
    width: 44px;
    height: 44px;
    border-width: 2px;
  }

  .action-icon {
    width: 22px;
    height: 22px;
  }

  .action-title {
    font-size: 0.7rem;
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
    padding: 0;
  }

  .profile-label {
    font-size: 0.6rem;
    padding: 0.25rem 0.8rem;
  }

  .profile-card {
    padding: 0.8rem 0.6rem;
    margin-bottom: 0.7rem;
    border-radius: 16px;
  }

  .profile-header {
    gap: 0.7rem;
  }

  .avatar-initials {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
    border-width: 2px;
  }

  .user-full-name {
    font-size: 1rem;
  }

  .role-badge {
    font-size: 0.75rem;
    padding: 0.2rem 0.6rem;
  }

  .user-email {
    font-size: 0.75rem;
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
    padding: 0.8rem;
    gap: 0.4rem;
  }

  .action-icon-wrapper {
    width: 42px;
    height: 42px;
    border-width: 2px;
  }

  .action-icon {
    width: 20px;
    height: 20px;
  }

  .action-title {
    font-size: 0.68rem;
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
    width: 40px;
    height: 40px;
    flex-shrink: 0;
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
    padding: 0;
    margin-top: 0;
  }

  .profile-label {
    font-size: 0.6rem;
    padding: 0.25rem 0.7rem;
  }

  .profile-card {
    padding: 0.7rem 0.5rem;
    margin-bottom: 0.6rem;
  }

  .profile-header {
    gap: 0.6rem;
  }

  .avatar-initials {
    width: 48px;
    height: 48px;
    font-size: 1.1rem;
    border-width: 2px;
  }

  .user-full-name {
    font-size: 0.95rem;
  }

  .role-badge {
    font-size: 0.7rem;
    padding: 0.15rem 0.5rem;
  }

  .user-email {
    font-size: 0.7rem;
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
    padding: 0.7rem;
    gap: 0.3rem;
  }

  .action-icon-wrapper {
    width: 38px;
    height: 38px;
    border-width: 2px;
  }

  .action-icon {
    width: 18px;
    height: 18px;
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

  .profile-label {
    font-size: 0.55rem;
    padding: 0.2rem 0.6rem;
  }

  .profile-card {
    padding: 0.6rem 0.4rem;
  }

  .profile-header {
    gap: 0.5rem;
  }

  .avatar-initials {
    width: 44px;
    height: 44px;
    font-size: 1rem;
    border-width: 2px;
  }

  .user-full-name {
    font-size: 0.9rem;
  }

  .role-badge {
    font-size: 0.65rem;
    padding: 0.1rem 0.4rem;
  }

  .user-email {
    font-size: 0.65rem;
  }

  .action-card {
    padding: 0.6rem;
    gap: 0.25rem;
  }

  .action-icon-wrapper {
    width: 36px;
    height: 36px;
    border-width: 2px;
  }

  .action-icon {
    width: 17px;
    height: 17px;
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
.dashboard-main::-webkit-scrollbar {
  width: 0;
  background: transparent;
}

.dashboard-main::-webkit-scrollbar-track {
  background: transparent;
}

.dashboard-main::-webkit-scrollbar-thumb {
  background: transparent;
}
</style>
