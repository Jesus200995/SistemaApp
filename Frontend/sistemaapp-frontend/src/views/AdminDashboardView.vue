<template>
  <div class="admin-container">
    <!-- Menú hamburguesa global -->
    <HamburgerMenu />

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
        <section class="stats-section">
          <h2 class="section-title">Estadísticas Generales</h2>
          
          <div class="stats-grid">
            <!-- Card: Total Usuarios -->
            <div class="stat-card stat-card-green">
              <div class="stat-icon stat-icon-green">
                <Users class="card-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Total Usuarios</p>
                <p class="stat-value">{{ overview.total_usuarios || 0 }}</p>
              </div>
            </div>

            <!-- Card: Total Sembradores -->
            <div class="stat-card stat-card-amber">
              <div class="stat-icon stat-icon-amber">
                <Sprout class="card-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Sembradores</p>
                <p class="stat-value">{{ overview.total_sembradores || 0 }}</p>
              </div>
            </div>

            <!-- Card: Total Seguimientos -->
            <div class="stat-card stat-card-blue">
              <div class="stat-icon stat-icon-blue">
                <BarChart3 class="card-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Seguimientos</p>
                <p class="stat-value">{{ overview.total_seguimientos || 0 }}</p>
              </div>
            </div>

            <!-- Card: Solicitudes Pendientes -->
            <div class="stat-card stat-card-red">
              <div class="stat-icon stat-icon-red">
                <AlertCircle class="card-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Solicitudes Pendientes</p>
                <p class="stat-value">{{ overview.pendientes || 0 }}</p>
              </div>
            </div>

            <!-- Card: Promedio de Avance -->
            <div class="stat-card stat-card-purple">
              <div class="stat-icon stat-icon-purple">
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
        <section class="solicitudes-section">
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
        <section class="notifications-section">
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
import { getSecureApiUrl } from '../utils/api'
import HamburgerMenu from '../components/HamburgerMenu.vue'
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
    const apiUrl = getSecureApiUrl()
    const response = await axios.get(
      `${apiUrl}/auth/admin/overview`,
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
    const apiUrl = getSecureApiUrl()
    const response = await axios.get(
      `${apiUrl}/solicitudes`,
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
    const apiUrl = getSecureApiUrl()
    const response = await axios.get(
      `${apiUrl}/notificaciones`,
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
  --color-primary: #16a34a;
  --color-secondary: #f59e0b;
  --color-info: #3b82f6;
  --color-warning: #ef4444;
  --color-accent: #8b5cf6;
  --bg-dark: #f0fdf4;
  --bg-card: rgba(255, 255, 255, 0.9);
  --text-primary: #1e3a2f;
  --text-secondary: #374151;
  --text-muted: #64748b;
  --border-light: rgba(22, 163, 74, 0.1);
  --border-accent: rgba(22, 163, 74, 0.2);
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
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
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
  opacity: 0.3;
  animation: blob 8s infinite;
  mix-blend-mode: multiply;
}

.blob-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #16a34a, #15803d);
  top: -50px;
  left: -50px;
  animation-delay: 0s;
}

.blob-2 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  bottom: 10%;
  right: 10%;
  animation-delay: 4s;
}

.blob-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #86efac, #4ade80);
  top: 50%;
  right: 5%;
  animation-delay: 2s;
}

/* ========== HEADER ========== */
.header-admin {
  position: relative;
  z-index: 10;
  padding: 1rem 1.2rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(22, 163, 74, 0.2);
  box-shadow: 0 4px 20px rgba(22, 163, 74, 0.1);
  width: 100%;
}

.header-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 60px; /* Espacio para el menú hamburguesa */
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
  border: 1.5px solid rgba(22, 163, 74, 0.4);
  background: rgba(22, 163, 74, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #16a34a;
  text-decoration: none;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.back-button:hover {
  background: rgba(22, 163, 74, 0.2);
  border-color: rgba(22, 163, 74, 0.6);
  color: #16a34a;
  box-shadow: 0 4px 15px rgba(22, 163, 74, 0.3);
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
  color: #16a34a;
  stroke-width: 2;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #16a34a;
  margin: 0;
  text-shadow: none;
}

.header-subtitle {
  font-size: 0.75rem;
  color: #64748b;
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
  padding: 1rem;
}

.admin-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* ========== SECCIONES ========== */
.stats-section,
.solicitudes-section,
.notifications-section {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 1rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(22, 163, 74, 0.08);
}

.section-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #16a34a;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 0 0.75rem 0;
  text-shadow: none;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #16a34a, #15803d);
  color: white;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.75rem;
}

