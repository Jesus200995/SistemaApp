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
              Agregar Solicitud
            </button>
          </div>
        </div>
      </header>

      <main class="view-main">
        <!-- Pestañas -->
        <div class="tabs-container">
          <div class="tabs-wrapper">
            <button 
              class="tab-btn" 
              :class="{ active: activeTab === 'pendientes' }"
              @click="activeTab = 'pendientes'"
            >
              <Clock :size="18" />
              <span>Pendientes</span>
              <span v-if="cambiosPendientes.length > 0" class="tab-badge">
                {{ cambiosPendientes.length }}
              </span>
            </button>
            <button 
              class="tab-btn" 
              :class="{ active: activeTab === 'enviadas' }"
              @click="activeTab = 'enviadas'"
            >
              <SendHorizontal :size="18" />
              <span>Enviadas</span>
              <span v-if="cambiosEnviados.length > 0" class="tab-badge tab-badge-enviadas">
                {{ cambiosEnviados.length }}
              </span>
            </button>
            <button 
              class="tab-btn" 
              :class="{ active: activeTab === 'historial' }"
              @click="activeTab = 'historial'"
            >
              <History :size="18" />
              <span>Historial</span>
            </button>
          </div>
          <div class="tabs-stats">
            <div class="stat-item">
              <span class="stat-label">Pendientes:</span>
              <span class="stat-value pending">{{ cambiosPendientes.length }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Enviadas:</span>
              <span class="stat-value sent">{{ cambiosEnviados.length }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Procesadas:</span>
              <span class="stat-value approved">{{ cambiosHistorial.length }}</span>
            </div>
          </div>
        </div>

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
                <th>{{ activeTab === 'enviadas' ? 'Dirigido a' : 'Propuesto por' }}</th>
                <th>Fecha Efecto</th>
                <th>SLA</th>
                <th>Estatus</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="cambio in cambiosFiltradosTab" 
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
                <td>{{ activeTab === 'enviadas' 
                    ? (cambio.destinatario?.nombre_completo?.split(' ')[0] || '-') 
                    : (cambio.propuesto_por?.nombre_completo?.split(' ')[0] || '-') }}</td>
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
          
          <div v-if="cambiosFiltradosTab.length === 0" class="empty-state">
            <GitBranch :size="48" />
            <p v-if="activeTab === 'pendientes'">No hay cambios pendientes por revisar</p>
            <p v-else-if="activeTab === 'enviadas'">No has enviado propuestas de cambio</p>
            <p v-else>No hay cambios en el historial</p>
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
          
          <!-- Selector de Destinatario en 2 pasos -->
          <div class="form-group">
            <label>
              <UserCheck :size="14" class="label-icon" />
              Dirigir a (Destinatario) *
            </label>
            
            <!-- Paso 1: Seleccionar Rol -->
            <div class="select-wrapper">
              <select 
                v-model="rolSeleccionado" 
                class="form-select"
                :class="{ 'loading-select': loadingUsuarios }"
                @change="onRolChange"
              >
                <option value="">-- Selecciona el tipo de destinatario --</option>
                <option 
                  v-for="grupo in rolesDisponiblesParaUsuario" 
                  :key="grupo.rol" 
                  :value="grupo.rol"
                >
                  {{ formatRolNombre(grupo.rol) }}
                </option>
              </select>
              <div v-if="loadingUsuarios" class="select-loading">
                <div class="mini-spinner"></div>
              </div>
            </div>

            <!-- Paso 2: Seleccionar Destinatario (con búsqueda) -->
            <div v-if="rolSeleccionado" class="persona-selector">
              <div class="search-input-wrapper">
                <Search :size="16" class="search-icon" />
                <input 
                  type="text" 
                  v-model="busquedaPersona" 
                  placeholder="Buscar destinatario por nombre o territorio..."
                  class="search-input"
                />
                <button 
                  v-if="busquedaPersona" 
                  @click="busquedaPersona = ''" 
                  class="clear-search"
                  type="button"
                >
                  <X :size="14" />
                </button>
              </div>
              
              <div class="personas-list">
                <div 
                  v-for="usuario in personasFiltradas" 
                  :key="usuario.id"
                  class="persona-item"
                  :class="{ 'selected': nuevoCambio.destino_id === usuario.id }"
                  @click="seleccionarPersona(usuario)"
                >
                  <div class="persona-avatar">
                    {{ getInitials(usuario.nombre) }}
                  </div>
                  <div class="persona-info">
                    <span class="persona-nombre">{{ usuario.nombre }}</span>
                    <span class="persona-territorio">{{ usuario.territorio || 'Sin territorio' }}</span>
                  </div>
                  <div v-if="nuevoCambio.destino_id === usuario.id" class="persona-check">
                    <Check :size="16" />
                  </div>
                </div>
                <div v-if="personasFiltradas.length === 0" class="personas-empty">
                  No se encontraron destinatarios
                </div>
              </div>
            </div>

            <!-- Usuario seleccionado -->
            <div v-if="usuarioSeleccionadoInfo" class="usuario-seleccionado">
              <Check :size="14" class="check-icon" />
              <span>Dirigido a: <strong>{{ usuarioSeleccionadoInfo.nombre }}</strong></span>
              <button type="button" @click="limpiarSeleccion" class="btn-limpiar">
                <X :size="14" />
              </button>
            </div>

            <p class="form-hint">
              <span v-if="loadingUsuarios" class="hint-loading">
                Cargando destinatarios...
              </span>
              <span v-else-if="usuariosDisponibles.length === 0" class="hint-error">
                No hay destinatarios disponibles
              </span>
              <span v-else-if="!rolSeleccionado" class="hint-info">
                Selecciona primero el tipo de destinatario
              </span>
            </p>
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
            <button type="button" @click="cerrarModalCrear" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn-primary" :disabled="creando || !nuevoCambio.destino_id">
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
  AlertTriangle, ArrowRight, UserCheck, Search, Clock, SendHorizontal, History
} from 'lucide-vue-next'

const auth = useAuthStore()
const API_URL = getSecureApiUrl()

// Estado
const cambios = ref([])
const pendientesCambios = ref(0)
const cambioSeleccionado = ref(null)
const activeTab = ref('pendientes')

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
  fecha_efecto: '',
  destino_id: null
})

