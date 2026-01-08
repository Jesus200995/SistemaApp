<template>
  <div class="usuarios-container">
    <!-- Menú hamburguesa global (solo móvil) -->
    <HamburgerMenu class="mobile-only-menu" />

    <!-- Sidebar para PC -->
    <DesktopSidebar />

    <!-- Fondo decorativo (solo móvil) -->
    <div class="background-decoration mobile-only">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <!-- ========== CONTENEDOR PRINCIPAL ========== -->
    <div class="main-wrapper">
      <!-- Header con botón de regreso (móvil) -->
      <header class="usuarios-header mobile-header">
        <div class="header-wrapper">
          <div class="header-left">
            <router-link to="/dashboard" class="back-button" title="Volver al Dashboard">
              <ArrowLeft class="back-icon" />
            </router-link>
            <div class="header-icon-small">
              <Users class="icon-stat" />
            </div>
            <div class="header-text">
              <h1 class="header-title">Usuarios</h1>
              <p class="header-subtitle">Gestión de usuarios</p>
            </div>
          </div>
          <div class="header-actions">
            <!-- Botón Crear Usuario (solo visible para admin, territorial, facilitador) -->
            <button 
              v-if="puedeCrearUsuarios" 
              @click="abrirModalCrearUsuario" 
              class="create-button" 
              title="Crear Usuario"
            >
              <UserPlus class="create-icon" />
              <span class="create-text">Crear Usuario</span>
            </button>
            <button @click="reload" class="reload-button" title="Recargar">
              <svg class="reload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M3 21v-5h5"></path>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <!-- Header Desktop con estilo blanco -->
      <header class="view-header">
        <div class="header-content">
          <div class="header-title">
            <Users :size="22" class="header-icon" />
            <div>
              <h1>Directorio de Personal</h1>
              <p class="header-subtitle">Gestión de usuarios del sistema</p>
            </div>
          </div>
          <div class="header-actions">
            <button 
              v-if="puedeCrearUsuarios" 
              @click="abrirModalCrearUsuario" 
              class="btn-primary"
            >
              <UserPlus :size="18" />
              <span>Crear Usuario</span>
            </button>
          </div>
        </div>
      </header>

      <!-- Contenido principal -->
      <main class="usuarios-main">
        <!-- Modal Crear Usuario (se teletransporta al body) -->
        <Teleport to="body">
          <Transition name="modal-fade">
        <div v-if="showModalCrear" class="nuevo-modal-overlay">
          <div class="nuevo-modal">
            <!-- Botón cerrar -->
            <button @click="cerrarModalCrearUsuario" class="nuevo-modal-close" type="button">
              <X :size="18" />
            </button>

            <!-- Contenido del modal con scroll -->
            <div class="nuevo-modal-content">
              <!-- Header compacto -->
              <div class="nuevo-modal-header">
                <div class="nuevo-modal-icon">
                  <UserPlus :size="20" />
                </div>
                <div class="nuevo-modal-titles">
                  <h2>Nuevo Usuario</h2>
                  <span>{{ getDescripcionRol() }}</span>
                </div>
              </div>

              <!-- Formulario -->
              <form @submit.prevent="crearUsuario" class="nuevo-modal-form">
                <!-- Fila 1: Nombre -->
                <div class="campo">
                  <label>Nombre completo <span class="req">*</span></label>
                  <input
                    v-model="nuevoUsuario.nombre"
                    type="text"
                    placeholder="Ingresa el nombre"
                    required
                    minlength="2"
                    @input="nuevoUsuario.nombre = nuevoUsuario.nombre.toUpperCase()"
                  />
                </div>

                <!-- Fila 2: Email y Contraseña -->
                <div class="campos-row">
                  <div class="campo">
                    <label>Email <span class="req">*</span></label>
                    <input
                      v-model="nuevoUsuario.email"
                      type="email"
                      placeholder="correo@ejemplo.com"
                      required
                    />
                  </div>
                  <div class="campo">
                    <label>Contraseña <span class="req">*</span></label>
                    <div class="input-password">
                      <input
                        v-model="nuevoUsuario.password"
                        :type="showPassword ? 'text' : 'password'"
                        placeholder="Mínimo 6 caracteres"
                        required
                        minlength="6"
                      />
                      <button type="button" @click="showPassword = !showPassword" class="btn-eye">
                        <Eye v-if="!showPassword" :size="16" />
                        <EyeOff v-else :size="16" />
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Fila 3: Rol y CURP -->
                <div class="campos-row">
                  <div class="campo">
                    <label>Rol <span class="req">*</span></label>
                    <select v-model="nuevoUsuario.rol" required>
                      <option value="" disabled>Seleccionar</option>
                      <option v-for="rol in rolesDisponibles" :key="rol.value" :value="rol.value">
                        {{ rol.label }}
                      </option>
                    </select>
                  </div>
                  <div class="campo">
                    <label>CURP <span class="req">*</span></label>
                    <input
                      v-model="nuevoUsuario.curp"
                      type="text"
                      placeholder="18 caracteres"
                      maxlength="18"
                      minlength="18"
                      required
                      @input="nuevoUsuario.curp = nuevoUsuario.curp.toUpperCase()"
                    />
                  </div>
                </div>

                <!-- Fila 4: Teléfono y Territorio -->
                <div class="campos-row">
                  <div class="campo">
                    <label>Teléfono</label>
                    <input
                      v-model="nuevoUsuario.telefono"
                      type="tel"
                      placeholder="10 dígitos"
                      maxlength="10"
                      @input="nuevoUsuario.telefono = nuevoUsuario.telefono.replace(/[^0-9]/g, '').slice(0, 10)"
                    />
                  </div>
                  <div class="campo">
                    <label>Territorio <span class="req">*</span></label>
                    <select v-model="nuevoUsuario.territorio" required>
                      <option value="" disabled>Seleccionar</option>
                      <option value="Acapulco - Centro - Norte - Tierra Caliente">Acapulco - Centro - Norte</option>
                      <option value="Acayucan">Acayucan</option>
                      <option value="Balancán">Balancán</option>
                      <option value="Chihuahua / Sonora">Chihuahua / Sonora</option>
                      <option value="Colima">Colima</option>
                      <option value="Comalcalco">Comalcalco</option>
                      <option value="Córdoba">Córdoba</option>
                      <option value="Costa Chica - Montaña">Costa Chica - Montaña</option>
                      <option value="Costa Grande - Sierra">Costa Grande - Sierra</option>
                      <option value="Durango / Zacatecas">Durango / Zacatecas</option>
                      <option value="Hidalgo">Hidalgo</option>
                      <option value="Istmo">Istmo</option>
                      <option value="Michoacán">Michoacán</option>
                      <option value="Mixteca">Mixteca</option>
                      <option value="Morelos">Morelos</option>
                      <option value="Nayarit / Jalisco">Nayarit / Jalisco</option>
                      <option value="Ocosingo">Ocosingo</option>
                      <option value="Palenque">Palenque</option>
                      <option value="Papantla">Papantla</option>
                      <option value="Pichucalco">Pichucalco</option>
                      <option value="Puebla">Puebla</option>
                      <option value="San Luis Potosí">San Luis Potosí</option>
                      <option value="Sinaloa">Sinaloa</option>
                      <option value="Tamaulipas">Tamaulipas</option>
                      <option value="Tantoyuca">Tantoyuca</option>
                      <option value="Tapachula">Tapachula</option>
                      <option value="Teapa">Teapa</option>
                      <option value="Tlaxcala / Estado de México">Tlaxcala / Edo. México</option>
                      <option value="Tzucacab / Opb">Tzucacab / Opb</option>
                      <option value="Xpujil">Xpujil</option>
                      <option value="Oficinas Centrales">Oficinas Centrales</option>
                    </select>
                  </div>
                </div>

                <!-- Botones -->
                <div class="nuevo-modal-actions">
                  <button type="button" @click="cerrarModalCrearUsuario" class="btn-cancel">
                    Cancelar
                  </button>
                  <button type="submit" class="btn-submit" :disabled="creando">
                    <Loader2 v-if="creando" :size="16" class="spinning" />
                    <span v-else>Crear Usuario</span>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </Transition>
        </Teleport>

        <!-- Modal de Edición de Usuario -->
        <Teleport to="body">
      <div v-if="showModalEditar" class="modal-overlay" @click.self="cerrarModalEditar">
        <div class="modal-edicion">
          <div class="modal-header">
            <h2 class="modal-title">Editar Usuario</h2>
            <button @click="cerrarModalEditar" class="modal-close-btn" title="Cerrar">
              <X class="modal-close-icon" />
            </button>
          </div>

          <form @submit.prevent="guardarEdicionUsuario" class="modal-form">
            <!-- Fila 1: Nombre y Email -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Nombre Completo *</label>
                <div class="input-wrapper">
                  <User class="input-icon" />
                  <input
                    v-model="usuarioEditando.nombre"
                    type="text"
                    placeholder="JUAN PÉREZ GARCÍA"
                    class="form-input"
                    required
                    minlength="2"
                    @input="usuarioEditando.nombre = usuarioEditando.nombre.toUpperCase()"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Email *</label>
                <div class="input-wrapper">
                  <Mail class="input-icon" />
                  <input
                    v-model="usuarioEditando.email"
                    type="email"
                    placeholder="usuario@example.com"
                    class="form-input"
                    required
                  />
                </div>
              </div>
            </div>

            <!-- Fila 2: CURP y Teléfono -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">CURP *</label>
                <div class="input-wrapper">
                  <IdCard class="input-icon" />
                  <input
                    v-model="usuarioEditando.curp"
                    type="text"
                    placeholder="XXXX######HXXXXX##"
                    class="form-input"
                    maxlength="18"
                    minlength="18"
                    pattern="[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}"
                    @input="usuarioEditando.curp = usuarioEditando.curp.toUpperCase()"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Teléfono</label>
                <div class="input-wrapper">
                  <Phone class="input-icon" />
                  <input
                    v-model="usuarioEditando.telefono"
                    type="tel"
                    placeholder="10 dígitos"
                    class="form-input"
                    maxlength="10"
                    minlength="10"
                    pattern="[0-9]{10}"
                    @input="usuarioEditando.telefono = usuarioEditando.telefono.replace(/[^0-9]/g, '').slice(0, 10)"
                  />
                </div>
              </div>
            </div>

            <!-- Fila 3: Territorio y Rol -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Territorio *</label>
                <div class="select-wrapper">
                  <MapPin class="input-icon" />
                  <select
                    v-model="usuarioEditando.territorio"
                    class="form-select"
                    required
                  >
                    <option value="">-- Selecciona territorio --</option>
                    <option value="Acapulco - Centro - Norte - Tierra Caliente">Acapulco - Centro - Norte - Tierra Caliente</option>
                    <option value="Acayucan">Acayucan</option>
                    <option value="Balancán">Balancán</option>
                    <option value="Chihuahua / Sonora">Chihuahua / Sonora</option>
                    <option value="Colima">Colima</option>
                    <option value="Comalcalco">Comalcalco</option>
                    <option value="Córdoba">Córdoba</option>
                    <option value="Costa Chica - Montaña">Costa Chica - Montaña</option>
                    <option value="Costa Grande - Sierra">Costa Grande - Sierra</option>
                    <option value="Durango / Zacatecas">Durango / Zacatecas</option>
                    <option value="Hidalgo">Hidalgo</option>
                    <option value="Istmo">Istmo</option>
                    <option value="Michoacán">Michoacán</option>
                    <option value="Mixteca">Mixteca</option>
                    <option value="Morelos">Morelos</option>
                    <option value="Nayarit / Jalisco">Nayarit / Jalisco</option>
                    <option value="Ocosingo">Ocosingo</option>
                    <option value="Palenque">Palenque</option>
                    <option value="Papantla">Papantla</option>
                    <option value="Pichucalco">Pichucalco</option>
                    <option value="Puebla">Puebla</option>
                    <option value="San Luis Potosí">San Luis Potosí</option>
                    <option value="Sinaloa">Sinaloa</option>
                    <option value="Tamaulipas">Tamaulipas</option>
                    <option value="Tantoyuca">Tantoyuca</option>
                    <option value="Tapachula">Tapachula</option>
                    <option value="Teapa">Teapa</option>
                    <option value="Tlaxcala / Estado de México">Tlaxcala / Estado de México</option>
                    <option value="Tzucacab / Opb">Tzucacab / Opb</option>
                    <option value="Xpujil">Xpujil</option>
                    <option value="Oficinas Centrales">Oficinas Centrales</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Rol</label>
                <div class="select-wrapper">
                  <Shield class="input-icon" />
                  <select
                    v-model="usuarioEditando.rol"
                    class="form-select"
                    disabled
                  >
                    <option :value="usuarioEditando.rol">{{ usuarioEditando.rol.toUpperCase().replace(/_/g, ' ') }}</option>
                  </select>
                </div>
                <span class="field-hint">El rol no se puede cambiar por seguridad</span>
              </div>
            </div>

            <!-- Botones de acciones -->
            <div class="modal-actions">
              <button type="button" @click="cerrarModalEditar" class="btn-cancelar">
                Cancelar
              </button>
              <button type="submit" class="btn-guardar" :disabled="editandoUsuario">
                {{ editandoUsuario ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
            </div>
          </form>
        </div>
      </div>
        </Teleport>

        <!-- Contenido principal -->
        <div class="usuarios-content">
          <!-- Buscador -->
          <div class="filters-section">
            <div class="search-wrapper">
              <Search class="search-icon" />
              <input
                v-model="search"
                type="text"
                placeholder="Buscar por nombre o email..."
                class="search-input"
              />
            </div>
            <div class="results-info">
              {{ filteredUsuarios.length }} de {{ usuarios.length }} usuarios
            </div>
          </div>

          <!-- Contadores por rol -->
          <div class="stats-grid">
            <div class="stat-item admin" v-if="adminCount > 0">
              <span class="stat-value">{{ adminCount }}</span>
              <span class="stat-label">Admins</span>
            </div>
            <div class="stat-item territorial" v-if="territorialCount > 0">
              <span class="stat-value">{{ territorialCount }}</span>
              <span class="stat-label">Territoriales</span>
            </div>
            <div class="stat-item facilitador" v-if="facilitadorCount > 0">
              <span class="stat-value">{{ facilitadorCount }}</span>
              <span class="stat-label">Facilitadores</span>
            </div>
            <div class="stat-item tecnico" v-if="tecnicoProductivoCount > 0">
              <span class="stat-value">{{ tecnicoProductivoCount }}</span>
              <span class="stat-label">Téc. Productivos</span>
            </div>
            <div class="stat-item tecnico-social" v-if="tecnicoSocialCount > 0">
              <span class="stat-value">{{ tecnicoSocialCount }}</span>
              <span class="stat-label">Téc. Sociales</span>
            </div>
            <div class="stat-item total">
              <span class="stat-value">{{ total }}</span>
              <span class="stat-label">Total</span>
            </div>
          </div>

          <!-- Tabla de Usuarios -->
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Email</th>
                  <th>CURP</th>
                  <th>Teléfono</th>
                  <th>Territorio</th>
                  <th>Rol</th>
                  <th>Estatus</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <!-- Skeleton loader -->
                <tr v-if="loading" v-for="n in limit" :key="'skeleton-' + n">
                  <td colspan="9">
                    <div class="skeleton-line"></div>
                  </td>
                </tr>

                <!-- Datos reales -->
                <tr 
                  v-for="u in filteredUsuarios" 
                  :key="u.id"
                  :class="getEstatusRowClass(u)"
                >
                  <td class="folio">{{ u.id }}</td>
                  <td class="nombre">{{ u.nombre }}</td>
                  <td class="email">{{ u.email }}</td>
                  <td>
                    <span class="curp-badge">{{ u.curp || '—' }}</span>
                  </td>
                  <td>{{ u.telefono || '—' }}</td>
                  <td>{{ u.territorio || '—' }}</td>
                  <td>
                    <span :class="['rol-badge', `rol-${u.rol}`]">
                      {{ formatRolTabla(u.rol) }}
                    </span>
                  </td>
                  <td>
                    <span :class="['estatus-badge', getEstatusBadgeClass(u)]">
                      {{ getEstatusLabel(u) }}
                    </span>
                  </td>
                  <td class="actions">
                    <button
                      @click="abrirModalEditar(u)"
                      class="btn-action info"
                      title="Editar usuario"
                    >
                      <Edit :size="16" />
                    </button>
                    <button
                      @click="abrirConfirmarEliminar(u.id, u.nombre)"
                      class="btn-action danger"
                      title="Eliminar usuario"
                    >
                      <Trash2 :size="16" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Estado vacío -->
            <div v-if="!loading && filteredUsuarios.length === 0" class="empty-state">
              <Search class="empty-icon" />
              <h3>No se encontraron usuarios</h3>
              <p>Intenta con otros términos de búsqueda</p>
            </div>
          </div>

      <!-- Paginación -->
      <div class="pagination-section">
        <button
          @click="prevPage"
          :disabled="page === 1"
          class="pagination-btn"
        >
          <ChevronLeft class="pagination-icon" />
          <span>Anterior</span>
        </button>

        <div class="pagination-info">
          <span class="page-current">{{ page }}</span>
          <span class="page-separator">/</span>
          <span class="page-total">{{ totalPages }}</span>
        </div>

        <button
          @click="nextPage"
          :disabled="page === totalPages"
          class="pagination-btn"
        >
          <span>Siguiente</span>
          <ChevronRight class="pagination-icon" />
        </button>
      </div>


      </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { Users, RotateCw, Search, ChevronLeft, ChevronRight, ArrowLeft, Edit, Trash2, UserPlus, X, User, Mail, Lock, Shield, Eye, EyeOff, Loader2, IdCard, Phone, MapPin } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import DesktopSidebar from '../components/DesktopSidebar.vue'
import Swal from 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'

const auth = useAuthStore()
const usuarios = ref([])
const search = ref('')
const loading = ref(true)
const page = ref(1)
const limit = 6
const total = ref(0)

// Estados para el modal de crear usuario
const showModalCrear = ref(false)
const creando = ref(false)
const showPassword = ref(false)
const puedeCrearUsuarios = ref(false)
const rolesDisponibles = ref([])

// Estados para el modal de edición
const showModalEditar = ref(false)
const editandoUsuario = ref(false)
const usuarioEditando = ref({
  id: null,
  nombre: '',
  email: '',
  rol: '',
  curp: '',
  telefono: '',
  territorio: ''
})

const nuevoUsuario = ref({
  nombre: '',
  email: '',
  password: '',
  rol: '',
  curp: '',
  telefono: '',
  territorio: ''
})

const totalPages = computed(() => Math.ceil(total.value / limit))

const filteredUsuarios = computed(() =>
  usuarios.value.filter(u =>
    u.nombre.toLowerCase().includes(search.value.toLowerCase()) ||
    u.email.toLowerCase().includes(search.value.toLowerCase())
  )
)

const adminCount = computed(() => usuarios.value.filter(u => u.rol === 'admin').length)
const territorialCount = computed(() => usuarios.value.filter(u => u.rol === 'territorial').length)
const facilitadorCount = computed(() => usuarios.value.filter(u => u.rol === 'facilitador').length)
const tecnicoProductivoCount = computed(() => usuarios.value.filter(u => u.rol === 'tecnico_productivo').length)
const tecnicoSocialCount = computed(() => usuarios.value.filter(u => u.rol === 'tecnico_social').length)

// Verificar si el usuario puede crear otros usuarios
const verificarPermisosCreacion = async () => {
  // Primero asegurarse de que el perfil del usuario esté cargado
  if (!auth.user) {
    await auth.fetchProfile()
  }
  
  const rolActual = auth.user?.rol?.toLowerCase()?.trim()
  console.log('🔍 DEBUG - Rol actual del usuario (original):', auth.user?.rol)
  console.log('🔍 DEBUG - Rol actual del usuario (normalizado):', rolActual)
  
  // Definir roles permitidos localmente como fallback
  const rolesPermitidosPorCreador = {
    admin: [
      { value: 'territorial', label: 'Territorial' }
    ],
    territorial: [
      { value: 'facilitador', label: 'Facilitador' }
    ],
    facilitador: [
      { value: 'tecnico_productivo', label: 'Técnico Productivo' },
      { value: 'tecnico_social', label: 'Técnico Social' }
    ]
  }
  
  // Verificar si el rol actual puede crear usuarios (comparación case-insensitive)
  if (rolesPermitidosPorCreador[rolActual]) {
    puedeCrearUsuarios.value = true
    rolesDisponibles.value = rolesPermitidosPorCreador[rolActual]
    console.log('✅ Usuario puede crear:', rolesDisponibles.value)
  } else {
    puedeCrearUsuarios.value = false
    rolesDisponibles.value = []
    console.log('❌ Usuario NO puede crear usuarios. Rol:', rolActual)
  }
  
  // Intentar también obtener desde el backend (opcional, como verificación adicional)
  try {
    const data = await auth.getRolesPermitidos()
    console.log('🔍 DEBUG - Respuesta del backend getRolesPermitidos:', data)
    if (data && data.puede_crear !== undefined) {
      puedeCrearUsuarios.value = data.puede_crear
      if (data.roles_permitidos && data.roles_permitidos.length > 0) {
        rolesDisponibles.value = data.roles_permitidos
      }
    }
  } catch (err) {
    console.warn('⚠️ No se pudo verificar permisos desde el backend, usando fallback local:', err)
  }
}

// Obtener descripción del rol según el usuario actual
const getDescripcionRol = () => {
  const rol = auth.user?.rol
  if (rol === 'admin') {
    return 'Crear usuario Territorial'
  } else if (rol === 'territorial') {
    return 'Crear usuario Facilitador'
  } else if (rol === 'facilitador') {
    return 'Crear Técnico Productivo o Social'
  }
  return ''
}

// Abrir modal de crear usuario
const abrirModalCrearUsuario = () => {
  nuevoUsuario.value = {
    nombre: '',
    email: '',
    password: '',
    rol: rolesDisponibles.value.length === 1 ? rolesDisponibles.value[0].value : '',
    curp: '',
    telefono: '',
    territorio: ''
  }
  showPassword.value = false
  showModalCrear.value = true
}

// Cerrar modal de crear usuario
const cerrarModalCrearUsuario = () => {
  showModalCrear.value = false
  nuevoUsuario.value = { nombre: '', email: '', password: '', rol: '', curp: '', telefono: '', territorio: '' }
}

// Crear usuario
const crearUsuario = async () => {
  if (!nuevoUsuario.value.nombre || !nuevoUsuario.value.email || !nuevoUsuario.value.password || !nuevoUsuario.value.rol) {
    Swal.fire('⚠️ Campos incompletos', 'Por favor completa todos los campos obligatorios', 'warning')
    return
  }

  // Validar territorio obligatorio
  if (!nuevoUsuario.value.territorio) {
    Swal.fire('⚠️ Territorio requerido', 'Debes seleccionar un territorio', 'warning')
    return
  }

  // Validar CURP obligatorio
  if (!nuevoUsuario.value.curp || !nuevoUsuario.value.curp.trim()) {
    Swal.fire('⚠️ CURP requerido', 'El CURP es obligatorio', 'warning')
    return
  }

  const curpRegex = /^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}$/
  if (!curpRegex.test(nuevoUsuario.value.curp.toUpperCase())) {
    Swal.fire('⚠️ CURP inválido', 'El CURP debe tener 18 caracteres en formato válido', 'warning')
    return
  }

  // Validar teléfono si se proporciona
  if (nuevoUsuario.value.telefono && nuevoUsuario.value.telefono.trim()) {
    const telefonoLimpio = nuevoUsuario.value.telefono.replace(/[^0-9]/g, '')
    if (telefonoLimpio.length < 10) {
      Swal.fire('⚠️ Teléfono inválido', 'El teléfono debe tener al menos 10 dígitos', 'warning')
      return
    }
  }

  creando.value = true

  try {
    console.log('🚀 Iniciando creación de usuario:', nuevoUsuario.value)
    
    const result = await auth.createUserHierarchical(
      nuevoUsuario.value.nombre,
      nuevoUsuario.value.email,
      nuevoUsuario.value.password,
      nuevoUsuario.value.rol,
      nuevoUsuario.value.curp || null,
      nuevoUsuario.value.telefono || null,
      nuevoUsuario.value.territorio
    )

    console.log('📦 Resultado de createUserHierarchical:', result)

    // Cerrar modal primero
    creando.value = false
    cerrarModalCrearUsuario()

    if (result && result.success) {
      // Mostrar mensaje de éxito con diseño profesional
      Swal.fire({
        icon: 'success',
        title: 'Usuario Creado',
        html: `
          <div class="swal-success-content">
            <div class="swal-success-item">
              <span class="swal-success-label">Nombre</span>
              <span class="swal-success-value">${result.data?.nombre || nuevoUsuario.value.nombre}</span>
            </div>
            <div class="swal-success-item">
              <span class="swal-success-label">Email</span>
              <span class="swal-success-value">${result.data?.email || nuevoUsuario.value.email}</span>
            </div>
            <div class="swal-success-item">
              <span class="swal-success-label">Rol</span>
              <span class="swal-success-badge">${(result.data?.rol || nuevoUsuario.value.rol).toUpperCase().replace('_', ' ')}</span>
            </div>
          </div>
        `,
        confirmButtonText: 'Aceptar',
        customClass: {
          popup: 'swal-success-popup',
          title: 'swal-success-title',
          htmlContainer: 'swal-success-html',
          confirmButton: 'swal-success-confirm',
          icon: 'swal-success-icon'
        },
        background: 'white',
        color: '#1e3a2f',
        showClass: {
          popup: 'animate__animated animate__fadeInUp animate__faster'
        },
        hideClass: {
          popup: 'animate__animated animate__fadeOutDown animate__faster'
        }
      })
      // Recargar lista de usuarios
      fetchUsuarios()
    } else {
      Swal.fire('❌ Error', result?.error || 'No se pudo crear el usuario', 'error')
    }
  } catch (err) {
    console.error('❌ Error al crear usuario:', err)
    creando.value = false
    cerrarModalCrearUsuario()
    Swal.fire('❌ Error', 'Ocurrió un error al crear el usuario', 'error')
  }
}

const fetchUsuarios = async () => {
  try {
    loading.value = true
    const apiUrl = getSecureApiUrl()
    const { data } = await axios.get(`${apiUrl}/auth/users`, {
      params: { page: page.value, limit },
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    usuarios.value = data.users
    total.value = data.total
  } catch (err) {
    console.error('Error al cargar usuarios:', err)
  } finally {
    loading.value = false
  }
}

const reload = () => fetchUsuarios()

// Formatear rol para mostrar en tabla
const formatRolTabla = (rol: string): string => {
  const roles: Record<string, string> = {
    admin: 'Admin',
    territorial: 'Territorial',
    facilitador: 'Facilitador',
    tecnico_productivo: 'Téc. Productivo',
    tecnico_social: 'Téc. Social',
    sembrador: 'Sembrador'
  }
  return roles[rol?.toLowerCase()] || rol?.replace(/_/g, ' ').toUpperCase() || '-'
}

// Funciones de estatus laboral
const getEstatusLabel = (u: any): string => {
  if (u.estatus_laboral === 'BAJA' || !u.activo) return 'Baja'
  if (u.tipo_ultima_accion === 'REASIGNACION') return 'Reasignación'
  return 'Activo'
}

const getEstatusBadgeClass = (u: any): string => {
  if (u.estatus_laboral === 'BAJA' || !u.activo) return 'estatus-baja'
  if (u.tipo_ultima_accion === 'REASIGNACION') return 'estatus-reasignacion'
  return 'estatus-activo'
}

const getEstatusRowClass = (u: any): string => {
  if (u.estatus_laboral === 'BAJA' || !u.activo) return 'row-estatus-baja'
  if (u.tipo_ultima_accion === 'REASIGNACION') return 'row-estatus-reasignacion'
  return 'row-estatus-activo'
}

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
    fetchUsuarios()
  }
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
    fetchUsuarios()
  }
}