.section-header {
  margin-bottom: 0.75rem;
}

.section-subtitle {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
}

/* ========== STATS GRID ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.75rem;
  justify-items: center;
}

.stat-card {
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(var(--card-rgb), 0.12) 0%,
    rgba(var(--card-rgb), 0.06) 50%,
    rgba(var(--card-rgb), 0.12) 100%
  );
  border-radius: 16px;
  padding: 1rem 0.75rem;
  width: 100%;
  max-width: 160px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.6rem;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1.5px solid rgba(var(--card-rgb), 0.25);
  box-shadow: 
    0 4px 15px rgba(var(--card-rgb), 0.1),
    inset 0 0 30px rgba(var(--card-rgb), 0.05);
}

.stat-card:hover {
  transform: translateY(-4px);
  background: linear-gradient(
    135deg,
    rgba(var(--card-rgb), 0.18) 0%,
    rgba(var(--card-rgb), 0.1) 50%,
    rgba(var(--card-rgb), 0.18) 100%
  );
  box-shadow: 
    0 8px 25px rgba(var(--card-rgb), 0.2),
    inset 0 0 40px rgba(var(--card-rgb), 0.08);
}

/* Variantes de color para cada card */
.stat-card-green {
  --card-rgb: 16, 185, 129;
}

.stat-card-amber {
  --card-rgb: 245, 158, 11;
}

.stat-card-blue {
  --card-rgb: 59, 130, 246;
}

.stat-card-red {
  --card-rgb: 239, 68, 68;
}

.stat-card-purple {
  --card-rgb: 139, 92, 246;
}