const accionModal = ref({
  show: false,
  cambio: null,
  accion: '',
  observaciones: ''
})

// === SELECTOR DE DESTINATARIOS ===
const usuariosDisponibles = ref([])
const loadingUsuarios = ref(false)
const rolSeleccionado = ref('')
const busquedaPersona = ref('')

// Normalizar rol a categoría
const normalizarRol = (rol) => {
  if (!rol) return ''
  const rolLower = rol.toLowerCase().replace(/[_\s-]/g, '')
  if (rolLower.includes('admin')) return 'admin'
  if (rolLower.includes('territorial')) return 'territorial'
  if (rolLower.includes('facilitador')) return 'facilitador'
  if (rolLower.includes('tecnico') || rolLower.includes('técnico')) return 'tecnico'
  return rol
}

// Agrupar usuarios por rol (normalizado)
const usuariosAgrupados = computed(() => {
  const grupos = {}
  
  usuariosDisponibles.value.forEach(usuario => {
    const categoria = normalizarRol(usuario.rol)
    if (!grupos[categoria]) {
      grupos[categoria] = []
    }
    grupos[categoria].push(usuario)
  })
  
  // Ordenar por jerarquía: admin > territorial > facilitador > tecnico
  const ordenRoles = ['admin', 'territorial', 'facilitador', 'tecnico']
  
  return ordenRoles
    .filter(rol => grupos[rol] && grupos[rol].length > 0)
    .map(rol => ({
      rol,
      usuarios: grupos[rol]
    }))
})