// Abrir modal de edición
const abrirModalEditar = (usuario) => {
  usuarioEditando.value = {
    id: usuario.id,
    nombre: usuario.nombre || '',
    email: usuario.email || '',
    rol: usuario.rol || '',
    curp: usuario.curp || '',
    telefono: usuario.telefono || '',
    territorio: usuario.territorio || ''
  }
  showModalEditar.value = true
}

// Cerrar modal de edición
const cerrarModalEditar = () => {
  showModalEditar.value = false
  usuarioEditando.value = {
    id: null,
    nombre: '',
    email: '',
    rol: '',
    curp: '',
    telefono: '',
    territorio: ''
  }
}

// Guardar edición del usuario
const guardarEdicionUsuario = async () => {
  if (!usuarioEditando.value.nombre || !usuarioEditando.value.email || !usuarioEditando.value.territorio) {
    Swal.fire('⚠️ Campos incompletos', 'Por favor completa todos los campos obligatorios', 'warning')
    return
  }

  editandoUsuario.value = true

  try {
    const apiUrl = getSecureApiUrl()
    const dataToUpdate = {
      nombre: usuarioEditando.value.nombre,
      email: usuarioEditando.value.email,
      curp: usuarioEditando.value.curp || null,
      telefono: usuarioEditando.value.telefono || null,
      territorio: usuarioEditando.value.territorio
    }

    await axios.put(`${apiUrl}/auth/users/${usuarioEditando.value.id}`, dataToUpdate, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })

    Swal.fire('✅ Actualizado', 'El usuario fue modificado correctamente.', 'success')
    cerrarModalEditar()
    fetchUsuarios()
  } catch (err) {
    console.error('❌ Error al actualizar usuario:', err)
    Swal.fire('❌ Error', err.response?.data?.detail || 'No se pudo actualizar el usuario.', 'error')
  } finally {
    editandoUsuario.value = false
  }
}

