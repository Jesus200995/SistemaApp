<template>
  <div class="admin-container">
    <!-- Fondo decorativo con blobs animados -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header principal -->
    <header class="header-admin">
      <div class="header-wrapper">
        <div class="header-left">
          <router-link to="/dashboard" class="back-button" title="Volver al Dashboard">
            <ArrowLeft class="back-icon" />
          </router-link>
          <div class="header-icon-small">
            <Settings class="icon-stat" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Administración</h1>
            <p class="header-subtitle">Panel de control</p>
          </div>
        </div>
        <button @click="recargarAdmin" class="reload-button" title="Recargar">
          <svg class="reload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M3 21v-5h5"></path>
          </svg>
        </button>
      </div>
    </header>

    <!-- Contenido principal -->
    <main class="admin-main">
      <div class="admin-content">
        <!-- Indicadores principales (Cards) -->
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
          class="stats-section"
        >
          <h2 class="section-title">Estadísticas Generales</h2>
          
          <div class="stats-grid">
            <!-- Card: Total Usuarios -->
            <div class="stat-card" :style="{ borderLeftColor: '#10b981' }">
              <div class="stat-icon" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%)">
                <Users class="card-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Total Usuarios</p>
                <p class="stat-value">{{ overview.total_usuarios || 0 }}</p>
              </div>
            </div>

            <!-- Card: Total Sembradores -->
            <div class="stat-card" :style="{ borderLeftColor: '#f59e0b' }">
              <div class="stat-icon" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%)">
                <Sprout class="card-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Sembradores</p>
                <p class="stat-value">{{ overview.total_sembradores || 0 }}</p>
              </div>
            </div>

            <!-- Card: Total Seguimientos -->
            <div class="stat-card" :style="{ borderLeftColor: '#3b82f6' }">
              <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)">
                <BarChart3 class="card-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Seguimientos</p>
                <p class="stat-value">{{ overview.total_seguimientos || 0 }}</p>
              </div>
            </div>

            <!-- Card: Solicitudes Pendientes -->
            <div class="stat-card" :style="{ borderLeftColor: '#ef4444' }">
              <div class="stat-icon" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%)">
                <AlertCircle class="card-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Solicitudes Pendientes</p>
                <p class="stat-value">{{ overview.pendientes || 0 }}</p>
              </div>
            </div>

            <!-- Card: Promedio de Avance -->
            <div class="stat-card" :style="{ borderLeftColor: '#8b5cf6' }">
              <div class="stat-icon" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)">
                <TrendingUp class="card-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Promedio de Avance</p>
                <p class="stat-value">{{ overview.promedio_avance || 0 }}%</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Solicitudes Pendientes -->
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 100, duration: 600 } }"
          class="solicitudes-section"
        >
          <div class="section-header">
            <h2 class="section-title">
              <span class="count-badge">{{ solicitudesPendientes.length }}</span>
              Solicitudes Pendientes
            </h2>
            <p class="section-subtitle">Gestión de solicitudes en espera de respuesta</p>
          </div>

          <!-- Estado vacío -->
          <div v-if="solicitudesPendientes.length === 0" class="empty-state">
            <div class="empty-icon">
              <CheckCircle />
            </div>
            <h3 class="empty-title">Sin solicitudes pendientes</h3>
            <p class="empty-text">Todas las solicitudes han sido procesadas</p>
          </div>

          <!-- Tabla de solicitudes -->
          <div v-else class="table-wrapper">
            <div class="table-container">
              <table class="requests-table">
                <thead>
                  <tr class="table-header-row">
                    <th class="table-header-cell">Tipo</th>
                    <th class="table-header-cell">Descripción</th>
                    <th class="table-header-cell">Usuario</th>
                    <th class="table-header-cell">Fecha</th>
                    <th class="table-header-cell">Estado</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(solicitud, index) in solicitudesPendientes"
                    :key="solicitud.id"
                    class="table-body-row"
                    :style="{ animation: `slideIn 0.3s ease ${index * 0.05}s` }"
                  >
                    <td class="table-cell">
                      <span class="tipo-badge" :class="`tipo-${solicitud.tipo}`">
                        {{ solicitud.tipo.toUpperCase() }}
                      </span>
                    </td>
                    <td class="table-cell">{{ solicitud.descripcion || 'N/A' }}</td>
                    <td class="table-cell">
                      <div class="cell-content">
                        <User class="icon-small" />
                        <span>{{ solicitud.usuario_nombre || 'Usuario' }}</span>
                      </div>
                    </td>
                    <td class="table-cell">
                      {{ formatDate(solicitud.fecha_solicitud) }}
                    </td>
                    <td class="table-cell">
                      <span class="estado-badge estado-pendiente">
                        En espera
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- Notificaciones Recientes -->
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200, duration: 600 } }"
          class="notifications-section"
        >
          <div class="section-header">
            <h2 class="section-title">
              <span class="count-badge">{{ notificacionesRecientes.length }}</span>
              Notificaciones Recientes
            </h2>
            <p class="section-subtitle">Últimas actividades del sistema</p>
          </div>

          <!-- Estado vacío -->
          <div v-if="notificacionesRecientes.length === 0" class="empty-state">
            <div class="empty-icon">
              <Bell />
            </div>
            <h3 class="empty-title">Sin notificaciones</h3>
            <p class="empty-text">No hay notificaciones en el sistema</p>
          </div>

          <!-- Lista de notificaciones -->
          <div v-else class="notifications-list">
            <div
              v-for="(notif, index) in notificacionesRecientes.slice(0, 10)"
              :key="notif.id"
              class="notification-item"
              :class="{ 'notif-unread': !notif.leido }"
              :style="{ animation: `slideIn 0.3s ease ${index * 0.05}s` }"
            >
              <div class="notif-icon" :style="{ borderLeftColor: getNotificationColor(notif.tipo) }">
                <component :is="getNotificationIcon(notif.tipo)" :size="16" />
              </div>
              <div class="notif-body">
                <p class="notif-titulo">{{ notif.titulo }}</p>
                <p class="notif-mensaje">{{ notif.mensaje }}</p>
                <p class="notif-tiempo">{{ formatTime(notif.created_at) }}</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Swal from 'sweetalert2'
