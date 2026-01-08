<template>
  <div class="estadisticas-container">
    <!-- Desktop Sidebar -->
    <DesktopSidebar />

    <!-- Menú hamburguesa global (solo móvil) -->
    <HamburgerMenu class="mobile-only" />

    <!-- Main Wrapper para PC -->
    <div class="main-wrapper">
      <!-- Header para PC -->
      <header class="view-header">
        <div class="header-content">
          <div class="header-title">
            <BarChart3 :size="22" class="header-icon" />
            <div>
              <h1>Estadísticas</h1>
              <p class="header-subtitle">Análisis del sistema</p>
            </div>
          </div>
          <div class="header-actions">
            <button @click="recargarEstadisticas" class="btn-secondary" title="Recargar">
              <RotateCw :size="18" />
            </button>
          </div>
        </div>
      </header>

      <!-- Fondo decorativo con blobs (solo móvil) -->
      <div class="background-blobs mobile-only">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
      </div>

      <!-- Header con botón de regreso (solo móvil) -->
      <header class="header-estadisticas mobile-only">
      <div class="header-wrapper">
        <div class="header-left">
          <router-link to="/dashboard" class="back-button" title="Volver al Dashboard">
            <ArrowLeft class="back-icon" />
          </router-link>
          <div class="header-icon-small">
            <BarChart3 class="icon-stat" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Estadísticas</h1>
            <p class="header-subtitle">Análisis del sistema</p>
          </div>
        </div>
        <button @click="recargarEstadisticas" class="reload-button" title="Recargar">
          <svg class="reload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M3 21v-5h5"></path>
          </svg>
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="estadisticas-main">
      <div class="estadisticas-content">
        <!-- Estadísticas Principales -->
        <section class="stats-section">
          <div class="stats-grid">
            <!-- Card 1: Total Sembradores -->
            <div class="stat-card stat-card-1">
              <div class="stat-icon-wrapper">
                <Users class="stat-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Total Sembradores</p>
                <p class="stat-value">{{ stats.total_sembradores }}</p>
                <p class="stat-change">
                  <span class="badge-success">✓ Activos</span>
                </p>
              </div>
            </div>

            <!-- Card 2: Total Seguimientos -->
            <div class="stat-card stat-card-2">
              <div class="stat-icon-wrapper">
                <CheckCircle2 class="stat-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Seguimientos Realizados</p>
                <p class="stat-value">{{ stats.total_seguimientos }}</p>
                <p class="stat-change">
                  <span class="badge-info">Registros</span>
                </p>
              </div>
            </div>

            <!-- Card 3: Promedio Avance -->
            <div class="stat-card stat-card-3">
              <div class="stat-icon-wrapper">
                <TrendingUp class="stat-icon" />
              </div>
              <div class="stat-content">
                <p class="stat-label">Promedio de Avance</p>
                <p class="stat-value">{{ stats.promedio_avance }}%</p>
                <div class="progress-mini">
                  <div class="progress-bar-mini">
                    <div class="progress-fill-mini" :style="{ width: stats.promedio_avance + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Gráfico de Cultivos -->
        <section class="chart-section">
          <div class="chart-header">
            <div class="chart-title-wrapper">
              <BarChart3 class="chart-title-icon" />
              <h2 class="chart-title">Distribución de Cultivos</h2>
            </div>
            <p class="chart-subtitle">Cantidad de sembradores por tipo de cultivo</p>
          </div>

          <div v-if="cultivoData.length > 0" class="chart-container">
            <div class="chart-wrapper">
              <Bar :data="chartData" :options="chartOptions" />
            </div>
          </div>

          <div v-else class="empty-chart">
            <BarChart3 class="empty-icon" />
            <p class="empty-text">No hay datos suficientes para mostrar gráficas</p>
            <p class="empty-subtext">Completa más seguimientos para ver análisis</p>
          </div>
        </section>

        <!-- Tabla de Cultivos Detallada -->
        <section class="table-section">
          <div class="table-header">
            <div class="table-title-wrapper">
              <List class="table-title-icon" />
              <h2 class="table-title">Detalle por Cultivo</h2>
            </div>
          </div>

          <div v-if="cultivoData.length > 0" class="table-wrapper">
            <table class="cultivos-table">
              <thead>
                <tr>
                  <th>Tipo de Cultivo</th>
                  <th>Cantidad</th>
                  <th>Porcentaje</th>
                  <th>Barra Visual</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(cultivo, idx) in cultivoDataDetailed" :key="idx" class="table-row">
                  <td class="cultivo-name">
                    <span class="cultivo-badge">{{ cultivo.nombre }}</span>
                  </td>
                  <td class="cultivo-cantidad">
                    <span class="cantidad-badge">{{ cultivo.cantidad }}</span>
                  </td>
                  <td class="cultivo-porcentaje">
                    {{ cultivo.porcentaje }}%
                  </td>
                  <td class="cultivo-bar">
                    <div class="bar-container">
                      <div class="bar-fill" :style="{ width: cultivo.porcentaje + '%', background: cultivo.color }"></div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="empty-table">
            <p>Sin datos de cultivos</p>
          </div>
        </section>

        <!-- Resumen General -->
        <section class="summary-section">
          <div class="summary-card">
            <div class="summary-header">
              <div class="summary-title-wrapper">
                <BarChart2 class="summary-title-icon" />
                <h3 class="summary-title">Resumen General</h3>
              </div>
            </div>
            <div class="summary-content">
              <div class="summary-item">
                <Users class="summary-item-icon" />
                <span class="summary-text">
                  Total de <strong>{{ stats.total_sembradores }}</strong> sembradores registrados en el sistema
                </span>
              </div>
              <div class="summary-item">
                <CheckCircle2 class="summary-item-icon" />
                <span class="summary-text">
                  Se han realizado <strong>{{ stats.total_seguimientos }}</strong> visitas de campo
                </span>
              </div>
              <div class="summary-item">
                <Leaf class="summary-item-icon" />
                <span class="summary-text">
                  Hay <strong>{{ Object.keys(stats.cultivos).length }}</strong> tipos de cultivos diferentes
                </span>
              </div>
              <div class="summary-item">
                <TrendingUp class="summary-item-icon" />
                <span class="summary-text">
                  Promedio de avance general es de <strong>{{ stats.promedio_avance }}%</strong>
                </span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
    </div> <!-- Cierre main-wrapper -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { getSecureApiUrl } from '../utils/api'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import DesktopSidebar from '../components/DesktopSidebar.vue'
