<template>
  <div class="dashboard-layout">
    <!-- Sidebar -->
    <DesktopSidebar :pendingCount="solicitudesPendientes" />

    <!-- Main Content Area -->
    <main class="dashboard-main">
      <!-- Top Header Bar -->
      <header class="top-bar">
        <div class="top-bar-left">
          <h1 class="page-title">Dashboard</h1>
          <span class="page-subtitle">Panel de Control</span>
        </div>
        <div class="top-bar-right">
          <div class="date-display">
            <Calendar :size="16" />
            <span>{{ currentDate }}</span>
          </div>
          <div class="user-quick-info">
            <div class="user-avatar-small">
              {{ getInitials(auth.user?.nombre || 'U') }}
            </div>
            <span class="user-name-small">{{ auth.user?.nombre?.split(' ')[0] || 'Usuario' }}</span>
          </div>
        </div>
      </header>

      <!-- Dashboard Content -->
      <div class="dashboard-content">
        <!-- Welcome Banner -->
        <section class="welcome-banner">
          <div class="welcome-text">
            <h2>¡Bienvenido de nuevo, <span class="highlight-name">{{ auth.user?.nombre?.split(' ')[0] || 'Usuario' }}</span>!</h2>
            <p class="welcome-subtitle">
              <span class="role-chip">{{ formatRole(auth.user?.rol || 'Usuario') }}</span>
              <span class="separator">•</span>
              <span class="status-online"><span class="online-dot"></span>En línea</span>
            </p>
          </div>
          <div class="welcome-illustration">
            <div class="floating-shapes">
              <div class="shape shape-1"></div>
              <div class="shape shape-2"></div>
              <div class="shape shape-3"></div>
            </div>
          </div>
        </section>

        <!-- Stats Cards Row -->
        <section class="stats-row">
          <div class="stat-card" :class="{ 'has-alert': cambiosAdscripcion.length > 0 }">
            <div class="stat-icon-wrapper solicitudes-icon">
              <GitBranch :size="22" />
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ cambiosAdscripcion.length }}</span>
              <span class="stat-label">Solicitudes Pendientes</span>
            </div>
            <router-link to="/cambios-adscripcion" class="stat-action">
              <ArrowRight :size="16" />
            </router-link>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrapper sembradores-icon">
              <Sprout :size="22" />
            </div>
            <div class="stat-info">
              <span class="stat-value">--</span>
              <span class="stat-label">Sembradores</span>
            </div>
            <router-link to="/sembradores" class="stat-action">
              <ArrowRight :size="16" />
            </router-link>
          </div>

          <div class="stat-card">
            <div class="stat-icon-wrapper mapa-icon">
              <MapPin :size="22" />
            </div>
            <div class="stat-info">
              <span class="stat-value">Ver</span>
              <span class="stat-label">Mapa Interactivo</span>
            </div>
            <router-link to="/mapa" class="stat-action">
              <ArrowRight :size="16" />
            </router-link>
          </div>

          <div v-if="['admin', 'territorial', 'facilitador'].includes(auth.user?.rol)" class="stat-card">
            <div class="stat-icon-wrapper stats-icon">
              <BarChart3 :size="22" />
            </div>
            <div class="stat-info">
              <span class="stat-value">Ver</span>
              <span class="stat-label">Estadísticas</span>
            </div>
            <router-link to="/estadisticas" class="stat-action">
              <ArrowRight :size="16" />
            </router-link>
          </div>
        </section>

        <!-- Two Column Layout -->
        <div class="two-column-layout">
          <!-- Left Column - Solicitudes -->
          <section class="column-left">
            <div class="section-card solicitudes-card">
              <div class="section-header">
                <div class="section-title-group">
                  <GitBranch :size="18" class="section-icon" />
                  <h3>Solicitudes Recientes</h3>
                </div>
                <router-link to="/cambios-adscripcion" class="see-all-link">
                  Ver todas <ChevronRight :size="14" />
                </router-link>
              </div>

              <div v-if="cambiosAdscripcion.length > 0" class="solicitudes-list">
                <div 
                  v-for="cambio in cambiosAdscripcion.slice(0, 5)"
                  :key="'cambio-' + cambio.id"
                  class="solicitud-item"
                  :class="{ 'autorizado': cambio.estatus === 'AUTORIZADO' }"
                >
                  <div class="solicitud-avatar" :class="getStatusClass(cambio.estatus)">
                    <MailOpen v-if="cambio.estatus === 'AUTORIZADO'" :size="16" />
                    <Clock v-else :size="16" />
                  </div>
                  <div class="solicitud-content">
                    <span class="solicitud-tipo">{{ formatTipoCambio(cambio.tipo_cambio) }}</span>
                    <span class="solicitud-persona">{{ cambio.persona?.nombre || 'Usuario' }}</span>
                  </div>
                  <div class="solicitud-meta">
                    <span class="solicitud-status" :class="cambio.estatus.toLowerCase()">
                      {{ formatEstatusCambio(cambio.estatus) }}
                    </span>
                    <span class="solicitud-time">{{ formatTimeAgo(cambio.fecha_creacion) }}</span>
                  </div>
                </div>
              </div>

              <div v-else class="empty-state">
                <div class="empty-icon">
                  <CheckCircle :size="32" />
                </div>
                <p>No hay solicitudes pendientes</p>
                <span class="empty-subtitle">¡Todo al día!</span>
              </div>
            </div>
          </section>

          <!-- Right Column - Quick Access & Tools -->
          <section class="column-right">
            <!-- Quick Access for Admin -->
            <div v-if="auth.user?.rol === 'admin'" class="section-card quick-access-card">
              <div class="section-header">
                <div class="section-title-group">
                  <Settings :size="18" class="section-icon" />
                  <h3>Administración</h3>
                </div>
              </div>
              <div class="quick-access-grid">
                <router-link to="/admin-panel" class="quick-card admin">
                  <div class="quick-icon"><Shield :size="20" /></div>
                  <span>Panel Global</span>
                </router-link>
                <router-link to="/usuarios" class="quick-card">
                  <div class="quick-icon"><Users :size="20" /></div>
                  <span>Usuarios</span>
                </router-link>
                <router-link to="/estadisticas" class="quick-card">
                  <div class="quick-icon"><BarChart3 :size="20" /></div>
                  <span>Estadísticas</span>
                </router-link>
                <router-link to="/importaciones" class="quick-card">
                  <div class="quick-icon"><Upload :size="20" /></div>
                  <span>Importar</span>
                </router-link>
              </div>
            </div>

            <!-- Quick Access for Territorial/Facilitador -->
            <div v-else-if="['territorial', 'facilitador'].includes(auth.user?.rol)" class="section-card quick-access-card">
              <div class="section-header">
                <div class="section-title-group">
                  <Briefcase :size="18" class="section-icon" />
                  <h3>Gestión</h3>
                </div>
              </div>
              <div class="quick-access-grid">
                <router-link to="/usuarios" class="quick-card">
                  <div class="quick-icon"><Users :size="20" /></div>
                  <span>{{ auth.user?.rol === 'territorial' ? 'Facilitadores' : 'Técnicos' }}</span>
                </router-link>
                <router-link to="/estadisticas" class="quick-card">
                  <div class="quick-icon"><BarChart3 :size="20" /></div>
                  <span>Estadísticas</span>
                </router-link>
              </div>
            </div>

            <!-- Quick Access for Técnicos -->
            <div v-else-if="auth.user?.rol?.includes('tecnico')" class="section-card quick-access-card">
              <div class="section-header">
                <div class="section-title-group">
                  <Clipboard :size="18" class="section-icon" />
                  <h3>Mis Herramientas</h3>
                </div>
              </div>
              <div class="quick-access-grid">
                <router-link to="/seguimiento" class="quick-card primary">
                  <div class="quick-icon"><Clipboard :size="20" /></div>
                  <span>Seguimiento</span>
                </router-link>
                <router-link to="/sembradores" class="quick-card">
                  <div class="quick-icon"><Sprout :size="20" /></div>
                  <span>Sembradores</span>
                </router-link>
              </div>
            </div>

            <!-- Modules Section -->
            <div v-if="['admin', 'territorial', 'facilitador'].includes(auth.user?.rol)" class="section-card modules-card">
              <div class="section-header">
                <div class="section-title-group">
                  <Building2 :size="18" class="section-icon" />
                  <h3>Módulos</h3>
                </div>
                <span class="module-badge">Personal Operativo</span>
              </div>
              <div class="modules-list">
                <router-link to="/estructura-territorial" class="module-item">
                  <div class="module-icon"><Globe :size="18" /></div>
                  <div class="module-info">
                    <span class="module-name">Estructura Territorial</span>
                    <span class="module-desc">Organigrama jerárquico</span>
                  </div>
                  <ChevronRight :size="16" class="module-arrow" />
                </router-link>
                <router-link to="/directorio" class="module-item">
                  <div class="module-icon"><Users :size="18" /></div>
                  <div class="module-info">
                    <span class="module-name">Directorio</span>
                    <span class="module-desc">Lista de personal</span>
                  </div>
                  <ChevronRight :size="16" class="module-arrow" />
                </router-link>
                <router-link to="/cambios-adscripcion" class="module-item highlight">
                  <div class="module-icon">
                    <GitBranch :size="18" />
                    <span v-if="cambiosAdscripcion.length > 0" class="module-count">{{ cambiosAdscripcion.length }}</span>
                  </div>
                  <div class="module-info">
                    <span class="module-name">Solicitudes</span>
                    <span class="module-desc">Cambios de adscripción</span>
                  </div>
                  <ChevronRight :size="16" class="module-arrow" />
                </router-link>
              </div>
            </div>

            <!-- Common Tools -->
            <div class="section-card tools-card">
              <div class="section-header">
                <div class="section-title-group">
                  <Zap :size="18" class="section-icon" />
                  <h3>Acceso Rápido</h3>
                </div>
              </div>
              <div class="tools-grid">
                <router-link to="/cambios-adscripcion" class="tool-item">
                  <GitBranch :size="20" />
                  <span>Solicitudes</span>
                  <span v-if="cambiosAdscripcion.length > 0" class="tool-badge">{{ cambiosAdscripcion.length }}</span>
                </router-link>
                <router-link to="/sembradores" class="tool-item">
                  <Sprout :size="20" />
                  <span>Sembradores</span>
                </router-link>
                <router-link to="/mapa" class="tool-item">
                  <Layers :size="20" />
                  <span>Capas</span>
                </router-link>
              </div>
            </div>
          </section>
        </div>
      </div>

      <!-- Footer -->
      <footer class="dashboard-footer">
        <p>© 2025 <strong>SistemaApp</strong> — Todos los derechos reservados</p>
      </footer>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import { useRouter } from 'vue-router'