/* Iconos de las cards - Circular con efecto vidrio líquido */
.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.stat-icon-green {
  background: linear-gradient(
    135deg,
    rgba(16, 185, 129, 0.25) 0%,
    rgba(5, 150, 105, 0.4) 50%,
    rgba(16, 185, 129, 0.25) 100%
  );
  border: 1.5px solid rgba(16, 185, 129, 0.5);
  box-shadow: 
    0 4px 15px rgba(16, 185, 129, 0.3),
    inset 0 0 20px rgba(16, 185, 129, 0.15),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.stat-icon-green .card-icon {
  color: #059669;
  filter: drop-shadow(0 1px 2px rgba(5, 150, 105, 0.4));
}

.stat-icon-amber {
  background: linear-gradient(
    135deg,
    rgba(245, 158, 11, 0.25) 0%,
    rgba(217, 119, 6, 0.4) 50%,
    rgba(245, 158, 11, 0.25) 100%
  );
  border: 1.5px solid rgba(245, 158, 11, 0.5);
  box-shadow: 
    0 4px 15px rgba(245, 158, 11, 0.3),
    inset 0 0 20px rgba(245, 158, 11, 0.15),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.stat-icon-amber .card-icon {
  color: #d97706;
  filter: drop-shadow(0 1px 2px rgba(217, 119, 6, 0.4));
}

.stat-icon-blue {
  background: linear-gradient(
    135deg,
    rgba(59, 130, 246, 0.25) 0%,
    rgba(37, 99, 235, 0.4) 50%,
    rgba(59, 130, 246, 0.25) 100%
  );
  border: 1.5px solid rgba(59, 130, 246, 0.5);
  box-shadow: 
    0 4px 15px rgba(59, 130, 246, 0.3),
    inset 0 0 20px rgba(59, 130, 246, 0.15),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.stat-icon-blue .card-icon {
  color: #2563eb;
  filter: drop-shadow(0 1px 2px rgba(37, 99, 235, 0.4));
}

.stat-icon-red {
  background: linear-gradient(
    135deg,
    rgba(239, 68, 68, 0.25) 0%,
    rgba(220, 38, 38, 0.4) 50%,
    rgba(239, 68, 68, 0.25) 100%
  );
  border: 1.5px solid rgba(239, 68, 68, 0.5);
  box-shadow: 
    0 4px 15px rgba(239, 68, 68, 0.3),
    inset 0 0 20px rgba(239, 68, 68, 0.15),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.stat-icon-red .card-icon {
  color: #dc2626;
  filter: drop-shadow(0 1px 2px rgba(220, 38, 38, 0.4));
}

.stat-icon-purple {
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.25) 0%,
    rgba(124, 58, 237, 0.4) 50%,
    rgba(139, 92, 246, 0.25) 100%
  );
  border: 1.5px solid rgba(139, 92, 246, 0.5);
  box-shadow: 
    0 4px 15px rgba(139, 92, 246, 0.3),
    inset 0 0 20px rgba(139, 92, 246, 0.15),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.stat-icon-purple .card-icon {
  color: #7c3aed;
  filter: drop-shadow(0 1px 2px rgba(124, 58, 237, 0.4));
}

.card-icon {
  width: 22px;
  height: 22px;
}

.stat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.stat-label {
  font-size: 0.65rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin: 0;
  line-height: 1.2;
}

.stat-value {
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0.2rem 0 0 0;
  line-height: 1;
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
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.1), rgba(22, 163, 74, 0.05));
  border-bottom: 1.5px solid var(--border-accent);
}

.table-header-cell {
  padding: 0.6rem 0.5rem;
  text-align: left;
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.table-body-row {
  border-bottom: 1px solid var(--border-light);
  transition: all 0.3s ease;
}

.table-body-row:hover {
  background: rgba(22, 163, 74, 0.05);
}

.table-cell {
  padding: 0.5rem;
  color: var(--text-primary);
  font-size: 0.75rem;
}

.cell-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon-small {
  width: 14px;
  height: 14px;
  color: var(--color-primary);
  flex-shrink: 0;
}

.tipo-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.tipo-solicitud {
  background: rgba(59, 130, 246, 0.15);
  color: #2563eb;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.tipo-reclamo {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.tipo-reporteSeguimiento {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
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
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

/* ========== EMPTY STATE ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem 1rem;
  text-align: center;
}

.empty-icon {
  width: 50px;
  height: 50px;
  background: rgba(22, 163, 74, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  color: #16a34a;
}

.empty-icon svg {
  width: 24px;
  height: 24px;
}

.empty-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.empty-text {
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* ========== NOTIFICATIONS LIST ========== */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.notification-item {
  display: flex;
  gap: 0.6rem;
  padding: 0.6rem;
  background: white;
  border-radius: 8px;
  border-left: 3px solid;
  transition: all 0.3s ease;
  border: 1px solid rgba(22, 163, 74, 0.1);
}

.notification-item.notif-unread {
  background: rgba(22, 163, 74, 0.05);
}

.notification-item:hover {
  background: rgba(22, 163, 74, 0.08);
  transform: translateX(2px);
}

.notif-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: rgba(22, 163, 74, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notif-icon svg {
  width: 16px;
  height: 16px;
  color: #16a34a;
}

.notif-body {
  flex: 1;
  min-width: 0;
}

.notif-titulo {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.15rem 0;
}

.notif-mensaje {
  font-size: 0.7rem;
  color: var(--text-secondary);
  margin: 0 0 0.25rem 0;
  line-height: 1.35;
}

.notif-tiempo {
  font-size: 0.65rem;
  color: var(--text-muted);
  margin: 0;
}

/* ========== RESPONSIVE ========== */

/* Pantallas grandes horizontales */
@media (min-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(5, 1fr);
  }
  
  .stat-card {
    max-width: 180px;
  }
}

/* Tablets y pantallas medianas */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(5, 1fr);
    gap: 0.5rem;
  }
  
  .stat-card {
    max-width: none;
    padding: 0.75rem 0.5rem;
  }
  
  .stat-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
  }
  
  .stat-label {
    font-size: 0.55rem;
  }
  
  .stat-value {
    font-size: 1.1rem;
  }
}