import Swal from 'sweetalert2'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { BarChart3, Users, CheckCircle2, TrendingUp, List, BarChart2, Leaf, ArrowLeft, RotateCw } from 'lucide-vue-next'

// Registrar componentes de Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const auth = useAuthStore()
const router = useRouter()
const API_URL = getSecureApiUrl()

// Estado
const stats = ref({
  total_sembradores: 0,
  total_seguimientos: 0,
  promedio_avance: 0,
  cultivos: {} as Record<string, number>
})

const loading = ref(false)

// Colores para los cultivos
const coloresFormatos: Record<string, string> = {
  'Maíz': '#f59e0b',
  'Frijol': '#ef4444',
  'Papa': '#8b5cf6',
  'Tomate': '#f87171',
  'Cebolla': '#fbbf24',
  'Lechuga': '#10b981',
  'Pepino': '#06b6d4',
  'Calabaza': '#f59e0b',
  'Zanahoria': '#fb923c',
  'Remolacha': '#ec4899'
}

// Funciones
const obtenerEstadisticas = async () => {
  try {
    loading.value = true
    const res = await axios.get(`${API_URL}/seguimientos/stats`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    stats.value = res.data
  } catch (error) {
    console.error('Error obteniendo estadísticas:', error)
  } finally {
    loading.value = false
  }
}

const recargarEstadisticas = () => {
  obtenerEstadisticas()
}

// Computed properties
const cultivoData = computed(() => {
  return Object.entries(stats.value.cultivos || {}).sort((a, b) => b[1] - a[1])
})

const cultivoDataDetailed = computed(() => {
  const total = Object.values(stats.value.cultivos || {}).reduce((a, b) => a + b, 0)
  return cultivoData.value.map(([nombre, cantidad], idx) => {
    const colores = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#14b8a6', '#f97316', '#6366f1']
    return {
      nombre,
      cantidad,
      porcentaje: total > 0 ? Math.round((cantidad / total) * 100) : 0,
      color: coloresFormatos[nombre] || colores[idx % colores.length]
    }
  })
})

const chartData = computed(() => ({
  labels: cultivoData.value.map(([nombre]) => nombre),
  datasets: [
    {
      label: 'Número de Sembradores',
      data: cultivoData.value.map(([, cantidad]) => cantidad),
      backgroundColor: [
        '#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6',
        '#06b6d4', '#ec4899', '#14b8a6', '#f97316', '#6366f1'
      ],
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 2,
      borderRadius: 8
    }
  ]
}))

const chartOptions: any = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      cornerRadius: 8,
      titleFont: { size: 14, weight: 600 },
      bodyFont: { size: 13 }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(148, 163, 184, 0.1)',
        drawBorder: false
      },
      ticks: {
        color: '#cbd5e1',
        font: { size: 12 }
      }
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
        color: '#cbd5e1',
        font: { size: 12 }
      }
    }
  }
}

