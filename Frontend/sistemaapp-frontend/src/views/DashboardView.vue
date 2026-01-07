<template>
  <div class="dashboard-container">
    <!-- Menú hamburguesa global (solo móvil) -->
    <HamburgerMenu :pendingCount="solicitudesPendientes" class="mobile-only-menu" />

    <!-- Sidebar para PC -->
    <DesktopSidebar :pendingCount="solicitudesPendientes" />

    <!-- ========== CONTENEDOR PRINCIPAL ========== -->
    <div class="main-wrapper">
      <!-- Header moderno con efecto vidrio líquido (móvil) -->
      <header class="dashboard-header mobile-header">
        <div class="header-content">
          <div class="logo-section">
            <div class="logo-icon">
              <!-- Icono SVG: Flor girando -->
              <svg viewBox="0 0 64 64" width="48" height="48" class="flower-logo-svg" xmlns="http://www.w3.org/2000/svg">
                <!-- Pétalos de la flor -->
                <g class="flower-petals">
                  <!-- Pétalo 1 (arriba) -->
                  <ellipse cx="32" cy="16" rx="8" ry="12" fill="#16a34a" opacity="0.9"/>
                  <!-- Pétalo 2 (arriba-derecha) -->
                  <ellipse cx="32" cy="16" rx="8" ry="12" fill="#22c55e" opacity="0.85" transform="rotate(60 32 32)"/>
                  <!-- Pétalo 3 (abajo-derecha) -->
                  <ellipse cx="32" cy="16" rx="8" ry="12" fill="#16a34a" opacity="0.9" transform="rotate(120 32 32)"/>
                  <!-- Pétalo 4 (abajo) -->
                  <ellipse cx="32" cy="16" rx="8" ry="12" fill="#22c55e" opacity="0.85" transform="rotate(180 32 32)"/>
                  <!-- Pétalo 5 (abajo-izquierda) -->
                  <ellipse cx="32" cy="16" rx="8" ry="12" fill="#16a34a" opacity="0.9" transform="rotate(240 32 32)"/>
                  <!-- Pétalo 6 (arriba-izquierda) -->
                  <ellipse cx="32" cy="16" rx="8" ry="12" fill="#22c55e" opacity="0.85" transform="rotate(300 32 32)"/>
                </g>
                <!-- Centro de la flor -->
                <circle cx="32" cy="32" r="8" fill="#15803d"/>
                <circle cx="32" cy="32" r="5" fill="#facc15"/>
                <circle cx="32" cy="32" r="2.5" fill="#eab308"/>
              </svg>
            </div>
            <div class="logo-text">
              <h1 class="app-title">Sistema de Administración</h1>
              <p class="app-subtitle">Panel de Control</p>
            </div>
          </div>
        </div>
      </header>

      <!-- Contenido principal -->
      <main class="dashboard-main">
        <div class="dashboard-content">
        
        <!-- Bienvenida y Perfil (Siempre visible) -->
        <section class="welcome-section">
          <div class="welcome-card">
            <div class="welcome-header">
              <div class="avatar-circle">
                {{ getInitials(auth.user?.nombre || 'U') }}
              </div>
              <div class="welcome-info">
                <h2 class="welcome-title">¡Bienvenido, {{ auth.user?.nombre?.split(' ')[0] || 'Usuario' }}!</h2>
                <div class="role-tag">{{ formatRole(auth.user?.rol || 'N/A') }}</div>
              </div>
            </div>
          </div>
        </section>

        <!-- Notificaciones Pendientes (Siempre visible si hay) -->
        <section v-if="solicitudesPendientesLista.length > 0" class="alerts-section">
          <div class="alerts-header">
            <div class="alerts-title-row">
              <Bell :size="20" class="alerts-icon" />
              <h3 class="alerts-title">Solicitudes Pendientes</h3>
            </div>
            <span class="alerts-count">{{ solicitudesPendientesLista.length }}</span>
          </div>
          
          <div class="alerts-list">
            <div 
              v-for="solicitud in solicitudesPendientesLista.slice(0, 3)"
              :key="'alert-' + solicitud.id"
              class="alert-card"
            >
              <div class="alert-icon">
                <FileText :size="20" />
              </div>
              <div class="alert-content">
                <p class="alert-type">{{ formatTipoSolicitud(solicitud.tipo) }}</p>
                <p class="alert-from">De: {{ solicitud.solicitante?.nombre || 'Usuario' }}</p>
                <p class="alert-time">{{ formatTimeAgo(solicitud.fecha) }}</p>
              </div>
              <router-link to="/solicitudes" class="alert-action">
                <ChevronRight :size="20" />
              </router-link>
            </div>
          </div>
        </section>

        <!-- Acceso Rápido: Solo Admin -->
        <section v-if="auth.user?.rol === 'admin'" class="quick-access-section">
          <h3 class="section-header">Panel de Administración</h3>
          <div class="access-grid-admin">
            <router-link to="/admin-panel" class="access-card admin-card">
              <div class="access-icon-wrapper admin-icon">
                <Settings :size="28" />
              </div>
              <div class="access-info">
                <h4 class="access-title">Panel Global</h4>
                <p class="access-desc">Control total del sistema</p>
              </div>
            </router-link>
            
            <router-link to="/usuarios" class="access-card">
              <div class="access-icon-wrapper">
                <Users :size="28" />
              </div>
              <div class="access-info">
                <h4 class="access-title">Usuarios</h4>
                <p class="access-desc">Gestionar todos los usuarios</p>
              </div>
            </router-link>
            
            <router-link to="/estadisticas" class="access-card">
              <div class="access-icon-wrapper">
                <BarChart3 :size="28" />
              </div>
              <div class="access-info">
                <h4 class="access-title">Estadísticas</h4>
                <p class="access-desc">Métricas y análisis</p>
              </div>
            </router-link>
          </div>
        </section>

        <!-- Acceso Rápido: Territorial -->
        <section v-if="auth.user?.rol === 'territorial'" class="quick-access-section">
          <h3 class="section-header">Gestión Territorial</h3>
          <div class="access-grid">
            <router-link to="/usuarios" class="access-card">
              <div class="access-icon-wrapper">
                <Users :size="28" />
              </div>
              <div class="access-info">
                <h4 class="access-title">Facilitadores</h4>
                <p class="access-desc">Gestionar facilitadores</p>
              </div>
            </router-link>
            
            <router-link to="/estadisticas" class="access-card">
              <div class="access-icon-wrapper">
                <BarChart3 :size="28" />
              </div>
              <div class="access-info">
                <h4 class="access-title">Estadísticas</h4>
                <p class="access-desc">Análisis de datos</p>
              </div>
            </router-link>
          </div>
        </section>

        <!-- Acceso Rápido: Facilitador -->
        <section v-if="auth.user?.rol === 'facilitador'" class="quick-access-section">
          <h3 class="section-header">Gestión de Facilitador</h3>
          <div class="access-grid">
            <router-link to="/usuarios" class="access-card">
              <div class="access-icon-wrapper">
                <Users :size="28" />
              </div>
              <div class="access-info">
                <h4 class="access-title">Técnicos</h4>
                <p class="access-desc">Gestionar técnicos</p>
              </div>
            </router-link>
            
            <router-link to="/estadisticas" class="access-card">
              <div class="access-icon-wrapper">
                <BarChart3 :size="28" />
              </div>
              <div class="access-info">
                <h4 class="access-title">Estadísticas</h4>
                <p class="access-desc">Ver métricas</p>
              </div>
            </router-link>
          </div>
        </section>

        <!-- Acceso Rápido: Técnicos -->
        <section v-if="auth.user?.rol?.includes('tecnico')" class="quick-access-section">
          <h3 class="section-header">Herramientas de Trabajo</h3>
          <div class="access-grid">
            <router-link to="/seguimiento" class="access-card primary-card">
              <div class="access-icon-wrapper primary-icon">
                <Clipboard :size="28" />
              </div>
              <div class="access-info">
                <h4 class="access-title">Seguimiento</h4>
                <p class="access-desc">Registrar visitas</p>
              </div>
            </router-link>
            
            <router-link to="/sembradores" class="access-card">
              <div class="access-icon-wrapper">
                <Sprout :size="28" />
              </div>
              <div class="access-info">
                <h4 class="access-title">Sembradores</h4>
                <p class="access-desc">Mis sembradores</p>
              </div>
            </router-link>
          </div>
        </section>

        <!-- Herramientas Comunes (Todos los roles) -->
        <section class="common-tools-section">
          <h3 class="section-header">Herramientas</h3>
          <div class="tools-grid">
            <router-link to="/solicitudes" class="tool-card">
              <div class="tool-icon-wrapper">
                <FileText :size="24" />
                <span v-if="solicitudesPendientes > 0" class="tool-badge">{{ solicitudesPendientes }}</span>
              </div>
              <span class="tool-label">Solicitudes</span>
            </router-link>
            
            <router-link to="/sembradores" class="tool-card">
              <div class="tool-icon-wrapper">
                <Sprout :size="24" />
              </div>
              <span class="tool-label">Sembradores</span>
            </router-link>
            
            <router-link to="/mapa" class="tool-card">
              <div class="tool-icon-wrapper">
                <MapPin :size="24" />
              </div>
              <span class="tool-label">Mapa</span>
            </router-link>
          </div>
        </section>

      </div>
    </main>

    <!-- Footer -->
    <footer class="dashboard-footer">
      <p>© 2025 <span class="footer-highlight">SistemaApp</span>. Todos los derechos reservados.</p>
    </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, onUnmounted } from 'vue'