@media (max-width: 768px) {
  .header-admin {
    padding: 0.6rem 0.8rem;
  }

  .header-wrapper {
    padding-right: 50px;
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
    font-size: 0.8rem;
  }

  .header-subtitle {
    font-size: 0.65rem;
  }

  .back-button,
  .reload-button {
    width: 34px;
    height: 34px;
  }

  .reload-icon,
  .back-icon {
    width: 18px;
    height: 18px;
  }

  .admin-main {
    padding: 0.75rem;
  }

  .admin-content {
    gap: 0.75rem;
  }

  .stats-section,
  .solicitudes-section,
  .notifications-section {
    padding: 0.75rem;
    border-radius: 10px;
  }

  .section-title {
    font-size: 0.85rem;
  }

  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }

  .stat-card {
    padding: 0.6rem 0.4rem;
    gap: 0.5rem;
  }

  .stat-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
  }

  .card-icon {
    width: 16px;
    height: 16px;
  }

  .stat-label {
    font-size: 0.6rem;
  }

  .stat-value {
    font-size: 1rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.4rem 0.35rem;
    font-size: 0.65rem;
  }

  .notification-item {
    padding: 0.5rem;
    gap: 0.5rem;
  }

  .notif-icon {
    width: 28px;
    height: 28px;
  }

  .notif-icon svg {
    width: 14px;
    height: 14px;
  }

  .notif-titulo {
    font-size: 0.75rem;
  }

  .notif-mensaje {
    font-size: 0.65rem;
  }
}

/* Móviles pequeños */
@media (max-width: 480px) {
  .admin-container {
    min-height: 100vh;
  }

  .header-admin {
    padding: 0.5rem 0.6rem;
  }

  .header-wrapper {
    padding-right: 45px;
    gap: 0.4rem;
  }

  .header-left {
    gap: 0.4rem;
  }

  .header-icon-small {
    width: 22px;
    height: 22px;
  }

  .icon-stat {
    width: 14px;
    height: 14px;
  }

  .header-title {
    font-size: 0.7rem;
  }

  .header-subtitle {
    font-size: 0.6rem;
  }

  .back-button,
  .reload-button {
    width: 30px;
    height: 30px;
  }

  .back-icon,
  .reload-icon {
    width: 16px;
    height: 16px;
  }

  .admin-main {
    padding: 0.5rem;
  }

  .admin-content {
    gap: 0.5rem;
  }

  .stats-section,
  .solicitudes-section,
  .notifications-section {
    padding: 0.6rem;
    border-radius: 8px;
  }

  .section-title {
    font-size: 0.75rem;
    gap: 0.4rem;
  }

  .count-badge {
    width: 20px;
    height: 20px;
    font-size: 0.65rem;
    border-radius: 4px;
  }

  .section-subtitle {
    font-size: 0.65rem;
  }

  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.4rem;
  }

  .stat-card {
    padding: 0.5rem 0.35rem;
    gap: 0.35rem;
    align-items: center;
  }

  .stat-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
  }

  .card-icon {
    width: 14px;
    height: 14px;
  }

  .stat-label {
    font-size: 0.5rem;
  }

  .stat-value {
    font-size: 0.9rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.3rem 0.25rem;
    font-size: 0.6rem;
  }

  .tipo-badge,
  .estado-badge {
    padding: 0.2rem 0.35rem;
    font-size: 0.55rem;
  }

  .notifications-list {
    gap: 0.35rem;
  }

  .notification-item {
    padding: 0.4rem;
    gap: 0.4rem;
    border-radius: 6px;
  }

  .notif-icon {
    width: 24px;
    height: 24px;
  }

  .notif-icon svg {
    width: 12px;
    height: 12px;
  }

  .notif-titulo {
    font-size: 0.7rem;
  }

  .notif-mensaje {
    font-size: 0.6rem;
  }

  .notif-tiempo {
    font-size: 0.55rem;
  }

  .empty-state {
    padding: 1rem;
  }

  .empty-icon {
    width: 40px;
    height: 40px;
  }

  .empty-icon svg {
    width: 20px;
    height: 20px;
  }

  .empty-title {
    font-size: 0.8rem;
  }

  .empty-text {
    font-size: 0.7rem;
  }
}

/* Orientación horizontal en móviles */
@media (max-height: 500px) and (orientation: landscape) {
  .header-admin {
    padding: 0.4rem 0.6rem;
  }

  .admin-main {
    padding: 0.4rem;
  }

  .stats-grid {
    grid-template-columns: repeat(5, 1fr);
  }

  .stat-card {
    flex-direction: row;
    padding: 0.4rem;
  }

  .stat-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
  }

  .stats-section,
  .solicitudes-section,
  .notifications-section {
    padding: 0.5rem;
  }

  .notifications-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.4rem;
  }
}
</style>