// Ciclo de vida
onMounted(() => {
  // 🔒 Validar rol: Solo admin, territorial, facilitador pueden acceder
  const rol = auth.user?.rol
  if (!rol || !['admin', 'territorial', 'facilitador'].includes(rol)) {
    // Redirigir a dashboard y mostrar error
    Swal.fire({
      icon: 'error',
      title: 'Acceso Denegado',
      text: 'No tienes permiso para acceder a reportes y estadísticas',
      confirmButtonText: 'Ir al Dashboard'
    }).then(() => {
      router.push('/dashboard')
    })
    return
  }
  obtenerEstadisticas()
})
</script>

<style scoped>
:root {
  --color-primary: #16a34a;
  --color-primary-dark: #15803d;
  --color-bg: #f0fdf4;
  --color-bg-dark: #dcfce7;
  --color-card: rgba(255, 255, 255, 0.9);
  --color-input: #f8fafc;
  --color-border: #bbf7d0;
  --color-text: #1e3a2f;
  --color-text-sec: #374151;
  --color-text-dim: #64748b;
}

.estadisticas-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #f0fdf4 100%);
  position: relative;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: flex;
  flex-direction: column;
}

/* ========== LAYOUT PC ========== */
@media (min-width: 1024px) {
  .estadisticas-container {
    flex-direction: row;
    background: #f8fafc;
  }
  .mobile-only {
    display: none !important;
  }
}

/* ========== MAIN WRAPPER UNIFICADO ========== */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin-left: clamp(180px, 18vw, 220px);
  width: calc(100% - clamp(180px, 18vw, 220px));
}

/* ========== VIEW HEADER ========== */
.view-header {
  display: block;
  background: white;
  padding: clamp(0.4rem, 1vw, 0.625rem) clamp(0.75rem, 2vw, 1.25rem);
  border-bottom: 1px solid #e5e7eb;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.header-title h1 {
  font-size: clamp(0.9rem, 2vw, 1.1rem);
  font-weight: 600;
  color: #14532d;
  margin: 0;
}

.header-subtitle {
  font-size: clamp(0.65rem, 1.2vw, 0.75rem);
  color: #6b7280;
  margin: 0;
}

.header-icon {
  color: #16a34a;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-secondary {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

/* ========== BLOBS ========== */
.background-blobs {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.blob {
  position: absolute;
  opacity: 0.3;
  filter: blur(120px);
  mix-blend-mode: multiply;
  border-radius: 50%;
}

.blob-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #16a34a, #15803d);
  top: -300px;
  left: -300px;
  animation: float 8s ease-in-out infinite;
}

.blob-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  top: 50%;
  right: -250px;
  animation: float 10s ease-in-out infinite reverse;
}