// @ts-ignore
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl, getSecureWsUrl } from '../utils/api'
import { useRouter } from 'vue-router'
import { LogOut, User, Mail, LayoutDashboard, BarChart3, Users, Settings, MapPin, Sprout, FileText, Smile, Clipboard, Check, Shield, Zap, Bell, Clock, CheckCircle, AlertCircle, Info, Eye, MessageSquare, Home, ChevronRight, Upload } from 'lucide-vue-next'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import DesktopSidebar from '../components/DesktopSidebar.vue'
import DesktopHeader from '../components/DesktopHeader.vue'
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
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #f0fdf4 100%);
  color: #1e3a2f;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  padding-top: 54px;
  box-sizing: border-box;
  position: relative;
  height: 100vh;
  will-change: scroll-position;
}

/* ========== LAYOUT PC ========== */
@media (min-width: 1024px) {
  .dashboard-container {
    flex-direction: row;
    padding-top: 0;
    background: #f8fafc;
  }

  .mobile-only-menu {
    display: none !important;
  }

  .mobile-header {
    display: none !important;
  }
}

/* ========== MAIN WRAPPER ========== */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

@media (min-width: 1024px) {
  .main-wrapper {
    margin-left: 220px;
    width: calc(100% - 220px);
  }
}

/* ========== HEADER (móvil) ========== */
.dashboard-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  backdrop-filter: blur(16px) saturate(180%);
  background: linear-gradient(
    135deg,
    rgba(134, 239, 172, 0.35) 0%,
    rgba(187, 247, 208, 0.4) 25%,
    rgba(255, 255, 255, 0.5) 50%,
    rgba(187, 247, 208, 0.4) 75%,
    rgba(134, 239, 172, 0.35) 100%
  );
  border-bottom: 1px solid rgba(22, 163, 74, 0.25);
  padding: 0;
  box-shadow: 
    0 4px 24px rgba(22, 163, 74, 0.15),
    0 1px 3px rgba(22, 163, 74, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(22, 163, 74, 0.1);
  width: 100%;
  height: 54px;
  box-sizing: border-box;
  /* Efecto de brillo líquido que se mueve */
  overflow: hidden;
}

