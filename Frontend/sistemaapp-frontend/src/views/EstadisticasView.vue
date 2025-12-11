<template>
  <div class="estadisticas-container">
    <!-- Menú hamburguesa global -->
    <HamburgerMenu />

    <!-- Fondo decorativo con blobs -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header con botón de regreso -->
    <header class="header-estadisticas">
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

    <!-- Pie de página -->
    <footer class="estadisticas-footer">
      <p>© 2025 <span class="footer-highlight">SistemaApp</span>. Reportes actualizados en tiempo real.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { getSecureApiUrl } from '../utils/api'
import HamburgerMenu from '../components/HamburgerMenu.vue'
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
import { BarChart3, Users, CheckCircle2, TrendingUp, List, BarChart2, Leaf, ArrowLeft } from 'lucide-vue-next'

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
  --color-primary: #10b981;
  --color-primary-dark: #059669;
  --color-bg: #0f172a;
  --color-bg-dark: #0a0f1e;
  --color-card: #1e293b;
  --color-input: #1a2332;
  --color-border: #334155;
  --color-text: #f1f5f9;
  --color-text-sec: #cbd5e1;
  --color-text-dim: #94a3b8;
}

.estadisticas-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
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
  opacity: 0.08;
  filter: blur(120px);
  mix-blend-mode: screen;
  border-radius: 50%;
}

.blob-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  top: -300px;
  left: -300px;
  animation: float 8s ease-in-out infinite;
}

.blob-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  top: 50%;
  right: -250px;
  animation: float 10s ease-in-out infinite reverse;
}

.blob-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #ec4899, #f59e0b);
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
  background: rgba(132, 204, 22, 0.12);
  border-bottom: 1px solid rgba(132, 204, 22, 0.1);
  backdrop-filter: blur(12px);
  padding: 1rem 1.2rem;
  box-shadow: 0 4px 20px rgba(132, 204, 22, 0.1);
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
  background: rgba(132, 204, 22, 0.1);
  border: 1.5px solid rgba(132, 204, 22, 0.4);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  color: #84cc16;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.back-button:hover {
  background: rgba(132, 204, 22, 0.2);
  transform: translateX(-4px);
  box-shadow: 0 4px 15px rgba(132, 204, 22, 0.3);
  border-color: rgba(132, 204, 22, 0.6);
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
  color: #84cc16;
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

.header-subtitle {
  font-size: 0.75rem;
  color: #cbd5e1;
  margin: 0;
  margin-top: 0.2rem;
}

/* ========== MAIN ========== */
.estadisticas-main {
  position: relative;
  z-index: 5;
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.estadisticas-content {
  display: grid;
  gap: 2rem;
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
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 1rem 0.9rem;
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  background: rgba(30, 41, 59, 0.7);
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(16, 185, 129, 0.15);
}

.stat-icon-wrapper {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
  stroke-width: 2;
}

.stat-card-1 .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(34, 197, 94, 0.15));
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.stat-card-2 .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.15));
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.stat-card-3 .stat-icon-wrapper {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.15));
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.7rem;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0;
}

.stat-change {
  font-size: 0.65rem;
  margin: 0;
}

.badge-success {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.65rem;
}

.badge-info {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.65rem;
}

.progress-mini {
  margin-top: 0.5rem;
}

.progress-bar-mini {
  height: 6px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill-mini {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #059669);
  transition: width 0.3s ease;
}

/* ========== CHART SECTION ========== */
.chart-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.chart-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.chart-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.chart-title-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
  stroke-width: 2;
  flex-shrink: 0;
}

.chart-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0 0 0.25rem 0;
}

.chart-subtitle {
  font-size: 0.75rem;
  color: #cbd5e1;
  margin: 0;
}

.chart-container {
  position: relative;
  height: 400px;
  margin-bottom: 1rem;
}

.chart-wrapper {
  width: 100%;
  height: 100%;
}

.empty-chart {
  text-align: center;
  padding: 3rem 2rem;
}

.empty-icon {
  width: 40px;
  height: 40px;
  color: #10b981;
  stroke-width: 2;
  margin: 0 auto 0.75rem;
}

.empty-text {
  font-size: 0.9rem;
  color: #f1f5f9;
  margin: 0 0 0.35rem 0;
}

.empty-subtext {
  font-size: 0.8rem;
  color: #cbd5e1;
  margin: 0;
}

/* ========== TABLE SECTION ========== */
.table-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.table-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.table-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.table-title-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
  stroke-width: 2;
  flex-shrink: 0;
}

.table-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.cultivos-table {
  width: 100%;
  border-collapse: collapse;
}

.cultivos-table thead {
  background: rgba(16, 185, 129, 0.15);
  border-bottom: 2px solid rgba(16, 185, 129, 0.3);
}