.blob-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #86efac, #4ade80);
  bottom: -200px;
  left: 50%;
  animation: float 12s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  33% { transform: translate(30px, -50px); }
  66% { transform: translate(-20px, 20px); }
}

/* ========== HEADER ========== */
.header-estadisticas {
  position: relative;
  z-index: 10;
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(22, 163, 74, 0.2);
  backdrop-filter: blur(12px);
  padding: 1rem 1.2rem;
  box-shadow: 0 4px 20px rgba(22, 163, 74, 0.1);
  width: 100%;
}

.header-wrapper {
  max-width: 1200px;
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

/* ========== BACK BUTTON ========== */
.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(22, 163, 74, 0.1);
  border: 1.5px solid rgba(22, 163, 74, 0.4);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  color: #16a34a;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.back-button:hover {
  background: rgba(22, 163, 74, 0.2);
  transform: translateX(-4px);
  box-shadow: 0 4px 15px rgba(22, 163, 74, 0.3);
  border-color: rgba(22, 163, 74, 0.6);
}

.back-button:active {
  transform: translateX(-2px);
}

.back-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2.5;
}

.icon-box {
  display: none;
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

.header-icon {
  width: 32px;
  height: 32px;
  color: #ffffff;
  stroke-width: 2;
}

.icon-emoji {
  font-size: 32px;
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

.header-subtitle {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0;
  margin-top: 0.2rem;
}

/* ========== MAIN ========== */
.estadisticas-main {
  position: relative;
  z-index: 5;
  padding: 1rem;
  width: 100%;
}

@media (min-width: 1024px) {
  .estadisticas-main {
    padding: 1.5rem 2rem;
    background: #f8fafc;
  }
  
  .estadisticas-content {
    gap: 2rem;
  }
}

.estadisticas-content {
  display: grid;
  gap: 1rem;
  width: 100%;
}

/* ========== STATS SECTION ========== */
.stats-section {
  position: relative;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
  border: 1.5px solid rgba(22, 163, 74, 0.2);
  border-radius: 14px;
  padding: 0.85rem 0.75rem;
  backdrop-filter: blur(12px);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(22, 163, 74, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

@media (min-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
  
  .stat-card {
    background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
    border: 1.5px solid #e2e8f0;
    padding: 2.5rem 2rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(22, 163, 74, 0.06);
    border-radius: 20px;
  }
  
  .stat-card::before {
    width: 150px;
    height: 150px;
  }
  
  .stat-icon-wrapper {
    width: 64px;
    height: 64px;
    border-radius: 16px;
  }
  
  .stat-icon {
    width: 28px;
    height: 28px;
  }
}

.stat-card:hover {
  border-color: #16a34a;
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 16px 40px rgba(22, 163, 74, 0.2), 0 4px 12px rgba(22, 163, 74, 0.12);
}

.stat-icon-wrapper {
  width: 32px;
  height: 32px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 18px;
  height: 18px;
  color: #16a34a;
  stroke-width: 2.5;
  transition: all 0.3s ease;
}

.stat-card-1 .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.25) 0%, rgba(21, 128, 61, 0.18) 100%);
  border: 1.5px solid rgba(22, 163, 74, 0.4);
}

.stat-card-1:hover .stat-icon-wrapper {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  border-color: #16a34a;
  transform: scale(1.15) rotate(-5deg);
  box-shadow: 0 6px 20px rgba(22, 163, 74, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.3);
}

.stat-card-1:hover .stat-icon {
  color: white;
}

.stat-card-2 .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(37, 99, 235, 0.18) 100%);
  border: 1.5px solid rgba(59, 130, 246, 0.4);
}

.stat-card-2 .stat-icon {
  color: #3b82f6;
}

.stat-card-2:hover .stat-icon-wrapper {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-color: #3b82f6;
  transform: scale(1.15) rotate(-5deg);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.3);
}