@media (min-width: 1024px) {
  .dashboard-header.mobile-header {
    display: none;
  }
}

.dashboard-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 200%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.4) 25%,
    rgba(134, 239, 172, 0.3) 50%,
    rgba(255, 255, 255, 0.4) 75%,
    transparent 100%
  );
  animation: liquidShine 4s ease-in-out infinite;
  pointer-events: none;
}

@keyframes liquidShine {
  0% { transform: translateX(0); }
  100% { transform: translateX(50%); }
}

.header-content {
  max-width: 100%;
  margin: 0;
  padding: 0 0.85rem;
  padding-right: 60px; /* Espacio para el menú hamburguesa */
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  height: 54px;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

.logo-section {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 0.6rem;
  min-width: 0;
  padding-left: 0.5rem;
}

.logo-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  padding: 0;
  margin: 0;
}

/* Flor girando */
.flower-logo-svg {
  width: 36px;
  height: 36px;
  filter: drop-shadow(0 2px 6px rgba(22, 163, 74, 0.4));
}

.flower-logo-svg .flower-petals {
  transform-origin: 32px 32px;
  animation: flowerSpin 8s linear infinite;
}

@keyframes flowerSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.custom-logo-svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  width: 36px;
  height: 36px;
}

.logo-text h1 {
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: -0.5px;
  margin: 0;
  font-family: 'Segoe UI', 'Trebuchet MS', sans-serif;
  /* Efecto de brillo verde suave pasando letra por letra */
  background: linear-gradient(
    90deg,
    #15803d 0%,
    #15803d 40%,
    #86efac 50%,
    #15803d 60%,
    #15803d 100%
  );
  background-size: 200% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: textShine 3s linear infinite;
}

@keyframes textShine {
  0% {
    background-position: 100% center;
  }
  100% {
    background-position: -100% center;
  }
}