import { 
  BarChart3, Users, Settings, MapPin, Sprout, Clipboard, 
  ChevronRight, Upload, GitBranch, Layers, Building2, Globe, 
  MailOpen, Clock, CheckCircle, ArrowRight, Calendar, Shield,
  Zap, Briefcase
} from 'lucide-vue-next'
import DesktopSidebar from '../components/DesktopSidebar.vue'
import axios from 'axios'

const auth = useAuthStore()
const router = useRouter()
const ws = ref<WebSocket | null>(null)
const solicitudesPendientes = ref(0)
const cambiosAdscripcion = ref<any[]>([])

let solicitudesInterval: ReturnType<typeof setInterval> | null = null

// Current date formatted
const currentDate = computed(() => {
  return new Date().toLocaleDateString('es-MX', { 
    weekday: 'long', 
    day: 'numeric', 
    month: 'long' 
  })
})

onMounted(() => {
  auth.fetchProfile()
  connectWebSocket()
  getSolicitudesPendientes()
  getCambiosAdscripcion()
  solicitudesInterval = setInterval(() => {
    getSolicitudesPendientes()
    getCambiosAdscripcion()
  }, 15000)
})

onUnmounted(() => {
  if (ws.value) ws.value.close()
  if (solicitudesInterval) clearInterval(solicitudesInterval)
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
    ws.value = new WebSocket(wsUrl)
    ws.value.onopen = () => {
      setInterval(() => {
        if (ws.value?.readyState === WebSocket.OPEN) ws.value?.send('ping')
      }, 30000)
    }
  } catch (error) {
    console.error('Error conectando WebSocket:', error)
  }
}

