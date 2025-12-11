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
        <div class="profile-card">
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
              @click="goTo(action.route)"
              class="action-card"
            >
              <!-- Badge de solicitudes pendientes -->
              <div 
                v-if="action.route === '/solicitudes' && solicitudesPendientes > 0" 
                class="solicitudes-badge"
              >
                {{ solicitudesPendientes }}
              </div>
              <div class="action-icon-wrapper">
                <component :is="action.icon" class="action-icon" />
              </div>
              <span class="action-title">{{ action.title }}</span>
            </div>
          </div>
        </div>

        <!-- Sección de notificaciones recientes -->
        <div class="notifications-section">
          <div class="notifications-header">
            <div class="header-left-notif">
              <Bell :size="18" class="header-bell-icon" />
              <h3 class="section-title">Notificaciones Recientes</h3>
            </div>
            <div class="notifications-badge-glass">
              {{ solicitudesPendientesLista.length }}
            </div>
          </div>

          <div v-if="solicitudesPendientesLista.length === 0" class="notifications-empty">
            <div class="empty-icon-wrapper">
              <Bell :size="24" class="empty-icon" />
            </div>
            <p>Sin notificaciones pendientes</p>
          </div>

          <div v-else class="notifications-list">
            <div 
              v-for="solicitud in solicitudesPendientesLista.slice(0, 3)"
              :key="'notif-' + solicitud.id"
              class="notif-card-pro"
            >
              <!-- Animación de fondo rojo -->
              <div class="notif-bg-pulse"></div>
              
              <!-- Icono de solicitud a la izquierda -->
              <div class="notif-icon-left">
                <FileText :size="22" class="notif-main-icon" />
                <span class="notif-icon-label">Solicitud</span>
              </div>
              
              <!-- Contenido -->
              <div class="notif-card-content">
                <!-- Fecha arriba del tipo -->
                <span class="notif-fecha-top">{{ formatFechaCorta(solicitud.fecha) }}</span>
                
                <!-- Tipo de solicitud (completo y destacado) -->
                <span class="notif-tipo-tag">{{ formatTipoSolicitud(solicitud.tipo) }}</span>
                
                <!-- Usuario y rol -->
                <div class="notif-user-details">
                  <span class="notif-user-name">{{ solicitud.solicitante?.nombre || 'Usuario' }}</span>
                  <span class="notif-user-rol">{{ formatRolUsuario(solicitud.solicitante?.rol) }}</span>
                </div>
                
                <!-- Descripción como mensaje con fondo vidrio -->
                <div v-if="solicitud.descripcion" class="notif-mensaje-box">
                  <p class="notif-mensaje-text">{{ truncateText(solicitud.descripcion, 60) }}</p>
                </div>
              </div>
              
              <!-- Botón Ver medio círculo derecho -->
              <router-link to="/solicitudes" class="notif-btn-semicircle">
                <span class="semicircle-text">Ir</span>
              </router-link>
            </div>
          </div>
        </div>


      </div>
    </main>

    <!-- Footer -->
    <footer class="dashboard-footer">
      <p>© 2025 <span class="footer-highlight">SistemaApp</span>. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, onUnmounted } from 'vue'
// @ts-ignore
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl, getSecureWsUrl } from '../utils/api'
import { useRouter } from 'vue-router'
import { LogOut, User, Mail, LayoutDashboard, BarChart3, Users, Settings, MapPin, Sprout, FileText, Smile, Clipboard, Check, Shield, Zap, Bell, Clock, CheckCircle, AlertCircle, Info, Eye, MessageSquare } from 'lucide-vue-next'
import axios from 'axios'

const auth = useAuthStore()
const router = useRouter()
const notificaciones = ref<any[]>([])
const ws = ref<WebSocket | null>(null)
const solicitudesPendientes = ref(0)
const solicitudesRecientes = ref<any[]>([])

// Intervalo para actualizar solicitudes en tiempo real
let solicitudesInterval: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  auth.fetchProfile()
  getNotificaciones()
  connectWebSocket()
  getSolicitudesPendientes()
  // Actualizar cada 30 segundos
  solicitudesInterval = setInterval(getSolicitudesPendientes, 30000)
})