// @ts-ignore
import { useAuthStore } from '../stores/auth'
import {
  ArrowLeft,
  Settings,
  Users,
  Sprout,
  BarChart3,
  AlertCircle,
  TrendingUp,
  CheckCircle,
  Bell,
  Clock,
  Info,
  User
} from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()

const overview = ref({
  total_usuarios: 0,
  total_sembradores: 0,
  total_seguimientos: 0,
  pendientes: 0,
  promedio_avance: 0
})

const solicitudesPendientes = ref<any[]>([])
const notificacionesRecientes = ref<any[]>([])

// ✅ Función: Obtener resumen global del admin
const getAdminOverview = async () => {
  try {
    const token = localStorage.getItem('token') || auth.token
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/auth/admin/overview`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    overview.value = response.data
    console.log('✅ Admin Overview cargado:', overview.value)
  } catch (error) {
    console.error('❌ Error cargando admin overview:', error)
  }
}

// ✅ Función: Obtener solicitudes pendientes
const getSolicitudesPendientes = async () => {
  try {
    const token = localStorage.getItem('token') || auth.token
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/solicitudes`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    solicitudesPendientes.value = (response.data || []).filter(
      (s: any) => s.estado === 'pendiente'
    )
    console.log('✅ Solicitudes pendientes cargadas:', solicitudesPendientes.value.length)
  } catch (error) {
    console.error('❌ Error cargando solicitudes:', error)
  }
}

// ✅ Función: Obtener notificaciones recientes
const getNotificacionesRecientes = async () => {
  try {
    const token = localStorage.getItem('token') || auth.token
    const response = await axios.get(
      `${import.meta.env.VITE_API_URL}/notificaciones`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    notificacionesRecientes.value = (response.data || []).reverse().slice(0, 10)
    console.log('✅ Notificaciones recientes cargadas:', notificacionesRecientes.value.length)
  } catch (error) {
    console.error('❌ Error cargando notificaciones:', error)
  }
}

// ✅ Funciones auxiliares de formato
const formatDate = (fecha: string | null) => {
  if (!fecha) return 'N/A'
  const date = new Date(fecha)
  return date.toLocaleDateString('es-CO')
}

const formatTime = (fecha: string | null) => {
  if (!fecha) return 'Hace poco'
  const date = new Date(fecha)
  const ahora = new Date()
  const diff = ahora.getTime() - date.getTime()
  const minutos = Math.floor(diff / 60000)
  const horas = Math.floor(diff / 3600000)
  const dias = Math.floor(diff / 86400000)

  if (minutos < 1) return 'Hace poco'
  if (minutos < 60) return `Hace ${minutos}m`
  if (horas < 24) return `Hace ${horas}h`
  if (dias < 7) return `Hace ${dias}d`
  return date.toLocaleDateString('es-CO')
}

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
    default:
      return Info
  }
}

const recargarAdmin = async () => {
  try {
    await getAdminOverview()
    await getSolicitudesPendientes()
    await getNotificacionesRecientes()
    await Swal.fire('✅ Recargado', 'El panel se ha actualizado', 'success')
  } catch (err) {
    await Swal.fire('❌ Error', 'No se pudo recargar el panel', 'error')
  }
}