const getSolicitudesPendientes = async () => {
  try {
    const token = localStorage.getItem('token') || auth.token
    const apiUrl = getSecureApiUrl()
    const response = await axios.get(`${apiUrl}/solicitudes`, { 
      headers: { Authorization: `Bearer ${token}` } 
    })
    const solicitudes = response.data || []
    const userId = auth.user?.id
    solicitudesPendientes.value = solicitudes.filter((s: any) => 
      s.estado === 'pendiente' && s.destino_id === userId && s.usuario_id !== userId
    ).length
  } catch (error) {
    console.error('Error cargando solicitudes:', error)
  }
}

const getCambiosAdscripcion = async () => {
  try {
    const token = localStorage.getItem('token') || auth.token
    const apiUrl = getSecureApiUrl()
    const response = await axios.get(`${apiUrl}/workflows/cambios-adscripcion`, { 
      headers: { Authorization: `Bearer ${token}` } 
    })
    const cambios = response.data?.items || []
    const userId = auth.user?.id
    cambiosAdscripcion.value = cambios.filter((c: any) => 
      (c.estatus === 'EN_REVISION' && c.destino_id === userId) ||
      (c.estatus === 'AUTORIZADO' && c.propuesto_por_id === userId)
    ).sort((a: any, b: any) => new Date(b.fecha_creacion).getTime() - new Date(a.fecha_creacion).getTime())
  } catch (error) {
    console.error('Error cargando cambios adscripción:', error)
  }
}