.stat-card-2:hover .stat-icon {
  color: white;
}

.stat-card-3 .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(217, 119, 6, 0.18) 100%);
  border: 1.5px solid rgba(245, 158, 11, 0.4);
}

.stat-card-3 .stat-icon {
  color: #f59e0b;
}

.stat-card-3:hover .stat-icon-wrapper {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-color: #f59e0b;
  transform: scale(1.15) rotate(-5deg);
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.3);
}

.stat-card-3:hover .stat-icon {
  color: white;
}

.stat-content {
  flex: 1;
  text-align: center;
  position: relative;
  z-index: 1;
}

.stat-label {
  font-size: 0.65rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 0;
  line-height: 1.2;
  text-align: center;
  font-weight: 600;
}

@media (min-width: 1024px) {
  .stat-label {
    font-size: 0.9rem;
    letter-spacing: 0.06em;
    margin-bottom: 0.5rem;
  }
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0.25rem 0;
  line-height: 1.1;
  text-align: center;
  letter-spacing: -0.5px;
}

@media (min-width: 1024px) {
  .stat-value {
    font-size: 2.5rem;
    margin: 0.75rem 0;
    letter-spacing: -1px;
  }
  
  .badge-success,
  .badge-info {
    font-size: 0.75rem;
    padding: 0.3rem 0.75rem;
    border-radius: 14px;
  }
}

.stat-change {
  font-size: 0.6rem;
  margin: 0.25rem 0 0 0;
}

.badge-success {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.2) 0%, rgba(22, 163, 74, 0.12) 100%);
  color: #16a34a;
  border-radius: 14px;
  font-weight: 700;
  font-size: 0.55rem;
  border: 1px solid rgba(22, 163, 74, 0.3);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.stat-card:hover .badge-success {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: white;
  border-color: #16a34a;
}

.badge-info {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.12) 100%);
  color: #3b82f6;
  border-radius: 14px;
  font-weight: 700;
  font-size: 0.55rem;
  border: 1px solid rgba(59, 130, 246, 0.3);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.stat-card:hover .badge-info {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-color: #3b82f6;
}

.progress-mini {
  margin-top: 0.75rem;
  width: 100%;
}

.progress-bar-mini {
  height: 8px;
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(22, 163, 74, 0.08) 100%);
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid rgba(22, 163, 74, 0.2);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.progress-fill-mini {
  height: 100%;
  background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%);
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.3);
  position: relative;
}

.progress-fill-mini::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.3) 0%, transparent 100%);
}

/* ========== CHART SECTION ========== */
.chart-section {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
  border: 1.5px solid rgba(22, 163, 74, 0.2);
  border-radius: 14px;
  padding: 1rem;
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;
}