// Abrir confirmación de eliminación
const abrirConfirmarEliminar = (id, nombre) => {
  Swal.fire({
    title: '¿Eliminar usuario?',
    html: `<p style="color: #374151; font-size: 1rem; margin: 1rem 0;">Estás a punto de eliminar a</p><p style="color: #dc2626; font-weight: 700; font-size: 1.1rem; margin: 0.5rem 0;">«${nombre}»</p><p style="color: #64748b; font-size: 0.9rem; margin: 1rem 0;">Esta acción no se puede deshacer.</p>`,
    icon: 'warning',
    iconHtml: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 3rem; height: 3rem; margin: 0 auto;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>',
    showCancelButton: true,
    confirmButtonText: 'Sí, eliminar usuario',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280',
    customClass: {
      popup: 'swal-delete-popup',
      title: 'swal-delete-title',
      htmlContainer: 'swal-delete-html',
      confirmButton: 'swal-delete-confirm',
      cancelButton: 'swal-delete-cancel'
    },
    background: 'white',
    didOpen: () => {
      const popup = document.querySelector('.swal2-popup') as HTMLElement | null;
      if (popup) {
        popup.style.border = '1.5px solid rgba(239, 68, 68, 0.3)';
        popup.style.boxShadow = '0 20px 60px rgba(239, 68, 68, 0.2)';
      }
    }
  }).then((result) => {
    if (result.isConfirmed) {
      eliminarUsuario(id)
    }
  })
}