.cultivos-table th {
  padding: 1rem;
  text-align: left;
  color: #10b981;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.cultivos-table tbody tr {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  transition: background-color 0.2s ease;
}

.cultivos-table tbody tr:hover {
  background-color: rgba(16, 185, 129, 0.05);
}

.table-row td {
  padding: 1rem;
  color: #e2e8f0;
}

.cultivo-name {
  min-width: 150px;
}

.cultivo-badge {
  display: inline-block;
  padding: 0.4rem 0.75rem;
  background: rgba(16, 185, 129, 0.15);
  border-left: 3px solid #10b981;
  border-radius: 4px;
  color: #f1f5f9;
  font-weight: 500;
}

.cultivo-cantidad {
  min-width: 100px;
}

.cantidad-badge {
  display: inline-block;
  padding: 0.4rem 0.75rem;
  background: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
  border-radius: 6px;
  font-weight: 600;
}

.cultivo-porcentaje {
  min-width: 100px;
  color: #f1f5f9;
  font-weight: 600;
}

.cultivo-bar {
  min-width: 200px;
}

.bar-container {
  width: 100%;
  height: 24px;
  background: rgba(148, 163, 184, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 4px;
}

.empty-table {
  text-align: center;
  padding: 1.5rem;
  color: #cbd5e1;
  font-size: 0.85rem;
  font-weight: 500;
}

/* ========== SUMMARY SECTION ========== */
.summary-section {
  position: relative;
}

.summary-card {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.05));
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 16px;
  padding: 1.25rem;
  backdrop-filter: blur(10px);
}

.summary-header {
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(16, 185, 129, 0.2);
}

.summary-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.summary-title-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
  stroke-width: 2;
  flex-shrink: 0;
}

.summary-title {
  font-size: 1rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0;
}

.summary-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.75rem;
}

.summary-item {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
}

.summary-item-icon {
  width: 18px;
  height: 18px;
  color: #10b981;
  stroke-width: 2;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.summary-text {
  color: #e2e8f0;
  line-height: 1.5;
  font-size: 0.8rem;
}

.summary-text strong {
  color: #10b981;
  font-weight: 700;
}

/* ========== FOOTER ========== */
.estadisticas-footer {
  position: relative;
  z-index: 5;
  text-align: center;
  padding: 1.5rem;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(10px);
  font-size: 0.9rem;
  color: #cbd5e1;
}

.footer-highlight {
  color: #10b981;
  font-weight: 700;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .header-estadisticas {
    padding: 0.8rem 1rem;
  }

  .header-title {
    font-size: 0.85rem;
  }

  .header-subtitle {
    font-size: 0.6rem;
  }

  .header-icon-small {
    width: 28px;
    height: 28px;
  }

  .icon-stat {
    width: 18px;
    height: 18px;
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

  .estadisticas-main {
    padding: 1.5rem 0.5rem;
  }

  .stats-grid {
    gap: 0.8rem;
  }

  .stat-label {
    font-size: 0.65rem;
  }

  .stat-value {
    font-size: 1.3rem;
  }

  .stat-change {
    font-size: 0.6rem;
  }

  .chart-section {
    padding: 1.5rem;
  }

  .cultivos-table {
    font-size: 0.7rem;
  }

  .cultivos-table th,
  .cultivos-table td {
    padding: 0.5rem 0.4rem;
  }
}

@media (max-width: 640px) {
  .header-title {
    font-size: 0.8rem;
  }

  .header-subtitle {
    font-size: 0.7rem;
  }

  .stat-label {
    font-size: 0.6rem;
  }

  .stat-value {
    font-size: 1.2rem;
  }

  .stat-change {
    font-size: 0.55rem;
  }

  .stats-grid {
    gap: 0.7rem;
  }
}

@media (max-width: 480px) {
  .header-estadisticas {
    padding: 0.6rem 0.8rem;
  }

  .header-wrapper {
    gap: 0.5rem;
  }

  .back-button {
    width: 36px;
    height: 36px;
  }

  .back-icon {
    width: 18px;
    height: 18px;
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

  .reload-button {
    width: 34px;
    height: 34px;
  }

  .reload-icon {
    width: 18px;
    height: 18px;
  }

  .estadisticas-container {
    padding: 0;
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
    gap: 0.6rem;
  }

  .stat-card {
    padding: 0.8rem 0.7rem;
  }

  .stat-icon-wrapper {
    width: 30px;
    height: 30px;
  }

  .stat-icon {
    width: 18px;
    height: 18px;
  }

  .chart-section {
    padding: 1rem;
  }

  .cultivos-table {
    font-size: 0.65rem;
  }

  .cultivos-table th,
  .cultivos-table td {
    padding: 0.4rem 0.3rem;
  }
}
</style>
