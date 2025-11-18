<template>
  <div class="seguimiento-container">
    <!-- Fondo decorativo con blobs -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header con botón de regreso -->
    <header class="header-seguimiento">
      <div class="header-wrapper">
        <div class="header-left">
          <router-link to="/dashboard" class="back-button" title="Volver al Dashboard">
            <ArrowLeft class="back-icon" />
          </router-link>
          <div class="icon-box">
            <Microscope class="header-icon" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Seguimiento de Campo</h1>
            <p class="header-subtitle">Registra visitas y progreso de tus sembradores</p>
          </div>
        </div>
      </div>
    </header>

    <!-- Tabs -->
    <div class="tabs-wrapper">
      <div class="tabs-container">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="activeTab = tab"
          :class="['tab', { active: activeTab === tab }]"
        >
          {{ tab }}
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <main class="seguimiento-main">
      <div class="seguimiento-content">
        <!-- Tab 1: Crear Seguimiento -->
        <section v-if="activeTab === 'Crear Seguimiento'" class="form-section">
          <div class="form-header">
            <h2 class="form-title">Registrar Seguimiento</h2>
            <p class="form-subtitle">Completa los detalles de tu visita</p>
          </div>

          <form @submit.prevent="crearSeguimiento" class="seguimiento-form">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Sembrador *</label>
                <div class="input-wrapper">
                  <select v-model="formulario.sembrador_id" required class="form-input form-select">
                    <option value="">-- Selecciona --</option>
                    <option v-for="sem in sembradores" :key="sem.id" :value="sem.id">
                      {{ sem.nombre }} - {{ sem.comunidad }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Fecha *</label>
                <div class="input-wrapper">
                  <input v-model="formulario.fecha_visita" type="date" required class="form-input" />
                </div>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Estado</label>
                <div class="input-wrapper">
                  <select v-model="formulario.estado_cultivo" class="form-input form-select">
                    <option value="">Selecciona</option>
                    <option value="Germinando">Germinando</option>
                    <option value="Vegetativo">Vegetativo</option>
                    <option value="Floración">Floración</option>
                    <option value="Fructificación">Fructificación</option>
                    <option value="Cosecha">Cosecha</option>
                    <option value="Plagas">Plagas</option>
                    <option value="Enfermedad">Enfermedad</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Avance %</label>
                <div class="input-wrapper">
                  <input v-model.number="formulario.avance_porcentaje" type="number" min="0" max="100" class="form-input" />
                </div>
              </div>
            </div>

            <div class="form-group full-width">
              <label class="form-label">Observaciones</label>
              <textarea v-model="formulario.observaciones" placeholder="Describe..." class="form-input textarea-input" rows="3"></textarea>
            </div>

            <div class="form-group full-width">
              <label class="form-label">URL Foto</label>
              <input v-model="formulario.foto_url" type="url" placeholder="https://..." class="form-input" />
            </div>

            <button type="submit" :disabled="cargando" class="btn-submit">
              {{ cargando ? '⏳ Guardando...' : '✅ Guardar' }}
            </button>
          </form>
        </section>

        <!-- Tab 2: Mis Seguimientos -->
        <section v-if="activeTab === 'Mis Seguimientos'" class="historial-section">
          <div class="section-header">
            <h2 class="section-title">Historial</h2>
            <span class="badge-count">{{ seguimientos.length }}</span>
          </div>

          <div v-if="seguimientos.length === 0" class="empty-state">
            <p>Sin seguimientos</p>
          </div>

          <div v-else class="table-wrapper">
            <table class="seguimiento-table">
              <thead>
                <tr>
                  <th>Sembrador</th>
                  <th>Fecha</th>
                  <th>Estado</th>
                  <th>% Avance</th>
                  <th>Observaciones</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="seg in seguimientos" :key="seg.id" class="table-row">
                  <td><strong>{{ seg.sembrador_nombre }}</strong></td>
                  <td>{{ formatearFecha(seg.fecha_visita) }}</td>
                  <td>
                    <span class="estado-badge" :class="'estado-' + seg.estado_cultivo">
                      {{ seg.estado_cultivo }}
                    </span>
                  </td>
                  <td>
                    <div class="progress-cell">
                      <div class="progress-bar-small">
                        <div class="progress-fill-small" :style="{ width: seg.avance_porcentaje + '%' }"></div>
                      </div>
                      <span>{{ seg.avance_porcentaje }}%</span>
                    </div>
                  </td>
                  <td class="text-ellipsis">{{ seg.observaciones?.substring(0, 30) || 'N/A' }}</td>
                  <td>
                    <button @click="eliminarSeguimiento(seg.id)" class="btn-action btn-delete">🗑️</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Tab 3: Reportes -->
        <section v-if="activeTab === 'Reportes'" class="reportes-section">
          <div class="reportes-grid">
            <div class="reporte-card">
              <h3>👥 Por Técnico</h3>
              <table v-if="reporteTecnico.length > 0" class="mini-table">
                <tr v-for="tech in reporteTecnico" :key="tech.tecnico_id">
                  <td>{{ tech.tecnico_nombre }}</td>
                  <td class="text-right">{{ tech.total_seguimientos }}</td>
                </tr>
              </table>
              <div v-else class="empty-state">Sin datos</div>
            </div>

            <div class="reporte-card">
              <h3>🌾 Por Cultivo</h3>
              <table v-if="reporteCultivo.length > 0" class="mini-table">
                <tr v-for="cul in reporteCultivo" :key="cul.cultivo">
                  <td>{{ cul.cultivo }}</td>
                  <td class="text-right">{{ cul.total_seguimientos }}</td>
                </tr>
              </table>
              <div v-else class="empty-state">Sin datos</div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'
import { ArrowLeft, Microscope, Plus, Trash2, Calendar, MapPin, AlertCircle } from 'lucide-vue-next'

const auth = useAuthStore()
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Interfaces
interface Sembrador {
  id: number
  nombre: string
  comunidad: string
}

interface Seguimiento {
  id: number
  sembrador_id: number
  sembrador_nombre: string
  fecha_visita: string
  estado_cultivo: string
  avance_porcentaje: number
  observaciones: string
  foto_url?: string
  creado_en: string
  comunidad: string
  cultivo_principal: string
  tecnico_nombre: string
}

interface ReporteTecnico {
  tecnico_id: number
  tecnico_nombre: string
  total_seguimientos: number
  avance_promedio: number
  rol: string
}

interface ReporteCultivo {
  cultivo: string
  total_seguimientos: number
  total_sembradores: number
  avance_promedio: number
}

// Estado
const activeTab = ref('Crear Seguimiento')
const tabs = ['Crear Seguimiento', 'Mis Seguimientos', 'Reportes']
const cargando = ref(false)

// Datos
const sembradores: Ref<Sembrador[]> = ref([])
const seguimientos: Ref<Seguimiento[]> = ref([])
const reporteTecnico: Ref<ReporteTecnico[]> = ref([])
const reporteCultivo: Ref<ReporteCultivo[]> = ref([])

// Formulario
const formulario = ref({
  sembrador_id: null as number | null,
  fecha_visita: new Date().toISOString().split('T')[0],
  estado_cultivo: '',
  observaciones: '',
  avance_porcentaje: 0,
  foto_url: ''
})

// Funciones
const obtenerSembradores = async () => {
  try {
    const response = await axios.get(`${API_URL}/sembradores/`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    sembradores.value = response.data.items || response.data || []
  } catch (error) {
    console.error('Error cargando sembradores:', error)
  }
}

const obtenerSeguimientos = async () => {
  try {
    const response = await axios.get(`${API_URL}/seguimientos/`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    seguimientos.value = response.data.items || response.data || []
  } catch (error) {
    console.error('Error cargando seguimientos:', error)
  }
}

const crearSeguimiento = async () => {
  if (!formulario.value.sembrador_id) {
    alert('Por favor selecciona un sembrador')
    return
  }

  cargando.value = true
  try {
    await axios.post(`${API_URL}/seguimientos/crear`, formulario.value, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    
    alert('✅ Seguimiento creado exitosamente')
    formulario.value = {
      sembrador_id: null,
      fecha_visita: new Date().toISOString().split('T')[0],
      estado_cultivo: '',
      observaciones: '',
      avance_porcentaje: 0,
      foto_url: ''
    }
    
    await obtenerSeguimientos()
    activeTab.value = 'Mis Seguimientos'
  } catch (error) {
    console.error('Error:', error)
    alert('❌ Error al crear seguimiento')
  } finally {
    cargando.value = false
  }
}

const eliminarSeguimiento = async (id: number) => {
  if (!confirm('¿Estás seguro de que deseas eliminar este seguimiento?')) return

  try {
    await axios.delete(`${API_URL}/seguimientos/${id}`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    
    alert('✅ Seguimiento eliminado')
    await obtenerSeguimientos()
  } catch (error) {
    console.error('Error:', error)
    alert('❌ Error al eliminar')
  }
}

const cargarReportes = async () => {
  try {
    const respTecnico = await axios.get(`${API_URL}/seguimientos/reportes/por-tecnico`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    reporteTecnico.value = respTecnico.data.items || []

    const respCultivo = await axios.get(`${API_URL}/seguimientos/reportes/por-cultivo`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    reporteCultivo.value = respCultivo.data.items || []
  } catch (error) {
    console.error('Error cargando reportes:', error)
  }
}

const formatearFecha = (fecha: string): string => {
  if (!fecha) return 'N/A'
  const date = new Date(fecha)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  obtenerSembradores()
  obtenerSeguimientos()
  cargarReportes()
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

.seguimiento-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* Blobs */
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

/* Header */
.header-seguimiento {
  position: relative;
  z-index: 10;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  backdrop-filter: blur(10px);
  padding: 1.5rem 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
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

/* ========== BACK BUTTON ========== */
.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  color: var(--color-primary);
}

.back-button:hover {
  background: rgba(16, 185, 129, 0.2);
  transform: translateX(-4px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
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
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.header-subtitle {
  color: #94a3b8;
  margin: 0.5rem 0 0 0;
  font-size: 0.95rem;
}

/* Main */
.seguimiento-main {
  position: relative;
  z-index: 5;
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.seguimiento-content {
  display: grid;
  gap: 2rem;
}

/* Tabs */
.tabs-wrapper {
  position: relative;
  z-index: 9;
  background: rgba(30, 41, 59, 0.3);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.tabs-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 0;
  padding: 0 1rem;
}

.tab {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: #cbd5e1;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.tab:hover {
  color: #e2e8f0;
  background: rgba(16, 185, 129, 0.05);
}

.tab.active {
  color: #10b981;
  border-bottom-color: #10b981;
}

/* Form Section */
.form-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.form-header {
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0 0 0.5rem 0;
}

.form-subtitle {
  color: #cbd5e1;
  margin: 0;
}

.seguimiento-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.3);
  border-radius: 8px;
  color: #f1f5f9;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-input:hover {
  border-color: rgba(148, 163, 184, 0.3);
}

.form-input:focus {
  outline: none;
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.7);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2310b981' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  padding-right: 2.5rem;
}

.form-select option {
  background: rgba(30, 41, 59, 0.9);
  color: #f1f5f9;
}

.textarea-input {
  resize: vertical;
  min-height: 100px;
}

.btn-submit {
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Historial */
.historial-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

.badge-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  border-radius: 50%;
  font-size: 0.85rem;
  font-weight: 700;
}

/* Table */
.table-wrapper {
  overflow-x: auto;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.seguimiento-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.seguimiento-table thead {
  background: rgba(16, 185, 129, 0.1);
  border-bottom: 2px solid rgba(16, 185, 129, 0.2);
}

.seguimiento-table th {
  padding: 1rem;
  text-align: left;
  color: var(--color-text-sec);
  font-weight: 600;
}

.seguimiento-table tbody tr {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  transition: background-color 0.2s ease;
}

.seguimiento-table tbody tr:hover {
  background-color: rgba(16, 185, 129, 0.05);
}

.table-row td {
  padding: 1rem;
  color: var(--color-text-dim);
}

.estado-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.estado-Germinando { background: rgba(34, 197, 94, 0.1); color: #86efac; }
.estado-Vegetativo { background: rgba(34, 197, 94, 0.15); color: #10b981; }
.estado-Floración { background: rgba(245, 158, 11, 0.1); color: #fbbf24; }
.estado-Fructificación { background: rgba(239, 68, 68, 0.1); color: #fca5a5; }
.estado-Cosecha { background: rgba(59, 130, 246, 0.1); color: #93c5fd; }
.estado-Plagas { background: rgba(239, 68, 68, 0.15); color: #fca5a5; }
.estado-Enfermedad { background: rgba(168, 85, 247, 0.1); color: #d8b4fe; }

.progress-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.progress-bar-small {
  flex: 1;
  height: 6px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 3px;
  overflow: hidden;
  min-width: 40px;
}

.progress-fill-small {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-dark));
  transition: width 0.3s ease;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: transparent;
}

.btn-delete {
  color: #f87171;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.1);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-dim);
}

/* Reportes */
.reportes-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.reportes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.reporte-card {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
}

.reporte-card h3 {
  color: var(--color-text);
  margin-top: 0;
  margin-bottom: 1rem;
}

.mini-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.mini-table tr {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.mini-table tr:last-child {
  border-bottom: none;
}

.mini-table td {
  padding: 0.75rem 0;
  color: var(--color-text-dim);
}

.text-right {
  text-align: right;
  color: var(--color-primary);
  font-weight: 600;
}

@media (max-width: 768px) {
  .seguimiento-container {
    padding: 0;
  }

  .back-button {
    width: 40px;
    height: 40px;
  }

  .back-icon {
    width: 18px;
    height: 18px;
  }

  .header-seguimiento {
    padding: 1.5rem 1rem;
  }

  .header-title {
    font-size: 1.5rem;
  }

  .seguimiento-main {
    padding: 1rem 0.5rem;
  }

  .form-section,
  .historial-section,
  .reportes-section {
    padding: 1.5rem 1rem;
    border-radius: 12px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .tabs-container {
    flex-wrap: wrap;
  }

  .table-wrapper {
    overflow-x: auto;
  }

  .seguimiento-table {
    font-size: 0.8rem;
  }

  .seguimiento-table th,
  .seguimiento-table td {
    padding: 0.75rem 0.5rem;
  }

  .reportes-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .back-button {
    width: 36px;
    height: 36px;
  }

  .back-icon {
    width: 16px;
    height: 16px;
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

  .form-title {
    font-size: 1.1rem;
  }

  .section-title {
    font-size: 1.1rem;
  }

  .tabs-container {
    overflow-x: auto;
  }
}
</style>