// ✅ Ciclo de vida
onMounted(async () => {
  // Verificar si el usuario es admin
  if (auth.user?.rol !== 'admin') {
    console.warn('⚠️ Acceso denegado: Solo admin puede acceder')
    router.push('/dashboard')
    return
  }

  // Cargar datos
  await getAdminOverview()
  await getSolicitudesPendientes()
  await getNotificacionesRecientes()
})
</script>

<style scoped>
/* ========== VARIABLES ========== */
:root {
  --color-primary: #10b981;
  --color-secondary: #f59e0b;
  --color-info: #3b82f6;
  --color-warning: #ef4444;
  --color-accent: #8b5cf6;
  --bg-dark: #0f172a;
  --bg-card: #1e293b;
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --border-light: rgba(148, 163, 184, 0.1);
  --border-accent: rgba(16, 185, 129, 0.2);
}

/* ========== ANIMACIONES ========== */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes blob {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20px, -50px) scale(1.1);
  }
  50% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  75% {
    transform: translate(50px, 50px) scale(1.05);
  }
}

/* ========== CONTENEDOR PRINCIPAL ========== */
.admin-container {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--bg-dark) 0%, #1a2742 100%);
  overflow-x: hidden;
}

/* ========== BACKGROUND BLOBS ========== */
.background-blobs {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.blob {
  position: absolute;
  border-radius: 50%;
  opacity: 0.08;
  animation: blob 8s infinite;
}

.blob-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  top: -50px;
  left: -50px;
  animation-delay: 0s;
}

.blob-2 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, var(--color-info), var(--color-accent));
  bottom: 10%;
  right: 10%;
  animation-delay: 4s;
}

.blob-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, var(--color-secondary), var(--color-warning));
  top: 50%;
  right: 5%;
  animation-delay: 2s;
}

/* ========== HEADER ========== */
.header-admin {
  position: relative;
  z-index: 10;
  padding: 1rem 1.2rem;
  background: rgba(132, 204, 22, 0.12);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(132, 204, 22, 0.1);
  box-shadow: 0 4px 20px rgba(132, 204, 22, 0.1);
  width: 100%;
}

.header-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.back-button {
  width: 40px;
  height: 40px;
  border: 1.5px solid rgba(132, 204, 22, 0.4);
  background: rgba(132, 204, 22, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #84cc16;
  text-decoration: none;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.back-button:hover {
  background: rgba(132, 204, 22, 0.2);
  border-color: rgba(132, 204, 22, 0.6);
  color: #84cc16;
  box-shadow: 0 4px 15px rgba(132, 204, 22, 0.3);
  transform: translateX(-4px);
}

.back-icon {
  width: 20px;
  height: 20px;
}

.header-icon-small {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: transparent;
  flex-shrink: 0;
}

.icon-stat {
  width: 20px;
  height: 20px;
  color: #84cc16;
  stroke-width: 2;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #84cc16;
  margin: 0;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.4);
}

.header-subtitle {
  font-size: 0.75rem;
  color: #cbd5e1;
  margin: 0;
  margin-top: 0.2rem;
}

/* ========== RELOAD BUTTON ========== */
.reload-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.1);
  border: 1.5px solid rgba(59, 130, 246, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  color: #3b82f6;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
  padding: 0;
}

.reload-button:hover {
  background: rgba(59, 130, 246, 0.2);
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  border-color: rgba(59, 130, 246, 0.6);
}

.reload-button:active {
  transform: scale(0.95);
}

.reload-icon {
  width: 22px;
  height: 22px;
  stroke-width: 2.5;
}

/* ========== MAIN ========== */
.admin-main {
  position: relative;
  z-index: 5;
  padding: 2rem;
}

.admin-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ========== SECCIONES ========== */
.stats-section,
.solicitudes-section,
.notifications-section {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.3));
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.section-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #84cc16;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0 0 1rem 0;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.3);
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--color-primary), #059669);
  color: white;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.875rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-subtitle {
  font-size: 0.95rem;
  color: var(--text-muted);
  margin-top: 0.5rem;
}