onUnmounted(() => {
  if (ws.value) {
    ws.value.close()
  }
  if (solicitudesInterval) {
    clearInterval(solicitudesInterval)
  }
})

const connectWebSocket = () => {
  try {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const apiUrl = getSecureApiUrl()
    
    let wsUrl = ''
    if (apiUrl.startsWith('/')) {
      wsUrl = `${protocol}//${window.location.host}${apiUrl}/notificaciones/ws`
    } else {
      const host = apiUrl.replace(/^(https?:\/\/)/, '').replace(/\/$/, '')
      wsUrl = `${protocol}//${host}/notificaciones/ws`
    }
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
    const apiUrl = getSecureApiUrl()
    const response = await axios.get(
      `${apiUrl}/notificaciones`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    notificaciones.value = (response.data || []).reverse()
    console.log('✅ Notificaciones cargadas en Dashboard:', notificaciones.value.length)
  } catch (error) {
    console.error('❌ Error cargando notificaciones:', error)
  }
}

// Obtener solicitudes pendientes
const getSolicitudesPendientes = async () => {
  try {
    const token = localStorage.getItem('token') || auth.token
    const apiUrl = getSecureApiUrl()
    const response = await axios.get(
      `${apiUrl}/solicitudes`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    const solicitudes = response.data || []
    const userId = auth.user?.id
    
    // Filtrar solo las pendientes que ME LLEGARON (no las que yo envié)
    solicitudesPendientes.value = solicitudes.filter((s: any) => 
      s.estado === 'pendiente' && 
      s.destino_id === userId &&
      s.usuario_id !== userId
    ).length
    
    // Guardar las solicitudes recientes (últimas 10 ordenadas por fecha)
    solicitudesRecientes.value = solicitudes
      .sort((a: any, b: any) => new Date(b.fecha).getTime() - new Date(a.fecha).getTime())
      .slice(0, 10)
    console.log('📋 Solicitudes pendientes (recibidas):', solicitudesPendientes.value)
    console.log('📋 Solicitudes recientes:', solicitudesRecientes.value.length)
  } catch (error) {
    console.error('❌ Error cargando solicitudes:', error)
  }
}

// Funciones auxiliares para solicitudes
const formatTipoSolicitud = (tipo: string): string => {
  const tipos: Record<string, string> = {
    cambio_superior: 'Cambio de Superior',
    alta_subordinado: 'Alta de Subordinado',
    baja_subordinado: 'Baja de Subordinado',
    cambio_territorio: 'Cambio de Territorio',
    otro: 'Otro'
  }
  return tipos[tipo] || tipo
}

const formatEstadoSolicitud = (estado: string): string => {
  const estados: Record<string, string> = {
    pendiente: 'Pendiente',
    aprobada: 'Aprobada',
    rechazada: 'Rechazada'
  }
  return estados[estado] || estado
}

const truncateText = (text: string, maxLength: number): string => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const formatTimeAgo = (fecha: string): string => {
  if (!fecha) return ''
  const now = new Date()
  const date = new Date(fecha)
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'Ahora'
  if (diffMins < 60) return `Hace ${diffMins}m`
  if (diffHours < 24) return `Hace ${diffHours}h`
  if (diffDays < 7) return `Hace ${diffDays}d`
  return date.toLocaleDateString('es-MX', { day: 'numeric', month: 'short' })
}

// Formato de fecha corta para notificaciones
const formatFechaCorta = (fecha: string): string => {
  if (!fecha) return ''
  const date = new Date(fecha)
  return date.toLocaleDateString('es-MX', { 
    day: 'numeric', 
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Obtener iniciales del nombre
const getInitials = (nombre: string | undefined): string => {
  if (!nombre) return '?'
  const parts = nombre.trim().split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return nombre.substring(0, 2).toUpperCase()
}

// Formatear rol de usuario
const formatRolUsuario = (rol: string | undefined): string => {
  if (!rol) return 'Usuario'
  const roles: Record<string, string> = {
    admin: 'Administrador',
    territorial: 'Territorial',
    facilitador: 'Facilitador',
    tecnico: 'Técnico',
    tecnico_operativo: 'Técnico Operativo',
    tecnico_titular: 'Técnico Titular',
    tecnico_productivo: 'Técnico Productivo',
    tecnico_social: 'Técnico Social',
    coordinador: 'Coordinador',
    sembrador: 'Sembrador',
    usuario: 'Usuario'
  }
  // Buscar coincidencia exacta primero
  if (roles[rol.toLowerCase()]) {
    return roles[rol.toLowerCase()]
  }
  // Si no hay coincidencia, formatear el texto (reemplazar _ por espacio y capitalizar)
  return rol.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')
}

// Lista de solicitudes pendientes (solo pendientes que ME LLEGARON, no las que YO envié)
const solicitudesPendientesLista = computed(() => {
  const userId = auth.user?.id
  return solicitudesRecientes.value.filter((s: any) => 
    s.estado === 'pendiente' && 
    s.destino_id === userId &&      // Me llegaron a mí
    s.usuario_id !== userId          // No las envié yo
  )
})

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

const actions = computed(() => {
  const rol = auth.user?.rol || ''
  const isTecnico = rol.includes('tecnico')
  const canManageUsers = ['admin', 'territorial', 'facilitador'].includes(rol)
  const canViewStats = ['admin', 'territorial', 'facilitador'].includes(rol)
  const isAdmin = rol === 'admin'
  
  const baseActions = []
  
  // Panel Global - Solo Admin
  if (isAdmin) {
    baseActions.push({ title: 'Panel Global', icon: Settings, route: '/admin-panel' })
  }
  
  // Usuarios - Solo Admin, Territorial, Facilitador
  if (canManageUsers) {
    baseActions.push({ title: 'Usuarios', icon: Users, route: '/usuarios' })
  }
  
  // Estadísticas - Solo Admin, Territorial, Facilitador
  if (canViewStats) {
    baseActions.push({ title: 'Estadísticas', icon: BarChart3, route: '/estadisticas' })
  }
  
  // Solicitudes - Todos los roles
  baseActions.push({ title: 'Solicitudes', icon: FileText, route: '/solicitudes' })
  
  // Sembradores - Todos los roles
  baseActions.push({ title: 'Sembradores', icon: Sprout, route: '/sembradores' })
  
  // Mapa - Todos los roles
  baseActions.push({ title: 'Mapa', icon: MapPin, route: '/mapa' })
  
  // Seguimiento - Solo técnicos
  if (isTecnico) {
    baseActions.push({ title: 'Seguimiento', icon: Clipboard, route: '/seguimiento' })
  }
  
  return baseActions
})

const goTo = (route: string) => {
  const validRoutes = ['/usuarios', '/estadisticas', '/solicitudes', '/mapa', '/sembradores', '/seguimiento', '/admin-panel']
  if (validRoutes.includes(route)) {
    router.push(route)
  } else {
    alert(`👉 Próximamente: ${route}`)
  }
}

const logout = () => {
  auth.logout()
  window.location.href = '/login'
}

// Formatear el rol correctamente (convertir a palabras legibles)
const formatRole = (role: string): string => {
  const roleMap: { [key: string]: string } = {
    admin: 'Administrador',
    territorial: 'Territorial',
    coordinador: 'Coordinador',
    facilitador: 'Facilitador',
    tecnico_productivo: 'Técnico Productivo',
    tecnico_social: 'Técnico Social',
    sembrador: 'Sembrador',
    usuario: 'Usuario',
  }
  return roleMap[role?.toLowerCase()] || role
}

// Obtener descripción de gestión de usuarios según el rol
const getUsuariosDesc = (): string => {
  const rol = auth.user?.rol
  if (rol === 'admin') {
    return 'Administrar todos los usuarios'
  } else if (rol === 'territorial') {
    return 'Gestionar facilitadores'
  } else if (rol === 'facilitador') {
    return 'Gestionar técnicos'
  }
  return 'Ver usuarios'
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
  padding-top: 62px;
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
  background: rgba(132, 204, 22, 0.18);
  border-bottom: 2px solid rgba(132, 204, 22, 0.3);
  padding: 0;
  box-shadow: 0 8px 40px rgba(132, 204, 22, 0.15);
  width: 100%;
  height: 62px;
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
  height: 62px;
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
  margin: 0;
}

.custom-logo-svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.logo-text h1 {
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: -0.5px;
  color: #ffffff;
  margin: 0;
  font-family: 'Segoe UI', 'Trebuchet MS', sans-serif;
  text-shadow: 0 0 10px rgba(132, 204, 22, 0.4);
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
  color: #84cc16;
  margin: 0.02rem 0 0 0;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-family: 'Segoe UI', sans-serif;
  animation: subtitle-fade-in 1s ease-out 0.2s forwards;
  opacity: 1;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.5);
  line-height: 1;
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
  padding: 1.5rem 1.2rem 3rem 1.2rem;
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
  background: rgba(132, 204, 22, 0.08);
  border: 1.5px solid rgba(132, 204, 22, 0.3);
  border-radius: 20px;
  padding: 1rem 0.8rem;
  backdrop-filter: blur(10px);
  text-align: left;
  margin-bottom: 1rem;
  box-shadow: 0 8px 32px rgba(132, 204, 22, 0.1);
  transition: all 0.3s ease;
  margin-top: -2px;
}

.profile-card:hover {
  border-color: rgba(132, 204, 22, 0.5);
  box-shadow: 0 12px 48px rgba(132, 204, 22, 0.2);
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
  color: #ffffff;
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
  color: #ffffff;
  text-align: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 0.5rem 0;
}

.section-title::before,
.section-title::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(132, 204, 22, 0.5), transparent);
  animation: greenLightPass 3s ease-in-out infinite;
}

.section-title::before {
  animation-delay: 0s;
}

.section-title::after {
  animation-delay: 0s;
}

@keyframes greenLightPass {
  0% {
    box-shadow: inset 0 0 0px rgba(132, 204, 22, 0.3);
  }
  50% {
    box-shadow: inset 0 0 15px rgba(132, 204, 22, 0.8);
  }
  100% {
    box-shadow: inset 0 0 0px rgba(132, 204, 22, 0.3);
  }
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
  position: relative;
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
  overflow: visible;
}

/* Badge de solicitudes pendientes */
.solicitudes-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: 700;
  color: white;
  background: radial-gradient(ellipse at 30% 30%, rgba(252, 165, 165, 0.6), rgba(248, 113, 113, 0.45) 50%, rgba(239, 68, 68, 0.35));
  border: 1px solid rgba(248, 113, 113, 0.5);
  border-radius: 50%;
  backdrop-filter: blur(10px);
  z-index: 10;
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
  border-radius: 28px;
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

/* Badge de solicitudes pendientes en módulos especializados */
.specialized-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: white;
  background: radial-gradient(ellipse at 30% 30%, rgba(252, 165, 165, 0.6), rgba(248, 113, 113, 0.45) 50%, rgba(239, 68, 68, 0.35));
  border: 1px solid rgba(248, 113, 113, 0.5);
  border-radius: 50%;
  backdrop-filter: blur(10px);
  z-index: 10;
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

/* ========== NOTIFICATIONS SECTION (Solicitudes Recientes) ========== */
.notifications-section {
  background: rgba(132, 204, 22, 0.06);
  border: 1.5px solid rgba(132, 204, 22, 0.25);
  border-radius: 16px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  backdrop-filter: blur(12px);
  box-shadow: 
    0 8px 32px rgba(132, 204, 22, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid rgba(132, 204, 22, 0.15);
}

.header-left-notif {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  line-height: 1;
}

.header-bell-icon {
  color: #f87171;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-left-notif .section-title {
  margin: 0;
  line-height: 1;
  display: flex;
  align-items: center;
}

/* Badge rojo suave estilo vidrio */
.notifications-badge-glass {
  min-width: 22px;
  height: 22px;
  padding: 0 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: white;
  background: radial-gradient(ellipse at 30% 30%, rgba(248, 113, 113, 0.5), rgba(239, 68, 68, 0.4) 50%, rgba(220, 38, 38, 0.3));
  border: 1px solid rgba(248, 113, 113, 0.4);
  border-radius: 50%;
  backdrop-filter: blur(10px);
  line-height: 1;
}

/* Tarjeta de notificación profesional */
.notif-card-pro {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.9rem;
  padding-right: 55px; /* Espacio para el botón semicírculo */
  background: rgba(30, 41, 59, 0.6);
  border-radius: 12px;
  border: 1px solid rgba(239, 68, 68, 0.2);
  transition: all 0.3s ease;
  overflow: hidden;
}

.notif-card-pro:hover {
  border-color: rgba(239, 68, 68, 0.35);
  transform: translateY(-2px);
}

/* Animación de fondo blanco suave de lado a lado */
.notif-bg-pulse {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.06) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmerSlide 4s ease-in-out infinite;
  pointer-events: none;
}

@keyframes shimmerSlide {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.notif-card-content {
  flex: 1;
  min-width: 0;
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding-left: 0.8rem;
  border-left: 1px solid rgba(148, 163, 184, 0.2);
}

/* Icono de solicitud a la izquierda */
.notif-icon-left {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  z-index: 1;
  gap: 0.15rem;
}

.notif-main-icon {
  color: #f87171;
}

.notif-icon-label {
  font-size: 0.5rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.notif-tipo-tag {
  font-size: 0.8rem;
  font-weight: 700;
  color: #f87171;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

/* Fecha arriba del contenido */
.notif-fecha-top {
  font-size: 0.65rem;
  color: #64748b;
  margin-bottom: 0.2rem;
  display: block;
}

.notif-user-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
  margin-bottom: 0.2rem;
}

.notif-user-name {
  font-size: 0.75rem;
  font-weight: 500;
  color: #cbd5e1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notif-user-rol {
  font-size: 0.65rem;
  color: #94a3b8;
  font-style: italic;
}

/* Botón Ver medio círculo pegado a la derecha */
.notif-btn-semicircle {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 42px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 6px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(37, 99, 235, 0.35) 100%);
  border: 1.5px solid rgba(96, 165, 250, 0.4);
  border-right: none;
  border-radius: 30px 0 0 30px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(12px);
  box-shadow: 
    -4px 0 20px rgba(59, 130, 246, 0.2),
    inset 2px 0 8px rgba(255, 255, 255, 0.1);
  z-index: 5;
}

.notif-btn-semicircle:hover {
  width: 50px;
  background: linear-gradient(135deg, rgba(96, 165, 250, 0.35) 0%, rgba(59, 130, 246, 0.45) 100%);
  border-color: rgba(147, 197, 253, 0.6);
  box-shadow: 
    -6px 0 25px rgba(59, 130, 246, 0.35),
    inset 2px 0 12px rgba(255, 255, 255, 0.15);
}

.semicircle-text {
  font-size: 0.7rem;
  font-weight: 600;
  color: #93c5fd;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.notif-btn-semicircle:hover .semicircle-text {
  color: #bfdbfe;
}

/* Caja de mensaje con fondo vidrio gris y esquina picuda */
.notif-mensaje-box {
  position: relative;
  background: rgba(100, 116, 139, 0.12);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 0 8px 8px 8px;
  padding: 0.35rem 0.6rem;
  backdrop-filter: blur(6px);
  margin-top: 0.15rem;
}

/* Esquina picuda tipo mensaje */
.notif-mensaje-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: -6px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 6px 8px 0;
  border-color: transparent rgba(100, 116, 139, 0.12) transparent transparent;
}

.notif-mensaje-text {
  font-size: 0.7rem;
  color: #94a3b8;
  margin: 0;
  line-height: 1.35;
  font-style: italic;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notif-descripcion {
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0.25rem 0;
  line-height: 1.3;
  font-style: italic;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

/* Botón Ver con efecto vidrio líquido sin brillo */
.notif-btn-glass {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-radius: 8px;
  color: #f87171;
  font-size: 0.75rem;
  font-weight: 600;
  text-decoration: none;
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.notif-btn-glass:hover {
  background: rgba(239, 68, 68, 0.18);
  border-color: rgba(239, 68, 68, 0.4);
  transform: scale(1.02);
}

@keyframes bellPulse {
  0%, 100% { transform: rotate(0deg); opacity: 1; }
  25% { transform: rotate(10deg); }
  50% { transform: rotate(-10deg); opacity: 0.8; }
  75% { transform: rotate(5deg); }
}

.notifications-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  color: #cbd5e1;
  text-align: center;
}

.empty-icon-wrapper {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.8rem;
}

.empty-icon {
  color: #f59e0b;
  opacity: 0.6;
}

.empty-hint {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 0.3rem;
}

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  max-height: 320px;
  overflow-y: auto;
  padding-right: 0.3rem;
}

/* Tarjeta de solicitud en notificaciones */
.solicitud-notif-card {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  padding: 0.9rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.15);
  transition: all 0.3s ease;
  position: relative;
}

.solicitud-notif-card:hover {
  background: rgba(30, 41, 59, 0.7);
  transform: translateX(4px);
  border-color: rgba(132, 204, 22, 0.3);
}

.solicitud-notif-card.sol-pendiente {
  border-left: 3px solid #f59e0b;
}

.solicitud-notif-card.sol-aprobada {
  border-left: 3px solid #10b981;
}

.solicitud-notif-card.sol-rechazada {
  border-left: 3px solid #ef4444;
}

.sol-status-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 0.2rem;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: dotPulse 2s ease-in-out infinite;
}

.status-dot.dot-pendiente {
  background: #f59e0b;
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
}

.status-dot.dot-aprobada {
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.5);
}