// Filtrar roles disponibles según el rol del usuario actual
const rolesDisponiblesParaUsuario = computed(() => {
  const rolUsuario = normalizarRol(auth.user?.rol || '')
  
  // Definir qué roles puede ver cada tipo de usuario
  const rolesPermitidos = {
    tecnico: ['facilitador', 'territorial'],     // Técnico puede enviar a Facilitadores y Territoriales
    facilitador: ['territorial', 'admin'],       // Facilitador puede enviar a Territoriales y Admin
    territorial: ['admin'],                      // Territorial puede enviar a Admin
    admin: ['admin', 'territorial', 'facilitador', 'tecnico'] // Admin puede enviar a todos
  }
  
  const permitidos = rolesPermitidos[rolUsuario] || []
  
  if (rolUsuario === 'admin') {
    return usuariosAgrupados.value
  }
  
  return usuariosAgrupados.value.filter(grupo => permitidos.includes(grupo.rol))
})

// Personas filtradas por rol y búsqueda
const personasFiltradas = computed(() => {
  if (!rolSeleccionado.value) return []
  
  const grupo = usuariosAgrupados.value.find(g => g.rol === rolSeleccionado.value)
  if (!grupo) return []
  
  const busqueda = busquedaPersona.value.toLowerCase().trim()
  if (!busqueda) return grupo.usuarios
  
  return grupo.usuarios.filter(u => 
    u.nombre?.toLowerCase().includes(busqueda) || 
    u.territorio?.toLowerCase().includes(busqueda)
  )
})

// Info del usuario seleccionado
const usuarioSeleccionadoInfo = computed(() => {
  if (!nuevoCambio.value.destino_id) return null
  return usuariosDisponibles.value.find(u => u.id === nuevoCambio.value.destino_id)
})

// Formatear nombre del rol
const formatRolNombre = (rol) => {
  const roles = {
    admin: 'Administradores',
    territorial: 'Territoriales',
    facilitador: 'Facilitadores',
    tecnico: 'Técnicos'
  }
  return roles[rol] || rol
}

// Obtener iniciales
const getInitials = (nombre) => {
  if (!nombre) return '?'
  const parts = nombre.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return nombre.substring(0, 2).toUpperCase()
}

// Cuando cambia el rol seleccionado
const onRolChange = () => {
  nuevoCambio.value.destino_id = null
  busquedaPersona.value = ''
}

// Seleccionar una persona
const seleccionarPersona = (usuario) => {
  nuevoCambio.value.destino_id = usuario.id
}

// Limpiar selección
const limpiarSeleccion = () => {
  nuevoCambio.value.destino_id = null
  rolSeleccionado.value = ''
  busquedaPersona.value = ''
}

// Cerrar modal y limpiar
const cerrarModalCrear = () => {
  showCrearCambio.value = false
  limpiarSeleccion()
  nuevoCambio.value = { tipo_cambio: '', objeto: '', resumen: '', fecha_efecto: '', destino_id: null }
}