.chart-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(22, 163, 74, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

@media (min-width: 1024px) {
  .chart-section {
    background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(22, 163, 74, 0.06);
  }
  
  .chart-title-icon {
    width: 24px;
    height: 24px;
  }
  
  .chart-title {
    font-size: 1.25rem;
  }
  
  .chart-subtitle {
    font-size: 0.85rem;
  }
  
  .chart-container {
    height: 350px;
  }
}

.chart-header {
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(22, 163, 74, 0.15);
  position: relative;
  z-index: 1;
}

.chart-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.chart-title-icon {
  width: 18px;
  height: 18px;
  color: #16a34a;
  stroke-width: 2.5;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.chart-section:hover .chart-title-icon {
  transform: scale(1.1) rotate(-5deg);
  color: #15803d;
}

.chart-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.3px;
}

.chart-subtitle {
  font-size: 0.7rem;
  color: #64748b;
  margin: 0.25rem 0 0 0;
  font-weight: 500;
}

.chart-container {
  position: relative;
  height: 280px;
  margin-bottom: 0.5rem;
}

.chart-wrapper {
  width: 100%;
  height: 100%;
}

.empty-chart {
  text-align: center;
  padding: 1.5rem 1rem;
}

.empty-icon {
  width: 32px;
  height: 32px;
  color: #16a34a;
  stroke-width: 2;
  margin: 0 auto 0.5rem;
}

.empty-text {
  font-size: 0.8rem;
  color: #1e3a2f;
  margin: 0 0 0.25rem 0;
}

.empty-subtext {
  font-size: 0.7rem;
  color: #64748b;
  margin: 0;
}

/* ========== TABLE SECTION ========== */
.table-section {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
  border: 1.5px solid rgba(22, 163, 74, 0.2);
  border-radius: 14px;
  padding: 1rem;
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;
}

.table-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(22, 163, 74, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

@media (min-width: 1024px) {
  .table-section {
    background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(22, 163, 74, 0.06);
  }
  
  .table-title-icon {
    width: 24px;
    height: 24px;
  }
  
  .table-title {
    font-size: 1.25rem;
  }
  
  .cultivos-table th {
    padding: 1rem 0.75rem;
    font-size: 0.85rem;
  }
  
  .table-row td {
    padding: 1rem 0.75rem;
    font-size: 0.95rem;
  }
  
  .cultivo-badge {
    padding: 0.45rem 0.85rem;
    font-size: 0.9rem;
  }
  
  .cantidad-badge {
    padding: 0.35rem 0.65rem;
    font-size: 0.85rem;
  }
  
  .bar-container {
    height: 24px;
  }
}

.table-header {
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(22, 163, 74, 0.15);
  position: relative;
  z-index: 1;
}

.table-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.table-title-icon {
  width: 18px;
  height: 18px;
  color: #16a34a;
  stroke-width: 2.5;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.table-section:hover .table-title-icon {
  transform: scale(1.1) rotate(-5deg);
  color: #15803d;
}

.table-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.3px;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 12px;
  border: 1.5px solid rgba(22, 163, 74, 0.2);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.04);
}

.cultivos-table {
  width: 100%;
  border-collapse: collapse;
}

.cultivos-table thead {
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(22, 163, 74, 0.1) 100%);
  border-bottom: 2px solid rgba(22, 163, 74, 0.3);
}

.cultivos-table th {
  padding: 0.75rem 0.5rem;
  text-align: left;
  color: #16a34a;
  font-weight: 700;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.cultivos-table tbody tr {
  border-bottom: 1px solid rgba(22, 163, 74, 0.12);
  transition: all 0.3s ease;
}

.cultivos-table tbody tr:hover {
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.08) 0%, rgba(22, 163, 74, 0.04) 100%);
  transform: translateX(4px);
}

.table-row td {
  padding: 0.65rem 0.5rem;
  color: #1e293b;
  font-size: 0.8rem;
  font-weight: 500;
}

.cultivo-name {
  min-width: 120px;
}

.cultivo-badge {
  display: inline-block;
  padding: 0.35rem 0.6rem;
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(22, 163, 74, 0.08) 100%);
  border-left: 3px solid #16a34a;
  border-radius: 6px;
  color: #1e293b;
  font-weight: 600;
  font-size: 0.75rem;
  transition: all 0.3s ease;
}

.cultivos-table tbody tr:hover .cultivo-badge {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: white;
  border-left-color: #15803d;
  transform: scale(1.05);
}

.cultivo-cantidad {
  min-width: 70px;
}

.cantidad-badge {
  display: inline-block;
  padding: 0.3rem 0.6rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.12) 100%);
  color: #2563eb;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.75rem;
  border: 1px solid rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
}

.cultivos-table tbody tr:hover .cantidad-badge {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-color: #2563eb;
  transform: scale(1.05);
}

.cultivo-porcentaje {
  min-width: 60px;
  color: #1e293b;
  font-weight: 700;
  font-size: 0.85rem;
}

.cultivo-bar {
  min-width: 140px;
}

.bar-container {
  width: 100%;
  height: 22px;
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(22, 163, 74, 0.08) 100%);
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid rgba(22, 163, 74, 0.2);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
}