.logo-text p {
  font-size: 0.55rem;
  color: #16a34a;
  margin: 0.02rem 0 0 0;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-family: 'Segoe UI', sans-serif;
  animation: subtitle-fade-in 1s ease-out 0.2s forwards;
  opacity: 1;
  text-shadow: none;
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
  gap: 0.3rem;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  padding: 0.3rem 0.5rem;
  border-radius: 6px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  font-size: 0.6rem;
  flex-shrink: 0;
  font-family: 'Segoe UI', sans-serif;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  margin-right: 0.4rem;
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

/* ========== RESPONSIVE - PANTALLAS GRANDES (solo aplica estilos que no afectan PC layout) ========== */
@media (min-width: 1200px) {
  /* El padding-top ya está en 0 para PC desde la media query de layout */
  .dashboard-header {
    height: 56px;
  }

  .header-content {
    height: 56px;
    padding-right: 65px;
  }

  .logo-icon {
    width: 42px;
    height: 42px;
  }

  .flower-logo-svg {
    width: 38px;
    height: 38px;
  }

  .logo-text h1 {
    font-size: 1.1rem;
  }

  .logo-text p {
    font-size: 0.6rem;
  }

  .logo-section {
    gap: 0.55rem;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding-top: 56px;
  }

  .dashboard-header {
    height: 56px;
  }

  .header-content {
    height: 56px;
    padding: 0 0.75rem;
    padding-right: 55px;
  }

  .logout-text {
    display: none;
  }

  .logout-btn {
    padding: 0.5rem;
  }

  .logo-icon {
    width: 42px;
    height: 42px;
  }

  .flower-logo-svg {
    width: 38px;
    height: 38px;
  }

  .logo-text h1 {
    font-size: 1.1rem;
  }

  .logo-text p {
    font-size: 0.6rem;
  }

  .logo-section {
    gap: 0.5rem;
    padding-left: 0.25rem;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding-top: 50px;
  }

  .dashboard-header {
    height: 50px;
  }

  .header-content {
    height: 50px;
    padding: 0 0.5rem;
    padding-right: 48px;
  }

  .logo-icon {
    width: 36px;
    height: 36px;
  }

  .flower-logo-svg {
    width: 32px;
    height: 32px;
  }

  .logo-text h1 {
    font-size: 0.95rem;
  }

  .logo-text p {
    font-size: 0.55rem;
  }

  .logo-section {
    gap: 0.4rem;
    padding-left: 0.15rem;
  }
}

@media (max-width: 360px) {
  .dashboard-container {
    padding-top: 46px;
  }

  .dashboard-header {
    height: 46px;
  }

  .header-content {
    height: 46px;
    padding: 0 0.35rem;
    padding-right: 42px;
  }

  .logo-icon {
    width: 32px;
    height: 32px;
  }

  .flower-logo-svg {
    width: 28px;
    height: 28px;
  }

  .logo-text h1 {
    font-size: 0.85rem;
    letter-spacing: -0.3px;
  }

  .logo-text p {
    font-size: 0.5rem;
    letter-spacing: 0.02em;
  }

  .logo-section {
    gap: 0.3rem;
    padding-left: 0.1rem;
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

@media (min-width: 1024px) {
  .dashboard-main {
    min-height: calc(100vh - 52px);
    padding: 1rem 1.5rem;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  }
}

.dashboard-content {
  width: 100%;
  max-width: 900px;
  padding: 1rem 0.9rem 2rem 0.9rem;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

@media (min-width: 1024px) {
  .dashboard-content {
    max-width: 100%;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
}

/* ========== PROFILE LABEL ========== */
.profile-label {
  display: inline-block;
  background: linear-gradient(90deg, #16a34a 0%, #15803d 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 5px 5px 0 0;
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-align: center;
  margin-bottom: 0;
  margin-left: 0.4rem;
  text-transform: none;
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.25);
}

@media (min-width: 1024px) {
  .profile-label {
    font-size: 0.75rem;
    padding: 0.35rem 1rem;
    border-radius: 8px 8px 0 0;
    margin-left: 0;
  }
}

/* ========== PROFILE CARD ========== */
.profile-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1.5px solid rgba(22, 163, 74, 0.25);
  border-radius: 16px;
  padding: 0.75rem 0.65rem;
  backdrop-filter: blur(10px);
  text-align: left;
  margin-bottom: 0.75rem;
  box-shadow: 0 8px 32px rgba(22, 163, 74, 0.1);
  transition: all 0.3s ease;
  margin-top: -2px;
}

@media (min-width: 1024px) {
  .profile-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    margin-bottom: 0;
    margin-top: 0;
  }
}

.profile-card:hover {
  border-color: rgba(22, 163, 74, 0.4);
  box-shadow: 0 12px 48px rgba(22, 163, 74, 0.15);
}

@media (min-width: 1024px) {
  .profile-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 8px 30px rgba(59, 130, 246, 0.12);
  }
}

/* ===== NEW PROFILE HEADER LAYOUT ===== */
.profile-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.9rem;
}

.avatar-initials {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid #16a34a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  font-weight: 700;
  color: #16a34a;
  text-shadow: none;
  background: rgba(22, 163, 74, 0.1);
  box-shadow: 
    inset 0 0 10px rgba(22, 163, 74, 0.1),
    0 0 15px rgba(22, 163, 74, 0.2);
}

.user-info-section {
  flex: 1;
}

.user-full-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #15803d;
  margin-bottom: 0.2rem;
}

