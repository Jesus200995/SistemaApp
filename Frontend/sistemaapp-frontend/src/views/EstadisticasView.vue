<template>
  <div class="estadisticas-container">
    <!-- Fondo decorativo -->
    <div class="background-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <!-- Contenido principal -->
    <div class="estadisticas-content">
      <!-- Header -->
      <div
        v-motion
        :initial="{ opacity: 0, y: -50 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
        class="estadisticas-header"
      >
        <div class="header-title">
          <BarChart3 class="header-icon" />
          <h1>Estadísticas del Sistema</h1>
        </div>
        <button @click="reload" class="reload-button">
          <RotateCw class="reload-icon" />
          <span>Recargar</span>
        </button>
      </div>

      <!-- KPI Cards -->
      <div class="kpi-grid">
        <div
          v-motion
          :initial="{ opacity: 0, scale: 0.9, y: 20 }"
          :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 100, duration: 600 } }"
          class="kpi-card"
        >
          <div class="kpi-icon users-icon">
            <Users class="icon-svg" />
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Total de Usuarios</p>
            <h2 class="kpi-value">{{ totalUsuarios }}</h2>
          </div>
        </div>

        <div
          v-motion
          :initial="{ opacity: 0, scale: 0.9, y: 20 }"
          :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 200, duration: 600 } }"
          class="kpi-card"
        >
          <div class="kpi-icon admins-icon">
            <Shield class="icon-svg" />
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Administradores</p>
            <h2 class="kpi-value">{{ totalAdmins }}</h2>
          </div>
        </div>

        <div
          v-motion
          :initial="{ opacity: 0, scale: 0.9, y: 20 }"
          :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 300, duration: 600 } }"
          class="kpi-card"
        >
          <div class="kpi-icon regular-icon">
            <UserCheck class="icon-svg" />
          </div>
          <div class="kpi-content">
            <p class="kpi-label">Usuarios Regulares</p>
            <h2 class="kpi-value">{{ totalRegulares }}</h2>
          </div>
        </div>

        <div
          v-motion
          :initial="{ opacity: 0, scale: 0.9, y: 20 }"
          :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 400, duration: 600 } }"
          class="kpi-card"
        >
          <div class="kpi-icon percent-icon">
            <TrendingUp class="icon-svg" />
          </div>
          <div class="kpi-content">
            <p class="kpi-label">% Admins</p>
            <h2 class="kpi-value">{{ adminPercentage }}%</h2>
          </div>
        </div>
      </div>

      <!-- Gráficas -->
      <div class="charts-grid">
        <!-- Doughnut Chart -->
        <div
          v-motion
          :initial="{ opacity: 0, y: 50 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 500, duration: 700 } }"
          class="chart-card"
        >
          <h3 class="chart-title">
            <Users class="chart-icon" />
            Distribución por Rol
          </h3>
          <div class="chart-container">
            <DoughnutChart :data="rolesChartData" :options="chartOptions" />
          </div>
        </div>

        <!-- Line Chart -->
        <div
          v-motion
          :initial="{ opacity: 0, y: 50 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 600, duration: 700 } }"
          class="chart-card"
        >
          <h3 class="chart-title">
            <TrendingUp class="chart-icon" />
            Crecimiento Simulado (Últimos 7 meses)
          </h3>
          <div class="chart-container">
            <LineChart :data="usersChartData" :options="chartOptions" />
          </div>
        </div>
      </div>

      <!-- Tabla de Resumen -->
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :enter="{ opacity: 1, transition: { delay: 700, duration: 600 } }"
        class="summary-card"
      >
        <h3 class="summary-title">
          <BarChart3 class="summary-icon" />
          Resumen General
        </h3>
        <div class="summary-content">
          <div class="summary-item">
            <span class="summary-label">Total de Usuarios:</span>
            <span class="summary-value">{{ totalUsuarios }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Admins:</span>
            <span class="summary-value admin">{{ totalAdmins }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Usuarios Regulares:</span>
            <span class="summary-value regular">{{ totalRegulares }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Ratio Admin/Total:</span>
            <span class="summary-value ratio">{{ adminPercentage }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { BarChart3, Users, TrendingUp, RotateCw, Shield, UserCheck } from 'lucide-vue-next'
import { Doughnut, Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js'
import { useAuthStore } from '../stores/auth'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
)

// Componentes para gráficas
const DoughnutChart = {
  extends: Doughnut,
  props: ['data', 'options'],
}
const LineChart = {
  extends: Line,
  props: ['data', 'options'],
}

const auth = useAuthStore()

const totalUsuarios = ref(0)
const totalAdmins = ref(0)
const totalRegulares = ref(0)

const adminPercentage = computed(() => {
  if (totalUsuarios.value === 0) return 0
  return Math.round((totalAdmins.value / totalUsuarios.value) * 100)
})

const rolesChartData = ref({
  labels: ['Administradores', 'Usuarios Regulares'],
  datasets: [
    {
      label: 'Cantidad',
      backgroundColor: ['#ef4444', '#10b981'],
      borderColor: ['#dc2626', '#059669'],
      borderWidth: 2,
      data: [0, 0],
    },
  ],
})

const usersChartData = ref({
  labels: ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4', 'Semana 5', 'Semana 6', 'Semana 7'],
  datasets: [
    {
      label: 'Nuevos Usuarios',
      borderColor: '#10b981',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      borderWidth: 3,
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#10b981',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 5,
      pointHoverRadius: 7,
      data: [],
    },
  ],
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 15,
        font: { size: 12, weight: 'bold' },
        color: '#64748b',
      },
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      titleFont: { size: 14, weight: 'bold' },
      bodyFont: { size: 13 },
      cornerRadius: 8,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(148, 163, 184, 0.1)',
        drawBorder: false,
      },
      ticks: {
        color: '#64748b',
        font: { size: 11 },
      },
    },
    x: {
      grid: {
        display: false,
        drawBorder: false,
      },
      ticks: {
        color: '#64748b',
        font: { size: 11 },
      },
    },
  },
}

const reload = async () => {
  try {
    const { data } = await axios.get(`${import.meta.env.VITE_API_URL}/auth/users`, {
      params: { page: 1, limit: 100 },
      headers: { Authorization: `Bearer ${auth.token}` },
    })

    totalUsuarios.value = data.total
    totalAdmins.value = data.users.filter(u => u.rol === 'admin').length
    totalRegulares.value = data.users.filter(u => u.rol !== 'admin').length

    rolesChartData.value.datasets[0].data = [totalAdmins.value, totalRegulares.value]

    // Datos simulados para crecimiento
    usersChartData.value.datasets[0].data = [5, 8, 6, 10, 7, 9, 12].map(() =>
      Math.floor(Math.random() * 15 + 5)
    )
  } catch (err) {
    console.error('Error al cargar estadísticas:', err)
  }
}

onMounted(() => {
  reload()
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ========== CONTAINER ========== */
.estadisticas-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 2rem 0;
}

/* ========== BACKGROUND BLOBS ========== */
.background-decoration {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.blob {
  position: absolute;
  opacity: 0.1;
  filter: blur(100px);
  mix-blend-mode: screen;
}

.blob-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #06b6d4, #3b82f6);
  border-radius: 50%;
  top: 0;
  left: -200px;
  animation: blob-animate 8s ease-in-out infinite;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  border-radius: 50%;
  bottom: -100px;
  right: -100px;
  animation: blob-animate 10s ease-in-out infinite reverse;
}

@keyframes blob-animate {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, 50px); }
}

