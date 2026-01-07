<template>
  <div class="cambios-container">
    <DesktopSidebar :pendingCount="pendientesCambios" />
    
    <div class="main-wrapper">
      <header class="view-header">
        <div class="header-content">
          <div class="header-title">
            <GitBranch :size="28" class="header-icon" />
            <div>
              <h1>Cambios de Adscripción</h1>
              <p class="header-subtitle">Gestión de movimientos operativos</p>
            </div>
          </div>
          
          <div class="header-actions">
            <button @click="showCrearCambio = true" class="btn-primary">
              <Plus :size="18" />
              Proponer Cambio
            </button>
          </div>
        </div>
      </header>

      <main class="view-main">
        <!-- Filtros -->
        <div class="filters-section">
          <div class="filter-group">
            <label>Estatus</label>
            <select v-model="filtros.estatus">
              <option value="">Todos</option>
              <option value="BORRADOR">Borrador</option>
              <option value="EN_REVISION">En Revisión</option>
              <option value="AUTORIZADO">Autorizado</option>
              <option value="APLICADO">Aplicado</option>
              <option value="RECHAZADO">Rechazado</option>
              <option value="CANCELADO">Cancelado</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>Tipo</label>
            <select v-model="filtros.tipo_cambio">
              <option value="">Todos</option>
              <option value="ALTA">Alta</option>
              <option value="BAJA">Baja</option>
              <option value="REASIGNACION">Reasignación</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>Objeto</label>
            <select v-model="filtros.objeto">
              <option value="">Todos</option>
              <option value="PERSONA_CAC">Persona ↔ CAC</option>
              <option value="PERSONA_RUTA">Persona ↔ Ruta</option>
              <option value="CAC_RUTA">CAC ↔ Ruta</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="filtros.vencidos" />
              Solo vencidos
            </label>
          </div>
          
          <button @click="cargarCambios" class="btn-filter">
            <RefreshCw :size="16" />
            Actualizar
          </button>
        </div>

        <!-- Tabla de Cambios -->
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Folio</th>
                <th>Tipo</th>
                <th>Objeto</th>
                <th>Resumen</th>
                <th>Propuesto por</th>
                <th>Fecha Efecto</th>
                <th>SLA</th>
                <th>Estatus</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="cambio in cambios" 
                :key="cambio.cambio_adscripcion_id"
                :class="{ vencido: cambio.vencido }"
              >
                <td class="folio">{{ cambio.folio }}</td>
                <td>
                  <span :class="['tipo-badge', cambio.tipo_cambio?.toLowerCase()]">
                    {{ cambio.tipo_cambio }}
                  </span>
                </td>
                <td class="objeto">{{ formatObjeto(cambio.objeto) }}</td>
                <td class="resumen">{{ cambio.resumen || '-' }}</td>
                <td>{{ cambio.propuesto_por?.nombre_completo?.split(' ')[0] || '-' }}</td>
                <td>{{ formatDate(cambio.fecha_efecto) }}</td>
                <td>
                  <span v-if="cambio.vencido" class="sla-badge vencido">
                    <AlertTriangle :size="14" />
                    Vencido
                  </span>
                  <span v-else-if="cambio.fecha_limite" class="sla-badge">
                    {{ formatDate(cambio.fecha_limite) }}
                  </span>
                  <span v-else>-</span>
                </td>
                <td>
                  <span :class="['estatus-badge', cambio.estatus?.toLowerCase()]">
                    {{ cambio.estatus }}
                  </span>
                </td>
                <td class="actions">
                  <button @click="verDetalle(cambio)" class="btn-action" title="Ver detalle">
                    <Eye :size="16" />
                  </button>
                  
                  <button 
                    v-if="cambio.estatus === 'BORRADOR' && esPropietario(cambio)"
                    @click="enviarARevision(cambio)"
                    class="btn-action primary"
                    title="Enviar a revisión"
                  >
                    <Send :size="16" />
                  </button>
                  
                  <button 
                    v-if="cambio.estatus === 'EN_REVISION' && puedeAutorizar"
                    @click="abrirAccion(cambio, 'AUTORIZAR')"
                    class="btn-action success"
                    title="Autorizar"
                  >
                    <Check :size="16" />
                  </button>
                  
                  <button 
                    v-if="cambio.estatus === 'EN_REVISION' && puedeAutorizar"
                    @click="abrirAccion(cambio, 'RECHAZAR')"
                    class="btn-action danger"
                    title="Rechazar"
                  >
                    <X :size="16" />
                  </button>
                  
                  <button 
                    v-if="cambio.estatus === 'AUTORIZADO' && isAdmin"
                    @click="abrirAccion(cambio, 'APLICAR')"
                    class="btn-action success"
                    title="Aplicar"
                  >
                    <PlayCircle :size="16" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div v-if="cambios.length === 0" class="empty-state">
            <GitBranch :size="48" />
            <p>No hay cambios de adscripción</p>
          </div>
        </div>
      </main>
    </div>
    
    <!-- Modal Crear Cambio -->
    <div v-if="showCrearCambio" class="modal-overlay" @click.self="showCrearCambio = false">
      <div class="modal-content modal-lg">
        <div class="modal-header">
          <h3>Proponer Cambio de Adscripción</h3>
          <button @click="showCrearCambio = false" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        
        <form @submit.prevent="crearCambio" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label>Tipo de Cambio</label>
              <select v-model="nuevoCambio.tipo_cambio" required>
                <option value="">Seleccionar...</option>
                <option value="ALTA">Alta</option>
                <option value="BAJA">Baja</option>
                <option value="REASIGNACION">Reasignación</option>
              </select>
            </div>
            
            <div class="form-group">
              <label>¿Qué afecta?</label>
              <select v-model="nuevoCambio.objeto" required>
                <option value="">Seleccionar...</option>
                <option value="PERSONA_CAC">Persona ↔ CAC</option>
                <option value="PERSONA_RUTA">Persona ↔ Ruta</option>
                <option value="CAC_RUTA">CAC ↔ Ruta</option>
              </select>
            </div>
          </div>
          
          <div class="form-group">
            <label>Descripción del cambio</label>
            <textarea v-model="nuevoCambio.resumen" rows="3" placeholder="Describir el cambio propuesto..."></textarea>
          </div>
          
          <div class="form-group">
            <label>Fecha efecto</label>
            <input type="date" v-model="nuevoCambio.fecha_efecto" />
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showCrearCambio = false" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn-primary" :disabled="creando">
              {{ creando ? 'Creando...' : 'Crear Propuesta' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Modal Detalle -->
    <div v-if="cambioSeleccionado" class="modal-overlay" @click.self="cambioSeleccionado = null">
      <div class="modal-content modal-lg">
        <div class="modal-header">
          <h3>Detalle del Cambio {{ cambioSeleccionado.folio }}</h3>
          <button @click="cambioSeleccionado = null" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        
        <div class="detalle-content">
          <div class="detalle-grid">
            <div class="detalle-item">
              <label>Folio</label>
              <span>{{ cambioSeleccionado.folio }}</span>
            </div>
            <div class="detalle-item">
              <label>Tipo</label>
              <span :class="['tipo-badge', cambioSeleccionado.tipo_cambio?.toLowerCase()]">
                {{ cambioSeleccionado.tipo_cambio }}
              </span>
            </div>
            <div class="detalle-item">
              <label>Objeto</label>
              <span>{{ formatObjeto(cambioSeleccionado.objeto) }}</span>
            </div>
            <div class="detalle-item">
              <label>Estatus</label>
              <span :class="['estatus-badge', cambioSeleccionado.estatus?.toLowerCase()]">
                {{ cambioSeleccionado.estatus }}
              </span>
            </div>
          </div>
          
          <div class="detalle-section" v-if="cambioSeleccionado.resumen">
            <label>Resumen</label>
            <p>{{ cambioSeleccionado.resumen }}</p>
          </div>
          
          <div class="comparador" v-if="cambioSeleccionado.antes || cambioSeleccionado.despues">
            <div class="comparador-col antes">
              <h4>Antes</h4>
              <pre>{{ JSON.stringify(cambioSeleccionado.antes, null, 2) }}</pre>
            </div>
            <div class="comparador-arrow">
              <ArrowRight :size="24" />
            </div>
            <div class="comparador-col despues">
              <h4>Después</h4>
              <pre>{{ JSON.stringify(cambioSeleccionado.despues, null, 2) }}</pre>
            </div>
          </div>
          
          <div class="detalle-section" v-if="cambioSeleccionado.observaciones">
            <label>Observaciones</label>
            <p>{{ cambioSeleccionado.observaciones }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal Acción -->
    <div v-if="accionModal.show" class="modal-overlay" @click.self="accionModal.show = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ accionModal.accion }} Cambio</h3>
          <button @click="accionModal.show = false" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        
        <form @submit.prevent="ejecutarAccion" class="modal-form">
          <div class="form-group">
            <label>Observaciones</label>
            <textarea v-model="accionModal.observaciones" rows="3" placeholder="Agregar observaciones..."></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="accionModal.show = false" class="btn-secondary">
              Cancelar
            </button>
            <button 
              type="submit" 
              :class="['btn-primary', accionModal.accion === 'RECHAZAR' ? 'danger' : '']"
              :disabled="ejecutando"
            >
              {{ ejecutando ? 'Procesando...' : accionModal.accion }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import axios from 'axios'
import DesktopSidebar from '../components/DesktopSidebar.vue'
import { 
  GitBranch, Plus, RefreshCw, Eye, Send, Check, X, PlayCircle,
  AlertTriangle, ArrowRight
} from 'lucide-vue-next'

const auth = useAuthStore()
const API_URL = getSecureApiUrl()

// Estado
const cambios = ref([])
const pendientesCambios = ref(0)
const cambioSeleccionado = ref(null)

// Filtros
const filtros = ref({
  estatus: '',
  tipo_cambio: '',
  objeto: '',
  vencidos: false
})

// Modales
const showCrearCambio = ref(false)
const creando = ref(false)
const ejecutando = ref(false)

const nuevoCambio = ref({
  tipo_cambio: '',
  objeto: '',
  resumen: '',
  fecha_efecto: ''
})

const accionModal = ref({
  show: false,
  cambio: null,
  accion: '',
  observaciones: ''
})

// Computed
const isAdmin = computed(() => auth.user?.rol?.toLowerCase() === 'admin')
const puedeAutorizar = computed(() => ['admin', 'territorial'].includes(auth.user?.rol?.toLowerCase()))

// Métodos
const cargarCambios = async () => {
  try {
    const params = {}
    if (filtros.value.estatus) params.estatus = filtros.value.estatus
    if (filtros.value.tipo_cambio) params.tipo_cambio = filtros.value.tipo_cambio
    if (filtros.value.objeto) params.objeto = filtros.value.objeto
    if (filtros.value.vencidos) params.vencidos = true
    
    const { data } = await axios.get(`${API_URL}/workflows/cambios-adscripcion`, {
      params,
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    cambios.value = data.items || []
    
    // Contar pendientes
    pendientesCambios.value = cambios.value.filter(c => 
      ['EN_REVISION', 'AUTORIZADO'].includes(c.estatus)
    ).length
  } catch (error) {
    console.error('Error cargando cambios:', error)
  }
}

const formatObjeto = (objeto) => {
  const map = {
    'PERSONA_CAC': 'Persona ↔ CAC',
    'PERSONA_RUTA': 'Persona ↔ Ruta',
    'PERSONA_TERRITORIO': 'Persona ↔ Territorio',
    'CAC_RUTA': 'CAC ↔ Ruta'
  }
  return map[objeto] || objeto
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-MX', { 
    day: '2-digit', 
    month: 'short', 
    year: 'numeric' 
  })
}

const esPropietario = (cambio) => {
  return cambio.propuesto_por?.persona_id === auth.user?.id
}

const verDetalle = async (cambio) => {
  try {
    const { data } = await axios.get(`${API_URL}/workflows/cambios-adscripcion/${cambio.cambio_adscripcion_id}`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    cambioSeleccionado.value = data
  } catch (error) {
    console.error('Error cargando detalle:', error)
  }
}

const crearCambio = async () => {
  try {
    creando.value = true
    await axios.post(`${API_URL}/workflows/cambios-adscripcion`, nuevoCambio.value, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    showCrearCambio.value = false
    nuevoCambio.value = { tipo_cambio: '', objeto: '', resumen: '', fecha_efecto: '' }
    cargarCambios()
  } catch (error) {
    console.error('Error creando cambio:', error)
    alert(error.response?.data?.detail || 'Error al crear cambio')
  } finally {
    creando.value = false
  }
}

const enviarARevision = async (cambio) => {
  try {
    await axios.post(`${API_URL}/workflows/cambios-adscripcion/${cambio.cambio_adscripcion_id}/enviar-revision`, {}, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    cargarCambios()
  } catch (error) {
    console.error('Error enviando a revisión:', error)
    alert(error.response?.data?.detail || 'Error')
  }
}

const abrirAccion = (cambio, accion) => {
  accionModal.value = {
    show: true,
    cambio,
    accion,
    observaciones: ''
  }
}

const ejecutarAccion = async () => {
  try {
    ejecutando.value = true
    await axios.post(
      `${API_URL}/workflows/cambios-adscripcion/${accionModal.value.cambio.cambio_adscripcion_id}/accion`,
      {
        accion: accionModal.value.accion,
        observaciones: accionModal.value.observaciones
      },
      { headers: { Authorization: `Bearer ${auth.token}` } }
    )
    accionModal.value.show = false
    cargarCambios()
  } catch (error) {
    console.error('Error ejecutando acción:', error)
    alert(error.response?.data?.detail || 'Error')
  } finally {
    ejecutando.value = false
  }
}

onMounted(() => {
  cargarCambios()
})
</script>

<style scoped>
.cambios-container {
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

.filters-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-end;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.filter-group label {
  font-size: 0.75rem;
  font-weight: 500;
  color: #6b7280;
}

.filter-group select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  min-width: 140px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.btn-filter {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.75rem;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
}

.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
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

.data-table tr:hover {
  background: #f9fafb;
}

.data-table tr.vencido {
  background: #fef2f2;
}

.folio {
  font-family: monospace;
  font-weight: 600;
  color: #1f2937;
}

.resumen {
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

.tipo-badge.alta {
  background: #dcfce7;
  color: #16a34a;
}

.tipo-badge.baja {
  background: #fee2e2;
  color: #dc2626;
}

.tipo-badge.reasignacion {
  background: #dbeafe;
  color: #2563eb;
}

.estatus-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.estatus-badge.borrador {
  background: #f3f4f6;
  color: #6b7280;
}

.estatus-badge.en_revision {
  background: #fef3c7;
  color: #d97706;
}

.estatus-badge.autorizado {
  background: #dbeafe;
  color: #2563eb;
}

.estatus-badge.aplicado {
  background: #dcfce7;
  color: #16a34a;
}

.estatus-badge.rechazado {
  background: #fee2e2;
  color: #dc2626;
}

.estatus-badge.cancelado {
  background: #f3f4f6;
  color: #9ca3af;
}

.sla-badge {
  font-size: 0.75rem;
  color: #6b7280;
}

.sla-badge.vencido {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #dc2626;
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
  transition: all 0.2s;
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

.btn-action.danger {
  background: #fee2e2;
  color: #dc2626;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
  overflow: auto;
}

.modal-content.modal-lg {
  max-width: 640px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  background: white;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
}

.modal-form {
  padding: 1.5rem;
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

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}

.form-group textarea {
  resize: vertical;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

.btn-primary.danger {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
}

.detalle-content {
  padding: 1.5rem;
}

.detalle-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.detalle-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detalle-item label {
  font-size: 0.75rem;
  color: #6b7280;
}

.detalle-section {
  margin-bottom: 1.5rem;
}

.detalle-section label {
  font-size: 0.75rem;
  color: #6b7280;
  display: block;
  margin-bottom: 0.375rem;
}

.detalle-section p {
  margin: 0;
  color: #1f2937;
}

.comparador {
  display: flex;
  align-items: stretch;
  gap: 1rem;
  margin: 1.5rem 0;
}

.comparador-col {
  flex: 1;
  padding: 1rem;
  border-radius: 8px;
}

.comparador-col h4 {
  margin: 0 0 0.5rem;
  font-size: 0.875rem;
}

.comparador-col pre {
  margin: 0;
  font-size: 0.75rem;
  white-space: pre-wrap;
}

.comparador-col.antes {
  background: #fef2f2;
}

.comparador-col.despues {
  background: #f0fdf4;
}

.comparador-arrow {
  display: flex;
  align-items: center;
  color: #9ca3af;
}

@media (max-width: 1024px) {
  .main-wrapper {
    margin-left: 0;
  }
  
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .table-container {
    overflow-x: auto;
  }
}
</style>