.role-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border: 1.5px solid #16a34a;
  border-radius: 5px;
  font-size: 0.7rem;
  font-weight: 600;
  color: #16a34a;
  margin-bottom: 0.2rem;
}

.user-email {
  font-size: 0.7rem;
  color: #166534;
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

/* ========== ACTIONS SECTION ========== */
.actions-section {
  margin-bottom: 0.75rem;
}

@media (min-width: 1024px) {
  .actions-section {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  }
}

.section-title {
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 0.6rem;
  color: #15803d;
  text-align: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.4rem 0;
}

@media (min-width: 1024px) {
  .section-title {
    font-size: 1rem;
    color: #1e3a5f;
    text-align: left;
    justify-content: flex-start;
    margin-bottom: 1rem;
  }

  .section-title::before,
  .section-title::after {
    display: none;
  }
}

.section-title::before,
.section-title::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(22, 163, 74, 0.4), transparent);
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
  grid-template-columns: repeat(auto-fit, minmax(75px, 1fr));
  gap: 0.45rem;
  margin-bottom: 0.75rem;
}

@media (min-width: 1024px) {
  .actions-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 1rem;
    margin-bottom: 0;
  }
}

@media (max-width: 768px) {
  .actions-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.4rem;
  }
}

@media (max-width: 480px) {
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.35rem;
  }
}

.action-card {
  position: relative;
  background: rgba(255, 255, 255, 0.9);
  border: 1.5px solid rgba(22, 163, 74, 0.25);
  border-radius: 14px;
  padding: 0.7rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  text-decoration: none;
  color: inherit;
  overflow: visible;
}

@media (min-width: 1024px) {
  .action-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1.25rem;
    gap: 0.6rem;
  }

  .action-card:hover {
    transform: translateY(-4px);
    border-color: #3b82f6;
    background: white;
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
  }
}

/* Badge de solicitudes pendientes */
.solicitudes-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 15px;
  height: 15px;
  padding: 0 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.55rem;
  font-weight: 700;
  color: white;
  background: radial-gradient(ellipse at 30% 30%, rgba(252, 165, 165, 0.6), rgba(248, 113, 113, 0.45) 50%, rgba(239, 68, 68, 0.35));
  border: 1px solid rgba(248, 113, 113, 0.5);
  border-radius: 50%;
  backdrop-filter: blur(10px);
  z-index: 10;
}

.action-card:hover {
  transform: translateY(-6px);
  border-color: #16a34a;
  background: rgba(22, 163, 74, 0.08);
  box-shadow: 0 10px 28px rgba(22, 163, 74, 0.2), inset 0 0 15px rgba(22, 163, 74, 0.05);
}

.action-card:active {
  transform: translateY(-3px);
}

.action-icon-wrapper {
  width: 36px;
  height: 36px;
  background: transparent;
  border: 2px solid #16a34a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 12px rgba(22, 163, 74, 0.3);
  transition: all 0.3s ease;
}

.action-card:hover .action-icon-wrapper {
  transform: scale(1.12) rotate(5deg);
  box-shadow: 0 0 20px rgba(22, 163, 74, 0.4);
  background: rgba(22, 163, 74, 0.1);
}

.action-icon {
  width: 18px;
  height: 18px;
  color: #16a34a;
  text-shadow: none;
}

.action-title {
  font-size: 0.6rem;
  font-weight: 600;
  color: #166534;
  text-align: center;
  transition: color 0.3s ease;
  letter-spacing: 0.5px;
}

.action-card:hover .action-title {
  color: #15803d;
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
  color: #1e3a2f;
  transition: color 0.3s ease;
}

.specialized-card:hover .specialized-title {
  color: #16a34a;
}

.specialized-desc {
  position: relative;
  z-index: 1;
  font-size: 0.75rem;
  color: #64748b;
  margin: 0;
  transition: color 0.3s ease;
}

.specialized-card:hover .specialized-desc {
  color: #374151;
}

.card-arrow {
  position: absolute;
  bottom: 1rem;
  right: 1.5rem;
  font-size: 1.25rem;
  color: #16a34a;
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
  background: rgba(240, 253, 244, 0.8);
  border: 1px solid rgba(22, 163, 74, 0.2);
  border-radius: 12px;
  padding: 0.8rem 0.6rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(22, 163, 74, 0.4);
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
  background: rgba(255, 255, 255, 0.9);
  border: 1.5px solid rgba(22, 163, 74, 0.2);
  border-radius: 12px;
  padding: 0.85rem;
  margin-bottom: 0.75rem;
  backdrop-filter: blur(12px);
  box-shadow: 
    0 8px 32px rgba(22, 163, 74, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
}

@media (min-width: 1024px) {
  .notifications-section {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    backdrop-filter: none;
    margin-bottom: 0;
  }
}

.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.7rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid rgba(132, 204, 22, 0.15);
}

