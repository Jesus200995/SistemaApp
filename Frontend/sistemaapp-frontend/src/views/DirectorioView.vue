<template>
  <div class="directorio-container">
    <DesktopSidebar />
    
    <div class="main-wrapper">
      <header class="view-header">
        <div class="header-content">
          <div class="header-title">
            <Users :size="22" class="header-icon" />
            <div>
              <h1>Directorio de Personal</h1>
              <p class="header-subtitle">{{ scopeLabel }}</p>
            </div>
          </div>
          
          <div class="header-actions">
            <button @click="exportarDirectorio" class="btn-secondary">
              <Download :size="18" />
              Exportar
            </button>
          </div>
        </div>
      </header>

      <main class="view-main">
        <!-- Filtros -->
        <div class="filters-bar">
          <div class="search-box">
            <Search :size="18" />
            <input 
              v-model="filtros.search" 
              type="text" 
              placeholder="Buscar por nombre, CURP o correo..."
              @input="debouncedSearch"
            />
          </div>
          
          <div class="filter-group">
            <select v-model="filtros.rol">
              <option value="">Todos los roles</option>
              <option value="TERRITORIAL">Territorial</option>
              <option value="FACILITADOR">Facilitador</option>
              <option value="TECNICO">Técnico</option>
            </select>
            
            <select v-model="filtros.perfil">
              <option value="">Todos los perfiles</option>
              <option value="TECNICO_SOCIAL">Técnico Social</option>
              <option value="TECNICO_PRODUCTIVO">Técnico Productivo</option>
            </select>
            
            <select v-model="filtros.territorio_id" v-if="auth.user?.rol === 'ADMINISTRADOR'">
              <option value="">Todos los territorios</option>
              <option v-for="t in territorios" :key="t.id" :value="t.id">
                {{ t.nombre }}
              </option>
            </select>
            
            <select v-model="filtros.ruta_id">
              <option value="">Todas las rutas</option>
              <option v-for="r in rutasFiltradas" :key="r.id" :value="r.id">
                {{ r.nombre }}
              </option>
            </select>
          </div>
          
          <div class="view-toggle">
            <button 
              :class="['toggle-btn', { active: viewMode === 'table' }]"
              @click="viewMode = 'table'"
            >
              <List :size="18" />
            </button>
            <button 
              :class="['toggle-btn', { active: viewMode === 'cards' }]"
              @click="viewMode = 'cards'"
            >
              <LayoutGrid :size="18" />
            </button>
          </div>
        </div>
        
        <!-- KPIs -->
        <div class="kpi-bar">
          <div class="kpi">
            <span class="kpi-value">{{ stats.total }}</span>
            <span class="kpi-label">Total</span>
          </div>
          <div class="kpi territorial">
            <span class="kpi-value">{{ stats.territoriales }}</span>
            <span class="kpi-label">Territoriales</span>
          </div>
          <div class="kpi facilitador">
            <span class="kpi-value">{{ stats.facilitadores }}</span>
            <span class="kpi-label">Facilitadores</span>
          </div>
          <div class="kpi tecnico">
            <span class="kpi-value">{{ stats.tecnicos }}</span>
            <span class="kpi-label">Técnicos</span>
          </div>
        </div>

        <!-- Vista Tabla -->
        <div v-if="viewMode === 'table'" class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>CURP</th>
                <th>Rol</th>
                <th>Perfil</th>
                <th>Estatus</th>
                <th>Territorio</th>
                <th>Ruta</th>
                <th>CAC</th>
                <th>Contacto</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="persona in personal" 
                :key="persona.id"
                :class="getEstatusRowClass(persona)"
              >
                <td class="nombre">
                  <div class="persona-name">
                    <span class="avatar">{{ getInitials(persona.nombre) }}</span>
                    {{ persona.nombre }}
                  </div>
                </td>
                <td class="curp">{{ persona.curp }}</td>
                <td>
                  <span :class="['rol-badge', persona.rol?.toLowerCase().replace('_', '-')]">
                    {{ formatRol(persona.rol) }}
                  </span>
                </td>
                <td>
                  <span v-if="persona.perfil_operativo" :class="['perfil-badge', persona.perfil_operativo?.toLowerCase()]">
                    {{ formatPerfil(persona.perfil_operativo) }}
                  </span>
                  <span v-else class="na">-</span>
                </td>
                <td>
                  <span :class="['estatus-badge', getEstatusBadgeClass(persona)]">
                    {{ getEstatusLabel(persona) }}
                  </span>
                </td>
                <td>{{ persona.territorio_nombre || '-' }}</td>
                <td>{{ persona.ruta_nombre || '-' }}</td>
                <td>{{ persona.cac_nombre || '-' }}</td>
                <td class="contacto">
                  <div v-if="persona.correo_contacto" class="contact-item">
                    <Mail :size="14" />
                    {{ persona.correo_contacto }}
                  </div>
                  <div v-if="persona.telefono" class="contact-item">
                    <Phone :size="14" />
                    {{ persona.telefono }}
                  </div>
                </td>
                <td class="actions">
                  <button @click="verDetalle(persona)" class="btn-action" title="Ver detalle">
                    <Eye :size="16" />
                  </button>
                  <button 
                    v-if="canEdit" 
                    @click="iniciarCambioAdscripcion(persona)" 
                    class="btn-action primary"
                    title="Cambiar adscripción"
                  >
                    <ArrowRightLeft :size="16" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div v-if="personal.length === 0" class="empty-state">
            <Users :size="48" />
            <p>No se encontró personal con los filtros aplicados</p>
          </div>
          
          <!-- Paginación -->
          <div v-if="totalPages > 1" class="pagination">
            <button @click="prevPage" :disabled="filtros.page === 1" class="page-btn">
              <ChevronLeft :size="18" />
            </button>
            <span class="page-info">Página {{ filtros.page }} de {{ totalPages }}</span>
            <button @click="nextPage" :disabled="filtros.page >= totalPages" class="page-btn">
              <ChevronRight :size="18" />
            </button>
          </div>
        </div>

        <!-- Vista Cards -->
        <div v-if="viewMode === 'cards'" class="cards-grid">
          <div v-for="persona in personal" :key="persona.id" class="persona-card">
            <div class="card-header">
              <span class="avatar large">{{ getInitials(persona.nombre) }}</span>
              <div class="card-info">
                <h3>{{ persona.nombre }}</h3>
                <span class="curp">{{ persona.curp }}</span>
              </div>
              <span :class="['rol-badge', persona.rol?.toLowerCase()]">
                {{ persona.rol }}
              </span>
            </div>
            
            <div class="card-body">
              <div class="info-row" v-if="persona.perfil_operativo">
                <Briefcase :size="14" />
                <span>{{ formatPerfil(persona.perfil_operativo) }}</span>
              </div>
              <div class="info-row" v-if="persona.territorio_nombre">
                <MapPin :size="14" />
                <span>{{ persona.territorio_nombre }}</span>
              </div>
              <div class="info-row" v-if="persona.ruta_nombre">
                <Route :size="14" />
                <span>{{ persona.ruta_nombre }}</span>
              </div>
              <div class="info-row" v-if="persona.cac_nombre">
                <Building :size="14" />
                <span>{{ persona.cac_nombre }}</span>
              </div>
              <div class="info-row" v-if="persona.correo_contacto">
                <Mail :size="14" />
                <span>{{ persona.correo_contacto }}</span>
              </div>
            </div>
            
            <div class="card-actions">
              <button @click="verDetalle(persona)" class="btn-outline">
                <Eye :size="16" />
                Ver detalle
              </button>
              <button 
                v-if="canEdit" 
                @click="iniciarCambioAdscripcion(persona)" 
                class="btn-primary"
              >
                <ArrowRightLeft :size="16" />
                Mover
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
    
    <!-- Modal Detalle Persona -->
    <div v-if="personaSeleccionada" class="modal-overlay" @click.self="personaSeleccionada = null">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Detalle de Personal</h3>
          <button @click="personaSeleccionada = null" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        
        <div class="modal-body">
          <div class="detalle-header">
            <span class="avatar xl">{{ getInitials(personaSeleccionada.nombre) }}</span>
            <div>
              <h2>{{ personaSeleccionada.nombre }}</h2>
              <span class="curp">{{ personaSeleccionada.curp }}</span>
            </div>
          </div>
          
          <div class="detalle-info">
            <div class="info-group">
              <label>Rol</label>
              <span :class="['rol-badge', personaSeleccionada.rol?.toLowerCase()]">
                {{ personaSeleccionada.rol }}
              </span>
            </div>
            
            <div class="info-group" v-if="personaSeleccionada.perfil_operativo">
              <label>Perfil Operativo</label>
              <span>{{ formatPerfil(personaSeleccionada.perfil_operativo) }}</span>
            </div>
            
            <div class="info-group" v-if="personaSeleccionada.territorio_nombre">
              <label>Territorio</label>
              <span>{{ personaSeleccionada.territorio_nombre }}</span>
            </div>
            
            <div class="info-group" v-if="personaSeleccionada.ruta_nombre">
              <label>Ruta</label>
              <span>{{ personaSeleccionada.ruta_nombre }}</span>
            </div>
            
            <div class="info-group" v-if="personaSeleccionada.cac_nombre">
              <label>CAC</label>
              <span>{{ personaSeleccionada.cac_nombre }}</span>
            </div>
            
            <div class="info-group" v-if="personaSeleccionada.correo_contacto">
              <label>Correo de Contacto</label>
              <span>{{ personaSeleccionada.correo_contacto }}</span>
            </div>
            
            <div class="info-group" v-if="personaSeleccionada.telefono">
              <label>Teléfono</label>
              <span>{{ personaSeleccionada.telefono }}</span>
            </div>
            
            <div class="info-group">
              <label>Última actualización</label>
              <span>{{ formatDate(personaSeleccionada.updated_at) }}</span>
            </div>
          </div>
          
          <!-- Historial de Asignaciones -->
          <div v-if="historialAsignaciones.length > 0" class="historial-section">
            <h4>Historial de Asignaciones</h4>
            <div class="timeline">
              <div v-for="h in historialAsignaciones" :key="h.id" class="timeline-item">
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                  <span class="timeline-date">{{ formatDate(h.fecha_inicio) }} - {{ h.fecha_fin ? formatDate(h.fecha_fin) : 'Actual' }}</span>
                  <p>{{ h.cac_nombre }} ({{ h.ruta_nombre }})</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer" v-if="canEdit">
          <button @click="personaSeleccionada = null" class="btn-secondary">
            Cerrar
          </button>
          <button @click="iniciarCambioAdscripcion(personaSeleccionada)" class="btn-primary">
            <ArrowRightLeft :size="18" />
            Cambiar Adscripción
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal Buscar por CURP -->
    <div v-if="showBuscarCURP" class="modal-overlay" @click.self="showBuscarCURP = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Buscar por CURP</h3>
          <button @click="showBuscarCURP = false" class="btn-close">
            <X :size="20" />
          </button>
        </div>
        
        <div class="modal-body">
          <div class="search-curp">
            <input 
              v-model="curpBusqueda" 
              type="text" 
              placeholder="Ingrese CURP completo..."
              maxlength="18"
              @keyup.enter="buscarPorCURP"
            />
            <button @click="buscarPorCURP" class="btn-primary" :disabled="curpBusqueda.length < 18">
              Buscar
            </button>
          </div>
          
          <div v-if="resultadoCURP" class="resultado-curp">
            <h4>Resultado encontrado:</h4>
            <div class="persona-card compact">
              <div class="card-header">
                <span class="avatar">{{ getInitials(resultadoCURP.nombre) }}</span>
                <div class="card-info">
                  <h3>{{ resultadoCURP.nombre }}</h3>
                  <span class="curp">{{ resultadoCURP.curp }}</span>
                </div>
              </div>
              <div class="card-body">
                <p><strong>Territorio:</strong> {{ resultadoCURP.territorio_nombre || 'N/A' }}</p>
                <p><strong>Ruta:</strong> {{ resultadoCURP.ruta_nombre || 'N/A' }}</p>
              </div>
            </div>
          </div>
          
          <div v-if="curpNoEncontrado" class="no-result">
            <XCircle :size="48" />
            <p>No se encontró persona con ese CURP</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import axios from 'axios'
