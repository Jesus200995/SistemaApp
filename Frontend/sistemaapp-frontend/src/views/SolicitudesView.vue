<template>
  <div class="solicitudes-container">
    <!-- Menú hamburguesa global -->
    <HamburgerMenu />

    <!-- Background decorativo -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header con botón de regreso -->
    <header class="solicitudes-header">
      <div class="header-wrapper">
        <div class="header-left">
          <router-link to="/dashboard" class="back-button" title="Volver al Dashboard">
            <ArrowLeft class="back-icon" />
          </router-link>
          <div class="header-icon-small">
            <FileText class="icon-stat" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Solicitudes</h1>
            <p class="header-subtitle">Gestión de solicitudes</p>
          </div>
        </div>
        <button @click="recargarSolicitudes" class="reload-button" title="Recargar">
          <svg class="reload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M3 21v-5h5"></path>
          </svg>
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="solicitudes-main">
      <div class="solicitudes-content">
        <!-- Formulario de creación -->
        <section class="form-section">
          <div class="form-card">
            <div class="form-header">
              <h2 class="form-title">Crear Nueva Solicitud</h2>
              <p class="form-subtitle">Completa los campos para enviar una solicitud</p>
            </div>

            <form @submit.prevent="crearSolicitud" class="form-container">
              <div class="form-grid">
                <!-- Tipo de solicitud -->
                <div class="form-group">
                  <label class="form-label">
                    <FileText :size="14" class="label-icon" />
                    Tipo de Solicitud *
                  </label>
                  <select v-model="form.tipo" class="form-select" required>
                    <option value="">-- Selecciona tipo de solicitud --</option>
                    <option value="cambio_superior">Cambio de superior</option>
                    <option value="alta_subordinado">Alta de subordinado</option>
                    <option value="baja_subordinado">Baja de subordinado</option>
                    <option value="cambio_territorio">Cambio de territorio</option>
                    <option value="otro">Otro</option>
                  </select>
                </div>

                <!-- Usuario Destino - Selector en dos pasos -->
                <div class="form-group">
                  <label class="form-label">
                    <UserCheck :size="14" class="label-icon" />
                    Enviar a *
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
                        {{ formatRol(grupo.rol) }}
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
                        :class="{ 'selected': form.destino_id === usuario.id }"
                        @click="seleccionarPersona(usuario)"
                      >
                        <div class="persona-avatar">
                          {{ getInitials(usuario.nombre) }}
                        </div>
                        <div class="persona-info">
                          <span class="persona-nombre">{{ usuario.nombre }}</span>
                          <span class="persona-territorio">{{ usuario.territorio || 'Sin territorio' }}</span>
                        </div>
                        <div v-if="form.destino_id === usuario.id" class="persona-check">
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
                    <span>Enviando a: <strong>{{ usuarioSeleccionadoInfo.nombre }}</strong></span>
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

                <!-- Descripción -->
                <div class="form-group form-group-full">
                  <label class="form-label">
                    <MessageSquare :size="14" class="label-icon" />
                    Descripción o Motivo *
                  </label>
                  <textarea
                    v-model="form.descripcion"
                    placeholder="Detalla el motivo de tu solicitud..."
                    class="form-textarea"
                    required
                    rows="4"
                  ></textarea>
                </div>

                <!-- Botón de envío -->
                <button type="submit" class="form-button" :disabled="loading || !form.destino_id">
                  <Send class="button-icon" />
                  <span>{{ loading ? 'Enviando...' : 'Enviar Solicitud' }}</span>
                </button>
              </div>
            </form>
          </div>
        </section>

        <!-- Sección de solicitudes con pestañas -->
        <section class="solicitudes-section">
          <!-- Pestañas -->
          <div class="tabs-container">
            <div class="tabs-wrapper">
              <button 
                class="tab-btn" 
                :class="{ active: activeTab === 'pendientes' }"
                @click="activeTab = 'pendientes'"
              >
                <Clock :size="18" />
                <span>Mis Solicitudes</span>
                <span v-if="solicitudesPendientes.length > 0" class="tab-badge">
                  {{ solicitudesPendientes.length }}
                </span>
              </button>
              <button 
                class="tab-btn" 
                :class="{ active: activeTab === 'enviadas' }"
                @click="activeTab = 'enviadas'"
              >
                <SendHorizontal :size="18" />
                <span>Enviadas</span>
                <span v-if="solicitudesEnviadas.length > 0" class="tab-badge tab-badge-enviadas">
                  {{ solicitudesEnviadas.length }}
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
                <span class="stat-value pending">{{ solicitudesPendientes.length }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Enviadas:</span>
                <span class="stat-value sent">{{ solicitudesEnviadas.length }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Procesadas:</span>
                <span class="stat-value approved">{{ solicitudesProcesadas.length }}</span>
              </div>
            </div>
          </div>

          <!-- Tab: Mis Solicitudes (Pendientes) -->
          <div v-show="activeTab === 'pendientes'" class="tab-content">
            <div v-if="solicitudesPendientes.length > 0" class="solicitudes-cards-grid">
              <div 
                v-for="solicitud in solicitudesPendientes" 
                :key="'pending-' + solicitud.id" 
                class="solicitud-card-pending"
              >
                <!-- Barra superior PENDIENTE -->
                <div class="card-pending-topbar">
                  <span class="topbar-text">PENDIENTE</span>
                </div>
                
                <!-- Campanita animada -->
                <div class="card-bell-icon">
                  <Bell :size="18" />
                </div>
                <div class="card-pending-header">
                  <div class="card-pending-user">
                    <div class="user-avatar">
                      {{ getInitials(solicitud.solicitante?.nombre) }}
                    </div>
                    <div class="user-details">
                      <span class="user-name">{{ solicitud.solicitante?.nombre || 'Usuario' }}</span>
                      <span class="user-rol" :class="getRolClass(solicitud.solicitante?.rol)">
                        {{ formatRolUsuario(solicitud.solicitante?.rol) }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div class="card-pending-body">
                  <span class="badge" :class="getBadgeClass(solicitud.tipo)">
                    {{ formatTipo(solicitud.tipo) }}
                  </span>
                  <p class="card-pending-descripcion">{{ truncarTexto(solicitud.descripcion, 60) }}</p>
                </div>
                
                <div class="card-pending-footer">
                  <span class="card-pending-fecha">
                    <Calendar :size="14" />
                    {{ formatFecha(solicitud.fecha) }}
                  </span>
                  <button
                    @click="abrirModalDetalle(solicitud)"
                    class="btn-ver-completo"
                  >
                    <Edit :size="16" />
                    Gestionar
                  </button>
                </div>
              </div>
            </div>

            <!-- Estado vacío pendientes -->
            <div v-else class="empty-state">
              <CheckCircle class="empty-icon success" />
              <p class="empty-title">¡Sin solicitudes pendientes!</p>
              <p class="empty-text">Todas tus solicitudes han sido procesadas</p>
            </div>
          </div>

          <!-- Tab: Enviadas (solicitudes que YO envié) -->
          <div v-show="activeTab === 'enviadas'" class="tab-content">
            <div v-if="solicitudesEnviadas.length > 0" class="solicitudes-table-wrapper">
              <div class="table-responsive">
                <table class="solicitudes-table">
                  <thead>
                    <tr>
                      <th>Enviada a</th>
                      <th>Tipo</th>
                      <th>Descripción</th>
                      <th>Estado</th>
                      <th>Fecha</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="solicitud in solicitudesEnviadas" :key="'enviada-' + solicitud.id" class="solicitud-row">
                      <td class="cell-solicitante">
                        <div class="solicitante-info">
                          <span class="solicitante-nombre">{{ solicitud.destinatario?.nombre || 'Sin asignar' }}</span>
                          <span class="solicitante-rol" :class="getRolClass(solicitud.destinatario?.rol)">
                            {{ formatRolUsuario(solicitud.destinatario?.rol) }}
                          </span>
                        </div>
                      </td>
                      <td class="cell-tipo">
                        <span class="badge" :class="getBadgeClass(solicitud.tipo)">
                          {{ formatTipo(solicitud.tipo) }}
                        </span>
                      </td>
                      <td class="cell-descripcion">{{ truncateText(solicitud.descripcion, 30) }}</td>
                      <td class="cell-estado">
                        <span class="status-badge" :class="`status-${solicitud.estado}`">
                          {{ formatEstado(solicitud.estado) }}
                        </span>
                      </td>
                      <td class="cell-fecha">{{ formatFecha(solicitud.fecha) }}</td>
                      <td class="cell-acciones">
                        <button
                          @click="abrirModalDetalle(solicitud)"
                          class="btn-ver-circular"
                          title="Ver detalles"
                        >
                          <Eye :size="18" />
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Estado vacío enviadas -->
            <div v-if="solicitudesEnviadas.length === 0" class="empty-state">
              <SendHorizontal class="empty-icon" />
              <p class="empty-title">No has enviado solicitudes</p>
              <p class="empty-text">Usa el formulario de arriba para crear una nueva solicitud</p>
            </div>
          </div>

          <!-- Tab: Historial (Aprobadas/Rechazadas) -->
          <div v-show="activeTab === 'historial'" class="tab-content">
            <!-- Vista Desktop: Tabla -->
            <div v-if="solicitudesProcesadas.length > 0" class="solicitudes-table-wrapper">
              <div class="table-responsive">
                <table class="solicitudes-table">
                  <thead>
                    <tr>
                      <th>Solicitante</th>
                      <th>Tipo</th>
                      <th>Descripción</th>
                      <th>Estado</th>
                      <th>Fecha</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="solicitud in solicitudesProcesadas" :key="solicitud.id" class="solicitud-row">
                      <td class="cell-solicitante">
                        <div class="solicitante-info">
                          <span class="solicitante-nombre">{{ solicitud.solicitante?.nombre || 'N/A' }}</span>
                          <span class="solicitante-rol" :class="getRolClass(solicitud.solicitante?.rol)">
                            {{ formatRolUsuario(solicitud.solicitante?.rol) }}
                          </span>
                        </div>
                      </td>
                      <td class="cell-tipo">
                        <span class="badge" :class="getBadgeClass(solicitud.tipo)">
                          {{ formatTipo(solicitud.tipo) }}
                        </span>
                      </td>
                      <td class="cell-descripcion">{{ truncateText(solicitud.descripcion, 30) }}</td>
                      <td class="cell-estado">
                        <span class="status-badge" :class="`status-${solicitud.estado}`">
                          {{ formatEstado(solicitud.estado) }}
                        </span>
                      </td>
                      <td class="cell-fecha">{{ formatFecha(solicitud.fecha) }}</td>
                      <td class="cell-acciones">
                        <button
                          @click="abrirModalDetalle(solicitud)"
                          class="btn-ver-circular"
                          title="Ver detalles"
                        >
                          <Eye :size="18" />
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Estado vacío historial -->
            <div v-if="solicitudesProcesadas.length === 0" class="empty-state">
              <FileText class="empty-icon" />
              <p class="empty-title">Sin historial</p>
              <p class="empty-text">No hay solicitudes aprobadas o rechazadas</p>
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- Modal de Detalle de Solicitud -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="showModalDetalle" class="modal-overlay" @click.self="cerrarModalDetalle">
          <div class="modal-detalle">
            <button class="modal-close" @click="cerrarModalDetalle">
              <X :size="20" />
            </button>
            
            <div class="modal-header">
              <div class="modal-icon-wrapper">
                <FileText :size="24" />
              </div>
              <div class="modal-title-group">
                <h3 class="modal-title">Detalle de Solicitud</h3>
                <span class="badge" :class="getBadgeClass(solicitudSeleccionada?.tipo || '')">
                  {{ formatTipo(solicitudSeleccionada?.tipo || '') }}
                </span>
              </div>
            </div>

            <div class="modal-body">
              <!-- Estado de la solicitud -->
              <div class="detalle-estado">
                <span class="status-badge status-large" :class="`status-${solicitudSeleccionada?.estado}`">
                  {{ formatEstado(solicitudSeleccionada?.estado || '') }}
                </span>
              </div>

              <!-- Información del solicitante -->
              <div class="detalle-section">
                <h4 class="detalle-label">
                  <User :size="16" />
                  Información del Solicitante
                </h4>
                <div class="detalle-user-card">
                  <div class="user-card-row">
                    <span class="user-card-label">Nombre:</span>
                    <span class="user-card-value">{{ solicitudSeleccionada?.solicitante?.nombre || 'N/A' }}</span>
                  </div>
                  <div class="user-card-row">
                    <span class="user-card-label">Rol:</span>
                    <span class="user-card-value rol-badge" :class="getRolClass(solicitudSeleccionada?.solicitante?.rol)">
                      {{ formatRolUsuario(solicitudSeleccionada?.solicitante?.rol) }}
                    </span>
                  </div>
                  <div class="user-card-row">
                    <span class="user-card-label">Email:</span>
                    <span class="user-card-value email">{{ solicitudSeleccionada?.solicitante?.email || 'N/A' }}</span>
                  </div>
                  <div class="user-card-row">
                    <span class="user-card-label">CURP:</span>
                    <span class="user-card-value curp">{{ solicitudSeleccionada?.solicitante?.curp || 'No registrado' }}</span>
                  </div>
                  <div class="user-card-row">
                    <span class="user-card-label">Territorio:</span>
                    <span class="user-card-value">{{ solicitudSeleccionada?.solicitante?.territorio || 'No asignado' }}</span>
                  </div>
                  <div v-if="solicitudSeleccionada?.solicitante?.telefono" class="user-card-row">
                    <span class="user-card-label">Teléfono:</span>
                    <span class="user-card-value">{{ solicitudSeleccionada?.solicitante?.telefono }}</span>
                  </div>
                </div>
              </div>

              <!-- Destinatario -->
              <div v-if="solicitudSeleccionada?.destinatario" class="detalle-section">
                <h4 class="detalle-label">
                  <UserCheck :size="16" />
                  Dirigida a
                </h4>
                <div class="detalle-destinatario">
                  <span class="dest-nombre">{{ solicitudSeleccionada?.destinatario?.nombre }}</span>
                  <span class="dest-rol" :class="getRolClass(solicitudSeleccionada?.destinatario?.rol)">
                    {{ formatRolUsuario(solicitudSeleccionada?.destinatario?.rol) }}
                  </span>
                </div>
              </div>

              <!-- Descripción completa -->
              <div class="detalle-section">
                <h4 class="detalle-label">
                  <MessageSquare :size="16" />
                  Descripción de la Solicitud
                </h4>
                <p class="detalle-descripcion">{{ solicitudSeleccionada?.descripcion }}</p>
              </div>

              <!-- Fecha -->
              <div class="detalle-section">
                <h4 class="detalle-label">
                  <Calendar :size="16" />
                  Fecha de Solicitud
                </h4>
                <p class="detalle-value">{{ formatFechaCompleta(solicitudSeleccionada?.fecha) }}</p>
              </div>
            </div>

            <!-- Acciones del modal -->
            <div v-if="canApprove(solicitudSeleccionada) && solicitudSeleccionada?.estado === 'pendiente'" class="modal-actions">
              <button 
                @click="aprobarDesdeModal()" 
                class="btn-modal btn-aprobar"
                :disabled="procesandoAccion"
              >
                <Check :size="18" />
                {{ procesandoAccion ? 'Procesando...' : 'Aprobar Solicitud' }}
              </button>
              <button 
                @click="rechazarDesdeModal()" 
                class="btn-modal btn-rechazar"
                :disabled="procesandoAccion"
              >
                <X :size="18" />
                {{ procesandoAccion ? 'Procesando...' : 'Rechazar Solicitud' }}
              </button>
            </div>

            <!-- Mensaje si es mi solicitud enviada -->
            <div v-else-if="esMiSolicitudEnviada && solicitudSeleccionada?.estado === 'pendiente'" class="modal-processed">
              <p class="processed-text sent">
                📤 Solicitud enviada - En espera de respuesta
              </p>
            </div>

            <!-- Mensaje si ya fue procesada -->
            <div v-else-if="solicitudSeleccionada?.estado !== 'pendiente'" class="modal-processed">
              <p v-if="solicitudSeleccionada?.estado === 'aprobada'" class="processed-text approved">
                ✅ Esta solicitud fue aprobada
              </p>
              <p v-else-if="solicitudSeleccionada?.estado === 'rechazada'" class="processed-text rejected">
                ❌ Esta solicitud fue rechazada
              </p>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Footer -->
    <footer class="solicitudes-footer">
      <p>© 2025 <span class="footer-highlight">SistemaApp</span>. Solicitudes en tiempo real.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import { FileText, Send, Check, X, ArrowLeft, UserCheck, MessageSquare, Eye, Calendar, User, Clock, History, CheckCircle, Bell, Search, Edit, SendHorizontal } from 'lucide-vue-next'

const auth = useAuthStore()
const form = ref({ tipo: '', destino_id: null as number | null, descripcion: '' })
const solicitudes = ref([])
const loading = ref(false)

// Estado de las pestañas
const activeTab = ref('pendientes')

// Estado del modal de detalle
const showModalDetalle = ref(false)
const solicitudSeleccionada = ref<any>(null)
const procesandoAccion = ref(false)

// Computed: Solicitudes RECIBIDAS pendientes (donde YO soy el destino y están pendientes)
// Excluye las que YO envié
const solicitudesPendientes = computed(() => {
  const userId = auth.user?.id
  return solicitudes.value.filter((s: any) => 
    s.estado === 'pendiente' && 
    s.destino_id === userId && 
    s.usuario_id !== userId  // Excluir las que yo envié
  )
})

// Computed: Solicitudes ENVIADAS por mí (donde YO soy el solicitante)
const solicitudesEnviadas = computed(() => {
  const userId = auth.user?.id
  return solicitudes.value.filter((s: any) => s.usuario_id === userId)
})

// Computed: Solicitudes procesadas (aprobadas o rechazadas) que YO recibí
// Excluye las que yo envié (esas van en "Enviadas")
const solicitudesProcesadas = computed(() => {
  const userId = auth.user?.id
  return solicitudes.value.filter((s: any) => 
    (s.estado === 'aprobada' || s.estado === 'rechazada') && 
    s.destino_id === userId &&
    s.usuario_id !== userId  // Excluir las que yo envié
  )
})

// Obtener iniciales del nombre
const getInitials = (nombre: string | undefined) => {
  if (!nombre) return '?'
  const parts = nombre.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return nombre.substring(0, 2).toUpperCase()
}

// Usuarios disponibles para enviar solicitud
const usuariosDisponibles = ref<any[]>([])
const loadingUsuarios = ref(false)

// Variables para el selector de dos pasos
const rolSeleccionado = ref('')
const busquedaPersona = ref('')

// Personas filtradas por rol y búsqueda
const personasFiltradas = computed(() => {
  if (!rolSeleccionado.value) return []
  
  const grupo = usuariosAgrupados.value.find(g => g.rol === rolSeleccionado.value)
  if (!grupo) return []
  
  const busqueda = busquedaPersona.value.toLowerCase().trim()
  if (!busqueda) return grupo.usuarios
  
  return grupo.usuarios.filter((u: any) => 
    u.nombre?.toLowerCase().includes(busqueda) || 
    u.territorio?.toLowerCase().includes(busqueda)
  )
})

// Info del usuario seleccionado
const usuarioSeleccionadoInfo = computed(() => {
  if (!form.value.destino_id) return null
  return usuariosDisponibles.value.find(u => u.id === form.value.destino_id)
})

// Cuando cambia el rol seleccionado
const onRolChange = () => {
  form.value.destino_id = null
  busquedaPersona.value = ''
}

// Seleccionar una persona
const seleccionarPersona = (usuario: any) => {
  form.value.destino_id = usuario.id
}

// Limpiar selección
const limpiarSeleccion = () => {
  form.value.destino_id = null
  rolSeleccionado.value = ''
  busquedaPersona.value = ''
}

// Función para normalizar rol a categoría
const normalizarRol = (rol: string): string => {
  const rolLower = rol.toLowerCase().replace(/[_\s-]/g, '')
  if (rolLower.includes('admin')) return 'admin'
  if (rolLower.includes('territorial')) return 'territorial'
  if (rolLower.includes('facilitador')) return 'facilitador'
  if (rolLower.includes('tecnico') || rolLower.includes('técnico')) return 'tecnico'
  return rol // Si no coincide, usar el rol original
}

// Agrupar usuarios por rol (normalizado)
const usuariosAgrupados = computed(() => {
  const grupos: { [key: string]: any[] } = {}
  
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

// Formatear nombre del rol
const formatRol = (rol: string): string => {
  const roles: { [key: string]: string } = {
    admin: 'Administradores',
    territorial: 'Territoriales',
    facilitador: 'Facilitadores',
    tecnico: 'Técnicos'
  }
  return roles[rol] || rol
}

// Filtrar roles disponibles según el rol del usuario actual
// Jerarquía: Técnico → Facilitador → Territorial → Admin
const rolesDisponiblesParaUsuario = computed(() => {
  const rolUsuario = normalizarRol(auth.user?.rol || '')
  
  // Definir qué roles puede ver cada tipo de usuario
  const rolesPermitidos: { [key: string]: string[] } = {
    tecnico: ['facilitador', 'territorial'],     // Técnico puede enviar a Facilitadores y Territoriales
    facilitador: ['territorial', 'admin'],       // Facilitador puede enviar a Territoriales y Admin
    territorial: ['admin'],                      // Territorial puede enviar a Admin
    admin: ['admin', 'territorial', 'facilitador', 'tecnico'] // Admin puede enviar a todos
  }
  
  const permitidos = rolesPermitidos[rolUsuario] || []
  
  // Si es admin, mostrar todos los roles disponibles
  if (rolUsuario === 'admin') {
    return usuariosAgrupados.value
  }
  
  // Filtrar solo los roles permitidos para este usuario
  return usuariosAgrupados.value.filter(grupo => permitidos.includes(grupo.rol))
})

// Cargar usuarios disponibles
const cargarUsuariosDisponibles = async () => {
  loadingUsuarios.value = true
  try {
    const apiUrl = getSecureApiUrl()
    console.log('🔍 Cargando usuarios superiores desde:', `${apiUrl}/users/superiores`)
    const res = await axios.get(`${apiUrl}/users/superiores`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    console.log('✅ Usuarios recibidos:', res.data)
    usuariosDisponibles.value = res.data.items || []
    
    if (usuariosDisponibles.value.length === 0) {
      console.warn('⚠️ No se encontraron usuarios superiores disponibles')
    }
  } catch (err: any) {
    console.error('❌ Error al cargar usuarios:', err.response?.data || err.message)
    usuariosDisponibles.value = []
    
    // Si el error es 404, puede que el endpoint no exista en el servidor
    if (err.response?.status === 404) {
      console.error('⚠️ El endpoint /users/superiores no existe. Asegúrate de actualizar el servidor.')
    }
  } finally {
    loadingUsuarios.value = false
  }
}

// Funciones auxiliares
const formatTipo = (tipo: string) => {
  const tipos: { [key: string]: string } = {
    cambio_superior: 'Cambio de Superior',
    alta_subordinado: 'Alta de Subordinado',
    baja_subordinado: 'Baja de Subordinado',
    cambio_territorio: 'Cambio de Territorio',
    otro: 'Otro'
  }
  return tipos[tipo] || tipo
}

const formatEstado = (estado: string) => {
  const estados: { [key: string]: string } = {
    pendiente: 'Pendiente',
    aprobada: 'Aprobada',
    rechazada: 'Rechazada'
  }
  return estados[estado] || estado
}

const formatFecha = (fecha: string) => {
  // Usar zona horaria CDMX
  const fechaStr = fecha.includes('T') ? fecha.split('T')[0] : fecha
  const [year, month, day] = fechaStr.split('-').map(Number)
  const date = new Date(year, month - 1, day, 12, 0, 0)
  
  return date.toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    timeZone: 'America/Mexico_City'
  })
}

// Truncar texto con puntos suspensivos
const truncarTexto = (texto: string, maxLength: number): string => {
  if (!texto) return ''
  return texto.length > maxLength ? texto.substring(0, maxLength) + '...' : texto
}

const getBadgeClass = (tipo: string) => {
  const tipos: { [key: string]: string } = {
    cambio_superior: 'badge-blue',
    alta_subordinado: 'badge-green',
    baja_subordinado: 'badge-red',
    cambio_territorio: 'badge-purple',
    otro: 'badge-gray'
  }
  return tipos[tipo] || 'badge-gray'
}

// Formatear rol del usuario para mostrar
const formatRolUsuario = (rol: string): string => {
  if (!rol) return 'N/A'
  const rolLower = rol.toLowerCase()
  if (rolLower.includes('admin')) return 'Admin'
  if (rolLower.includes('territorial')) return 'Territorial'
  if (rolLower.includes('facilitador')) return 'Facilitador'
  if (rolLower.includes('tecnico') || rolLower.includes('técnico')) {
    if (rolLower.includes('productivo')) return 'Téc. Productivo'
    if (rolLower.includes('social')) return 'Téc. Social'
    return 'Técnico'
  }
  return rol
}

// Clase CSS según el rol
const getRolClass = (rol: string): string => {
  if (!rol) return ''
  const rolLower = rol.toLowerCase()
  if (rolLower.includes('admin')) return 'rol-admin'
  if (rolLower.includes('territorial')) return 'rol-territorial'
  if (rolLower.includes('facilitador')) return 'rol-facilitador'
  if (rolLower.includes('tecnico') || rolLower.includes('técnico')) return 'rol-tecnico'
  return ''
}

const countByStatus = (estado: string) => {
  return solicitudes.value.filter(s => s.estado === estado).length
}

// Truncar texto
const truncateText = (text: string, maxLength: number) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

// Formato de fecha completa
const formatFechaCompleta = (fecha: string) => {
  if (!fecha) return ''
  const fechaStr = fecha.includes('T') ? fecha.split('T')[0] : fecha
  const [year, month, day] = fechaStr.split('-').map(Number)
  const date = new Date(year, month - 1, day, 12, 0, 0)
  
  return date.toLocaleDateString('es-MX', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'America/Mexico_City'
  })
}

// Funciones del modal de detalle
const abrirModalDetalle = (solicitud: any) => {
  solicitudSeleccionada.value = solicitud
  showModalDetalle.value = true
  document.body.style.overflow = 'hidden'
}

const cerrarModalDetalle = () => {
  showModalDetalle.value = false
  solicitudSeleccionada.value = null
  procesandoAccion.value = false
  document.body.style.overflow = ''
}

// Aprobar/Rechazar desde modal
const aprobarDesdeModal = async () => {
  if (!solicitudSeleccionada.value) return
  procesandoAccion.value = true
  await actualizarEstado(solicitudSeleccionada.value.id, 'aprobada')
  cerrarModalDetalle()
}

const rechazarDesdeModal = async () => {
  if (!solicitudSeleccionada.value) return
  procesandoAccion.value = true
  await actualizarEstado(solicitudSeleccionada.value.id, 'rechazada')
  cerrarModalDetalle()
}

const canApprove = (solicitud: any) => {
  // NUNCA puede aprobar sus propias solicitudes
  if (solicitud?.usuario_id === auth.user?.id) return false
  
  // Admin puede aprobar todas (excepto las propias)
  if (auth.user?.rol === 'admin') return true
  
  // Territorial/Facilitador puede aprobar las dirigidas a él
  if (auth.user?.rol === 'territorial' || auth.user?.rol === 'facilitador') {
    return solicitud.destino_id === auth.user?.id
  }
  return false
}

// Computed para verificar si la solicitud seleccionada fue enviada por mí
const esMiSolicitudEnviada = computed(() => {
  return solicitudSeleccionada.value?.usuario_id === auth.user?.id
})

// API calls
const getSolicitudes = async () => {
  try {
    const apiUrl = getSecureApiUrl()
    console.log('📡 getSolicitudes - URL:', apiUrl)
    console.log('🔑 getSolicitudes - Token:', auth.token ? 'Presente' : 'AUSENTE')
    
    if (!auth.token) {
      console.error('❌ getSolicitudes - No hay token de autenticación')
      return
    }
    
    const res = await axios.get(`${apiUrl}/solicitudes`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    solicitudes.value = res.data
    console.log('✅ getSolicitudes - Recibidas:', res.data?.length || 0, 'solicitudes')
  } catch (err) {
    console.error('❌ Error al obtener solicitudes:', err.response?.status, err.response?.data || err.message)
    if (err.response?.status === 401) {
      console.log('🔒 Token inválido en getSolicitudes')
    }
  }
}

const crearSolicitud = async () => {
  if (!form.value.tipo || !form.value.descripcion) {
    await Swal.fire('⚠️ Campos requeridos', 'Completa el tipo y la descripción', 'warning')
    return
  }

  loading.value = true
  try {
    const payload: any = {
      tipo: form.value.tipo,
      descripcion: form.value.descripcion
    }
    if (form.value.destino_id) {
      payload.destino_id = parseInt(form.value.destino_id as any)
    }

    const apiUrl = getSecureApiUrl()
    await axios.post(`${apiUrl}/solicitudes`, payload, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })

    await Swal.fire('✅ Enviada', 'La solicitud se ha registrado correctamente', 'success')
    form.value = { tipo: '', destino_id: null, descripcion: '' }
    await getSolicitudes()
  } catch (err: any) {
    await Swal.fire(
      '❌ Error',
      err.response?.data?.detail || 'No se pudo enviar la solicitud',
      'error'
    )
  } finally {
    loading.value = false
  }
}

const actualizarEstado = async (id: number, nuevo_estado: string) => {
  const confirmacion = await Swal.fire({
    title: '¿Confirmar acción?',
    text: `¿Deseas ${nuevo_estado === 'aprobada' ? 'aprobar' : 'rechazar'} esta solicitud?`,
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Sí, confirmar',
    cancelButtonText: 'Cancelar'
  })

  if (!confirmacion.isConfirmed) return

  try {
    const apiUrl = getSecureApiUrl()
    await axios.put(
      `${apiUrl}/solicitudes/${id}/estado`,
      { estado: nuevo_estado },
      { headers: { Authorization: `Bearer ${auth.token}` } }
    )

    await Swal.fire('✅ Actualizada', 'El estado se actualizó correctamente', 'success')
    await getSolicitudes()
  } catch (err: any) {
    await Swal.fire('❌ Error', err.response?.data?.detail || 'No se pudo actualizar', 'error')
  }
}

const recargarSolicitudes = async () => {
  loading.value = true
  try {
    await getSolicitudes()
    await cargarUsuariosDisponibles()
    await Swal.fire('✅ Recargado', 'Las solicitudes se han actualizado', 'success')
  } catch (err) {
    await Swal.fire('❌ Error', 'No se pudo recargar las solicitudes', 'error')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await Promise.all([
    getSolicitudes(),
    cargarUsuariosDisponibles()
  ])
})
</script>

<style scoped>
/* ========== VARIABLES ========== */
:root {
  --color-primary: #16a34a;
  --color-primary-dark: #15803d;
  --color-bg-primary: #f0fdf4;
  --color-bg-secondary: #dcfce7;
  --color-bg-tertiary: #f0fdf4;
  --color-text-primary: #1e3a2f;
  --color-text-secondary: #374151;
  --color-text-dim: #64748b;
  --color-border: rgba(22, 163, 74, 0.15);
  --color-blue: #3b82f6;
  --color-red: #ef4444;
  --color-yellow: #f59e0b;
  --color-purple: #8b5cf6;
}

/* ========== LAYOUT ========== */
.solicitudes-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #f0fdf4 100%);
  position: relative;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: flex;
  flex-direction: column;
}

/* ========== BACKGROUND BLOBS ========== */
.background-blobs {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.blob {
  position: absolute;
  opacity: 0.3;
  filter: blur(120px);
  mix-blend-mode: multiply;
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
.solicitudes-header {
  position: relative;
  z-index: 10;
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(22, 163, 74, 0.2);
  backdrop-filter: blur(12px);
  padding: 1rem 1.2rem;
  box-shadow: 0 4px 20px rgba(22, 163, 74, 0.1);
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
  background: rgba(255, 255, 255, 0.9);
  border: 1.5px solid rgba(22, 163, 74, 0.4);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  color: #16a34a;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.back-button:hover {
  background: rgba(22, 163, 74, 0.1);
  transform: translateX(-4px);
  box-shadow: 0 4px 15px rgba(22, 163, 74, 0.3);
  border-color: rgba(22, 163, 74, 0.6);
}

.back-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2.5;
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
  color: #16a34a;
  stroke-width: 2;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #15803d;
  margin: 0;
}

.header-subtitle {
  font-size: 0.75rem;
  color: #64748b;
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

/* ========== MAIN CONTENT ========== */
.solicitudes-main {
  flex: 1;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem 1rem;
  overflow-y: auto;
  position: relative;
  z-index: 5;
}

.solicitudes-content {
  width: 100%;
  max-width: 1000px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ========== FORM SECTION ========== */
.form-section {
  position: relative;
}

.form-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(22, 163, 74, 0.2);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(22, 163, 74, 0.1);
}

.form-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.form-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #15803d;
  margin: 0 0 0.3rem 0;
}

.form-subtitle {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

.form-container {
  width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group-full {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.form-select,
.form-input,
.form-textarea {
  background: white;
  border: 1px solid rgba(22, 163, 74, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #1e3a2f;
  font-size: 0.9rem;
  font-family: inherit;
  transition: all 0.3s ease;
  width: 100%;
  box-sizing: border-box;
}

.form-select:focus,
.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
  background: white;
}

.form-input {
  height: 44px;
}

.form-select {
  height: 46px;
  padding-right: 2.5rem;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 16px;
  cursor: pointer;
}

.form-select:hover {
  border-color: rgba(22, 163, 74, 0.5);
}

/* ========== SELECT MEJORADO ========== */
.select-wrapper {
  position: relative;
}

.form-select optgroup {
  background: #f0fdf4;
  color: #15803d;
  font-weight: 600;
  padding: 0.5rem;
}

.form-select option {
  background: white;
  color: #1e3a2f;
  padding: 0.5rem;
}

.loading-select {
  opacity: 0.7;
  pointer-events: none;
}

.select-loading {
  position: absolute;
  right: 2.5rem;
  top: 50%;
  transform: translateY(-50%);
}

.mini-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(16, 185, 129, 0.3);
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========== LABEL CON ICONO ========== */
.label-icon {
  display: inline-block;
  vertical-align: middle;
  margin-right: 0.35rem;
  color: #16a34a;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-hint {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 0.35rem;
}

.hint-loading {
  color: #64748b;
}

.hint-error {
  color: #f59e0b;
}

.hint-success {
  color: #16a34a;
}

.hint-info {
  color: #94a3b8;
}

/* ========== SELECTOR DE PERSONA EN DOS PASOS ========== */
.persona-selector {
  margin-top: 0.75rem;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(22, 163, 74, 0.2);
  border-radius: 12px;
  padding: 0.75rem;
}

.search-input-wrapper {
  position: relative;
  margin-bottom: 0.75rem;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
}

.search-input {
  width: 100%;
  padding: 0.6rem 2.5rem 0.6rem 2.5rem;
  background: white;
  border: 1px solid rgba(22, 163, 74, 0.3);
  border-radius: 8px;
  color: #1e3a2f;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: rgba(22, 163, 74, 0.5);
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}

.search-input::placeholder {
  color: #64748b;
}

.clear-search {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(239, 68, 68, 0.2);
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ef4444;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-search:hover {
  background: rgba(239, 68, 68, 0.3);
}

.personas-list {
  max-height: 200px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.personas-list::-webkit-scrollbar {
  width: 6px;
}

.personas-list::-webkit-scrollbar-track {
  background: rgba(22, 163, 74, 0.1);
  border-radius: 3px;
}

.personas-list::-webkit-scrollbar-thumb {
  background: rgba(22, 163, 74, 0.4);
  border-radius: 3px;
}

.persona-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.6rem 0.75rem;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(22, 163, 74, 0.15);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.persona-item:hover {
  background: rgba(22, 163, 74, 0.1);
  border-color: rgba(22, 163, 74, 0.3);
}

.persona-item.selected {
  background: rgba(22, 163, 74, 0.15);
  border-color: rgba(22, 163, 74, 0.5);
}

.persona-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: transparent;
  border: 2px solid #16a34a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: #16a34a;
  flex-shrink: 0;
}

.persona-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.persona-nombre {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1e3a2f;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.persona-territorio {
  font-size: 0.7rem;
  color: #94a3b8;
}

.persona-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #10b981;
  flex-shrink: 0;
}

.personas-empty {
  text-align: center;
  padding: 1rem;
  color: #94a3b8;
  font-size: 0.8rem;
}

/* Usuario seleccionado */
.usuario-seleccionado {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.6rem 0.75rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  font-size: 0.8rem;
  color: #10b981;
}

.usuario-seleccionado .check-icon {
  color: #16a34a;
}

.usuario-seleccionado strong {
  color: #1e3a2f;
}

.btn-limpiar {
  margin-left: auto;
  background: rgba(239, 68, 68, 0.15);
  border: none;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ef4444;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-limpiar:hover {
  background: rgba(239, 68, 68, 0.3);
}

.form-button {
  grid-column: 1 / -1;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border: none;
  color: white;
  padding: 0.875rem 1.5rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.form-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.form-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-icon {
  width: 18px;
  height: 18px;
}

/* ========== SOLICITUDES SECTION ========== */
.solicitudes-section {
  position: relative;
}

/* ========== TABS ========== */
.tabs-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  padding-bottom: 0;
  flex-wrap: wrap;
  gap: 1rem;
}

.tabs-wrapper {
  display: flex;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 4px;
  border: 1px solid rgba(22, 163, 74, 0.2);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.25rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.tab-btn:hover {
  color: #1e3a2f;
  background: rgba(22, 163, 74, 0.1);
}

.tab-btn.active {
  color: #10b981;
  background: rgba(16, 185, 129, 0.15);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  font-size: 0.7rem;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #f87171, #ef4444);
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(248, 113, 113, 0.5);
}

.tab-badge.tab-badge-enviadas {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

.tab-badge.historial {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
}

.tabs-stats {
  display: flex;
  gap: 1rem;
}

.tabs-stats .stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.tabs-stats .stat-value.rejected {
  color: #a855f7;
}

/* ========== TAB CONTENT ========== */
.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ========== CARDS GRID (Pendientes) ========== */
.solicitudes-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1rem;
}

.solicitud-card-pending {
  position: relative;
  background: linear-gradient(90deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(254, 202, 202, 0.2) 25%, 
    rgba(254, 202, 202, 0.15) 50%, 
    rgba(254, 202, 202, 0.2) 75%, 
    rgba(255, 255, 255, 0.95) 100%
  );
  background-size: 200% 100%;
  border-radius: 16px;
  padding: 1.25rem;
  padding-top: 2.5rem; /* Espacio para la barra superior */
  border: 1px solid rgba(248, 113, 113, 0.3);
  border-left: 4px solid #f87171;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  overflow: visible;
  margin-top: 10px;
  animation: cardShimmer 5s ease-in-out infinite;
}

/* Barra superior PENDIENTE */
.card-pending-topbar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 24px;
  background: linear-gradient(90deg, rgba(248, 113, 113, 0.3) 0%, rgba(248, 113, 113, 0.15) 50%, rgba(248, 113, 113, 0.3) 100%);
  border-radius: 16px 16px 0 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(248, 113, 113, 0.25);
}

.topbar-text {
  font-size: 0.65rem;
  font-weight: 700;
  color: #f87171;
  letter-spacing: 2px;
  text-transform: uppercase;
}

@keyframes cardShimmer {
  0% { 
    background-position: 100% 0;
  }
  50% { 
    background-position: 0% 0;
  }
  100% { 
    background-position: 100% 0;
  }
}

.solicitud-card-pending:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(248, 113, 113, 0.15);
  border-color: rgba(248, 113, 113, 0.5);
  animation-play-state: paused;
  background: linear-gradient(135deg, rgba(254, 202, 202, 0.3), rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.98));
  background-size: 100% 100%;
}

.solicitud-card-pending:hover .card-bell-icon {
  animation: bellShake 0.8s ease-in-out infinite;
}

/* Campanita animada - Círculo rojo vidrio líquido pequeño */
.card-bell-icon {
  position: absolute;
  top: -10px;
  right: -6px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(ellipse at 30% 30%, rgba(252, 165, 165, 0.6), rgba(248, 113, 113, 0.4) 50%, rgba(239, 68, 68, 0.3));
  border: 1.5px solid rgba(248, 113, 113, 0.6);
  backdrop-filter: blur(12px);
  box-shadow: 
    0 3px 12px rgba(248, 113, 113, 0.4),
    0 0 15px rgba(248, 113, 113, 0.2),
    inset 0 1px 3px rgba(255, 255, 255, 0.3),
    inset 0 -1px 3px rgba(0, 0, 0, 0.1);
  color: white;
  animation: bellShake 2s ease-in-out infinite;
  z-index: 10;
}

.card-bell-icon svg {
  width: 14px;
  height: 14px;
}

@keyframes bellShake {
  0%, 100% { transform: rotate(0deg); }
  10% { transform: rotate(14deg); }
  20% { transform: rotate(-12deg); }
  30% { transform: rotate(10deg); }
  40% { transform: rotate(-8deg); }
  50% { transform: rotate(6deg); }
  60% { transform: rotate(-4deg); }
  70% { transform: rotate(2deg); }
  80%, 100% { transform: rotate(0deg); }
}

.card-pending-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.card-pending-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: transparent;
  border: 2px solid #00ff88;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: #00ff88;
  box-shadow: 0 0 15px rgba(0, 255, 136, 0.4), inset 0 0 10px rgba(0, 255, 136, 0.1);
  text-shadow: 0 0 8px rgba(0, 255, 136, 0.6);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e3a2f;
}

.user-rol {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
  background: rgba(0, 255, 136, 0.1);
  color: #00ff88;
  border: 1px solid rgba(0, 255, 136, 0.3);
  text-shadow: 0 0 8px rgba(0, 255, 136, 0.5);
}

.status-pendiente {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 4px 10px;
  background: rgba(248, 113, 113, 0.15);
  color: #f87171;
  border-radius: 6px;
  border: 1px solid rgba(248, 113, 113, 0.3);
}

.card-pending-body {
  margin-bottom: 1rem;
}

.card-pending-body .badge {
  margin-bottom: 0.75rem;
  border-radius: 20px;
  padding: 0.4rem 1rem;
}

.card-pending-descripcion {
  font-size: 0.85rem;
  color: #374151;
  line-height: 1.5;
  margin: 0;
}

.card-pending-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.card-pending-fecha {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  color: #94a3b8;
}

.btn-ver-completo {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #93c5fd;
  background: rgba(59, 130, 246, 0.2);
  border: 1.5px solid rgba(59, 130, 246, 0.4);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-ver-completo:hover {
  transform: translateY(-2px);
  background: rgba(59, 130, 246, 0.35);
  border-color: rgba(96, 165, 250, 0.6);
  color: #bfdbfe;
}

.btn-ver-completo:active {
  transform: scale(0.98);
}

/* Empty state icon success */
.empty-icon.success {
  color: #10b981;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.15);
  flex-wrap: wrap;
  gap: 0.75rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1e3a2f;
  margin: 0;
}

.section-stats {
  display: flex;
  gap: 1.25rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 0.65rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e3a2f;
}

.stat-value.pending {
  color: #f87171;
}

.stat-value.sent {
  color: #3b82f6;
}

.stat-value.approved {
  color: #16a34a;
}

/* ========== TABLE ========== */
.solicitudes-table-wrapper {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(22, 163, 74, 0.2);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.table-responsive {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.solicitudes-table {
  width: 100%;
  min-width: 650px;
  border-collapse: collapse;
  font-size: 0.85rem;
  table-layout: fixed;
}

.solicitudes-table thead {
  background: linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%);
  border-bottom: 2px solid rgba(22, 163, 74, 0.3);
}

.solicitudes-table th {
  padding: 0.85rem;
  text-align: left;
  font-weight: 600;
  color: #10b981;
  text-transform: uppercase;
  font-size: 0.7rem;
  letter-spacing: 0.05em;
}

.solicitudes-table th:last-child {
  text-align: center;
}

.solicitud-row {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  transition: all 0.3s ease;
}

.solicitud-row:hover {
  background: rgba(16, 185, 129, 0.05);
}

.solicitudes-table td {
  padding: 0.85rem;
  color: #374151;
}

/* ========== CELDA SOLICITANTE ========== */
.cell-solicitante {
  width: 18%;
  min-width: 110px;
}

.solicitante-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.solicitante-nombre {
  font-weight: 600;
  color: #1e3a2f;
  font-size: 0.85rem;
}

.solicitante-rol {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
  background: rgba(0, 255, 136, 0.1);
  color: #00ff88;
  border: 1px solid rgba(0, 255, 136, 0.3);
  text-shadow: 0 0 8px rgba(0, 255, 136, 0.5);
}

/* Clases de rol - Todos en verde neon */
.rol-admin,
.rol-territorial,
.rol-facilitador,
.rol-tecnico {
  background: rgba(0, 255, 136, 0.1);
  color: #00ff88;
  border: 1px solid rgba(0, 255, 136, 0.3);
  text-shadow: 0 0 8px rgba(0, 255, 136, 0.5);
}

.cell-tipo {
  width: 15%;
  min-width: 100px;
}

.cell-descripcion {
  width: 25%;
  min-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cell-estado {
  width: 12%;
  min-width: 90px;
}

.cell-fecha {
  width: 13%;
  min-width: 90px;
  font-size: 0.8rem;
}

.cell-acciones {
  width: 10%;
  min-width: 60px;
  text-align: center;
}

.cell-acciones .btn-ver-circular {
  margin: 0 auto;
}

/* ========== BADGES ========== */
.badge {
  display: inline-block;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-green {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.badge-blue {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.badge-red {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.badge-purple {
  background: rgba(139, 92, 246, 0.15);
  color: #8b5cf6;
}

.badge-gray {
  background: rgba(148, 163, 184, 0.15);
  color: #64748b;
}

/* ========== STATUS BADGES ========== */
.status-badge {
  display: inline-block;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-pendiente {
  background: rgba(248, 113, 113, 0.15);
  color: #f87171;
}

.status-aprobada {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.status-rechazada {
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}

/* ========== ACTION BUTTONS ========== */
.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.approve-btn {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.approve-btn:hover {
  background: rgba(16, 185, 129, 0.3);
  transform: translateY(-2px);
}

.reject-btn {
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}

.reject-btn:hover {
  background: rgba(168, 85, 247, 0.3);
  transform: translateY(-2px);
}

.action-icon {
  width: 18px;
  height: 18px;
}

/* ========== BOTÓN VER CIRCULAR AZUL VIDRIO LÍQUIDO ========== */
.btn-ver-circular {
  width: 38px;
  height: 38px;
  min-width: 38px;
  min-height: 38px;
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(ellipse at 30% 30%, rgba(96, 165, 250, 0.4), rgba(59, 130, 246, 0.2) 50%, rgba(37, 99, 235, 0.15));
  border: 1.5px solid rgba(96, 165, 250, 0.5);
  color: #93c5fd;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(12px);
  box-shadow: 
    0 4px 20px rgba(59, 130, 246, 0.3),
    0 0 30px rgba(59, 130, 246, 0.15),
    inset 0 2px 4px rgba(255, 255, 255, 0.2),
    inset 0 -2px 4px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
}

.btn-ver-circular:hover {
  background: radial-gradient(ellipse at 30% 30%, rgba(147, 197, 253, 0.5), rgba(96, 165, 250, 0.35) 50%, rgba(59, 130, 246, 0.25));
  border-color: rgba(147, 197, 253, 0.7);
  transform: scale(1.15);
  box-shadow: 
    0 8px 30px rgba(59, 130, 246, 0.45),
    0 0 40px rgba(96, 165, 250, 0.3),
    inset 0 2px 6px rgba(255, 255, 255, 0.3),
    inset 0 -2px 6px rgba(0, 0, 0, 0.1);
  color: #bfdbfe;
}

.btn-ver-circular:active {
  transform: scale(0.95);
  box-shadow: 
    0 2px 10px rgba(59, 130, 246, 0.3),
    inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Centrar la celda de acciones */
.cell-acciones {
  text-align: center !important;
  display: flex !important;
  align-items: center;
  justify-content: center;
}

/* ========== BOTÓN VER DETALLE ========== */
.view-btn {
  background: rgba(99, 102, 241, 0.15);
  color: #818cf8;
}

.view-btn:hover {
  background: rgba(99, 102, 241, 0.3);
  transform: translateY(-2px);
}

/* ========== MOBILE CARDS ========== */
.mobile-view {
  display: none;
}

.desktop-view {
  display: block;
}

.solicitudes-cards {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.solicitud-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(22, 163, 74, 0.15);
  transition: all 0.3s ease;
}

.solicitud-card:hover {
  border-color: rgba(22, 163, 74, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(22, 163, 74, 0.1);
}

.solicitud-card.card-pending {
  border-left: 3px solid #f87171;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.card-solicitante {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.solicitante-nombre-card {
  font-weight: 600;
  color: #1e3a2f;
  font-size: 0.9rem;
}

.solicitante-rol-card {
  font-size: 0.65rem;
  font-weight: 500;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
}

.card-tipo-row {
  margin-bottom: 0.5rem;
}

.badge-small {
  font-size: 0.65rem;
  padding: 0.2rem 0.5rem;
}

.status-small {
  font-size: 0.6rem;
  padding: 0.2rem 0.4rem;
}

.card-descripcion {
  font-size: 0.85rem;
  color: #374151;
  margin: 0 0 0.75rem 0;
  line-height: 1.4;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-fecha {
  font-size: 0.75rem;
  color: #94a3b8;
}

.btn-ver-detalle {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #818cf8;
  background: rgba(99, 102, 241, 0.15);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-ver-detalle:hover {
  background: rgba(99, 102, 241, 0.3);
}

/* ========== MODAL DETALLE ========== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(22, 163, 74, 0.2);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.modal-detalle {
  background: white;
  border-radius: 16px;
  border: 1px solid rgba(22, 163, 74, 0.2);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 60px rgba(22, 163, 74, 0.15);
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.15);
  border: none;
  color: #ef4444;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
}

.modal-close:hover {
  background: rgba(239, 68, 68, 0.3);
  transform: scale(1.1);
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(22, 163, 74, 0.15);
}

.modal-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.2), rgba(21, 128, 61, 0.2));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #16a34a;
}

.modal-title-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.modal-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e3a2f;
  margin: 0;
}

.modal-body {
  padding: 1.5rem;
}

.detalle-estado {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.status-large {
  font-size: 0.9rem;
  padding: 0.5rem 1.25rem;
}

.detalle-section {
  margin-bottom: 1.25rem;
}

.detalle-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  margin: 0 0 0.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detalle-label svg {
  color: #16a34a;
}

.detalle-value {
  font-size: 0.9rem;
  color: #1e3a2f;
  margin: 0;
}

.detalle-user-info {
  background: rgba(22, 163, 74, 0.05);
  border-radius: 8px;
  padding: 0.75rem;
  border: 1px solid rgba(22, 163, 74, 0.1);
}

/* Card de usuario en el modal */
.detalle-user-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 1rem;
  border: 1px solid rgba(22, 163, 74, 0.15);
}

.user-card-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(22, 163, 74, 0.08);
}

.user-card-row:last-child {
  border-bottom: none;
}

.user-card-label {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 500;
}

.user-card-value {
  font-size: 0.85rem;
  color: #1e3a2f;
  font-weight: 500;
  text-align: right;
}

.user-card-value.rol-badge {
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  background: rgba(22, 163, 74, 0.1);
  color: #16a34a;
  border: 1px solid rgba(22, 163, 74, 0.3);
}

.user-card-value.email {
  color: #60a5fa;
  font-size: 0.8rem;
}

.user-card-value.curp {
  font-family: monospace;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
}

/* Destinatario en modal */
.detalle-destinatario {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(22, 163, 74, 0.05);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  border: 1px solid rgba(22, 163, 74, 0.1);
}

.dest-nombre {
  font-size: 0.9rem;
  color: #1e3a2f;
  font-weight: 500;
}

.dest-rol {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  background: rgba(22, 163, 74, 0.1);
  color: #16a34a;
  border: 1px solid rgba(22, 163, 74, 0.3);
}

.user-name {
  font-size: 0.9rem;
  color: #1e3a2f;
  margin: 0;
  font-weight: 500;
}

.detalle-descripcion {
  font-size: 0.9rem;
  color: #374151;
  line-height: 1.6;
  margin: 0;
  background: rgba(22, 163, 74, 0.05);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid rgba(22, 163, 74, 0.1);
}

/* ========== ACCIONES DEL MODAL ========== */
.modal-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  border-top: 1px solid rgba(22, 163, 74, 0.15);
  background: rgba(240, 253, 244, 0.5);
}

.btn-modal {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.85rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-modal:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-aprobar {
  background: linear-gradient(135deg, #059669, #047857);
  color: white;
  box-shadow: 0 4px 15px rgba(5, 150, 105, 0.3);
}

.btn-aprobar:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4);
}

.btn-rechazar {
  background: linear-gradient(135deg, #a855f7, #8b5cf6);
  color: white;
  box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
}

.btn-rechazar:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4);
}

.modal-processed {
  padding: 1.25rem 1.5rem;
  text-align: center;
  border-top: 1px solid rgba(22, 163, 74, 0.15);
}

.processed-text {
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0;
}

.processed-text.approved {
  color: #10b981;
}

.processed-text.rejected {
  color: #a855f7;
}

.processed-text.sent {
  color: #3b82f6;
}

/* ========== ANIMACIONES DEL MODAL ========== */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-detalle,
.modal-fade-leave-to .modal-detalle {
  transform: scale(0.9) translateY(20px);
}

/* ========== EMPTY STATE ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  background: rgba(255, 255, 255, 0.9);
  border: 1px dashed rgba(22, 163, 74, 0.3);
  border-radius: 12px;
  text-align: center;
}

.empty-icon {
  width: 36px;
  height: 36px;
  color: #16a34a;
  margin-bottom: 0.75rem;
  opacity: 0.8;
}

.empty-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e3a2f;
  margin: 0 0 0.35rem 0;
}

.empty-text {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

/* ========== FOOTER ========== */
.solicitudes-footer {
  position: relative;
  z-index: 5;
  text-align: center;
  padding: 1.25rem;
  border-top: 1px solid rgba(22, 163, 74, 0.2);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  font-size: 0.8rem;
  color: #64748b;
}

.footer-highlight {
  color: #16a34a;
  font-weight: 700;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  /* Tabs responsive */
  .tabs-container {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }
  
  .tabs-wrapper {
    width: 100%;
    justify-content: center;
  }
  
  .tab-btn {
    flex: 1;
    justify-content: center;
    padding: 0.6rem 0.75rem;
    font-size: 0.8rem;
  }
  
  .tab-btn span:not(.tab-badge) {
    display: none;
  }
  
  .tabs-stats {
    justify-content: center;
    width: 100%;
  }
  
  /* Cards grid responsive */
  .solicitudes-cards-grid {
    grid-template-columns: 1fr;
  }
  
  .solicitud-card-pending {
    padding: 1rem;
    padding-top: 2.2rem; /* Espacio para la barra PENDIENTE */
    margin-top: 10px;
  }
  
  .card-pending-topbar {
    height: 22px;
  }
  
  .topbar-text {
    font-size: 0.6rem;
  }
  
  .card-bell-icon {
    width: 24px;
    height: 24px;
    top: -8px;
    right: -5px;
  }
  
  .card-bell-icon svg {
    width: 12px;
    height: 16px;
  }
  
  .user-avatar {
    width: 36px;
    height: 36px;
    min-width: 36px;
    min-height: 36px;
    font-size: 0.75rem;
    border-radius: 50%;
  }
  
  /* Botón ver circular responsive */
  .btn-ver-circular {
    width: 34px;
    height: 34px;
    min-width: 34px;
    min-height: 34px;
  }
  
  .user-name {
    font-size: 0.85rem;
  }
  
  .solicitudes-header {
    padding: 0.8rem 1rem;
  }

  .header-icon-small {
    width: 28px;
    height: 28px;
  }

  .icon-stat {
    width: 18px;
    height: 18px;
  }

  .header-title {
    font-size: 0.85rem;
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

  .solicitudes-main {
    padding: 1rem 0.5rem;
  }

  .form-title {
    font-size: 1.1rem;
  }

  .form-card {
    padding: 1.5rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
  
  /* Modal responsive */
  .modal-detalle {
    max-width: 95%;
    margin: 0.5rem;
  }
  
  .modal-header {
    padding: 1.25rem;
  }
  
  .modal-icon-wrapper {
    width: 40px;
    height: 40px;
  }
  
  .modal-title {
    font-size: 1rem;
  }
  
  .modal-body {
    padding: 1.25rem;
  }
  
  .modal-actions {
    padding: 1rem 1.25rem;
  }
  
  .btn-modal {
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
  }

  /* Centrar sección de historial en móviles */
  .section-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .section-title {
    margin-bottom: 0.5rem;
  }

  .section-stats {
    justify-content: center;
    width: 100%;
  }
  
  /* Tabla responsive */
  .solicitudes-table-wrapper {
    margin: 0 -0.5rem;
    border-radius: 8px;
  }
  
  .solicitudes-table {
    min-width: 600px;
    font-size: 0.75rem;
  }
  
  .solicitudes-table th,
  .solicitudes-table td {
    padding: 0.6rem 0.5rem;
  }
  
  .cell-solicitante {
    min-width: 100px;
  }
  
  .solicitante-nombre {
    font-size: 0.8rem;
  }
  
  .solicitante-rol {
    font-size: 0.65rem;
    padding: 0.1rem 0.4rem;
  }
  
  .cell-descripcion {
    min-width: 100px;
  }
  
  .badge {
    font-size: 0.65rem;
    padding: 0.3rem 0.5rem;
  }
  
  .status-badge {
    font-size: 0.65rem;
    padding: 0.25rem 0.5rem;
  }
  
  .btn-ver-circular {
    width: 32px;
    height: 32px;
    min-width: 32px;
    min-height: 32px;
  }
  
  .btn-ver-circular svg {
    width: 16px;
    height: 16px;
  }
}

@media (max-width: 640px) {
  .solicitudes-header {
    padding: 0.75rem 0.9rem;
  }

  .header-icon-small {
    width: 28px;
    height: 28px;
  }

  .icon-stat {
    width: 18px;
    height: 18px;
  }

  .header-title {
    font-size: 0.8rem;
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

  .form-title {
    font-size: 1.05rem;
  }

  .solicitudes-table {
    font-size: 0.7rem;
    min-width: 550px;
  }

  .solicitudes-table th,
  .solicitudes-table td {
    padding: 0.5rem 0.4rem;
  }
  
  .cell-solicitante {
    min-width: 90px;
  }
  
  .cell-tipo {
    min-width: 85px;
  }
  
  .cell-descripcion {
    min-width: 90px;
  }
  
  .cell-estado {
    min-width: 75px;
  }
  
  .cell-fecha {
    min-width: 80px;
  }
  
  .cell-acciones {
    min-width: 55px;
  }
}

@media (max-width: 480px) {
  .solicitudes-header {
    padding: 0.7rem 0.8rem;
  }

  .solicitudes-container {
    min-height: auto;
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

  .back-button {
    width: 34px;
    height: 34px;
  }

  .back-icon {
    width: 16px;
    height: 16px;
  }

  .reload-button {
    width: 34px;
    height: 34px;
  }

  .reload-icon {
    width: 18px;
    height: 18px;
  }

  .form-card {
    padding: 1rem;
  }

  .form-title {
    font-size: 1rem;
  }

  .solicitudes-table {
    font-size: 0.65rem;
    min-width: 500px;
  }

  .solicitudes-table th,
  .solicitudes-table td {
    padding: 0.4rem 0.3rem;
  }
  
  .solicitante-nombre {
    font-size: 0.7rem;
  }
  
  .solicitante-rol {
    font-size: 0.6rem;
  }
  
  .badge {
    font-size: 0.6rem;
    padding: 0.25rem 0.4rem;
  }
  
  .btn-ver-circular {
    width: 30px;
    height: 30px;
    min-width: 30px;
    min-height: 30px;
  }
  
  .btn-ver-circular svg {
    width: 14px;
    height: 14px;
  }
}
</style>
