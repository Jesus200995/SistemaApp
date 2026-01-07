<template>
  <div class="importaciones-container">
    <DesktopSidebar />
    
    <div class="main-wrapper">
      <header class="view-header">
        <div class="header-content">
          <div class="header-title">
            <Upload :size="28" class="header-icon" />
            <div>
              <h1>Importaciones</h1>
              <p class="header-subtitle">Carga de bases - Solo Administrador</p>
            </div>
          </div>
        </div>
      </header>

      <main class="view-main">
        <!-- Sección Subir Archivo -->
        <div class="upload-section">
          <div class="section-header">
            <FileUp :size="20" />
            <h2>Subir Archivo</h2>
          </div>
          
          <form @submit.prevent="subirArchivo" class="upload-form">
            <div class="form-row">
              <div class="form-group">
                <label>Tipo de Importación</label>
                <select v-model="uploadData.tipo" required>
                  <option value="">Seleccionar...</option>
                  <option value="PERSONAL">Personal</option>
                  <option value="RUTAS_CAC">Rutas y CAC</option>
                </select>
              </div>
              
              <div class="form-group">
                <label>Archivo (CSV)</label>
                <div class="file-input-wrapper">
                  <input 
                    type="file" 
                    @change="handleFileSelect" 
                    accept=".csv,.xlsx,.xls"
                    ref="fileInput"
                  />
                  <span class="file-name">
                    {{ uploadData.file?.name || 'Seleccionar archivo...' }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="form-group">
              <label>Notas (opcional)</label>
              <textarea v-model="uploadData.notas" rows="2" placeholder="Notas sobre esta importación..."></textarea>
            </div>
            
            <button type="submit" class="btn-primary" :disabled="!uploadData.file || subiendo">
              <Upload :size="18" />
              {{ subiendo ? 'Subiendo...' : 'Subir Archivo' }}
            </button>
          </form>
        </div>

        <!-- Historial de Importaciones -->
        <div class="history-section">
          <div class="section-header">
            <History :size="20" />
            <h2>Historial de Importaciones</h2>
          </div>
          
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Tipo</th>
                  <th>Archivo</th>
                  <th>Filas</th>
                  <th>Errores</th>
                  <th>Warnings</th>
                  <th>Estatus</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="imp in importaciones" :key="imp.id">
                  <td class="id">#{{ imp.id }}</td>
                  <td>
                    <span :class="['tipo-badge', imp.tipo?.toLowerCase()]">
                      {{ imp.tipo }}
                    </span>
                  </td>
                  <td class="archivo">{{ imp.archivo_nombre }}</td>
                  <td>{{ imp.filas_totales }}</td>
                  <td>
                    <span v-if="imp.errores_criticos > 0" class="error-count">
                      {{ imp.errores_criticos }}
                    </span>
                    <span v-else class="success-count">0</span>
                  </td>
                  <td>
                    <span v-if="imp.warnings > 0" class="warning-count">
                      {{ imp.warnings }}
                    </span>
                    <span v-else>0</span>
                  </td>
                  <td>
                    <span :class="['estatus-badge', imp.estatus?.toLowerCase().replace('_', '-')]">
                      {{ formatEstatus(imp.estatus) }}
                    </span>
                  </td>
                  <td>{{ formatDate(imp.created_at) }}</td>
                  <td class="actions">
                    <button 
                      v-if="imp.estatus === 'PENDIENTE'"
                      @click="validarImportacion(imp)"
                      class="btn-action primary"
                      title="Validar"
                    >
                      <CheckCircle :size="16" />
                    </button>
                    
                    <button 
                      v-if="imp.estatus === 'LISTO_PUBLICAR'"
                      @click="verDetalles(imp)"
                      class="btn-action"
                      title="Ver detalles"
                    >
                      <Eye :size="16" />
                    </button>
                    
                    <button 
                      v-if="imp.estatus === 'LISTO_PUBLICAR' && imp.errores_criticos === 0"
                      @click="confirmarPublicar(imp)"
                      class="btn-action success"
                      title="Publicar"
                    >
                      <Rocket :size="16" />
                    </button>
                    
                    <button 
                      v-if="imp.errores_criticos > 0 || imp.warnings > 0"
                      @click="descargarReporte(imp)"
                      class="btn-action"
                      title="Descargar reporte de errores"
                    >
                      <Download :size="16" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            
            <div v-if="importaciones.length === 0" class="empty-state">
              <FileUp :size="48" />
              <p>No hay importaciones</p>
            </div>
          </div>
        </div>
      </main>
    </div>
    
    <!-- Modal Detalles / Resolución Manual -->
    <div v-if="importacionSeleccionada" class="modal-overlay" @click.self="importacionSeleccionada = null">
      <div class="modal-content modal-xl">
        <div class="modal-header">
          <h3>Importación #{{ importacionSeleccionada.id }}</h3>
          <button @click="importacionSeleccionada = null" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        
        <div class="modal-body">
          <!-- Resumen -->
          <div class="summary-cards">
            <div class="summary-card">
              <FileText :size="24" />
              <div>
                <span class="value">{{ importacionSeleccionada.filas_totales }}</span>
                <span class="label">Filas Totales</span>
              </div>
            </div>
            <div class="summary-card success">
              <Check :size="24" />
              <div>
                <span class="value">{{ importacionSeleccionada.filas_validas }}</span>
                <span class="label">Filas Válidas</span>
              </div>
            </div>
            <div class="summary-card error">
              <XCircle :size="24" />
              <div>
                <span class="value">{{ importacionSeleccionada.errores_criticos }}</span>
                <span class="label">Errores Críticos</span>
              </div>
            </div>
            <div class="summary-card warning">
              <AlertTriangle :size="24" />
              <div>
                <span class="value">{{ importacionSeleccionada.warnings }}</span>
                <span class="label">Warnings</span>
              </div>
            </div>
          </div>
          
          <!-- Tabla de detalles pendientes -->
          <div v-if="detallesPendientes.length > 0" class="detalles-section">
            <h4>Registros pendientes de resolución ({{ detallesPendientes.length }})</h4>
            
            <div class="detalles-list">
              <div v-for="detalle in detallesPendientes" :key="detalle.id" class="detalle-card">
                <div class="detalle-header">
                  <span class="fila-num">Fila {{ detalle.fila_numero }}</span>
                  <span :class="['problema-badge', detalle.tipo_problema?.toLowerCase()]">
                    {{ detalle.tipo_problema }}
                  </span>
                </div>
                
                <div class="detalle-datos">
                  <pre>{{ JSON.stringify(detalle.datos_originales, null, 2) }}</pre>
                </div>
                
                <div v-if="detalle.coincidencias_sugeridas?.length > 0" class="coincidencias">
                  <label>Coincidencias sugeridas:</label>
                  <div class="coincidencias-list">
                    <button 
                      v-for="c in detalle.coincidencias_sugeridas"
                      :key="c.id"
                      @click="resolverMatch(detalle.id, c.id)"
                      class="coincidencia-btn"
                    >
                      {{ c.nombre }} ({{ c.curp || 'Sin CURP' }})
                    </button>
                  </div>
                </div>
                
                <div class="detalle-actions">
                  <button @click="resolverMatch(detalle.id, null, true)" class="btn-secondary">
                    Marcar como Vacante
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div v-else-if="importacionSeleccionada.estatus === 'LISTO_PUBLICAR'" class="ready-message">
            <CheckCircle :size="48" class="success-icon" />
            <p>La importación está lista para publicar</p>
          </div>
        </div>
        
        <div class="modal-footer" v-if="importacionSeleccionada.estatus === 'LISTO_PUBLICAR' && importacionSeleccionada.errores_criticos === 0">
          <button @click="importacionSeleccionada = null" class="btn-secondary">
            Cerrar
          </button>
          <button @click="publicarImportacion(importacionSeleccionada)" class="btn-primary" :disabled="publicando">
            <Rocket :size="18" />
            {{ publicando ? 'Publicando...' : 'Publicar Importación' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal Confirmar Publicación -->
    <div v-if="confirmPublish" class="modal-overlay" @click.self="confirmPublish = null">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Confirmar Publicación</h3>
          <button @click="confirmPublish = null" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        
        <div class="modal-body">
          <div class="confirm-message">
            <AlertTriangle :size="48" class="warning-icon" />
            <p>¿Estás seguro de publicar esta importación?</p>
            <p class="subtext">Esta acción aplicará los cambios en las tablas oficiales.</p>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="confirmPublish = null" class="btn-secondary">
            Cancelar
          </button>
          <button @click="publicarImportacion(confirmPublish)" class="btn-primary" :disabled="publicando">
            {{ publicando ? 'Publicando...' : 'Sí, Publicar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import axios from 'axios'
import DesktopSidebar from '../components/DesktopSidebar.vue'
import { 
  Upload, FileUp, History, CheckCircle, Eye, Rocket, Download,
  X, FileText, Check, XCircle, AlertTriangle
} from 'lucide-vue-next'

const auth = useAuthStore()
const API_URL = getSecureApiUrl()

// Estado
const importaciones = ref([])
const importacionSeleccionada = ref(null)
const detallesPendientes = ref([])
const confirmPublish = ref(null)
const subiendo = ref(false)
const publicando = ref(false)
const fileInput = ref(null)

// Upload data
const uploadData = ref({
  tipo: '',
  file: null,
  notas: ''
})

// Métodos
const cargarImportaciones = async () => {
  try {
    const { data } = await axios.get(`${API_URL}/importaciones/`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    importaciones.value = data.items || []
  } catch (error) {
    console.error('Error cargando importaciones:', error)
  }
}

const handleFileSelect = (event) => {
  uploadData.value.file = event.target.files[0]
}

const subirArchivo = async () => {
  if (!uploadData.value.file || !uploadData.value.tipo) return
  
  try {
    subiendo.value = true
    
    const formData = new FormData()
    formData.append('archivo', uploadData.value.file)
    formData.append('tipo', uploadData.value.tipo)
    if (uploadData.value.notas) {
      formData.append('notas', uploadData.value.notas)
    }
    
    await axios.post(`${API_URL}/importaciones/subir`, formData, {
      headers: { 
        Authorization: `Bearer ${auth.token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Reset form
    uploadData.value = { tipo: '', file: null, notas: '' }
    if (fileInput.value) fileInput.value.value = ''
    
    cargarImportaciones()
  } catch (error) {
    console.error('Error subiendo archivo:', error)
    alert(error.response?.data?.detail || 'Error al subir archivo')
  } finally {
    subiendo.value = false
  }
}

const validarImportacion = async (imp) => {
  try {
    await axios.post(`${API_URL}/importaciones/${imp.id}/validar`, {}, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    cargarImportaciones()
  } catch (error) {
    console.error('Error validando:', error)
    alert(error.response?.data?.detail || 'Error al validar')
  }
}

const verDetalles = async (imp) => {
  try {
    const { data } = await axios.get(`${API_URL}/importaciones/${imp.id}`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    importacionSeleccionada.value = data
    
    // Cargar detalles pendientes
    const { data: detalles } = await axios.get(`${API_URL}/importaciones/${imp.id}/detalles-pendientes`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    detallesPendientes.value = detalles.items || []
  } catch (error) {
    console.error('Error cargando detalles:', error)
  }
}

const resolverMatch = async (detalleId, personaId, esVacante = false) => {
  try {
    await axios.post(`${API_URL}/importaciones/${importacionSeleccionada.value.id}/resolver-match`, {
      detalle_id: detalleId,
      persona_id: personaId,
      es_vacante: esVacante
    }, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    
    // Recargar detalles
    verDetalles(importacionSeleccionada.value)
  } catch (error) {
    console.error('Error resolviendo match:', error)
  }
}

const confirmarPublicar = (imp) => {
  confirmPublish.value = imp
}

const publicarImportacion = async (imp) => {
  try {
    publicando.value = true
    
    const { data } = await axios.post(`${API_URL}/importaciones/${imp.id}/publicar`, {}, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    
    alert(`Importación publicada exitosamente!\n\n${JSON.stringify(data.resumen, null, 2)}`)
    
    importacionSeleccionada.value = null
    confirmPublish.value = null
    cargarImportaciones()
  } catch (error) {
    console.error('Error publicando:', error)
    alert(error.response?.data?.detail || 'Error al publicar')
  } finally {
    publicando.value = false
  }
}

const descargarReporte = async (imp) => {
  try {
    const { data } = await axios.get(`${API_URL}/importaciones/${imp.id}/reporte-errores`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    
    // Convertir a CSV y descargar
    const csv = data.errores.map(e => 
      `${e.fila},${e.tipo_problema},"${JSON.stringify(e.datos)}"`
    ).join('\n')
    
    const blob = new Blob([`Fila,Problema,Datos\n${csv}`], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `errores_importacion_${imp.id}.csv`
    a.click()
  } catch (error) {
    console.error('Error descargando reporte:', error)
  }
}

const formatEstatus = (estatus) => {
  const map = {
    'PENDIENTE': 'Pendiente',
    'VALIDANDO': 'Validando',
    'LISTO_PUBLICAR': 'Listo para Publicar',
    'PUBLICADO': 'Publicado',
    'ERROR': 'Error'
  }
  return map[estatus] || estatus
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-MX', { 
    day: '2-digit', 
    month: 'short', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  cargarImportaciones()
})
</script>

<style scoped>
.importaciones-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 50%, #f0fdf4 100%);
}

.main-wrapper {
  flex: 1;
  margin-left: 220px;
  display: flex;
  flex-direction: column;
}

.view-header {
  background: white;
  padding: 1rem 1.5rem;
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
  gap: 0.75rem;
}

.header-title h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #14532d;
  margin: 0;
}

.header-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.header-icon {
  color: #16a34a;
}

.view-main {
  flex: 1;
  padding: 1.5rem;
  overflow: auto;
}

.upload-section,
.history-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.section-header h2 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.upload-form {
  max-width: 600px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.375rem;
  color: #374151;
}

.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}

.file-input-wrapper {
  position: relative;
}

.file-input-wrapper input[type="file"] {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-name {
  display: block;
  padding: 0.625rem 0.75rem;
  border: 1px dashed #d1d5db;
  border-radius: 6px;
  color: #6b7280;
  cursor: pointer;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.data-table th {
  background: #f9fafb;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #6b7280;
}

.id {
  font-weight: 600;
  color: #6b7280;
}

.archivo {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tipo-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.tipo-badge.personal {
  background: #dbeafe;
  color: #2563eb;
}

.tipo-badge.rutas_cac {
  background: #fce7f3;
  color: #db2777;
}

.estatus-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.estatus-badge.pendiente {
  background: #f3f4f6;
  color: #6b7280;
}

.estatus-badge.validando {
  background: #fef3c7;
  color: #d97706;
}

.estatus-badge.listo-publicar {
  background: #dbeafe;
  color: #2563eb;
}

.estatus-badge.publicado {
  background: #dcfce7;
  color: #16a34a;
}

.estatus-badge.error {
  background: #fee2e2;
  color: #dc2626;
}

.error-count {
  color: #dc2626;
  font-weight: 600;
}

.warning-count {
  color: #d97706;
  font-weight: 600;
}

.success-count {
  color: #16a34a;
}

.actions {
  display: flex;
  gap: 0.375rem;
}

.btn-action {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  color: #6b7280;
}

.btn-action:hover {
  background: #e5e7eb;
}

.btn-action.primary {
  background: #dbeafe;
  color: #2563eb;
}

.btn-action.success {
  background: #dcfce7;
  color: #16a34a;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 0.625rem 1rem;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
  color: #9ca3af;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-content.modal-xl {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
}

.modal-body {
  padding: 1.5rem;
  overflow: auto;
  flex: 1;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
}

.summary-card .value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
}

.summary-card .label {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
}

.summary-card.success {
  background: #f0fdf4;
  color: #16a34a;
}

.summary-card.error {
  background: #fef2f2;
  color: #dc2626;
}

.summary-card.warning {
  background: #fffbeb;
  color: #d97706;
}

.detalles-section h4 {
  margin: 0 0 1rem;
  font-size: 0.875rem;
  color: #374151;
}

.detalle-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
}

.detalle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.fila-num {
  font-weight: 600;
  color: #1f2937;
}

.problema-badge {
  font-size: 0.7rem;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  background: #fee2e2;
  color: #dc2626;
}

.detalle-datos pre {
  font-size: 0.75rem;
  background: white;
  padding: 0.5rem;
  border-radius: 4px;
  overflow-x: auto;
  margin: 0.5rem 0;
}

.coincidencias {
  margin: 0.5rem 0;
}

.coincidencias label {
  font-size: 0.75rem;
  color: #6b7280;
}

.coincidencias-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
  margin-top: 0.25rem;
}

.coincidencia-btn {
  padding: 0.25rem 0.5rem;
  background: #dbeafe;
  border: none;
  border-radius: 4px;
  font-size: 0.75rem;
  color: #2563eb;
  cursor: pointer;
}

.coincidencia-btn:hover {
  background: #bfdbfe;
}

.detalle-actions {
  margin-top: 0.75rem;
}

.ready-message {
  text-align: center;
  padding: 2rem;
}

.success-icon {
  color: #16a34a;
  margin-bottom: 0.5rem;
}

.confirm-message {
  text-align: center;
  padding: 1rem;
}

.warning-icon {
  color: #d97706;
  margin-bottom: 0.5rem;
}

.subtext {
  font-size: 0.875rem;
  color: #6b7280;
}

@media (max-width: 1024px) {
  .main-wrapper {
    margin-left: 0;
  }
  
  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