import DesktopSidebar from '../components/DesktopSidebar.vue'
import { 
  Users, Download, Search, List, LayoutGrid, Eye, ArrowRightLeft,
  Mail, Phone, MapPin, Route, Building, Briefcase, X,
  ChevronLeft, ChevronRight, XCircle
} from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()
const API_URL = getSecureApiUrl()

// Estado
const personal = ref([])
const territorios = ref([])
const rutas = ref([])
const personaSeleccionada = ref(null)
const historialAsignaciones = ref([])
const showBuscarCURP = ref(false)
const curpBusqueda = ref('')
const resultadoCURP = ref(null)
const curpNoEncontrado = ref(false)
const viewMode = ref('table')
const totalItems = ref(0)
const stats = ref({
  total: 0,
  territoriales: 0,
  facilitadores: 0,
  tecnicos: 0
})

const filtros = ref({
  search: '',
  rol: '',
  perfil: '',
  territorio_id: '',
  ruta_id: '',
  page: 1,
  limit: 20
})

// Computed
const scopeLabel = computed(() => {
  const user = auth.user
  if (user?.rol === 'ADMINISTRADOR') return 'Todos los territorios'
  if (user?.rol === 'TERRITORIAL') return user.territorio_nombre || 'Mi territorio'
  return 'Mi directorio'
})