.bar-fill {
  height: 100%;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 6px;
  position: relative;
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.3);
}

.bar-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.3) 0%, transparent 100%);
  border-radius: 6px 6px 0 0;
}

.empty-table {
  text-align: center;
  padding: 1.5rem;
  color: #64748b;
  font-size: 0.85rem;
  font-weight: 500;
}

/* ========== SUMMARY SECTION ========== */
.summary-section {
  position: relative;
}

.summary-card {
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.12) 0%, rgba(21, 128, 61, 0.06) 100%);
  border: 1.5px solid rgba(22, 163, 74, 0.25);
  border-radius: 14px;
  padding: 0.85rem;
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;
}

.summary-card::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(22, 163, 74, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

@media (min-width: 1024px) {
  .summary-card {
    background: linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(21, 128, 61, 0.08) 100%);
    border: 1.5px solid rgba(22, 163, 74, 0.3);
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 4px 20px rgba(22, 163, 74, 0.15), 0 2px 8px rgba(22, 163, 74, 0.1);
  }
  
  .summary-title-icon {
    width: 24px;
    height: 24px;
  }
  
  .summary-title {
    font-size: 1.25rem;
  }
  
  .summary-content {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
  }
  
  .summary-item {
    gap: 0.75rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 14px;
    border: 1px solid rgba(22, 163, 74, 0.15);
    transition: all 0.3s ease;
  }
  
  .summary-item:hover {
    background: white;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(22, 163, 74, 0.15);
  }
  
  .summary-item-icon {
    width: 22px;
    height: 22px;
    margin-top: 0;
  }
  
  .summary-text {
    font-size: 1rem;
    line-height: 1.6;
  }
}

.summary-header {
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(22, 163, 74, 0.2);
  position: relative;
  z-index: 1;
}

.summary-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.summary-title-icon {
  width: 16px;
  height: 16px;
  color: #16a34a;
  stroke-width: 2;
  flex-shrink: 0;
}

.summary-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #1e3a2f;
  margin: 0;
}

.summary-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.5rem;
}

.summary-item {
  display: flex;
  align-items: flex-start;
  gap: 0.4rem;
}