.header-left-notif {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  line-height: 1;
}

.header-bell-icon {
  color: #f87171;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
}

.header-left-notif .section-title {
  margin: 0;
  line-height: 1;
  display: flex;
  align-items: center;
  font-size: 0.75rem;
}

/* Badge rojo suave estilo vidrio */
.notifications-badge-glass {
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6rem;
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
  gap: 0.6rem;
  padding: 0.65rem;
  padding-right: 45px; /* Espacio para el botón semicírculo */
  background: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
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
  gap: 0.15rem;
  padding-left: 0.6rem;
  border-left: 1px solid rgba(22, 163, 74, 0.2);
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
  gap: 0.1rem;
}

.notif-main-icon {
  color: #f87171;
  width: 18px;
  height: 18px;
}

.notif-icon-label {
  font-size: 0.45rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.notif-tipo-tag {
  font-size: 0.65rem;
  font-weight: 700;
  color: #f87171;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

/* Fecha arriba del contenido */
.notif-fecha-top {
  font-size: 0.55rem;
  color: #64748b;
  margin-bottom: 0.15rem;
  display: block;
}

.notif-user-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
  margin-bottom: 0.15rem;
}

.notif-user-name {
  font-size: 0.65rem;
  font-weight: 500;
  color: #15803d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notif-user-rol {
  font-size: 0.55rem;
  color: #166534;
  font-style: italic;
}

/* Botón Ver medio círculo pegado a la derecha */
.notif-btn-semicircle {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 35px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 5px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(37, 99, 235, 0.35) 100%);
  border: 1.5px solid rgba(96, 165, 250, 0.4);
  border-right: none;
  border-radius: 24px 0 0 24px;
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
  width: 42px;
  background: linear-gradient(135deg, rgba(96, 165, 250, 0.35) 0%, rgba(59, 130, 246, 0.45) 100%);
  border-color: rgba(147, 197, 253, 0.6);
  box-shadow: 
    -6px 0 25px rgba(59, 130, 246, 0.35),
    inset 2px 0 12px rgba(255, 255, 255, 0.15);
}

.semicircle-text {
  font-size: 0.6rem;
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
  border-radius: 0 6px 6px 6px;
  padding: 0.25rem 0.45rem;
  backdrop-filter: blur(6px);
  margin-top: 0.1rem;
}

/* Esquina picuda tipo mensaje */
.notif-mensaje-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: -5px;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 5px 6px 0;
  border-color: transparent rgba(100, 116, 139, 0.12) transparent transparent;
}

.notif-mensaje-text {
  font-size: 0.55rem;
  color: #94a3b8;
  margin: 0;
  line-height: 1.3;
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
  color: #64748b;
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
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  border: 1px solid rgba(22, 163, 74, 0.2);
  transition: all 0.3s ease;
  position: relative;
}

.solicitud-notif-card:hover {
  background: white;
  transform: translateX(4px);
  border-color: rgba(22, 163, 74, 0.4);
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
  color: #374151;
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
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  border-left: 3px solid;
  transition: all 0.3s ease;
}

.notification-card.notif-unread {
  background: rgba(240, 253, 244, 0.8);
}

.notification-card:hover {
  background: white;
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
  color: #1e3a2f;
  font-weight: 600;
  font-size: 0.85rem;
  margin: 0 0 0.2rem 0;
  word-break: break-word;
}

.notif-message {
  color: #374151;
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
  padding: 0.5rem;
  border-top: 1px solid rgba(22, 163, 74, 0.1);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  font-size: 0.55rem;
  color: #166534;
}

@media (min-width: 1024px) {
  .dashboard-footer {
    background: white;
    border-top: 1px solid #e2e8f0;
    padding: 1rem;
    font-size: 0.8rem;
    color: #64748b;
  }
}

.footer-highlight {
  color: #15803d;
  font-weight: 600;
}