const formatTipoCambio = (tipo: string): string => {
  const tipos: Record<string, string> = { ALTA: 'Alta', BAJA: 'Baja', REASIGNACION: 'Reasignación' }
  return tipos[tipo] || tipo
}

const formatEstatusCambio = (estatus: string): string => {
  const estatuses: Record<string, string> = {
    EN_REVISION: 'En Revisión', AUTORIZADO: 'Autorizado', APLICADO: 'Aplicado',
    RECHAZADO: 'Rechazado', CANCELADO: 'Cancelado'
  }
  return estatuses[estatus] || estatus
}

const getStatusClass = (estatus: string): string => {
  const classes: Record<string, string> = {
    EN_REVISION: 'status-pending', AUTORIZADO: 'status-success',
    RECHAZADO: 'status-error', CANCELADO: 'status-cancelled'
  }
  return classes[estatus] || 'status-pending'
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
  if (diffMins < 60) return `${diffMins}m`
  if (diffHours < 24) return `${diffHours}h`
  if (diffDays < 7) return `${diffDays}d`
  return date.toLocaleDateString('es-MX', { day: 'numeric', month: 'short' })
}

const getInitials = (nombre: string | undefined): string => {
  if (!nombre) return '?'
  const parts = nombre.trim().split(' ')
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase()
  return nombre.substring(0, 2).toUpperCase()
}

const formatRole = (role: string): string => {
  const roleMap: Record<string, string> = {
    admin: 'Administrador', territorial: 'Territorial', coordinador: 'Coordinador',
    facilitador: 'Facilitador', tecnico_productivo: 'Técnico Productivo',
    tecnico_social: 'Técnico Social', sembrador: 'Sembrador', usuario: 'Usuario'
  }
  return roleMap[role?.toLowerCase()] || role
}
</script>

<style scoped>
/* ========== BASE LAYOUT ========== */
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background: #f8fafc;
}

.dashboard-main {
  flex: 1;
  margin-left: clamp(180px, 18vw, 220px);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-x: hidden;
}

