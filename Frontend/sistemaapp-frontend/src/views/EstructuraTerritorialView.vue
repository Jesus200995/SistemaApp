<template>
  <div class="estructura-container">
    <!-- Sidebar -->
    <DesktopSidebar :pendingCount="pendientesCambios" />
    
    <div class="main-wrapper">
      <!-- Header -->
      <header class="view-header">
        <div class="header-content">
          <div class="header-title">
            <Building2 :size="28" class="header-icon" />
            <div>
              <h1>Estructura Territorial</h1>
              <p class="header-subtitle">Gestión de Territorios → Rutas → CAC</p>
            </div>
          </div>
          
          <div class="header-actions" v-if="isAdmin">
            <button @click="showCreateTerritorio = true" class="btn-primary">
              <Plus :size="18" />
              Nuevo Territorio
            </button>
          </div>
        </div>
      </header>

      <main class="view-main">
        <!-- Vista de 3 columnas -->
        <div class="three-column-layout">
          
          <!-- Columna 1: Territorios -->
          <div class="column territorios-column">
            <div class="column-header">
              <MapPin :size="20" />
              <h3>Territorios</h3>
              <span class="count-badge">{{ territorios.length }}</span>
            </div>
            
            <div class="search-box">
              <Search :size="16" />
              <input 
                type="text" 
                v-model="searchTerritorio" 
                placeholder="Buscar territorio..."
              />
            </div>
            
            <div class="column-list">
              <div 
                v-for="territorio in territoriosFiltrados" 
                :key="territorio.id"
                :class="['list-item', { active: territorioSeleccionado?.id === territorio.id }]"
                @click="seleccionarTerritorio(territorio)"
              >
                <div class="item-info">
                  <span class="item-name">{{ territorio.nombre }}</span>
                  <span class="item-meta">{{ territorio.estado_region || 'Sin región' }}</span>
                </div>
                <div class="item-kpis">
                  <span class="kpi" :title="'Rutas'">
                    <Route :size="14" />
                    {{ territorio.kpis?.rutas || 0 }}
                  </span>
                  <span class="kpi" :title="'CAC'">
                    <Users :size="14" />
                    {{ territorio.kpis?.cac_total || 0 }}
                  </span>
                  <span v-if="territorio.kpis?.vacantes_ts > 0 || territorio.kpis?.vacantes_tp > 0" class="kpi warning">
                    <AlertTriangle :size="14" />
                    {{ (territorio.kpis?.vacantes_ts || 0) + (territorio.kpis?.vacantes_tp || 0) }}
                  </span>
                </div>
              </div>
              
              <div v-if="territoriosFiltrados.length === 0" class="empty-state">
                <MapPin :size="32" />
                <p>No hay territorios</p>
              </div>
            </div>
          </div>

          <!-- Columna 2: Rutas del territorio seleccionado -->
          <div class="column rutas-column">
            <div class="column-header">
              <Route :size="20" />
              <h3>Rutas</h3>
              <span class="count-badge">{{ rutas.length }}</span>
              <button v-if="territorioSeleccionado && canCreateRuta" @click="showCreateRuta = true" class="btn-icon">
                <Plus :size="16" />
              </button>
            </div>
            
            <div v-if="territorioSeleccionado" class="column-list">
              <div 
                v-for="ruta in rutas" 
                :key="ruta.ruta_id"
                :class="['list-item', { active: rutaSeleccionada?.ruta_id === ruta.ruta_id }]"
                @click="seleccionarRuta(ruta)"
              >
                <div class="item-info">
                  <span class="item-name">{{ ruta.nombre }}</span>
                  <div class="facilitadores">
                    <span v-for="f in ruta.facilitadores" :key="f.persona_id" class="facilitador-tag">
                      <UserCheck :size="12" />
                      {{ f.nombre_completo?.split(' ')[0] || 'N/A' }}
                      <span class="tipo-tag">{{ f.tipo_participacion === 'PRINCIPAL' ? 'P' : 'A' }}</span>
                    </span>
                    <span v-if="!ruta.facilitadores?.length" class="vacante-tag">
                      <AlertCircle :size="12" />
                      Sin Facilitador
                    </span>
                  </div>
                </div>
                <div class="item-kpis">
                  <span class="kpi" :title="'CAC'">
                    <Building :size="14" />
                    {{ ruta.kpis?.cac_total || 0 }}
                  </span>
                  <span v-if="ruta.kpis?.vacantes_ts > 0" class="kpi warning" :title="'Vacantes TS'">
                    TS: {{ ruta.kpis?.vacantes_ts }}
                  </span>
                  <span v-if="ruta.kpis?.vacantes_tp > 0" class="kpi warning" :title="'Vacantes TP'">
                    TP: {{ ruta.kpis?.vacantes_tp }}
                  </span>
                </div>
              </div>
              
              <div v-if="rutas.length === 0" class="empty-state">
                <Route :size="32" />
                <p>No hay rutas en este territorio</p>
              </div>
            </div>
            
            <div v-else class="empty-state">
              <ArrowLeft :size="32" />
              <p>Selecciona un territorio</p>
            </div>
          </div>

          <!-- Columna 3: CAC de la ruta seleccionada -->
          <div class="column cac-column">
            <div class="column-header">
              <Building :size="20" />
              <h3>CAC</h3>
              <span class="count-badge">{{ cacs.length }}</span>
              <button v-if="rutaSeleccionada && canCreateCAC" @click="showCreateCAC = true" class="btn-icon">
                <Plus :size="16" />
              </button>
            </div>
            
            <div class="filter-chips" v-if="rutaSeleccionada">
              <button 
                :class="['chip', { active: filtroCAC === 'all' }]"
                @click="filtroCAC = 'all'"
              >
                Todas
              </button>
              <button 
                :class="['chip', { active: filtroCAC === 'vacante' }]"
                @click="filtroCAC = 'vacante'"
              >
                <AlertTriangle :size="14" />
                Con Vacante
              </button>
              <button 
                :class="['chip', { active: filtroCAC === 'sin_coords' }]"
                @click="filtroCAC = 'sin_coords'"
              >
                <MapPinOff :size="14" />
                Sin Coords
              </button>
            </div>
            
            <div v-if="rutaSeleccionada" class="column-list cac-list">
              <div 
                v-for="cac in cacsFiltradas" 
                :key="cac.cac_id"
                class="cac-card"
                @click="verDetalleCAC(cac)"
              >
                <div class="cac-header">
                  <span class="cac-nombre">{{ cac.nombre }}</span>
                  <span :class="['estatus-badge', cac.estatus?.toLowerCase()]">
                    {{ cac.estatus }}
                  </span>
                </div>
                
                <div class="cac-tecnicos">
                  <div class="tecnico">
                    <span class="tecnico-label">TS:</span>
                    <span v-if="cac.tecnico_social" class="tecnico-nombre">
                      {{ cac.tecnico_social.nombre_completo?.split(' ')[0] }}
                    </span>
                    <span v-else class="vacante">VACANTE</span>
                  </div>
                  <div class="tecnico">
                    <span class="tecnico-label">TP:</span>
                    <span v-if="cac.tecnico_productivo" class="tecnico-nombre">
                      {{ cac.tecnico_productivo.nombre_completo?.split(' ')[0] }}
                    </span>
                    <span v-else class="vacante">VACANTE</span>
                  </div>
                </div>
                
                <div class="cac-coords" v-if="cac.latitud && cac.longitud">
                  <MapPin :size="12" />
                  <span>{{ cac.latitud?.toFixed(4) }}, {{ cac.longitud?.toFixed(4) }}</span>
                </div>
                <div class="cac-coords warning" v-else>
                  <MapPinOff :size="12" />
                  <span>Sin coordenadas</span>
                </div>
              </div>
              
              <div v-if="cacsFiltradas.length === 0" class="empty-state">
                <Building :size="32" />
                <p>No hay CAC en esta ruta</p>
              </div>
            </div>
            
            <div v-else class="empty-state">
              <ArrowLeft :size="32" />
              <p>Selecciona una ruta</p>
            </div>
          </div>
        </div>
      </main>
    </div>
    
    <!-- Modal Crear Territorio -->
    <div v-if="showCreateTerritorio" class="modal-overlay" @click.self="showCreateTerritorio = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Nuevo Territorio</h3>
          <button @click="showCreateTerritorio = false" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        <form @submit.prevent="crearTerritorio" class="modal-form">
          <div class="form-group">
            <label>Nombre del Territorio</label>
            <input v-model="nuevoTerritorio.nombre" type="text" required />
          </div>
          <div class="form-group">
            <label>Estado/Región</label>
            <input v-model="nuevoTerritorio.estado_region" type="text" />
          </div>
          <div class="form-actions">
            <button type="button" @click="showCreateTerritorio = false" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn-primary" :disabled="creando">
              {{ creando ? 'Creando...' : 'Crear Territorio' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Modal Crear Ruta -->
    <div v-if="showCreateRuta" class="modal-overlay" @click.self="showCreateRuta = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Nueva Ruta</h3>
          <button @click="showCreateRuta = false" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        <form @submit.prevent="crearRuta" class="modal-form">
          <div class="form-group">
            <label>Nombre de la Ruta</label>
            <input v-model="nuevaRuta.nombre" type="text" required />
          </div>
          <div class="form-group">
            <label>Territorio</label>
            <input type="text" :value="territorioSeleccionado?.nombre" disabled />
          </div>
          <div class="form-actions">
            <button type="button" @click="showCreateRuta = false" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn-primary" :disabled="creando">
              {{ creando ? 'Creando...' : 'Crear Ruta' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Modal Crear CAC -->
    <div v-if="showCreateCAC" class="modal-overlay" @click.self="showCreateCAC = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Nueva CAC</h3>
          <button @click="showCreateCAC = false" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        <form @submit.prevent="crearCAC" class="modal-form">
          <div class="form-group">
            <label>Nombre de la CAC</label>
            <input v-model="nuevaCAC.nombre" type="text" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Latitud</label>
              <input v-model.number="nuevaCAC.latitud" type="number" step="0.000001" />
            </div>
            <div class="form-group">
              <label>Longitud</label>
              <input v-model.number="nuevaCAC.longitud" type="number" step="0.000001" />
            </div>
          </div>
          <div class="form-actions">
            <button type="button" @click="showCreateCAC = false" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn-primary" :disabled="creando">
              {{ creando ? 'Creando...' : 'Crear CAC' }}
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
  Building2, Building, MapPin, Route, Users, Search, Plus, X,
  UserCheck, AlertCircle, AlertTriangle, ArrowLeft, MapPinOff
} from 'lucide-vue-next'

const auth = useAuthStore()
const API_URL = getSecureApiUrl()

// Estado
const territorios = ref([])
const rutas = ref([])
const cacs = ref([])
const territorioSeleccionado = ref(null)
const rutaSeleccionada = ref(null)
const searchTerritorio = ref('')
const filtroCAC = ref('all')
const pendientesCambios = ref(0)

// Modales
const showCreateTerritorio = ref(false)
const showCreateRuta = ref(false)
const showCreateCAC = ref(false)
const creando = ref(false)

// Formularios
const nuevoTerritorio = ref({ nombre: '', estado_region: '' })
const nuevaRuta = ref({ nombre: '' })
const nuevaCAC = ref({ nombre: '', latitud: null, longitud: null })

// Computed
const isAdmin = computed(() => auth.user?.rol?.toLowerCase() === 'admin')
const canCreateRuta = computed(() => ['admin', 'territorial'].includes(auth.user?.rol?.toLowerCase()))
const canCreateCAC = computed(() => ['admin', 'territorial', 'facilitador'].includes(auth.user?.rol?.toLowerCase()))

const territoriosFiltrados = computed(() => {
  if (!searchTerritorio.value) return territorios.value
  return territorios.value.filter(t => 
    t.nombre.toLowerCase().includes(searchTerritorio.value.toLowerCase())
  )
})

const cacsFiltradas = computed(() => {
  let filtradas = cacs.value
  if (filtroCAC.value === 'vacante') {
    filtradas = filtradas.filter(c => c.estatus === 'VACANTE' || !c.tecnico_social || !c.tecnico_productivo)
  } else if (filtroCAC.value === 'sin_coords') {
    filtradas = filtradas.filter(c => !c.latitud || !c.longitud)
  }
  return filtradas
})

// Métodos
const cargarTerritorios = async () => {
  try {
    const { data } = await axios.get(`${API_URL}/estructura/territorios`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    territorios.value = data.items || []
  } catch (error) {
    console.error('Error cargando territorios:', error)
  }
}

const cargarRutas = async (territorioId) => {
  try {
    const { data } = await axios.get(`${API_URL}/estructura/rutas`, {
      params: { territorio_id: territorioId },
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    rutas.value = data.items || []
  } catch (error) {
    console.error('Error cargando rutas:', error)
  }
}

const cargarCACs = async (rutaId) => {
  try {
    const { data } = await axios.get(`${API_URL}/estructura/cac`, {
      params: { ruta_id: rutaId },
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    cacs.value = data.items || []
  } catch (error) {
    console.error('Error cargando CACs:', error)
  }
}

const seleccionarTerritorio = (territorio) => {
  territorioSeleccionado.value = territorio
  rutaSeleccionada.value = null
  cacs.value = []
  cargarRutas(territorio.id)
}

const seleccionarRuta = (ruta) => {
  rutaSeleccionada.value = ruta
  cargarCACs(ruta.ruta_id)
}

const verDetalleCAC = (cac) => {
  // TODO: Abrir modal de detalle de CAC
  console.log('Ver CAC:', cac)
}

const crearTerritorio = async () => {
  try {
    creando.value = true
    await axios.post(`${API_URL}/estructura/territorios`, nuevoTerritorio.value, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    showCreateTerritorio.value = false
    nuevoTerritorio.value = { nombre: '', estado_region: '' }
    cargarTerritorios()
  } catch (error) {
    console.error('Error creando territorio:', error)
    alert(error.response?.data?.detail || 'Error al crear territorio')
  } finally {
    creando.value = false
  }
}

const crearRuta = async () => {
  try {
    creando.value = true
    await axios.post(`${API_URL}/estructura/rutas`, {
      ...nuevaRuta.value,
      territorio_id: territorioSeleccionado.value.id
    }, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    showCreateRuta.value = false
    nuevaRuta.value = { nombre: '' }
    cargarRutas(territorioSeleccionado.value.id)
  } catch (error) {
    console.error('Error creando ruta:', error)
    alert(error.response?.data?.detail || 'Error al crear ruta')
  } finally {
    creando.value = false
  }
}

const crearCAC = async () => {
  try {
    creando.value = true
    await axios.post(`${API_URL}/estructura/cac`, {
      ...nuevaCAC.value,
      ruta_id: rutaSeleccionada.value.ruta_id
    }, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    showCreateCAC.value = false
    nuevaCAC.value = { nombre: '', latitud: null, longitud: null }
    cargarCACs(rutaSeleccionada.value.ruta_id)
  } catch (error) {
    console.error('Error creando CAC:', error)
    alert(error.response?.data?.detail || 'Error al crear CAC')
  } finally {
    creando.value = false
  }
}

onMounted(() => {
  cargarTerritorios()
})
</script>

<style scoped>
.estructura-container {
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
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3);
}

.view-main {
  flex: 1;
  padding: 1rem;
  overflow: hidden;
}

.three-column-layout {
  display: grid;
  grid-template-columns: 1fr 1fr 1.5fr;
  gap: 1rem;
  height: calc(100vh - 140px);
}

.column {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.column-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  background: #fafafa;
}

.column-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.count-badge {
  background: #16a34a;
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.btn-icon {
  margin-left: auto;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0fdf4;
  border: 1px solid #16a34a;
  border-radius: 6px;
  color: #16a34a;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #16a34a;
  color: white;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.search-box input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 0.875rem;
}

.column-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.list-item {
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 0.5rem;
  border: 1px solid transparent;
}

.list-item:hover {
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.list-item.active {
  background: #dcfce7;
  border-color: #16a34a;
}

.item-info {
  margin-bottom: 0.5rem;
}

.item-name {
  font-weight: 600;
  color: #1f2937;
  display: block;
}

.item-meta {
  font-size: 0.75rem;
  color: #6b7280;
}

.item-kpis {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.kpi {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #6b7280;
  background: #f3f4f6;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
}

.kpi.warning {
  background: #fef3c7;
  color: #d97706;
}

.facilitadores {
  display: flex;
  gap: 0.375rem;
  margin-top: 0.375rem;
  flex-wrap: wrap;
}

.facilitador-tag {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.7rem;
  background: #dbeafe;
  color: #1d4ed8;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
}

.tipo-tag {
  background: #1d4ed8;
  color: white;
  padding: 0 0.25rem;
  border-radius: 2px;
  font-size: 0.65rem;
}

.vacante-tag {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.7rem;
  background: #fee2e2;
  color: #dc2626;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
}

.filter-chips {
  display: flex;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.chip {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.75rem;
  background: #f3f4f6;
  border: 1px solid transparent;
  border-radius: 999px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.chip:hover {
  background: #e5e7eb;
}

.chip.active {
  background: #dcfce7;
  border-color: #16a34a;
  color: #16a34a;
}

.cac-card {
  background: #fafafa;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.cac-card:hover {
  border-color: #16a34a;
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.1);
}

.cac-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.cac-nombre {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.875rem;
}

.estatus-badge {
  font-size: 0.65rem;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-weight: 600;
}

.estatus-badge.ok {
  background: #dcfce7;
  color: #16a34a;
}

.estatus-badge.vacante {
  background: #fee2e2;
  color: #dc2626;
}

.estatus-badge.pendiente {
  background: #fef3c7;
  color: #d97706;
}

.cac-tecnicos {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.tecnico {
  font-size: 0.75rem;
}

.tecnico-label {
  color: #6b7280;
}

.tecnico-nombre {
  color: #1f2937;
  font-weight: 500;
}

.vacante {
  color: #dc2626;
  font-weight: 500;
}

.cac-coords {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.7rem;
  color: #6b7280;
}

.cac-coords.warning {
  color: #d97706;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #9ca3af;
  text-align: center;
}

.empty-state p {
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

/* Modal */
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
  box-shadow: 0 20px 50px rgba(0,0,0,0.2);
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

.form-group input {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}

.form-group input:focus {
  outline: none;
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
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

.btn-secondary {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

@media (max-width: 1024px) {
  .main-wrapper {
    margin-left: 0;
  }
  
  .three-column-layout {
    grid-template-columns: 1fr;
    height: auto;
  }
  
  .column {
    max-height: 400px;
  }
}
</style>
