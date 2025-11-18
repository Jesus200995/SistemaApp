<template>
  <div class="seguimiento-container">
    <!-- Header -->
    <div class="header">
      <h1>📊 Seguimiento de Campo</h1>
      <p class="subtitle">Registra visitas, observaciones y progreso de tus sembradores</p>
    </div>

    <!-- Navigation Tabs -->
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

    <!-- Tab: Nuevo Seguimiento -->
    <div v-if="activeTab === 'Crear Seguimiento'" class="tab-content">
      <form @submit.prevent="crearSeguimiento" class="form-container">
        <div class="form-grid">
          <!-- Seleccionar Sembrador -->
          <div class="form-group">
            <label>🌱 Sembrador *</label>
            <select v-model="formulario.sembrador_id" required class="input-select">
              <option value="">-- Selecciona un sembrador --</option>
              <option
                v-for="sem in sembradores"
                :key="sem.id"
                :value="sem.id"
              >
                {{ sem.nombre }} ({{ sem.comunidad }})
              </option>
            </select>
          </div>

          <!-- Fecha de Visita -->
          <div class="form-group">
            <label>📅 Fecha de Visita *</label>
            <input
              v-model="formulario.fecha_visita"
              type="datetime-local"
              required
              class="input-text"
            />
          </div>

          <!-- Estado del Cultivo -->
          <div class="form-group">
            <label>🌿 Estado del Cultivo</label>
            <select v-model="formulario.estado_cultivo" class="input-select">
              <option value="">-- Selecciona estado --</option>
              <option value="Germinando">🌱 Germinando</option>
              <option value="Vegetativo">🌿 Vegetativo</option>
              <option value="Floración">🌻 Floración</option>
              <option value="Fructificación">🍅 Fructificación</option>
              <option value="Cosecha">✂️ Cosecha</option>
              <option value="Plagas">🐛 Plagas</option>
              <option value="Enfermedad">😷 Enfermedad</option>
            </select>
          </div>

          <!-- Avance en Porcentaje -->
          <div class="form-group">
            <label>📈 Avance de Progreso (%)</label>
            <div class="progress-input">
              <input
                v-model.number="formulario.avance_porcentaje"
                type="range"
                min="0"
                max="100"
                step="5"
                class="input-range"
              />
              <span class="percentage">{{ formulario.avance_porcentaje }}%</span>
            </div>
          </div>

          <!-- Observaciones -->
          <div class="form-group full-width">
            <label>📝 Observaciones</label>
            <textarea
              v-model="formulario.observaciones"
              placeholder="Describe lo que observaste en el campo..."
              rows="4"
              class="input-textarea"
            ></textarea>
          </div>

          <!-- URL de Foto (opcional) -->
          <div class="form-group full-width">
            <label>📸 URL de Foto (opcional)</label>
            <input
              v-model="formulario.foto_url"
              type="url"
              placeholder="https://ejemplo.com/foto.jpg"
              class="input-text"
            />
          </div>
        </div>

        <!-- Botones -->
        <div class="form-actions">
          <button type="submit" :disabled="cargando" class="btn btn-primary">
            <span v-if="cargando">⏳ Guardando...</span>
            <span v-else>✅ Guardar Seguimiento</span>
          </button>
          <button type="reset" class="btn btn-secondary">
            🔄 Limpiar Formulario
          </button>
        </div>
      </form>
    </div>

    <!-- Tab: Mis Seguimientos -->
    <div v-if="activeTab === 'Mis Seguimientos'" class="tab-content">
      <div class="seguimientos-grid">
        <div v-if="seguimientos.length === 0" class="empty-state">
          <p>No hay seguimientos registrados aún</p>
          <p class="subtitle">Crea el primero haciendo clic en "Crear Seguimiento"</p>
        </div>

        <div
          v-for="seg in seguimientos"
          :key="seg.id"
          class="seguimiento-card"
        >
          <!-- Encabezado Tarjeta -->
          <div class="card-header">
            <h3>{{ seg.sembrador_nombre }}</h3>
            <span class="badge" :class="'badge-' + estadoColor(seg.estado_cultivo)">
              {{ seg.estado_cultivo }}
            </span>
          </div>

          <!-- Cuerpo Tarjeta -->
          <div class="card-body">
            <div class="info-row">
              <span class="label">📍 Comunidad:</span>
              <span class="value">{{ seg.comunidad }}</span>
            </div>
            <div class="info-row">
              <span class="label">🌾 Cultivo:</span>
              <span class="value">{{ seg.cultivo_principal }}</span>
            </div>
            <div class="info-row">
              <span class="label">📅 Fecha de Visita:</span>
              <span class="value">{{ formatearFecha(seg.fecha_visita) }}</span>
            </div>
            <div class="info-row">
              <span class="label">👤 Técnico:</span>
              <span class="value">{{ seg.tecnico_nombre }}</span>
            </div>

            <!-- Progreso -->
            <div class="progress-section">
              <div class="progress-label">
                <span>Progreso</span>
                <span class="progress-value">{{ seg.avance_porcentaje }}%</span>
              </div>
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{ width: seg.avance_porcentaje + '%' }"
                ></div>
              </div>
            </div>

            <!-- Observaciones -->
            <div v-if="seg.observaciones" class="observations">
              <p><strong>📝 Observaciones:</strong></p>
              <p>{{ seg.observaciones }}</p>
            </div>

            <!-- Foto -->
            <div v-if="seg.foto_url" class="foto-section">
              <img :src="seg.foto_url" :alt="seg.sembrador_nombre" />
            </div>
          </div>

          <!-- Pie Tarjeta -->
          <div class="card-footer">
            <small>Creado: {{ formatearFecha(seg.creado_en) }}</small>
            <div class="card-actions">
              <button @click="editarSeguimiento(seg)" class="btn-small btn-edit">✏️</button>
              <button @click="eliminarSeguimiento(seg.id)" class="btn-small btn-delete">🗑️</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab: Reportes -->
    <div v-if="activeTab === 'Reportes'" class="tab-content">
      <div class="reportes-container">
        <!-- Reporte por Técnico -->
        <div class="reporte-section">
          <h2>👥 Reporte por Técnico</h2>
          <div v-if="reporteTecnico.length === 0" class="empty-state">
            <p>No hay datos para mostrar</p>
          </div>
          <table v-else class="reporte-table">
            <thead>
              <tr>
                <th>Técnico</th>
                <th>Rol</th>
                <th>Seguimientos</th>
                <th>Avance Promedio</th>
                <th>Último Seguimiento</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="tech in reporteTecnico" :key="tech.tecnico_id">
                <td>{{ tech.tecnico_nombre }}</td>
                <td><span class="badge" :class="'badge-' + tech.rol">{{ tech.rol }}</span></td>
                <td class="text-center">{{ tech.total_seguimientos }}</td>
                <td>
                  <div class="mini-progress">
                    <div
                      class="mini-progress-fill"
                      :style="{ width: tech.avance_promedio + '%' }"
                    ></div>
                    <span>{{ tech.avance_promedio }}%</span>
                  </div>
                </td>
                <td>{{ tech.ultimo_seguimiento ? formatearFecha(tech.ultimo_seguimiento) : 'N/A' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Reporte por Cultivo -->
        <div class="reporte-section">
          <h2>🌾 Reporte por Cultivo</h2>
          <div v-if="reporteCultivo.length === 0" class="empty-state">
            <p>No hay datos para mostrar</p>
          </div>
          <table v-else class="reporte-table">
            <thead>
              <tr>
                <th>Cultivo</th>
                <th>Sembradores</th>
                <th>Seguimientos</th>
                <th>Avance Promedio</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="cul in reporteCultivo" :key="cul.cultivo">
                <td><strong>{{ cul.cultivo }}</strong></td>
                <td class="text-center">{{ cul.total_sembradores }}</td>
                <td class="text-center">{{ cul.total_seguimientos }}</td>
                <td>
                  <div class="mini-progress">
                    <div
                      class="mini-progress-fill"
                      :style="{ width: cul.avance_promedio + '%' }"
                    ></div>
                    <span>{{ cul.avance_promedio }}%</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from 'axios'

const auth = useAuthStore()

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Estado del componente
const activeTab = ref('Crear Seguimiento')
const tabs = ['Crear Seguimiento', 'Mis Seguimientos', 'Reportes']
const cargando = ref(false)

// Datos
const sembradores = ref([])
const seguimientos = ref([])
const reporteTecnico = ref([])
const reporteCultivo = ref([])

// Formulario
const formulario = ref({
  sembrador_id: null,
  fecha_visita: new Date().toISOString().slice(0, 16),
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
      fecha_visita: new Date().toISOString().slice(0, 16),
      estado_cultivo: '',
      observaciones: '',
      avance_porcentaje: 0,
      foto_url: ''
    }
    
    // Refrescar lista
    await obtenerSeguimientos()
    activeTab.value = 'Mis Seguimientos'
  } catch (error) {
    console.error('Error:', error)
    alert('❌ Error al crear seguimiento')
  } finally {
    cargando.value = false
  }
}

const editarSeguimiento = (seg) => {
  console.log('Editar:', seg)
  // Aquí iría la lógica de edición
  alert('Funcionalidad en desarrollo')
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
    // Reporte por Técnico
    const respTecnico = await axios.get(`${API_URL}/seguimientos/reportes/por-tecnico`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    reporteTecnico.value = respTecnico.data.items || []

    // Reporte por Cultivo
    const respCultivo = await axios.get(`${API_URL}/seguimientos/reportes/por-cultivo`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    reporteCultivo.value = respCultivo.data.items || []
  } catch (error) {
    console.error('Error cargando reportes:', error)
  }
}

const formatearFecha = (fecha: string) => {
  if (!fecha) return 'N/A'
  const date = new Date(fecha)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const estadoColor = (estado: string) => {
  const colores = {
    'Germinando': 'info',
    'Vegetativo': 'success',
    'Floración': 'warning',
    'Fructificación': 'primary',
    'Cosecha': 'success',
    'Plagas': 'danger',
    'Enfermedad': 'danger'
  }
  return colores[estado] || 'secondary'
}

onMounted(() => {
  obtenerSembradores()
  obtenerSeguimientos()
  cargarReportes()
})
</script>

<style scoped>
.seguimiento-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  padding: 2rem;
  color: #cbd5e1;
}

.header {
  margin-bottom: 2rem;
  text-align: center;
}

.header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #f1f5f9;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #94a3b8;
  font-size: 1.05rem;
}

/* Tabs */
.tabs-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid rgba(148, 163, 184, 0.2);
  flex-wrap: wrap;
}