// Eliminar usuario
const eliminarUsuario = async (id) => {
  try {
    const apiUrl = getSecureApiUrl()
    await axios.delete(`${apiUrl}/auth/users/${id}`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    Swal.fire('🗑️ Eliminado', 'El usuario ha sido eliminado.', 'success')
    fetchUsuarios()
  } catch (err) {
    console.error('❌ Error al eliminar usuario:', err)
    Swal.fire('❌ Error', err.response?.data?.detail || 'No se pudo eliminar el usuario.', 'error')
  }
}

onMounted(async () => {
  // Primero cargar el perfil del usuario si no está cargado
  if (!auth.user) {
    await auth.fetchProfile()
  }
  // Luego verificar permisos y cargar usuarios
  await verificarPermisosCreacion()
  fetchUsuarios()
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ========== CONTAINER ========== */
.usuarios-container {
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #f0fdf4 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

/* ========== LAYOUT PC ========== */
@media (min-width: 1024px) {
  .usuarios-container {
    flex-direction: row;
    background: #f8fafc;
  }

  .mobile-only-menu {
    display: none !important;
  }

  .mobile-header {
    display: none !important;
  }

  .mobile-only {
    display: none !important;
  }
}

/* ========== MAIN WRAPPER ========== */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
}

@media (min-width: 1024px) {
  .main-wrapper {
    margin-left: 220px;
    width: calc(100% - 220px);
  }
}

/* ========== VIEW HEADER (ESTILO BLANCO) ========== */
.view-header {
  display: none;
}

@media (min-width: 1024px) {
  .view-header {
    display: block;
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
    gap: 0.5rem;
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
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .btn-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(22, 163, 74, 0.35);
  }
}

/* ========== USUARIOS MAIN ========== */
.usuarios-main {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  z-index: 5;
}

@media (min-width: 1024px) {
  .usuarios-main {
    padding: 1rem 1.5rem;
    background: #f8fafc;
  }
}

/* ========== BACKGROUND BLOBS ========== */
.background-decoration {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.blob {
  position: absolute;
  opacity: 0.3;
  filter: blur(100px);
  mix-blend-mode: multiply;
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
.usuarios-content {
  position: relative;
  z-index: 5;
  padding: 1rem 0.75rem;
  max-width: 1100px;
  margin: 0 auto;
  margin-top: 60px;
  overflow-y: auto;
}

@media (min-width: 1024px) {
  .usuarios-content {
    max-width: 100%;
    padding: 0;
    margin-top: 0;
  }
  height: calc(100vh - 60px);
  width: 100%;
  box-sizing: border-box;
}

/* ========== HEADER ========== */
.usuarios-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(22, 163, 74, 0.2);
  backdrop-filter: blur(12px);
  padding: 0.6rem 0.8rem;
  box-shadow: 0 4px 20px rgba(22, 163, 74, 0.1);
  width: 100%;
  box-sizing: border-box;
}

.header-wrapper {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 50px;
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
  width: 34px;
  height: 34px;
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

.back-button:active {
  transform: translateX(-2px);
}

.back-icon {
  width: 18px;
  height: 18px;
  stroke-width: 2.5;
}

.header-icon-small {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  background: transparent;
  flex-shrink: 0;
}

.icon-stat {
  width: 18px;
  height: 18px;
  color: #16a34a;
  stroke-width: 2;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #15803d;
  margin: 0;
}

.header-subtitle {
  font-size: 0.65rem;
  color: #64748b;
  margin: 0;
  margin-top: 0.1rem;
}

.reload-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
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
  width: 18px;
  height: 18px;
  stroke-width: 2.5;
}

/* ========== USUARIOS CARD ========== */
.usuarios-card {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(22, 163, 74, 0.2);
  border-radius: 14px;
  padding: 1rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(22, 163, 74, 0.08);
  margin-bottom: 1rem;
}

@media (min-width: 1024px) {
  .usuarios-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }
}

/* ========== SEARCH SECTION ========== */
.search-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.search-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 10px;
  width: 16px;
  height: 16px;
  color: #16a34a;
  pointer-events: none;
}

.search-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(22, 163, 74, 0.3);
  border-radius: 8px;
  padding: 0.5rem 0.75rem 0.5rem 2rem;
  color: #1e3a2f;
  font-size: 0.75rem;
  transition: all 0.3s ease;
}

@media (min-width: 1024px) {
  .search-input {
    font-size: 0.9rem;
    padding: 0.65rem 1rem 0.65rem 2.5rem;
  }
}

.search-input::placeholder {
  color: #64748b;
}

.search-input:focus {
  outline: none;
  border-color: #16a34a;
  background: white;
  box-shadow: 0 0 0 2px rgba(22, 163, 74, 0.15);
}

.results-info {
  font-size: 0.75rem;
  color: #6b7280;
  white-space: nowrap;
  padding: 0.5rem 0.75rem;
  background: #f9fafb;
  border-radius: 6px;
}

/* ========== FILTERS SECTION ========== */
.filters-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

/* ========== TABLE CONTAINER ========== */
.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
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

.folio {
  font-family: monospace;
  font-weight: 600;
  color: #1f2937;
}

.nombre {
  font-weight: 500;
  color: #1f2937;
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.email {
  color: #6b7280;
  font-size: 0.875rem;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.curp-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: #f3f4f6;
  color: #374151;
  border-radius: 4px;
  font-size: 0.7rem;
  font-family: monospace;
}

.rol-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.rol-badge.rol-admin {
  background: #fee2e2;
  color: #dc2626;
}

.rol-badge.rol-territorial {
  background: #dbeafe;
  color: #2563eb;
}

.rol-badge.rol-facilitador {
  background: #dcfce7;
  color: #16a34a;
}

.rol-badge.rol-tecnico_productivo {
  background: #fef3c7;
  color: #d97706;
}

.rol-badge.rol-tecnico_social {
  background: #e0e7ff;
  color: #4f46e5;
}

.rol-badge.rol-sembrador {
  background: #ecfccb;
  color: #65a30d;
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

.btn-action.info {
  background: #dbeafe;
  color: #2563eb;
}

.btn-action.info:hover {
  background: #bfdbfe;
}

.btn-action.danger {
  background: #fee2e2;
  color: #dc2626;
}

.btn-action.danger:hover {
  background: #fecaca;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: #9ca3af;
}

.empty-state h3 {
  margin: 0.5rem 0 0.25rem 0;
  font-size: 1rem;
  color: #6b7280;
}

.empty-state p {
  margin: 0;
  font-size: 0.875rem;
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: #d1d5db;
}

.skeleton-line {
  height: 1rem;
  background: linear-gradient(90deg, #f3f4f6 0%, #e5e7eb 50%, #f3f4f6 100%);
  border-radius: 4px;
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* Responsive table */
@media (max-width: 1024px) {
  .table-container {
    overflow-x: auto;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
  }
  
  .nombre {
    max-width: 120px;
  }
  
  .email {
    max-width: 150px;
    font-size: 0.75rem;
  }
}

@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-wrapper {
    width: 100%;
  }
  
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }
  
  .stat-item {
    padding: 0.75rem 0.5rem;
  }
  
  .stat-value {
    font-size: 1.25rem;
  }
  
  .stat-label {
    font-size: 0.6rem;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.5rem;
    font-size: 0.7rem;
  }
  
  .data-table th:nth-child(3),
  .data-table td:nth-child(3),
  .data-table th:nth-child(4),
  .data-table td:nth-child(4),
  .data-table th:nth-child(5),
  .data-table td:nth-child(5) {
    display: none;
  }
  
  .nombre {
    max-width: 100px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.4rem;
  }
  
  .stat-item {
    padding: 0.6rem 0.4rem;
    border-radius: 10px;
  }
  
  .stat-value {
    font-size: 1.1rem;
  }
  
  .stat-label {
    font-size: 0.55rem;
  }
}

@keyframes pulse-loading {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ========== PAGINATION ========== */
.pagination-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 0.75rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%);
  border: 1px solid rgba(22, 163, 74, 0.3);
  color: #15803d;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #bbf7d0 0%, #dcfce7 100%);
  border-color: rgba(22, 163, 74, 0.5);
  transform: translateY(-2px);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-icon {
  width: 14px;
  height: 14px;
}

.pagination-info {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
}

.page-current {
  color: #16a34a;
  font-size: 1rem;
}

.page-separator {
  color: #64748b;
}

.page-total {
  color: #94a3b8;
}

/* ========== STATS GRID (Contadores) ========== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem 0.75rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: currentColor;
  opacity: 0.8;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.7rem;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

/* Colores por rol */
.stat-item.admin {
  color: #dc2626;
  border-color: rgba(220, 38, 38, 0.2);
  background: linear-gradient(135deg, #fef2f2 0%, #fff 100%);
}
.stat-item.admin .stat-value {
  color: #dc2626;
}

.stat-item.territorial {
  color: #7c3aed;
  border-color: rgba(124, 58, 237, 0.2);
  background: linear-gradient(135deg, #f5f3ff 0%, #fff 100%);
}
.stat-item.territorial .stat-value {
  color: #7c3aed;
}

.stat-item.facilitador {
  color: #2563eb;
  border-color: rgba(37, 99, 235, 0.2);
  background: linear-gradient(135deg, #eff6ff 0%, #fff 100%);
}
.stat-item.facilitador .stat-value {
  color: #2563eb;
}

.stat-item.tecnico {
  color: #d97706;
  border-color: rgba(217, 119, 6, 0.2);
  background: linear-gradient(135deg, #fffbeb 0%, #fff 100%);
}
.stat-item.tecnico .stat-value {
  color: #d97706;
}

.stat-item.tecnico-social {
  color: #0891b2;
  border-color: rgba(8, 145, 178, 0.2);
  background: linear-gradient(135deg, #ecfeff 0%, #fff 100%);
}
.stat-item.tecnico-social .stat-value {
  color: #0891b2;
}

.stat-item.total {
  color: #059669;
  border-color: rgba(5, 150, 105, 0.2);
  background: linear-gradient(135deg, #ecfdf5 0%, #fff 100%);
}
.stat-item.total .stat-value {
  color: #059669;
}

/* ========== HEADER ACTIONS ========== */
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* ========== CREATE BUTTON ========== */
.create-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 8px;
  padding: 0.4rem 0.75rem;
  color: white;
  font-weight: 600;
  font-size: 0.65rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 12px rgba(16, 185, 129, 0.3);
}

.create-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 16px rgba(16, 185, 129, 0.4);
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
}

.create-button:active {
  transform: translateY(0);
}

.create-icon {
  width: 14px;
  height: 14px;
}

.create-text {
  display: inline;
}

@media (max-width: 640px) {
  .create-text {
    display: none;
  }
  
  .create-button {
    padding: 0.4rem;
    border-radius: 50%;
    width: 30px;
    height: 30px;
  }
}

/* ========================================
   NUEVO MODAL CREAR USUARIO - DISEÑO LIMPIO
   ======================================== */

/* Transición del modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.25s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-from .nuevo-modal,
.modal-fade-leave-to .nuevo-modal {
  transform: scale(0.95) translateY(-20px);
}

/* Overlay */
.nuevo-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
  box-sizing: border-box;
  overflow-y: auto;
}

/* Modal Container */
.nuevo-modal {
  position: relative;
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 8px 10px -6px rgba(0, 0, 0, 0.1);
}

/* Botón Cerrar */
.nuevo-modal-close {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border: none;
  border-radius: 8px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
}
.nuevo-modal-close:hover {
  background: #fee2e2;
  color: #dc2626;
}

/* Contenido con scroll */
.nuevo-modal-content {
  max-height: 90vh;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Header */
.nuevo-modal-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 24px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-bottom: 1px solid #bbf7d0;
}

.nuevo-modal-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  border-radius: 12px;
  color: white;
  flex-shrink: 0;
}

.nuevo-modal-titles {
  flex: 1;
  min-width: 0;
}
.nuevo-modal-titles h2 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: #15803d;
  line-height: 1.3;
}
.nuevo-modal-titles span {
  display: block;
  font-size: 0.75rem;
  color: #4ade80;
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Formulario */
.nuevo-modal-form {
  padding: 20px 24px 24px;
}

/* Campos individuales */
.campo {
  margin-bottom: 14px;
}
.campo label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}
.campo .req {
  color: #ef4444;
}
.campo input,
.campo select {
  width: 100%;
  height: 42px;
  padding: 0 12px;
  background: #f9fafb;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.875rem;
  color: #1f2937;
  transition: all 0.15s ease;
  box-sizing: border-box;
}
.campo input::placeholder {
  color: #9ca3af;
}
.campo input:focus,
.campo select:focus {
  outline: none;
  background: #fff;
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}
.campo select {
  appearance: none;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%236b7280'%3E%3Cpath fill-rule='evenodd' d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z' clip-rule='evenodd'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px;
  padding-right: 36px;
}

/* Campos en fila (2 columnas) */
.campos-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 14px;
}

/* Input password */
.input-password {
  position: relative;
}
.input-password input {
  padding-right: 40px;
}
.btn-eye {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-eye:hover {
  color: #16a34a;
}

/* Botones de acción */
.nuevo-modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.btn-cancel,
.btn-submit {
  flex: 1;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-cancel {
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  color: #6b7280;
}
.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-submit {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  border: none;
  color: white;
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3);
}
.btn-submit:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(22, 163, 74, 0.4);
}
.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinning {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===== RESPONSIVE ===== */
@media (max-width: 540px) {
  .nuevo-modal-overlay {
    padding: 1rem;
    align-items: center;
    justify-content: center;
  }
  
  .nuevo-modal {
    max-height: 90vh;
    margin: auto;
  }
  
  .nuevo-modal-header {
    padding: 16px 20px;
  }
  
  .nuevo-modal-icon {
    width: 40px;
    height: 40px;
  }
  
  .nuevo-modal-titles h2 {
    font-size: 1rem;
  }
  
  .nuevo-modal-form {
    padding: 16px 20px 20px;
  }
  
  .campos-row {
    grid-template-columns: 1fr;
    gap: 0;
    margin-bottom: 0;
  }
  
  .campos-row .campo {
    margin-bottom: 14px;
  }
  
  .campo input,
  .campo select {
    height: 46px;
    font-size: 16px; /* Previene zoom iOS */
  }
}

@media (max-width: 380px) {
  .nuevo-modal-overlay {
    padding: 0.75rem;
    align-items: center;
    justify-content: center;
  }
  
  .nuevo-modal {
    margin: auto;
  }
  
  .nuevo-modal-header {
    padding: 14px 16px;
  }
  
  .nuevo-modal-icon {
    width: 36px;
    height: 36px;
  }
  
  .nuevo-modal-form {
    padding: 14px 16px 18px;
  }
  
  .campo {
    margin-bottom: 12px;
  }
  
  .nuevo-modal-actions {
    flex-direction: column;
    gap: 8px;
  }
}

/* Landscape móviles */
@media (max-height: 500px) and (orientation: landscape) {
  .nuevo-modal-overlay {
    padding: 0.5rem;
  }
  
  .nuevo-modal {
    max-width: 600px;
    max-height: 95vh;
  }
  
  .nuevo-modal-header {
    padding: 12px 20px;
  }
  
  .nuevo-modal-icon {
    width: 36px;
    height: 36px;
  }
  
  .nuevo-modal-titles h2 {
    font-size: 0.95rem;
  }
  
  .nuevo-modal-titles span {
    display: none;
  }
  
  .nuevo-modal-form {
    padding: 12px 20px 16px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px 16px;
  }
  
  .campo {
    margin-bottom: 0;
  }
  
  .campos-row {
    display: contents;
  }
  
  .campos-row .campo {
    margin-bottom: 0;
  }
  
  .nuevo-modal-actions {
    grid-column: span 2;
    margin-top: 12px;
    padding-top: 12px;
    flex-direction: row;
  }
}

/* ========== MODAL EDICION (existente) ========== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  overflow: auto;
  padding: 1rem 0;
}

.modal-edicion {
  background: white;
  border: 1px solid rgba(22, 163, 74, 0.2);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(22, 163, 74, 0.15);
  backdrop-filter: blur(12px);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease;
  flex-shrink: 0;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-edicion .modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(22, 163, 74, 0.1);
  background: rgba(22, 163, 74, 0.05);
  border-radius: 16px 16px 0 0;
}

.modal-edicion .modal-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #15803d;
  margin: 0;
}

.modal-close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.modal-close-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
}

.modal-close-icon {
  width: 20px;
  height: 20px;
  color: #ef4444;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #1e3a2f;
  margin-bottom: 0.5rem;
}

.input-icon {
  width: 16px;
  height: 16px;
  color: #16a34a;
}

.input-wrapper,
.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper .input-icon,
.select-wrapper .input-icon {
  position: absolute;
  left: 0.75rem;
  pointer-events: none;
}

.form-input,
.form-select {
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(22, 163, 74, 0.3);
  border-radius: 10px;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  color: #1e3a2f;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: #64748b;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #16a34a;
  background: white;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.15);
}

.form-select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1rem;
  padding-right: 2.5rem;
}

.form-select option {
  background: white;
  color: #1e3a2f;
}

.form-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.field-hint {
  display: block;
  font-size: 0.7rem;
  color: #64748b;
  margin-top: 0.3rem;
  font-style: italic;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(132, 204, 22, 0.1);
}

.btn-cancelar {
  flex: 1;
  padding: 0.75rem 1rem;
  background: rgba(107, 114, 128, 0.1);
  border: 1px solid rgba(107, 114, 128, 0.3);
  border-radius: 8px;
  color: #d1d5db;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-cancelar:hover {
  background: rgba(107, 114, 128, 0.2);
  border-color: rgba(107, 114, 128, 0.5);
}

.btn-guardar {
  flex: 1;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #16a34a, #15803d);
  border: 1px solid rgba(22, 163, 74, 0.5);
  border-radius: 8px;
  color: white;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.2);
}

.btn-guardar:hover:not(:disabled) {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  box-shadow: 0 6px 16px rgba(22, 163, 74, 0.3);
  transform: translateY(-2px);
}

.btn-guardar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ========== BOTONES CIRCULARES ========== */
.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1.5px solid rgba(22, 163, 74, 0.3);
  background: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
  padding: 0;
}

.action-btn:hover {
  transform: scale(1.1);
}

.action-icon {
  width: 18px;
  height: 18px;
  stroke-width: 2;
}

.edit-btn {
  border-color: rgba(16, 185, 129, 0.4);
}

.edit-btn .action-icon {
  color: #10b981;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: rgba(16, 185, 129, 0.2);
  border-color: rgba(16, 185, 129, 0.7);
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.3);
}

.edit-btn:hover .action-icon {
  color: #34d399;
  filter: drop-shadow(0 0 4px rgba(16, 185, 129, 0.5));
}

.delete-btn {
  border-color: rgba(239, 68, 68, 0.4);
}

.delete-btn .action-icon {
  color: #ef4444;
  transition: all 0.3s ease;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.7);
  box-shadow: 0 0 12px rgba(239, 68, 68, 0.3);
}

.delete-btn:hover .action-icon {
  color: #f87171;
  filter: drop-shadow(0 0 4px rgba(239, 68, 68, 0.5));
}

.actions-group {
  display: flex;
  gap: 0.25rem;
  align-items: center;
  justify-content: center;
}

/* ========== RESPONSIVE MODAL ========== */

/* ========== TABLETS & LANDSCAPE ========== */
@media (max-height: 700px) and (min-width: 768px) {
  .modal-overlay {
    padding: 0.5rem;
  }

  .modal-edicion {
    max-height: 95vh;
    max-width: 700px;
  }

  .modal-header {
    padding: 1.2rem;
  }

  .modal-form {
    padding: 1.2rem;
    gap: 0.8rem;
  }

  .form-row {
    gap: 0.8rem;
  }
}

/* ========== LANDSCAPE MODE ========== */
@media (orientation: landscape) and (min-height: 500px) {
  .modal-edicion {
    max-height: 90vh;
    border-radius: 14px;
  }

  .modal-header {
    padding: 1rem 1.5rem;
  }

  .modal-form {
    padding: 1rem 1.5rem;
    gap: 0.75rem;
  }

  .form-row {
    gap: 0.75rem;
  }

  .form-group {
    margin-bottom: 0.5rem;
  }
}

/* ========== TABLET VERTICAL (768px) ========== */
@media (min-width: 768px) and (max-width: 1024px) {
  .modal-edicion {
    max-width: 550px;
    max-height: 90vh;
  }

  .modal-header {
    padding: 1.3rem;
  }

  .modal-form {
    padding: 1.3rem;
  }

  .form-row {
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  .modal-actions {
    gap: 0.8rem;
  }
}

/* ========== TABLET HORIZONTAL (1024px+) ========== */
@media (min-width: 1024px) {
  .modal-edicion {
    max-width: 650px;
  }

  .form-row {
    grid-template-columns: 1fr 1fr;
    gap: 1.2rem;
  }
}

/* ========== MOBILE VERTICAL (< 640px) ========== */
@media (max-width: 640px) {
  .modal-overlay {
    padding: 0.75rem;
    align-items: center;
    justify-content: center;
  }

  .modal-edicion {
    width: calc(100% - 1.5rem);
    max-width: 100%;
    max-height: 90vh;
    border-radius: 16px;
    margin: auto;
    animation: modalSlideIn 0.3s ease;
  }

  .modal-header {
    padding: 1.2rem 1.2rem 0.8rem;
    border-radius: 16px 16px 0 0;
  }

  .modal-title {
    font-size: 1.2rem;
  }

  .modal-close-btn {
    width: 38px;
    height: 38px;
  }

  .modal-close-icon {
    width: 18px;
    height: 18px;
  }

  .modal-form {
    padding: 1.2rem;
    gap: 0.9rem;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 0.9rem;
  }

  .form-label {
    font-size: 0.8rem;
  }

  .form-input,
  .form-select {
    font-size: 16px;
    padding: 0.7rem 1rem 0.7rem 2.3rem;
  }

  .input-icon {
    width: 15px;
    height: 15px;
    left: 0.65rem;
  }

  .modal-actions {
    flex-direction: column;
    gap: 0.7rem;
    margin-top: 0.8rem;
    padding-top: 0.8rem;
  }

  .btn-cancelar,
  .btn-guardar {
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
    border-radius: 8px;
  }

  .field-hint {
    font-size: 0.65rem;
  }
}

/* ========== MOBILE SMALL (< 480px) ========== */
@media (max-width: 480px) {
  .modal-overlay {
    padding: 0.5rem;
  }

  .modal-edicion {
    max-height: 88vh;
    border-radius: 20px 20px 0 0;
  }

  .modal-header {
    padding: 1rem 1rem 0.6rem;
  }

  .modal-title {
    font-size: 1.1rem;
  }

  .modal-form {
    padding: 1rem;
    gap: 0.75rem;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .form-label {
    font-size: 0.75rem;
  }

  .form-input,
  .form-select {
    padding: 0.65rem 0.9rem 0.65rem 2.2rem;
    font-size: 16px;
  }

  .input-icon {
    width: 14px;
    height: 14px;
    left: 0.6rem;
  }

  .modal-actions {
    flex-direction: column;
    gap: 0.6rem;
  }

  .btn-cancelar,
  .btn-guardar {
    padding: 0.65rem 0.9rem;
    font-size: 0.8rem;
  }
}

/* ========== EXTRA SMALL (< 375px) ========== */
@media (max-width: 375px) {
  .modal-edicion {
    max-height: 90vh;
  }

  .modal-header {
    padding: 0.9rem 0.9rem 0.5rem;
  }

  .modal-title {
    font-size: 1rem;
  }

  .modal-close-btn {
    width: 34px;
    height: 34px;
  }

  .modal-form {
    padding: 0.9rem;
  }

  .form-label {
    font-size: 0.7rem;
  }

  .form-input,
  .form-select {
    padding: 0.6rem 0.8rem 0.6rem 2rem;
    font-size: 15px;
  }

  .input-icon {
    width: 13px;
    height: 13px;
  }

  .btn-cancelar,
  .btn-guardar {
    padding: 0.6rem 0.8rem;
    font-size: 0.75rem;
  }
}

/* ========== SWEETALERT MODAL DELETE ========== */
:deep(.swal-delete-popup) {
  background: white !important;
  border: 1.5px solid rgba(239, 68, 68, 0.3) !important;
  border-radius: 16px !important;
  box-shadow: 0 20px 60px rgba(239, 68, 68, 0.15) !important;
  backdrop-filter: blur(12px) !important;
}

:deep(.swal-delete-title) {
  color: #dc2626 !important;
  font-size: 1.4rem !important;
  font-weight: 700 !important;
}

:deep(.swal-delete-html) {
  color: #374151 !important;
  font-size: 0.95rem !important;
}

:deep(.swal-delete-confirm) {
  background: linear-gradient(135deg, #ef4444, #dc2626) !important;
  border: none !important;
  color: white !important;
  font-weight: 700 !important;
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
  transition: all 0.3s ease !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}

:deep(.swal-delete-confirm:hover) {
  background: linear-gradient(135deg, #f87171, #ef4444) !important;
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
  transform: translateY(-2px) !important;
}

:deep(.swal-delete-confirm:active) {
  transform: translateY(0) !important;
}

:deep(.swal-delete-cancel) {
  background: rgba(107, 114, 128, 0.1) !important;
  border: 1px solid rgba(107, 114, 128, 0.3) !important;
  color: #374151 !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

:deep(.swal-delete-cancel:hover) {
  background: rgba(107, 114, 128, 0.2) !important;
  border-color: rgba(107, 114, 128, 0.5) !important;
}

:deep(.swal2-icon-warning) {
  border-color: rgba(239, 68, 68, 0.3) !important;
  background: rgba(239, 68, 68, 0.05) !important;
}

/* ========== SWEETALERT2 CONTAINER CENTERING ========== */
:deep(.swal2-container) {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 1001 !important;
}

:deep(.swal-delete-popup) {
  margin: auto !important;
}

/* ========== RESPONSIVE SWEETALERT ========== */
@media (max-width: 640px) {
  :deep(.swal-delete-popup) {
    padding: 1.2rem !important;
    margin: auto !important;
  }

  :deep(.swal-delete-title) {
    font-size: 1.2rem !important;
  }

  :deep(.swal-delete-html) {
    font-size: 0.9rem !important;
  }

  :deep(.swal-delete-confirm),
  :deep(.swal-delete-cancel) {
    padding: 0.65rem 1.2rem !important;
    font-size: 0.85rem !important;
  }
}

@media (max-width: 480px) {
  :deep(.swal-delete-popup) {
    padding: 1rem !important;
    margin: 0.5rem !important;
  }

  :deep(.swal-delete-title) {
    font-size: 1.1rem !important;
    margin-bottom: 0.8rem !important;
  }

  :deep(.swal-delete-html) {
    font-size: 0.85rem !important;
  }

  :deep(.swal2-actions) {
    flex-direction: column !important;
    gap: 0.7rem !important;
  }

  :deep(.swal-delete-confirm),
  :deep(.swal-delete-cancel) {
    width: 100% !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.8rem !important;
  }

  :deep(.swal2-icon) {
    font-size: 2rem !important;
  }
}

@media (max-width: 375px) {
  :deep(.swal-delete-popup) {
    padding: 0.9rem !important;
  }

  :deep(.swal-delete-title) {
    font-size: 1rem !important;
  }

  :deep(.swal-delete-html) {
    font-size: 0.8rem !important;
  }

  :deep(.swal-delete-confirm),
  :deep(.swal-delete-cancel) {
    padding: 0.65rem 0.9rem !important;
    font-size: 0.75rem !important;
  }
}

/* ========== SWEETALERT SUCCESS MODAL ========== */
:deep(.swal-success-popup) {
  border-radius: 16px !important;
  border: 1px solid rgba(16, 185, 129, 0.3) !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 30px rgba(16, 185, 129, 0.15) !important;
  padding: 1.5rem !important;
  max-width: 420px !important;
  width: 90% !important;
  margin: auto !important;
}

:deep(.swal-success-title) {
  font-size: 1.5rem !important;
  font-weight: 700 !important;
  color: #10b981 !important;
  text-shadow: 0 0 10px rgba(16, 185, 129, 0.3) !important;
  margin-bottom: 0.5rem !important;
}

:deep(.swal-success-icon) {
  border-color: rgba(16, 185, 129, 0.4) !important;
  margin-bottom: 1rem !important;
}

:deep(.swal-success-icon .swal2-success-ring) {
  border-color: rgba(16, 185, 129, 0.3) !important;
}

:deep(.swal-success-icon .swal2-success-line-tip),
:deep(.swal-success-icon .swal2-success-line-long) {
  background-color: #10b981 !important;
}

:deep(.swal-success-html) {
  padding: 0 !important;
  margin-top: 0.5rem !important;
}

:deep(.swal-success-content) {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(240, 253, 244, 0.8);
  border-radius: 12px;
  border: 1px solid rgba(22, 163, 74, 0.2);
}

:deep(.swal-success-item) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0.8rem;
  background: rgba(220, 252, 231, 0.8);
  border-radius: 8px;
  border: 1px solid rgba(22, 163, 74, 0.2);
}

:deep(.swal-success-label) {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

:deep(.swal-success-value) {
  font-size: 0.9rem;
  color: #1e3a2f;
  font-weight: 600;
  text-align: right;
  max-width: 60%;
  word-break: break-word;
}

:deep(.swal-success-badge) {
  font-size: 0.75rem;
  padding: 0.3rem 0.75rem;
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.2), rgba(22, 163, 74, 0.1));
  border: 1px solid rgba(22, 163, 74, 0.4);
  border-radius: 20px;
  color: #16a34a;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

:deep(.swal-success-confirm) {
  background: linear-gradient(135deg, #10b981, #059669) !important;
  border: 1px solid rgba(16, 185, 129, 0.5) !important;
  border-radius: 10px !important;
  padding: 0.75rem 2rem !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  color: #0f172a !important;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
  transition: all 0.3s ease !important;
}

:deep(.swal-success-confirm:hover) {
  background: linear-gradient(135deg, #34d399, #10b981) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
}

/* ========== SWEETALERT SUCCESS RESPONSIVE ========== */
@media (max-width: 640px) {
  :deep(.swal-success-popup) {
    padding: 1.25rem !important;
    max-width: 95% !important;
    border-radius: 14px !important;
  }

  :deep(.swal-success-title) {
    font-size: 1.3rem !important;
  }

  :deep(.swal-success-content) {
    padding: 0.75rem;
    gap: 0.6rem;
  }

  :deep(.swal-success-item) {
    padding: 0.5rem 0.65rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
  }

  :deep(.swal-success-value) {
    max-width: 100%;
    text-align: left;
  }

  :deep(.swal-success-confirm) {
    padding: 0.7rem 1.5rem !important;
    font-size: 0.9rem !important;
    width: 100% !important;
  }
}

@media (max-width: 480px) {
  :deep(.swal-success-popup) {
    padding: 1rem !important;
  }

  :deep(.swal-success-title) {
    font-size: 1.2rem !important;
  }

  :deep(.swal-success-content) {
    padding: 0.6rem;
    gap: 0.5rem;
  }

  :deep(.swal-success-item) {
    padding: 0.45rem 0.55rem;
  }

  :deep(.swal-success-label) {
    font-size: 0.75rem;
  }

  :deep(.swal-success-value) {
    font-size: 0.85rem;
  }

  :deep(.swal-success-badge) {
    font-size: 0.7rem;
    padding: 0.25rem 0.6rem;
  }
}

@media (max-width: 375px) {
  :deep(.swal-success-popup) {
    padding: 0.9rem !important;
  }

  :deep(.swal-success-title) {
    font-size: 1.1rem !important;
  }

  :deep(.swal-success-label) {
    font-size: 0.7rem;
  }

  :deep(.swal-success-value) {
    font-size: 0.8rem;
  }
}

/* ========== SCROLLBAR ========== */
</style>