@media (min-width: 1024px) {
  .footer-highlight {
    color: #3b82f6;
  }
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

/* ========== LANDSCAPE MOBILE ========== */
@media (max-height: 500px) and (orientation: landscape) {
  .dashboard-container {
    padding-top: 44px;
    height: 100vh;
  }

  .dashboard-header {
    height: 44px;
  }

  .header-content {
    height: 44px;
    padding: 0 0.4rem;
    padding-right: 44px;
  }

  .logo-icon {
    width: 32px;
    height: 32px;
  }

  .flower-logo-svg {
    width: 28px;
    height: 28px;
  }

  .custom-logo-svg {
    width: 28px;
    height: 28px;
  }

  .logo-text h1 {
    font-size: 0.85rem;
  }

  .logo-text p {
    font-size: 0.45rem;
  }

  .logo-section {
    gap: 0.3rem;
    padding-left: 0.1rem;
  }

  .dashboard-content {
    padding: 0.6rem 0.7rem 1rem 0.7rem;
  }

  .profile-label {
    font-size: 0.5rem;
    padding: 0.15rem 0.5rem;
  }

  .profile-card {
    padding: 0.5rem 0.4rem;
    margin-bottom: 0.5rem;
  }

  .profile-header {
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .avatar-initials {
    width: 36px;
    height: 36px;
    font-size: 0.85rem;
  }

  .user-full-name {
    font-size: 0.75rem;
  }

  .role-badge {
    font-size: 0.55rem;
    padding: 0.1rem 0.35rem;
  }

  .user-email {
    font-size: 0.55rem;
  }

  .section-title {
    font-size: 0.65rem;
    margin-bottom: 0.4rem;
  }

  .actions-grid {
    grid-template-columns: repeat(auto-fit, minmax(55px, 1fr));
    gap: 0.3rem;
  }

  .action-card {
    padding: 0.4rem;
    gap: 0.2rem;
    border-radius: 10px;
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
    font-size: 0.5rem;
  }

  .notifications-section {
    padding: 0.5rem;
    margin-bottom: 0.4rem;
  }

  .notifications-header {
    margin-bottom: 0.4rem;
    padding-bottom: 0.3rem;
  }

  .notif-card-pro {
    padding: 0.4rem;
    padding-right: 35px;
    gap: 0.4rem;
  }

  .notif-main-icon {
    width: 14px;
    height: 14px;
  }

  .notif-tipo-tag {
    font-size: 0.5rem;
  }

  .notif-fecha-top {
    font-size: 0.45rem;
  }

  .notif-user-name {
    font-size: 0.5rem;
  }

  .notif-user-rol {
    font-size: 0.45rem;
  }

  .notif-btn-semicircle {
    width: 28px;
    height: 36px;
  }

  .semicircle-text {
    font-size: 0.45rem;
  }

  .dashboard-footer {
    padding: 0.3rem;
    font-size: 0.45rem;
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

/* ========== NUEVO DISEÑO JERÁRQUICO ========== */

/* Welcome Section */
.welcome-section {
  margin-bottom: 1.5rem;
}

.welcome-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1.5px solid #e2e8f0;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(22, 163, 74, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.welcome-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(22, 163, 74, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.welcome-card:hover {
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.1), 0 4px 12px rgba(22, 163, 74, 0.12);
  transform: translateY(-2px);
}

.welcome-header {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  position: relative;
  z-index: 1;
}

.avatar-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  box-shadow: 0 6px 20px rgba(22, 163, 74, 0.3), inset 0 2px 4px rgba(255, 255, 255, 0.3);
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.welcome-card:hover .avatar-circle {
  transform: scale(1.05);
  box-shadow: 0 8px 28px rgba(22, 163, 74, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.3);
}

.welcome-info {
  flex: 1;
}

.welcome-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.5px;
}

.role-tag {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.15), rgba(22, 163, 74, 0.08));
  color: #16a34a;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1.5px solid rgba(22, 163, 74, 0.25);
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.welcome-card:hover .role-tag {
  border-color: rgba(22, 163, 74, 0.4);
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.2), rgba(22, 163, 74, 0.12));
}

@media (min-width: 1024px) {
  .welcome-card {
    padding: 2rem;
  }

  .avatar-circle {
    width: 80px;
    height: 80px;
    font-size: 2rem;
  }

  .welcome-title {
    font-size: 1.75rem;
  }

  .role-tag {
    font-size: 0.95rem;
    padding: 0.5rem 1rem;
  }
}

/* Alerts Section */
.alerts-section {
  margin-bottom: 1.5rem;
}

.alerts-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding: 0 0.25rem;
}

.alerts-title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.alerts-icon {
  color: #ef4444;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

.alerts-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.alerts-count {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 28px;
  padding: 0 0.5rem;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-radius: 14px;
  font-size: 0.8rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.alert-card {
  background: linear-gradient(135deg, #fff5f5 0%, #fffbfb 100%);
  border: 1.5px solid #fee2e2;
  border-left: 5px solid #ef4444;
  border-radius: 14px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.alert-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, transparent 0%, rgba(239, 68, 68, 0.05) 100%);
  pointer-events: none;
}

.alert-card:hover {
  border-color: #ef4444;
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.15), 0 2px 8px rgba(239, 68, 68, 0.1);
  transform: translateX(6px);
  background: linear-gradient(135deg, #fff5f5 0%, #fef2f2 100%);
}

.alert-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.08));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ef4444;
  flex-shrink: 0;
  transition: all 0.3s ease;
  box-shadow: inset 0 2px 4px rgba(239, 68, 68, 0.1);
}

.alert-card:hover .alert-icon {
  transform: scale(1.1) rotate(5deg);
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.12));
}