/* ========== STATS GRID ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  border-left: 4px solid;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-card:hover {
  transform: translateY(-4px);
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(16, 185, 129, 0.3);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon {
  width: 28px;
  height: 28px;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0.25rem 0 0 0;
}

/* ========== TABLE ========== */
.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.table-container {
  min-width: 100%;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header-row {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
  border-bottom: 2px solid var(--border-accent);
}

.table-header-cell {
  padding: 1rem;
  text-align: left;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.table-body-row {
  border-bottom: 1px solid var(--border-light);
  transition: all 0.3s ease;
}

.table-body-row:hover {
  background: rgba(16, 185, 129, 0.05);
}

.table-cell {
  padding: 1rem;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.cell-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icon-small {
  width: 16px;
  height: 16px;
  color: var(--color-primary);
  flex-shrink: 0;
}

.tipo-badge {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.tipo-solicitud {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.tipo-reclamo {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.tipo-reporteSeguimiento {
  background: rgba(245, 158, 11, 0.2);
  color: #fcd34d;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.estado-badge {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.estado-pendiente {
  background: rgba(245, 158, 11, 0.2);
  color: #fcd34d;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

/* ========== EMPTY STATE ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  color: var(--color-primary);
}

.empty-icon svg {
  width: 40px;
  height: 40px;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.empty-text {
  font-size: 0.95rem;
  color: var(--text-muted);
}

/* ========== NOTIFICATIONS LIST ========== */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.notification-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.4);
  border-radius: 12px;
  border-left: 4px solid;
  transition: all 0.3s ease;
}

.notification-item.notif-unread {
  background: rgba(16, 185, 129, 0.05);
}

.notification-item:hover {
  background: rgba(30, 41, 59, 0.6);
  transform: translateX(4px);
}

.notif-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(16, 185, 129, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notif-icon svg {
  width: 20px;
  height: 20px;
  color: var(--color-primary);
}

.notif-body {
  flex: 1;
  min-width: 0;
}

.notif-titulo {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.25rem 0;
}

.notif-mensaje {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.notif-tiempo {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin: 0;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .header-admin {
    padding: 0.8rem 1rem;
  }

  .header-icon-small {
    width: 28px;
    height: 28px;
  }

  .icon-stat {
    width: 18px;
    height: 18px;
  }

  .header-title {
    font-size: 0.85rem;
  }

  .header-subtitle {
    font-size: 0.7rem;
  }

  .reload-button {
    width: 36px;
    height: 36px;
  }

  .reload-icon {
    width: 20px;
    height: 20px;
  }

  .admin-main {
    padding: 1rem;
  }

  .stats-section,
  .solicitudes-section,
  .notifications-section {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 1.1rem;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 1rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-value {
    font-size: 1.3rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.6rem 0.5rem;
    font-size: 0.75rem;
  }

  .table-header-cell {
    font-size: 0.7rem;
  }
}

@media (max-width: 640px) {
  .header-admin {
    padding: 0.75rem 0.9rem;
  }

  .header-icon-small {
    width: 28px;
    height: 28px;
  }

  .icon-stat {
    width: 18px;
    height: 18px;
  }

  .header-title {
    font-size: 0.8rem;
  }

  .header-subtitle {
    font-size: 0.7rem;
  }

  .reload-button {
    width: 36px;
    height: 36px;
  }

  .reload-icon {
    width: 20px;
    height: 20px;
  }

  .section-title {
    font-size: 1.05rem;
  }

  .stats-grid {
    gap: 0.8rem;
  }

  .stat-value {
    font-size: 1.2rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.5rem 0.4rem;
    font-size: 0.7rem;
  }
}

@media (max-width: 480px) {
  .admin-container {
    min-height: 100vh;
  }

  .header-admin {
    padding: 0.7rem 0.8rem;
  }

  .header-icon-small {
    width: 26px;
    height: 26px;
  }

  .icon-stat {
    width: 16px;
    height: 16px;
  }

  .header-title {
    font-size: 0.75rem;
  }

  .header-subtitle {
    font-size: 0.65rem;
  }

  .back-button {
    width: 34px;
    height: 34px;
  }

  .back-icon {
    width: 16px;
    height: 16px;
  }

  .reload-button {
    width: 34px;
    height: 34px;
  }

  .reload-icon {
    width: 18px;
    height: 18px;
  }

  .back-icon {
    width: 16px;
    height: 16px;
  }

  .admin-main {
    padding: 0.75rem;
  }

  .stats-section,
  .solicitudes-section,
  .notifications-section {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.6rem;
  }

  .stat-card {
    padding: 0.75rem;
    gap: 0.6rem;
  }

  .stat-label {
    font-size: 0.65rem;
  }

  .stat-value {
    font-size: 1.1rem;
  }

  .section-title {
    font-size: 1rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.4rem 0.3rem;
    font-size: 0.65rem;
  }

  .notification-item {
    padding: 0.75rem;
    gap: 0.6rem;
  }

  .notif-icon {
    width: 28px;
    height: 28px;
  }

  .notif-titulo {
    font-size: 0.8rem;
  }

  .notif-mensaje {
    font-size: 0.7rem;
  }
}
</style>