.status-dot.dot-rechazada {
  background: #ef4444;
  box-shadow: 0 0 8px rgba(239, 68, 68, 0.5);
}

@keyframes dotPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
}

.sol-notif-content {
  flex: 1;
  min-width: 0;
}

.sol-notif-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
  flex-wrap: wrap;
}

.sol-tipo-badge {
  background: rgba(132, 204, 22, 0.15);
  color: #a3e635;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.sol-estado-text {
  font-size: 0.65rem;
  font-weight: 600;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
}

.sol-estado-text.estado-pendiente {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
}

.sol-estado-text.estado-aprobada {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.sol-estado-text.estado-rechazada {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.sol-descripcion {
  color: #e2e8f0;
  font-size: 0.8rem;
  line-height: 1.4;
  margin: 0 0 0.5rem 0;
  word-break: break-word;
}

.sol-meta {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.sol-fecha,
.sol-user {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.7rem;
  color: #94a3b8;
}

.sol-view-btn {
  background: linear-gradient(
    135deg,
    rgba(132, 204, 22, 0.2) 0%,
    rgba(132, 204, 22, 0.1) 100%
  );
  border: 1px solid rgba(132, 204, 22, 0.3);
  border-radius: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #84cc16;
  transition: all 0.3s ease;
  flex-shrink: 0;
  text-decoration: none;
}

.sol-view-btn:hover {
  background: rgba(132, 204, 22, 0.3);
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(132, 204, 22, 0.3);
}

/* Botón ver todas */
.view-all-solicitudes-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.7rem 1rem;
  background: linear-gradient(
    135deg,
    rgba(132, 204, 22, 0.15) 0%,
    rgba(132, 204, 22, 0.08) 100%
  );
  border: 1px solid rgba(132, 204, 22, 0.25);
  border-radius: 10px;
  color: #a3e635;
  font-size: 0.8rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  backdrop-filter: blur(8px);
}

.view-all-solicitudes-btn:hover {
  background: rgba(132, 204, 22, 0.25);
  border-color: rgba(132, 204, 22, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(132, 204, 22, 0.2);
}

/* Legacy styles para compatibilidad */
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