.alert-content {
  flex: 1;
  min-width: 0;
  position: relative;
  z-index: 1;
}

.alert-type {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.alert-from {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0 0 0.15rem 0;
}

.alert-time {
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0;
}

.alert-action {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: #f8fafc;
  border-radius: 8px;
  color: #64748b;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.alert-action:hover {
  background: #16a34a;
  color: white;
}

/* Quick Access Section */
.quick-access-section {
  margin-bottom: 1.5rem;
}

.section-header {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1rem 0.25rem;
}

.access-grid,
.access-grid-admin {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 640px) {
  .access-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .access-grid-admin {
    grid-template-columns: repeat(3, 1fr);
  }
}

.access-card {
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.access-card::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(22, 163, 74, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.access-card:hover {
  border-color: #16a34a;
  box-shadow: 0 10px 30px rgba(22, 163, 74, 0.18), 0 4px 10px rgba(22, 163, 74, 0.1);
  transform: translateY(-4px);
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
}

.access-card.admin-card {
  grid-column: span 1;
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.08), rgba(22, 163, 74, 0.03));
  border-color: rgba(22, 163, 74, 0.35);
}

.access-card.admin-card:hover {
  border-color: #16a34a;
  box-shadow: 0 10px 30px rgba(22, 163, 74, 0.25), 0 4px 10px rgba(22, 163, 74, 0.12);
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.1), rgba(22, 163, 74, 0.05));
}

.access-card.primary-card {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.03));
  border-color: rgba(59, 130, 246, 0.35);
}

.access-card.primary-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.25), 0 4px 10px rgba(59, 130, 246, 0.12);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
}

.access-icon-wrapper {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #16a34a;
  flex-shrink: 0;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.access-card:hover .access-icon-wrapper {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: white;
  transform: scale(1.15);
  box-shadow: 0 6px 16px rgba(22, 163, 74, 0.35), inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.access-icon-wrapper.admin-icon {
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.15), rgba(22, 163, 74, 0.08));
  color: #16a34a;
}

.access-icon-wrapper.primary-icon {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(59, 130, 246, 0.08));
  color: #3b82f6;
}

.access-card.primary-card:hover .access-icon-wrapper {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.35), inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.access-info {
  flex: 1;
  position: relative;
  z-index: 1;
}

.access-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.35rem 0;
  letter-spacing: -0.3px;
}

.access-desc {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

/* Common Tools Section */
.common-tools-section {
  margin-bottom: 1.5rem;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.tool-card {
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  padding: 1.5rem 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.tool-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: -20px;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(22, 163, 74, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.tool-card:hover {
  border-color: #16a34a;
  box-shadow: 0 8px 24px rgba(22, 163, 74, 0.16), 0 2px 6px rgba(22, 163, 74, 0.08);
  transform: translateY(-4px);
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
}

.tool-icon-wrapper {
  position: relative;
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #16a34a;
  transition: all 0.3s ease;
  z-index: 1;
  box-shadow: inset 0 2px 4px rgba(22, 163, 74, 0.1);
}

.tool-card:hover .tool-icon-wrapper {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: white;
  transform: scale(1.15) rotate(-5deg);
  box-shadow: 0 6px 16px rgba(22, 163, 74, 0.3), inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.tool-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  min-width: 24px;
  height: 24px;
  padding: 0 0.4rem;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
  border: 2px solid white;
  animation: pulse 2s infinite;
}

.tool-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1e293b;
  text-align: center;
  position: relative;
  z-index: 1;
  letter-spacing: -0.2px;
}

@media (min-width: 1024px) {
  .dashboard-content {
    gap: 2rem;
  }

  .welcome-section,
  .alerts-section,
  .quick-access-section,
  .common-tools-section {
    margin-bottom: 0;
  }

  .section-header {
    font-size: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .tools-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }

  .tool-card {
    padding: 1.75rem 1.5rem;
    border-radius: 16px;
  }

  .tool-icon-wrapper {
    width: 56px;
    height: 56px;
    font-size: 1.5rem;
  }

  .access-card {
    padding: 2rem;
    border-radius: 18px;
    gap: 1.5rem;
  }

  .access-icon-wrapper {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    font-size: 1.75rem;
  }

  .access-title {
    font-size: 1.15rem;
  }

  .access-desc {
    font-size: 0.9rem;
  }

  .welcome-card {
    padding: 2.5rem;
    border-radius: 20px;
  }

  .avatar-circle {
    width: 88px;
    height: 88px;
    font-size: 2.2rem;
  }

  .welcome-title {
    font-size: 1.875rem;
  }

  .role-tag {
    font-size: 0.95rem;
    padding: 0.6rem 1.2rem;
  }

  .alert-card {
    padding: 1.25rem 1.5rem;
    border-radius: 16px;
  }
}
</style>
