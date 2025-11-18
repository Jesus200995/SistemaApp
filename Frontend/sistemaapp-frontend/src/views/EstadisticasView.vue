<template>
  <div class="estadisticas-container">
    <!-- Fondo decorativo con blobs -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header -->
    <header class="header-estadisticas">
      <div class="header-wrapper">
        <div class="header-left">
          <div class="icon-box">
            <BarChart3 class="header-icon" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Reportes y Estadísticas</h1>
            <p class="header-subtitle">Análisis en tiempo real del sistema</p>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="estadisticas-main">
      <div class="estadisticas-content">
        <!-- Estadísticas Principales -->
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
          class="stats-section"
        >
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
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200, duration: 600 } }"
          class="chart-section"
        >
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
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 400, duration: 600 } }"
          class="table-section"
        >
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
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 600, duration: 600 } }"
          class="summary-section"
        >
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
    <footer
      v-motion
      :initial="{ opacity: 0 }"
      :enter="{ opacity: 1, transition: { delay: 800, duration: 600 } }"
      class="estadisticas-footer"
    >
      <p>© 2025 <span class="footer-highlight">SistemaApp</span>. Reportes actualizados en tiempo real.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
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
import { BarChart3, Users, CheckCircle2, TrendingUp, List, BarChart2, Leaf } from 'lucide-vue-next'

// Registrar componentes de Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const auth = useAuthStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

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
  background: linear-gradient(135deg, var(--color-bg) 0%, var(--color-bg-dark) 100%);
  position: relative;
  overflow: hidden;
}

/* ========== BLOBS ========== */
.background-blobs {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 0;
  pointer-events: none;
}

.blob {
  position: absolute;
  filter: blur(40px);
  opacity: 0.08;
  border-radius: 50%;
}

.blob-1 {
  width: 400px;
  height: 400px;
  background: var(--color-primary);
  top: -50%;
  left: -10%;
  animation: float 20s infinite ease-in-out;
}

.blob-2 {
  width: 300px;
  height: 300px;
  background: #3b82f6;
  top: 50%;
  right: -5%;
  animation: float 15s infinite ease-in-out reverse;
}

.blob-3 {
  width: 350px;
  height: 350px;
  background: #8b5cf6;
  bottom: -10%;
  left: 50%;
  animation: float 25s infinite ease-in-out;
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
  padding: 2rem 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  backdrop-filter: blur(10px);
}

.header-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.icon-box {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.2);
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

.header-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

.header-subtitle {
  color: var(--color-text-dim);
  margin: 0.5rem 0 0 0;
  font-size: 0.95rem;
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
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  background: rgba(30, 41, 59, 0.7);
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(16, 185, 129, 0.15);
}

.stat-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon {
  width: 32px;
  height: 32px;
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
  font-size: 0.85rem;
  color: var(--color-text-dim);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 0.5rem 0;
}

.stat-value {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 0.5rem 0;
}

.stat-change {
  font-size: 0.8rem;
  margin: 0;
}

.badge-success {
  display: inline-block;
  padding: 0.3rem 0.75rem;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border-radius: 20px;
  font-weight: 600;
}

.badge-info {
  display: inline-block;
  padding: 0.3rem 0.75rem;
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border-radius: 20px;
  font-weight: 600;
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
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-dark));
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
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 0.25rem 0;
}

.chart-subtitle {
  font-size: 0.85rem;
  color: var(--color-text-dim);
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
  width: 48px;
  height: 48px;
  color: #10b981;
  stroke-width: 2;
  margin: 0 auto 1rem;
}

.empty-text {
  font-size: 1.1rem;
  color: var(--color-text);
  margin: 0 0 0.5rem 0;
}

.empty-subtext {
  color: var(--color-text-dim);
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
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-text);
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
  background: rgba(16, 185, 129, 0.1);
  border-bottom: 2px solid rgba(16, 185, 129, 0.2);
}

.cultivos-table th {
  padding: 1rem;
  text-align: left;
  color: var(--color-text-sec);
  font-weight: 600;
  font-size: 0.9rem;
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
  color: var(--color-text-dim);
}

.cultivo-name {
  min-width: 150px;
}

.cultivo-badge {
  display: inline-block;
  padding: 0.4rem 0.75rem;
  background: rgba(16, 185, 129, 0.1);
  border-left: 3px solid var(--color-primary);
  border-radius: 4px;
  color: var(--color-text);
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
  color: var(--color-text);
  font-weight: 500;
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
  padding: 2rem;
  color: var(--color-text-dim);
}

/* ========== SUMMARY SECTION ========== */
.summary-section {
  position: relative;
}

.summary-card {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.05));
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.summary-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
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
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

.summary-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.summary-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.summary-item-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
  stroke-width: 2;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.summary-text {
  color: var(--color-text-dim);
  line-height: 1.6;
  font-size: 0.95rem;
}

.summary-text strong {
  color: var(--color-primary);
  font-weight: 600;
}

/* ========== FOOTER ========== */
.estadisticas-footer {
  position: relative;
  z-index: 5;
  text-align: center;
  padding: 1.5rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(10px);
  font-size: 0.85rem;
  color: var(--color-text-dim);
}

.footer-highlight {
  color: var(--color-primary);
  font-weight: 600;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .estadisticas-main {
    padding: 1rem 0.5rem;
  }

  .header-title {
    font-size: 1.5rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
  }

  .stat-icon-wrapper {
    width: 56px;
    height: 56px;
  }

  .icon-emoji {
    font-size: 28px;
  }

  .stat-icon {
    font-size: 2rem;
  }

  .chart-container {
    height: 300px;
  }

  .cultivos-table {
    font-size: 0.85rem;
  }

  .cultivos-table th,
  .cultivos-table td {
    padding: 0.75rem 0.5rem;
  }

  .summary-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .estadisticas-container {
    padding: 0;
  }

  .header-estadisticas {
    padding: 1rem;
  }

  .header-left {
    gap: 1rem;
  }

  .icon-box {
    width: 48px;
    height: 48px;
  }

  .icon-emoji {
    font-size: 24px;
  }

  .header-title {
    font-size: 1.25rem;
  }

  .stat-value {
    font-size: 1.8rem;
  }

  .chart-section,
  .table-section,
  .summary-card {
    padding: 1.25rem 1rem;
  }

  .chart-title,
  .table-title,
  .summary-title {
    font-size: 1.1rem;
  }

  .chart-container {
    height: 250px;
  }
}
</style>