const canEdit = computed(() => {
  return ['ADMINISTRADOR', 'TERRITORIAL'].includes(auth.user?.rol)
})

const totalPages = computed(() => Math.ceil(totalItems.value / filtros.value.limit))

const rutasFiltradas = computed(() => {
  if (!filtros.value.territorio_id) return rutas.value
  return rutas.value.filter(r => r.territorio_id === parseInt(filtros.value.territorio_id))
})

// Métodos
let searchTimeout
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    filtros.value.page = 1
    cargarDirectorio()
  }, 300)
}

const cargarDirectorio = async () => {
  try {
    const params = new URLSearchParams()
    if (filtros.value.search) params.append('search', filtros.value.search)
    if (filtros.value.rol) params.append('rol', filtros.value.rol)
    if (filtros.value.perfil) params.append('perfil', filtros.value.perfil)
    if (filtros.value.territorio_id) params.append('territorio_id', filtros.value.territorio_id)
    if (filtros.value.ruta_id) params.append('ruta_id', filtros.value.ruta_id)
    params.append('page', filtros.value.page)
    params.append('limit', filtros.value.limit)
    
    const { data } = await axios.get(`${API_URL}/estructura/directorio?${params.toString()}`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    
    personal.value = data.items || []
    totalItems.value = data.total || 0
    
    // Calcular stats
    stats.value = {
      total: data.total || 0,
      territoriales: data.stats?.territoriales || 0,
      facilitadores: data.stats?.facilitadores || 0,
      tecnicos: data.stats?.tecnicos || 0
    }
  } catch (error) {
    console.error('Error cargando directorio:', error)
  }
}

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

const cargarRutas = async () => {
  try {
    const { data } = await axios.get(`${API_URL}/estructura/rutas`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    rutas.value = data.items || []
  } catch (error) {
    console.error('Error cargando rutas:', error)
  }
}

const verDetalle = async (persona) => {
  personaSeleccionada.value = persona
  
  // Cargar historial si es técnico
  if (persona.rol === 'TECNICO') {
    try {
      const { data } = await axios.get(`${API_URL}/estructura/persona/${persona.id}/historial`, {
        headers: { Authorization: `Bearer ${auth.token}` }
      })
      historialAsignaciones.value = data.items || []
    } catch (error) {
      historialAsignaciones.value = []
    }
  } else {
    historialAsignaciones.value = []
  }
}

const iniciarCambioAdscripcion = (persona) => {
  router.push({
    name: 'CambiosAdscripcion',
    query: { persona_id: persona.id }
  })
}

const buscarPorCURP = async () => {
  if (curpBusqueda.value.length < 18) return
  
  try {
    curpNoEncontrado.value = false
    resultadoCURP.value = null
    
    const { data } = await axios.get(`${API_URL}/estructura/buscar-curp?curp=${curpBusqueda.value}`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    
    if (data) {
      resultadoCURP.value = data
    } else {
      curpNoEncontrado.value = true
    }
  } catch (error) {
    curpNoEncontrado.value = true
  }
}

const exportarDirectorio = async () => {
  try {
    const params = new URLSearchParams()
    if (filtros.value.search) params.append('search', filtros.value.search)
    if (filtros.value.rol) params.append('rol', filtros.value.rol)
    if (filtros.value.territorio_id) params.append('territorio_id', filtros.value.territorio_id)
    params.append('format', 'csv')
    
    const { data } = await axios.get(`${API_URL}/estructura/directorio/exportar?${params.toString()}`, {
      headers: { Authorization: `Bearer ${auth.token}` },
      responseType: 'blob'
    })
    
    const url = URL.createObjectURL(data)
    const a = document.createElement('a')
    a.href = url
    a.download = `directorio_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
  } catch (error) {
    console.error('Error exportando:', error)
  }
}

const prevPage = () => {
  if (filtros.value.page > 1) {
    filtros.value.page--
    cargarDirectorio()
  }
}

const nextPage = () => {
  if (filtros.value.page < totalPages.value) {
    filtros.value.page++
    cargarDirectorio()
  }
}

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()
}

const formatPerfil = (perfil) => {
  const map = {
    'TECNICO_SOCIAL': 'T. Social',
    'TECNICO_PRODUCTIVO': 'T. Productivo'
  }
  return map[perfil] || perfil
}

const formatRol = (rol) => {
  if (!rol) return '-'
  const map = {
    'admin': 'Administrador',
    'administrador': 'Administrador',
    'territorial': 'Territorial',
    'facilitador': 'Facilitador',
    'tecnico_social': 'Técnico Social',
    'tecnico_productivo': 'Técnico Productivo',
    'tecnico': 'Técnico'
  }
  return map[rol.toLowerCase()] || rol
}

// Funciones de estatus laboral
const getEstatusLabel = (u) => {
  if (u.estatus_laboral === 'BAJA' || !u.activo) return 'Baja'
  if (u.tipo_ultima_accion === 'REASIGNACION') return 'Reasignación'
  return 'Activo'
}

const getEstatusBadgeClass = (u) => {
  if (u.estatus_laboral === 'BAJA' || !u.activo) return 'estatus-baja'
  if (u.tipo_ultima_accion === 'REASIGNACION') return 'estatus-reasignacion'
  return 'estatus-activo'
}

const getEstatusRowClass = (u) => {
  if (u.estatus_laboral === 'BAJA' || !u.activo) return 'row-estatus-baja'
  if (u.tipo_ultima_accion === 'REASIGNACION') return 'row-estatus-reasignacion'
  return 'row-estatus-activo'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-MX', { 
    day: '2-digit', 
    month: 'short', 
    year: 'numeric'
  })
}

// Watchers
watch(() => filtros.value.territorio_id, () => {
  filtros.value.ruta_id = ''
})

watch([() => filtros.value.rol, () => filtros.value.perfil, () => filtros.value.territorio_id, () => filtros.value.ruta_id], () => {
  filtros.value.page = 1
  cargarDirectorio()
})

onMounted(() => {
  cargarDirectorio()
  cargarTerritorios()
  cargarRutas()
})
</script>

<style scoped>
.directorio-container {
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
  padding: 0.625rem 1.25rem;
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
  font-size: 1.1rem;
  font-weight: 600;
  color: #14532d;
  margin: 0;
}

.header-subtitle {
  font-size: 0.75rem;
  color: #6b7280;
  margin: 0;
}

.header-icon {
  color: #16a34a;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.view-main {
  flex: 1;
  padding: 1.5rem;
  overflow: auto;
}

.filters-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  flex: 1;
  min-width: 250px;
}

.search-box input {
  border: none;
  outline: none;
  flex: 1;
  font-size: 0.875rem;
}

.filter-group {
  display: flex;
  gap: 0.5rem;
}

.filter-group select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  font-size: 0.875rem;
}

.view-toggle {
  display: flex;
  background: white;
  border-radius: 6px;
  overflow: hidden;
}

.toggle-btn {
  padding: 0.5rem;
  border: 1px solid #e5e7eb;
  background: white;
  cursor: pointer;
  color: #6b7280;
}

.toggle-btn.active {
  background: #16a34a;
  color: white;
  border-color: #16a34a;
}

.kpi-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.kpi {
  background: white;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.kpi-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

.kpi-label {
  font-size: 0.75rem;
  color: #6b7280;
}

.kpi.territorial { border-left: 3px solid #8b5cf6; }
.kpi.facilitador { border-left: 3px solid #3b82f6; }
.kpi.tecnico { border-left: 3px solid #16a34a; }

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

.persona-name {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #16a34a, #15803d);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
}

.avatar.large {
  width: 48px;
  height: 48px;
  font-size: 1rem;
}

.avatar.xl {
  width: 64px;
  height: 64px;
  font-size: 1.25rem;
}

.curp {
  font-family: monospace;
  font-size: 0.8rem;
  color: #6b7280;
}

.rol-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.rol-badge.admin,
.rol-badge.administrador {
  background: #fef3c7;
  color: #d97706;
}

.rol-badge.territorial {
  background: #ede9fe;
  color: #7c3aed;
}

.rol-badge.facilitador {
  background: #dbeafe;
  color: #2563eb;
}

.rol-badge.tecnico,
.rol-badge.tecnico-social {
  background: #dcfce7;
  color: #16a34a;
}

.rol-badge.tecnico-productivo {
  background: #fce7f3;
  color: #db2777;
}

/* Estilos de estatus laboral */
.estatus-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.estatus-activo {
  background: #dcfce7;
  color: #166534;
}

.estatus-baja {
  background: #f3f4f6;
  color: #6b7280;
}

.estatus-reasignacion {
  background: #fef3c7;
  color: #92400e;
}

/* Estilos de filas según estatus */
tr.row-estatus-baja {
  background: #f9fafb !important;
}

tr.row-estatus-baja td {
  color: #9ca3af;
}

tr.row-estatus-activo {
  background: #f0fdf4 !important;
}

tr.row-estatus-reasignacion {
  background: #fffbeb !important;
}

.perfil-badge {
  font-size: 0.75rem;
  color: #4b5563;
}

.na {
  color: #9ca3af;
}

.contacto {
  max-width: 180px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #6b7280;
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
  color: #9ca3af;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.page-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.875rem;
  color: #6b7280;
}

/* Cards Grid */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1rem;
}

.persona-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.persona-card .card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.persona-card .card-info h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.persona-card .card-body {
  padding: 1rem;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4b5563;
  margin-bottom: 0.5rem;
}

.info-row svg {
  color: #9ca3af;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.btn-outline {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
}

.btn-primary {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.5rem;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
}

.btn-secondary {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
  max-width: 520px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
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

.detalle-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.detalle-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.detalle-info {
  display: grid;
  gap: 1rem;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-group label {
  font-size: 0.75rem;
  color: #6b7280;
  text-transform: uppercase;
}

.historial-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.historial-section h4 {
  margin: 0 0 1rem;
  font-size: 0.875rem;
  color: #374151;
}

.timeline {
  position: relative;
  padding-left: 1.5rem;
}

.timeline-item {
  position: relative;
  padding-bottom: 1rem;
}

.timeline-marker {
  position: absolute;
  left: -1.5rem;
  width: 8px;
  height: 8px;
  background: #16a34a;
  border-radius: 50%;
  margin-top: 6px;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -1.25rem;
  top: 14px;
  width: 1px;
  height: calc(100% - 8px);
  background: #e5e7eb;
}

.timeline-item:last-child::before {
  display: none;
}

.timeline-date {
  font-size: 0.75rem;
  color: #6b7280;
}

.timeline-content p {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
}

.search-curp {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.search-curp input {
  flex: 1;
  padding: 0.625rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-family: monospace;
  text-transform: uppercase;
}

.resultado-curp {
  margin-top: 1rem;
}

.resultado-curp h4 {
  margin: 0 0 0.75rem;
  font-size: 0.875rem;
  color: #374151;
}

.persona-card.compact {
  border: 1px solid #e5e7eb;
}

.no-result {
  text-align: center;
  padding: 2rem;
  color: #dc2626;
}

@media (max-width: 1024px) {
  .main-wrapper {
    margin-left: 0;
  }
  
  .filters-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-group {
    flex-wrap: wrap;
  }
  
  .kpi-bar {
    flex-wrap: wrap;
  }
}
</style>