/* ========== CONTENT ========== */
.estadisticas-content {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* ========== HEADER ========== */
.estadisticas-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 32px;
  height: 32px;
  color: #10b981;
}

.estadisticas-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #e2e8f0;
}

.reload-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.75rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.reload-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4);
}

.reload-button:active {
  transform: translateY(0);
}

.reload-icon {
  width: 18px;
  height: 18px;
}

/* ========== KPI GRID ========== */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.kpi-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  transition: all 0.3s ease;
}

.kpi-card:hover {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border-color: rgba(148, 163, 184, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

.kpi-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.users-icon {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.admins-icon {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.regular-icon {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(59, 130, 246, 0.1));
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.percent-icon {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(168, 85, 247, 0.1));
  border: 1px solid rgba(168, 85, 247, 0.3);
}

.icon-svg {
  width: 28px;
  height: 28px;
  color: #10b981;
}

.admins-icon .icon-svg {
  color: #ef4444;
}

.regular-icon .icon-svg {
  color: #3b82f6;
}

.percent-icon .icon-svg {
  color: #a855f7;
}

.kpi-content {
  flex: 1;
}

.kpi-label {
  font-size: 0.875rem;
  color: #94a3b8;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.kpi-value {
  font-size: 2rem;
  font-weight: 700;
  color: #e2e8f0;
}

/* ========== CHARTS GRID ========== */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.chart-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 1.5rem;
}

.chart-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
}

.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}

/* ========== SUMMARY CARD ========== */
.summary-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.summary-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.summary-icon {
  width: 28px;
  height: 28px;
  color: #10b981;
}

.summary-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.summary-item:hover {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.4);
}

.summary-label {
  font-size: 0.95rem;
  color: #94a3b8;
  font-weight: 500;
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #10b981;
}

.summary-value.admin {
  color: #ef4444;
}

.summary-value.regular {
  color: #3b82f6;
}

.summary-value.ratio {
  color: #a855f7;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .estadisticas-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .header-title {
    width: 100%;
    justify-content: center;
  }

  .estadisticas-header h1 {
    font-size: 1.5rem;
  }

  .reload-button {
    width: 100%;
    justify-content: center;
  }

  .kpi-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .kpi-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .kpi-label {
    font-size: 0.8rem;
  }

  .kpi-value {
    font-size: 1.75rem;
  }

  .charts-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .summary-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .estadisticas-container {
    padding: 1rem 0;
  }

  .estadisticas-content {
    padding: 0 1rem;
  }

  .estadisticas-header {
    padding: 1rem;
    gap: 0.75rem;
  }

  .header-icon {
    width: 24px;
    height: 24px;
  }

  .estadisticas-header h1 {
    font-size: 1.25rem;
  }

  .kpi-grid {
    grid-template-columns: 1fr;
  }

  .kpi-card {
    padding: 1rem;
  }

  .kpi-icon {
    width: 50px;
    height: 50px;
  }

  .icon-svg {
    width: 24px;
    height: 24px;
  }

  .kpi-value {
    font-size: 1.5rem;
  }

  .chart-card {
    padding: 1rem;
  }

  .summary-card {
    padding: 1rem;
  }

  .summary-title {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
  }
}

/* ========== CHART CANVAS ========== */
canvas {
  height: 300px !important;
}
</style>