// Cargar usuarios disponibles
const cargarUsuariosDisponibles = async () => {
  loadingUsuarios.value = true
  try {
    const res = await axios.get(`${API_URL}/users/superiores`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    usuariosDisponibles.value = res.data.items || []
  } catch (err) {
    console.error('Error al cargar usuarios:', err)
    usuariosDisponibles.value = []
  } finally {
    loadingUsuarios.value = false
  }
}

// Computed
const isAdmin = computed(() => auth.user?.rol?.toLowerCase() === 'admin')
const puedeAutorizar = computed(() => ['admin', 'territorial'].includes(auth.user?.rol?.toLowerCase()))

// Cambios pendientes: EN_REVISION dirigidos a mí (donde yo soy el destinatario)
const cambiosPendientes = computed(() => {
  const userId = auth.user?.id
  return cambios.value.filter(c => 
    ['EN_REVISION', 'AUTORIZADO'].includes(c.estatus) && 
    c.destino_id === userId
  )
})

// Cambios enviados: propuestos por mí
const cambiosEnviados = computed(() => {
  const userId = auth.user?.id
  return cambios.value.filter(c => 
    c.propuesto_por?.persona_id === userId || c.propuesto_por_id === userId
  )
})

// Historial: cambios ya procesados (APLICADO, RECHAZADO, CANCELADO)
const cambiosHistorial = computed(() => {
  return cambios.value.filter(c => 
    ['APLICADO', 'RECHAZADO', 'CANCELADO'].includes(c.estatus)
  )
})

// Cambios filtrados según la pestaña activa
const cambiosFiltradosTab = computed(() => {
  switch (activeTab.value) {
    case 'pendientes':
      return cambiosPendientes.value
    case 'enviadas':
      return cambiosEnviados.value
    case 'historial':
      return cambiosHistorial.value
    default:
      return cambios.value
  }
})

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
    cerrarModalCrear()
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
  cargarUsuariosDisponibles()
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

/* === ESTILOS DE PESTAÑAS === */
.tabs-container {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.tabs-wrapper {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: #e5e7eb;
}

.tab-btn.active {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  border-color: transparent;
  color: white;
}

.tab-badge {
  background: #dc2626;
  color: white;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.125rem 0.375rem;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

.tab-btn.active .tab-badge {
  background: white;
  color: #16a34a;
}

.tab-badge-enviadas {
  background: #2563eb;
}

.tab-btn.active .tab-badge-enviadas {
  background: white;
  color: #2563eb;
}

.tabs-stats {
  display: flex;
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8rem;
}

.stat-label {
  color: #6b7280;
}

.stat-value {
  font-weight: 600;
}

.stat-value.pending {
  color: #dc2626;
}

.stat-value.sent {
  color: #2563eb;
}

.stat-value.approved {
  color: #16a34a;
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

/* === ESTILOS DEL SELECTOR DE DESTINATARIOS === */
.label-icon {
  display: inline;
  vertical-align: middle;
  margin-right: 0.25rem;
}

.select-wrapper {
  position: relative;
}

.form-select {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  background: white;
}

.form-select.loading-select {
  padding-right: 2.5rem;
}

.select-loading {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
}

.mini-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e5e7eb;
  border-top-color: #16a34a;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.persona-selector {
  margin-top: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.search-input-wrapper {
  position: relative;
  padding: 0.5rem;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 0.5rem 2rem;
  padding-left: 2.25rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}

.clear-search {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.25rem;
}

.personas-list {
  max-height: 200px;
  overflow-y: auto;
}

.persona-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background 0.15s;
}

.persona-item:hover {
  background: #f0fdf4;
}

.persona-item.selected {
  background: #dcfce7;
}

.persona-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #16a34a, #15803d);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  flex-shrink: 0;
}

.persona-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.persona-nombre {
  font-weight: 500;
  color: #1f2937;
  font-size: 0.875rem;
}

.persona-territorio {
  font-size: 0.75rem;
  color: #6b7280;
}

.persona-check {
  color: #16a34a;
}

.personas-empty {
  padding: 1rem;
  text-align: center;
  color: #9ca3af;
  font-size: 0.875rem;
}

.usuario-seleccionado {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.75rem 1rem;
  background: #dcfce7;
  border-radius: 8px;
  color: #16a34a;
  font-size: 0.875rem;
}

.usuario-seleccionado .check-icon {
  flex-shrink: 0;
}

.btn-limpiar {
  margin-left: auto;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
}

.btn-limpiar:hover {
  color: #dc2626;
}

.form-hint {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.hint-loading {
  color: #2563eb;
}

.hint-error {
  color: #dc2626;
}

.hint-info {
  color: #6b7280;
}
</style>