.tab {
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  color: #94a3b8;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.tab:hover {
  color: #cbd5e1;
  background: rgba(16, 185, 129, 0.05);
}

.tab.active {
  color: #10b981;
  border-bottom-color: #10b981;
}

/* Form */
.form-container {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #cbd5e1;
  font-size: 0.95rem;
}

.input-text,
.input-select,
.input-textarea {
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.3);
  border-radius: 8px;
  color: #cbd5e1;
  font-family: inherit;
  transition: all 0.3s ease;
}

.input-text:focus,
.input-select:focus,
.input-textarea:focus {
  outline: none;
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.input-textarea {
  resize: vertical;
  font-size: 0.95rem;
}

.input-select option {
  background: #1e293b;
  color: #cbd5e1;
}

/* Progress Input */
.progress-input {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.input-range {
  flex: 1;
  height: 6px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 4px;
  outline: none;
  -webkit-appearance: none;
}

.input-range::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: #10b981;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.input-range::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #10b981;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}

.percentage {
  color: #10b981;
  font-weight: bold;
  min-width: 50px;
  text-align: right;
}

/* Buttons */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: rgba(148, 163, 184, 0.2);
  color: #cbd5e1;
}

.btn-secondary:hover {
  background: rgba(148, 163, 184, 0.3);
}

/* Seguimientos Grid */
.seguimientos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 3rem 2rem;
  background: rgba(30, 41, 59, 0.8);
  border: 2px dashed rgba(148, 163, 184, 0.2);
  border-radius: 12px;
}