/* ========== TOP BAR ========== */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 50;
}

.top-bar-left {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.page-subtitle {
  font-size: 0.875rem;
  color: #64748b;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.date-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.875rem;
  text-transform: capitalize;
}

.user-quick-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-avatar-small {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
}

.user-name-small {
  font-size: 0.875rem;
  font-weight: 500;
  color: #1e293b;
}

/* ========== DASHBOARD CONTENT ========== */
.dashboard-content {
  flex: 1;
  padding: 1.5rem;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ========== WELCOME BANNER ========== */
.welcome-banner {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 50%, #15803d 100%);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(34, 197, 94, 0.25);
}

.welcome-text {
  position: relative;
  z-index: 2;
}

.welcome-text h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.75rem 0;
}

.highlight-name {
  color: #bbf7d0;
}

.welcome-subtitle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
}

.role-chip {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 500;
}

.separator {
  opacity: 0.5;
}

.status-online {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.online-dot {
  width: 8px;
  height: 8px;
  background: #bbf7d0;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.1); }
}

.welcome-illustration {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 40%;
  overflow: hidden;
}

.floating-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.shape-1 {
  width: 120px;
  height: 120px;
  top: -20px;
  right: 40px;
  animation: float 6s ease-in-out infinite;
}

.shape-2 {
  width: 80px;
  height: 80px;
  bottom: -10px;
  right: 120px;
  animation: float 8s ease-in-out infinite reverse;
}

.shape-3 {
  width: 60px;
  height: 60px;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  animation: float 5s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

/* ========== STATS ROW ========== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  position: relative;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.stat-card.has-alert {
  border-color: #fbbf24;
  background: linear-gradient(135deg, #fffbeb 0%, white 100%);
}

.stat-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.solicitudes-icon {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #b45309;
}

.sembradores-icon {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  color: #16a34a;
}

.mapa-icon {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #2563eb;
}

.stats-icon {
  background: linear-gradient(135deg, #f3e8ff, #e9d5ff);
  color: #9333ea;
}

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.stat-label {
  display: block;
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 0.1rem;
}

.stat-action {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.2s ease;
  text-decoration: none;
}

.stat-action:hover {
  background: #22c55e;
  color: white;
}

/* ========== TWO COLUMN LAYOUT ========== */
.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.column-left, .column-right {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ========== SECTION CARDS ========== */
.section-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f1f5f9;
}

.section-title-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-icon {
  color: #22c55e;
}

.section-title-group h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.see-all-link {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: #22c55e;
  text-decoration: none;
  font-weight: 500;
  transition: gap 0.2s ease;
}

.see-all-link:hover {
  gap: 0.5rem;
}

/* ========== SOLICITUDES LIST ========== */
.solicitudes-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.solicitud-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 10px;
  background: #f8fafc;
  transition: all 0.2s ease;
}

.solicitud-item:hover {
  background: #f1f5f9;
}

.solicitud-item.autorizado {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.solicitud-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.status-pending {
  background: #fef3c7;
  color: #b45309;
}

.status-success {
  background: #dcfce7;
  color: #16a34a;
}

.status-error {
  background: #fee2e2;
  color: #dc2626;
}

.status-cancelled {
  background: #f1f5f9;
  color: #64748b;
}

.solicitud-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.solicitud-tipo {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
}

.solicitud-persona {
  font-size: 0.75rem;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.solicitud-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.solicitud-status {
  font-size: 0.65rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.solicitud-status.en_revision {
  background: #fef3c7;
  color: #b45309;
}

.solicitud-status.autorizado {
  background: #dcfce7;
  color: #16a34a;
}

.solicitud-status.rechazado {
  background: #fee2e2;
  color: #dc2626;
}

.solicitud-time {
  font-size: 0.7rem;
  color: #94a3b8;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
}

.empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #dcfce7;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #22c55e;
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 0.9rem;
  color: #1e293b;
  font-weight: 500;
  margin: 0;
}

.empty-subtitle {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 0.25rem;
}

/* ========== QUICK ACCESS GRID ========== */
.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.quick-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 10px;
  background: #f8fafc;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.quick-card:hover {
  background: #f1f5f9;
  transform: translateY(-2px);
  border-color: #e2e8f0;
}

.quick-card.admin {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.quick-card.admin:hover {
  background: linear-gradient(135deg, #fde68a 0%, #fcd34d 100%);
}

.quick-card.primary {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
}

.quick-card.primary:hover {
  background: linear-gradient(135deg, #bbf7d0 0%, #86efac 100%);
}

.quick-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #22c55e;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.quick-card.admin .quick-icon {
  color: #b45309;
}

.quick-card span {
  font-size: 0.8rem;
  font-weight: 500;
  color: #1e293b;
}

/* ========== MODULES ========== */
.module-badge {
  font-size: 0.7rem;
  font-weight: 600;
  color: #22c55e;
  background: #dcfce7;
  padding: 0.2rem 0.6rem;
  border-radius: 10px;
}

.modules-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.module-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 10px;
  background: #f8fafc;
  text-decoration: none;
  transition: all 0.2s ease;
}

.module-item:hover {
  background: #f1f5f9;
  transform: translateX(4px);
}

.module-item.highlight {
  background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%);
}

.module-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #22c55e;
  flex-shrink: 0;
  position: relative;
}

.module-count {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 16px;
  height: 16px;
  background: #ef4444;
  color: white;
  font-size: 0.6rem;
  font-weight: 700;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.module-info {
  flex: 1;
  min-width: 0;
}

.module-name {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
}

.module-desc {
  display: block;
  font-size: 0.75rem;
  color: #64748b;
}

.module-arrow {
  color: #94a3b8;
  flex-shrink: 0;
}

/* ========== TOOLS GRID ========== */
.tools-grid {
  display: flex;
  gap: 0.5rem;
}

.tool-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.75rem 0.5rem;
  border-radius: 10px;
  background: #f8fafc;
  text-decoration: none;
  transition: all 0.2s ease;
  position: relative;
  color: #64748b;
}

.tool-item:hover {
  background: #22c55e;
  color: white;
}

.tool-item span {
  font-size: 0.7rem;
  font-weight: 500;
}

.tool-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 16px;
  height: 16px;
  background: #ef4444;
  color: white;
  font-size: 0.6rem;
  font-weight: 700;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

/* ========== FOOTER ========== */
.dashboard-footer {
  padding: 1rem;
  text-align: center;
  border-top: 1px solid #e2e8f0;
  background: white;
}

.dashboard-footer p {
  margin: 0;
  font-size: 0.75rem;
  color: #94a3b8;
}

.dashboard-footer strong {
  color: #22c55e;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .dashboard-main {
    margin-left: 0;
    padding-top: 56px;
  }

  .top-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
  }

  .top-bar-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 0;
  }

  .page-title {
    font-size: 1.25rem;
  }

  .page-subtitle {
    font-size: 0.75rem;
  }

  .date-display {
    display: none;
  }

  .dashboard-content {
    padding: 1rem;
  }

  .welcome-banner {
    padding: 1.5rem;
  }

  .welcome-text h2 {
    font-size: 1.25rem;
  }

  .welcome-illustration {
    display: none;
  }

  .stats-row {
    grid-template-columns: 1fr 1fr;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-icon-wrapper {
    width: 40px;
    height: 40px;
  }

  .stat-value {
    font-size: 1.25rem;
  }

  .quick-access-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .top-bar {
    padding: 0.75rem 1rem;
  }

  .user-name-small {
    display: none;
  }

  .stats-row {
    grid-template-columns: 1fr;
  }

  .welcome-banner {
    padding: 1.25rem;
  }

  .welcome-text h2 {
    font-size: 1.1rem;
  }

  .welcome-subtitle {
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .tools-grid {
    flex-wrap: wrap;
  }

  .tool-item {
    flex: 1 1 calc(33.33% - 0.5rem);
    min-width: 0;
  }
}
</style>