.summary-item-icon {
  width: 14px;
  height: 14px;
  color: #16a34a;
  stroke-width: 2;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.summary-text {
  color: #374151;
  line-height: 1.4;
  font-size: 0.7rem;
}

.summary-text strong {
  color: #16a34a;
  font-weight: 700;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .header-estadisticas {
    padding: 0.7rem 0.8rem;
  }

  .header-title {
    font-size: 0.85rem;
  }

  .header-subtitle {
    font-size: 0.65rem;
  }

  .header-icon-small {
    width: 28px;
    height: 28px;
  }

  .icon-stat {
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

  .estadisticas-main {
    padding: 0.75rem 0.5rem;
  }

  .stats-grid {
    gap: 0.6rem;
  }

  .chart-section,
  .table-section {
    padding: 0.75rem;
  }
  
  .chart-container {
    height: 220px;
  }

  .cultivos-table th,
  .cultivos-table td {
    padding: 0.4rem 0.35rem;
  }
  
  .summary-content {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .header-estadisticas {
    padding: 0.6rem 0.75rem;
  }

  .header-title {
    font-size: 0.8rem;
  }

  .header-subtitle {
    font-size: 0.6rem;
  }
  
  .back-button {
    width: 34px;
    height: 34px;
  }

  .back-icon {
    width: 16px;
    height: 16px;
  }

  .stat-label {
    font-size: 0.55rem;
  }

  .stat-value {
    font-size: 1.1rem;
  }

  .stat-change {
    font-size: 0.5rem;
  }

  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }
  
  .stat-card {
    padding: 0.6rem 0.5rem;
  }
  
  .stat-icon-wrapper {
    width: 28px;
    height: 28px;
  }
  
  .stat-icon {
    width: 16px;
    height: 16px;
  }
  
  .chart-container {
    height: 180px;
  }
  
  .chart-title,
  .table-title {
    font-size: 0.85rem;
  }
  
  .summary-card {
    padding: 0.6rem;
  }
  
  .summary-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .header-estadisticas {
    padding: 0.5rem 0.6rem;
  }

  .header-wrapper {
    gap: 0.4rem;
    padding-right: 50px;
  }

  .back-button {
    width: 32px;
    height: 32px;
  }

  .back-icon {
    width: 14px;
    height: 14px;
  }

  .header-icon-small {
    width: 24px;
    height: 24px;
  }

  .icon-stat {
    width: 14px;
    height: 14px;
  }

  .header-title {
    font-size: 0.75rem;
  }

  .header-subtitle {
    font-size: 0.55rem;
  }

  .reload-button {
    width: 30px;
    height: 30px;
  }

  .reload-icon {
    width: 16px;
    height: 16px;
  }

  .estadisticas-main {
    padding: 0.5rem 0.4rem;
  }
  
  .estadisticas-content {
    gap: 0.6rem;
  }

  .stat-label {
    font-size: 0.5rem;
  }

  .stat-value {
    font-size: 1rem;
  }

  .stat-change {
    font-size: 0.45rem;
  }
  
  .badge-success,
  .badge-info {
    padding: 0.1rem 0.3rem;
    font-size: 0.45rem;
  }

  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.4rem;
  }

  .stat-card {
    padding: 0.5rem 0.4rem;
    border-radius: 10px;
  }

  .stat-icon-wrapper {
    width: 24px;
    height: 24px;
    border-radius: 6px;
  }

  .stat-icon {
    width: 14px;
    height: 14px;
  }

  .chart-section,
  .table-section {
    padding: 0.6rem;
    border-radius: 10px;
  }
  
  .chart-container {
    height: 160px;
  }
  
  .chart-title-icon,
  .table-title-icon {
    width: 14px;
    height: 14px;
  }
  
  .chart-title,
  .table-title {
    font-size: 0.8rem;
  }
  
  .chart-subtitle {
    font-size: 0.6rem;
  }

  .cultivos-table th {
    font-size: 0.55rem;
    padding: 0.35rem 0.25rem;
  }
  
  .cultivos-table td {
    padding: 0.3rem 0.25rem;
    font-size: 0.65rem;
  }
  
  .cultivo-badge {
    padding: 0.2rem 0.35rem;
    font-size: 0.6rem;
  }
  
  .cantidad-badge {
    padding: 0.15rem 0.3rem;
    font-size: 0.6rem;
  }
  
  .cultivo-bar {
    min-width: 80px;
  }
  
  .bar-container {
    height: 12px;
  }
  
  .summary-card {
    padding: 0.5rem;
    border-radius: 10px;
  }
  
  .summary-title {
    font-size: 0.75rem;
  }
  
  .summary-text {
    font-size: 0.6rem;
  }
}

/* Landscape móviles */
@media (max-height: 500px) and (orientation: landscape) {
  .estadisticas-main {
    padding: 0.5rem;
  }
  
  .estadisticas-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }
  
  .stats-section {
    grid-column: span 2;
  }
  
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.4rem;
  }
  
  .stat-card {
    padding: 0.4rem;
    flex-direction: row;
    gap: 0.4rem;
  }
  
  .stat-value {
    font-size: 1rem;
  }
  
  .chart-container {
    height: 140px;
  }
  
  .summary-section {
    grid-column: span 2;
  }
  
  .summary-content {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Pantallas muy pequeñas */
@media (max-width: 360px) {
  .header-left {
    gap: 0.3rem;
  }
  
  .header-icon-small {
    display: none;
  }
  
  .header-title {
    font-size: 0.7rem;
  }
  
  .header-subtitle {
    font-size: 0.5rem;
  }
  
  .stat-card {
    padding: 0.4rem 0.3rem;
  }
  
  .stat-label {
    font-size: 0.45rem;
  }
  
  .stat-value {
    font-size: 0.9rem;
  }
  
  .chart-container {
    height: 140px;
  }
}
</style>