.empty-state p {
  font-size: 1.1rem;
  margin: 0.5rem 0;
}

/* Tarjeta */
.seguimiento-card {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.seguimiento-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.1);
  transform: translateY(-2px);
}

.card-header {
  padding: 1rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
  border-bottom: 1px solid rgba(16, 185, 129, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  color: #f1f5f9;
  font-size: 1.2rem;
}

.badge {
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge-info { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.badge-success { background: rgba(16, 185, 129, 0.2); color: #10b981; }
.badge-warning { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.badge-primary { background: rgba(8, 145, 178, 0.2); color: #0891b2; }
.badge-danger { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.badge-secondary { background: rgba(148, 163, 184, 0.2); color: #94a3b8; }
.badge-facilitador { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.badge-territorial { background: rgba(168, 85, 247, 0.2); color: #a855f7; }
.badge-tecnico_productivo { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
.badge-tecnico_social { background: rgba(37, 99, 235, 0.2); color: #2563eb; }

.card-body {
  padding: 1rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  color: #94a3b8;
  font-weight: 500;
}

.value {
  color: #cbd5e1;
  font-weight: 600;
}

/* Progress Bar */
.progress-section {
  margin: 1rem 0;
  padding: 1rem 0;
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 8px;
  padding: 1rem;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #94a3b8;
}

.progress-value {
  color: #10b981;
  font-weight: bold;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  transition: width 0.3s ease;
}

/* Observations */
.observations {
  margin: 1rem 0;
  padding: 1rem;
  background: rgba(16, 185, 129, 0.05);
  border-left: 3px solid #10b981;
  border-radius: 4px;
}

.observations p {
  margin: 0.5rem 0;
  line-height: 1.5;
}

/* Foto */
.foto-section {
  margin: 1rem 0;
}

.foto-section img {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.card-footer {
  padding: 1rem;
  background: rgba(15, 23, 42, 0.5);
  border-top: 1px solid rgba(148, 163, 184, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-footer small {
  color: #64748b;
  font-size: 0.85rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-small {
  padding: 0.4rem 0.6rem;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  border-radius: 4px;
}

.btn-edit {
  color: #3b82f6;
}

.btn-edit:hover {
  background: rgba(59, 130, 246, 0.1);
}

.btn-delete {
  color: #ef4444;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.1);
}

/* Reportes */
.reportes-container {
  display: grid;
  gap: 2rem;
}

.reporte-section {
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 2rem;
}

.reporte-section h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #f1f5f9;
  font-size: 1.5rem;
}

.reporte-table {
  width: 100%;
  border-collapse: collapse;
}

.reporte-table thead {
  background: rgba(16, 185, 129, 0.1);
  border-bottom: 2px solid rgba(16, 185, 129, 0.3);
}

.reporte-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #cbd5e1;
}

.reporte-table td {
  padding: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  color: #cbd5e1;
}

.reporte-table tbody tr:hover {
  background: rgba(16, 185, 129, 0.05);
}

.text-center {
  text-align: center;
}

.mini-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(15, 23, 42, 0.5);
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
}

.mini-progress-fill {
  height: 4px;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  border-radius: 2px;
  min-width: 40px;
}

.mini-progress span {
  font-size: 0.85rem;
  color: #10b981;
  font-weight: bold;
  min-width: 40px;
  text-align: right;
}

@media (max-width: 768px) {
  .seguimiento-container {
    padding: 1rem;
  }

  .header h1 {
    font-size: 1.8rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .seguimientos-grid {
    grid-template-columns: 1fr;
  }

  .tabs-container {
    flex-direction: column;
    gap: 0.25rem;
    border-bottom: none;
  }

  .tab {
    border-left: 3px solid transparent;
    border-bottom: none;
    width: 100%;
    text-align: left;
  }

  .tab.active {
    border-left-color: #10b981;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .reporte-table {
    font-size: 0.85rem;
  }

  .reporte-table th,
  .reporte-table td {
    padding: 0.75rem 0.5rem;
  }
}
</style>
