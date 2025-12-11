<template>
  <div class="usuarios-container">
    <!-- Menú hamburguesa global -->
    <HamburgerMenu />

    <!-- Fondo decorativo -->
    <div class="background-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <!-- Header con botón de regreso -->
    <header class="usuarios-header">
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

    <!-- Modal Crear Usuario -->
    <Teleport to="body">
      <div v-if="showModalCrear" class="modal-overlay" @click.self="cerrarModalCrearUsuario">
        <div class="modal-crear-usuario">
          <div class="modal-header">
            <div class="modal-icon">
              <UserPlus class="modal-icon-svg" />
            </div>
            <h2 class="modal-title">Crear Nuevo Usuario</h2>
            <p class="modal-subtitle">{{ getDescripcionRol() }}</p>
            <button @click="cerrarModalCrearUsuario" class="modal-close">
              <X class="close-icon" />
            </button>
          </div>

          <form @submit.prevent="crearUsuario" class="modal-form">
            <div class="form-group">
              <label for="nombre" class="form-label">
                <User class="label-icon" />
                Nombre completo
              </label>
              <input
                id="nombre"
                v-model="nuevoUsuario.nombre"
                type="text"
                class="form-input"
                placeholder="NOMBRE COMPLETO"
                required
                minlength="2"
                @input="nuevoUsuario.nombre = nuevoUsuario.nombre.toUpperCase()"
              />
            </div>

            <div class="form-group">
              <label for="email" class="form-label">
                <Mail class="label-icon" />
                Correo electrónico
              </label>
              <input
                id="email"
                v-model="nuevoUsuario.email"
                type="email"
                class="form-input"
                placeholder="correo@ejemplo.com"
                required
              />
            </div>

            <div class="form-group">
              <label for="password" class="form-label">
                <Lock class="label-icon" />
                Contraseña
              </label>
              <div class="password-wrapper">
                <input
                  id="password"
                  v-model="nuevoUsuario.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="Mínimo 6 caracteres"
                  required
                  minlength="6"
                />
                <button type="button" @click="showPassword = !showPassword" class="toggle-password">
                  <Eye v-if="!showPassword" class="eye-icon" />
                  <EyeOff v-else class="eye-icon" />
                </button>
              </div>
            </div>

            <div class="form-group">
              <label for="rol" class="form-label">
                <Shield class="label-icon" />
                Rol del usuario
              </label>
              <select
                id="rol"
                v-model="nuevoUsuario.rol"
                class="form-select"
                required
              >
                <option value="" disabled>Selecciona un rol</option>
                <option 
                  v-for="rol in rolesDisponibles" 
                  :key="rol.value" 
                  :value="rol.value"
                >
                  {{ rol.label }}
                </option>
              </select>
            </div>

            <!-- Campo CURP -->
            <div class="form-group">
              <label for="curp" class="form-label">
                <IdCard class="label-icon" />
                CURP
              </label>
              <input
                id="curp"
                v-model="nuevoUsuario.curp"
                type="text"
                class="form-input"
                placeholder="XXXX######HXXXXX##"
                maxlength="18"
                minlength="18"
                pattern="[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[A-Z0-9]{2}"
                @input="nuevoUsuario.curp = nuevoUsuario.curp.toUpperCase()"
                required
              />
              <span class="field-hint">18 caracteres alfanuméricos (obligatorio)</span>
            </div>

            <!-- Campo Teléfono -->
            <div class="form-group">
              <label for="telefono" class="form-label">
                <Phone class="label-icon" />
                Número de Teléfono
              </label>
              <input
                id="telefono"
                v-model="nuevoUsuario.telefono"
                type="tel"
                class="form-input"
                placeholder="10 dígitos"
                maxlength="10"
                minlength="10"
                pattern="[0-9]{10}"
                @input="nuevoUsuario.telefono = nuevoUsuario.telefono.replace(/[^0-9]/g, '').slice(0, 10)"
              />
              <span class="field-hint" v-if="nuevoUsuario.telefono && nuevoUsuario.telefono.length > 0 && nuevoUsuario.telefono.length < 10">{{ nuevoUsuario.telefono.length }}/10 dígitos</span>
            </div>

            <!-- Campo Territorio -->
            <div class="form-group">
              <label for="territorio" class="form-label">
                <MapPin class="label-icon" />
                Territorio <span class="required-mark">*</span>
              </label>
              <select
                id="territorio"
                v-model="nuevoUsuario.territorio"
                class="form-select"
                required
              >
                <option value="" disabled>Selecciona un territorio</option>
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

            <div class="form-actions">
              <button type="button" @click="cerrarModalCrearUsuario" class="btn-cancelar">
                Cancelar
              </button>
              <button type="submit" class="btn-crear" :disabled="creando">
                <Loader2 v-if="creando" class="spinner" />
                <span v-else>Crear Usuario</span>
              </button>
            </div>
          </form>
        </div>
      </div>
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
      <!-- Tarjeta principal -->
      <div class="usuarios-card">
        <!-- Buscador -->
        <div class="search-section">
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

        <!-- Tabla responsiva (Desktop) -->
        <div class="hidden md:block table-wrapper">
          <table class="users-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Email</th>
                <th>CURP</th>
                <th>Teléfono</th>
                <th>Territorio</th>
                <th>Rol</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <!-- Skeleton loader -->
              <tr v-if="loading" v-for="n in limit" :key="'skeleton-' + n" class="skeleton-row">
                <td colspan="8">
                  <div class="skeleton-line"></div>
                </td>
              </tr>

              <!-- Datos reales -->
              <tr
                v-for="u in filteredUsuarios"
                :key="u.id"
                class="user-row"
              >
                <td class="cell-id">
                  <span class="id-badge">{{ u.id }}</span>
                </td>
                <td class="cell-nombre">
                  <div class="nombre-content">
                    <span>{{ u.nombre }}</span>
                  </div>
                </td>
                <td class="cell-email">{{ u.email }}</td>
                <td class="cell-curp">
                  <span class="curp-badge">{{ u.curp || '—' }}</span>
                </td>
                <td class="cell-telefono">
                  <span class="telefono-text">{{ u.telefono || '—' }}</span>
                </td>
                <td class="cell-territorio">
                  <span class="territorio-badge">{{ u.territorio || '—' }}</span>
                </td>
                <td class="cell-rol">
                  <span :class="['rol-badge', `rol-${u.rol}`]">
                    {{ u.rol.toUpperCase().replace(/_/g, ' ') }}
                  </span>
                </td>
                <td class="cell-actions">
                  <div class="actions-group">
                    <button
                      @click="abrirModalEditar(u)"
                      class="action-btn edit-btn"
                      title="Editar usuario"
                    >
                      <Edit class="action-icon" />
                    </button>
                    <button
                      @click="abrirConfirmarEliminar(u.id, u.nombre)"
                      class="action-btn delete-btn"
                      title="Eliminar usuario"
                    >
                      <Trash2 class="action-icon" />
                    </button>
                  </div>
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

        <!-- Cards Mobile -->
        <div class="md:hidden cards-wrapper">
          <!-- Skeleton loader -->
          <div v-if="loading" v-for="n in limit" :key="'card-skeleton-' + n" class="skeleton-card">
            <div class="skeleton-line" style="width: 60%"></div>
            <div class="skeleton-line" style="width: 80%; margin-top: 0.5rem"></div>
          </div>

          <!-- Datos reales -->
          <div
            v-for="u in filteredUsuarios"
            :key="u.id"
            class="user-card"
          >
            <div class="card-header">
              <div class="card-nombre">
                <div class="card-avatar">{{ u.nombre.charAt(0).toUpperCase() }}</div>
                <div class="card-info">
                  <h3>{{ u.nombre }}</h3>
                  <p class="card-email">{{ u.email }}</p>
                </div>
              </div>
              <span :class="['rol-badge', `rol-${u.rol}`]">
                {{ u.rol.toUpperCase().replace(/_/g, ' ') }}
              </span>
            </div>
            <div class="card-details">
              <div class="detail-item">
                <span class="detail-label">CURP:</span>
                <span class="detail-value">{{ u.curp || '—' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Tel:</span>
                <span class="detail-value">{{ u.telefono || '—' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Territorio:</span>
                <span class="detail-value">{{ u.territorio || '—' }}</span>
              </div>
            </div>
          </div>

          <!-- Estado vacío -->
          <div v-if="!loading && filteredUsuarios.length === 0" class="empty-state">
            <Search class="empty-icon" />
            <h3>No se encontraron usuarios</h3>
            <p>Intenta con otros términos de búsqueda</p>
          </div>
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

      <!-- Estadísticas -->
      <div class="stats-section">
        <div class="stat-card" v-if="adminCount > 0">
          <div class="stat-number">{{ adminCount }}</div>
          <div class="stat-label">Admins</div>
        </div>
        <div class="stat-card" v-if="territorialCount > 0">
          <div class="stat-number">{{ territorialCount }}</div>
          <div class="stat-label">Territoriales</div>
        </div>
        <div class="stat-card" v-if="facilitadorCount > 0">
          <div class="stat-number">{{ facilitadorCount }}</div>
          <div class="stat-label">Facilitadores</div>
        </div>
        <div class="stat-card" v-if="tecnicoProductivoCount > 0">
          <div class="stat-number">{{ tecnicoProductivoCount }}</div>
          <div class="stat-label">Téc. Productivos</div>
        </div>
        <div class="stat-card" v-if="tecnicoSocialCount > 0">
          <div class="stat-number">{{ tecnicoSocialCount }}</div>
          <div class="stat-label">Téc. Sociales</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ total }}</div>
          <div class="stat-label">Total</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { Users, RotateCw, Search, ChevronLeft, ChevronRight, ArrowLeft, Edit, Trash2, UserPlus, X, User, Mail, Lock, Shield, Eye, EyeOff, Loader2, IdCard, Phone, MapPin } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import HamburgerMenu from '../components/HamburgerMenu.vue'
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
    return 'Como Coordinador Territorial (Admin), puedes crear usuarios Territoriales'
  } else if (rol === 'territorial') {
    return 'Como Territorial, puedes crear usuarios Facilitadores'
  } else if (rol === 'facilitador') {
    return 'Como Facilitador, puedes crear Técnicos Productivos o Técnicos Sociales'
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
        background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
        color: '#e2e8f0',
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
    html: `<p style="color: #e2e8f0; font-size: 1rem; margin: 1rem 0;">Estás a punto de eliminar a</p><p style="color: #fca5a5; font-weight: 700; font-size: 1.1rem; margin: 0.5rem 0;">«${nombre}»</p><p style="color: #cbd5e1; font-size: 0.9rem; margin: 1rem 0;">Esta acción no se puede deshacer.</p>`,
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
    background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
    didOpen: () => {
      const popup = document.querySelector('.swal2-popup');
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
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
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
.usuarios-content {
  position: relative;
  z-index: 5;
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
  margin-top: 70px;
  overflow-y: auto;
  height: calc(100vh - 70px);
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
  background: rgba(132, 204, 22, 0.12);
  border-bottom: 1px solid rgba(132, 204, 22, 0.1);
  backdrop-filter: blur(12px);
  padding: 1rem 1.2rem;
  box-shadow: 0 4px 20px rgba(132, 204, 22, 0.1);
  width: 100%;
  box-sizing: border-box;
}

.header-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
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
  background: rgba(132, 204, 22, 0.1);
  border: 1.5px solid rgba(132, 204, 22, 0.4);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  color: #84cc16;
  backdrop-filter: blur(10px);
  flex-shrink: 0;
}

.back-button:hover {
  background: rgba(132, 204, 22, 0.2);
  transform: translateX(-4px);
  box-shadow: 0 4px 15px rgba(132, 204, 22, 0.3);
  border-color: rgba(132, 204, 22, 0.6);
}

.back-button:active {
  transform: translateX(-2px);
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
  color: #84cc16;
  stroke-width: 2;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #84cc16;
  margin: 0;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.4);
}

.header-subtitle {
  font-size: 0.75rem;
  color: #cbd5e1;
  margin: 0;
  margin-top: 0.2rem;
}

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

/* ========== USUARIOS CARD ========== */
.usuarios-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 20px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  margin-bottom: 1.5rem;
}

/* ========== SEARCH SECTION ========== */
.search-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  width: 20px;
  height: 20px;
  color: #10b981;
  pointer-events: none;
}

.search-input {
  width: 100%;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 10px;
  padding: 0.6rem 1rem 0.6rem 2.5rem;
  color: #e2e8f0;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: #64748b;
}

.search-input:focus {
  outline: none;
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.7);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.results-info {
  font-size: 0.875rem;
  color: #94a3b8;
  white-space: nowrap;
  padding: 0.5rem 1rem;
}

/* ========== TABLE (DESKTOP) ========== */
.table-wrapper {
  overflow-x: auto;
  margin-bottom: 1rem;
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.75rem;
}

.users-table thead {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
  border-bottom: 2px solid rgba(16, 185, 129, 0.3);
}

.users-table thead th {
  padding: 0.6rem 0.5rem;
  text-align: left;
  font-weight: 600;
  color: #10b981;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.7rem;
}

.skeleton-row {
  animation: pulse-loading 2s ease-in-out infinite;
}

.skeleton-line {
  height: 1rem;
  background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.2) 50%, rgba(16, 185, 129, 0.1) 100%);
  border-radius: 4px;
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

@keyframes pulse-loading {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.user-row {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  transition: all 0.3s ease;
}

.user-row:hover {
  background: rgba(16, 185, 129, 0.05);
  border-bottom-color: rgba(16, 185, 129, 0.2);
}

.users-table td {
  padding: 0.6rem 0.5rem;
  color: #cbd5e1;
}

/* Cell Styles */
.cell-id {
  width: 80px;
}

.id-badge {
  display: inline-block;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.85rem;
}

.cell-nombre {
  font-weight: 500;
}

.nombre-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nombre-avatar {
  width: 32px;
  height: 32px;
  background: transparent;
  border: 2px solid #84cc16;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #84cc16;
  font-weight: 600;
  font-size: 0.75rem;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.5);
}

.cell-email {
  color: #94a3b8;
  font-size: 0.9rem;
}

.cell-curp {
  font-family: 'Courier New', monospace;
  width: 140px;
}

.curp-badge {
  display: inline-block;
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.cell-telefono {
  width: 110px;
}

.telefono-text {
  display: inline-block;
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 500;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.cell-territorio {
  width: 150px;
}

.territorio-badge {
  display: inline-block;
  background: rgba(236, 72, 153, 0.15);
  color: #f472b6;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.8rem;
  border: 1px solid rgba(236, 72, 153, 0.3);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}

.cell-rol {
  text-align: center;
}

.cell-actions {
  text-align: center;
  width: 100px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  margin: 0 0.25rem;
}

.action-icon {
  width: 18px;
  height: 18px;
}

.edit-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  transform: scale(1.2);
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  transform: scale(1.2);
}

.rol-badge {
  display: inline-block;
  padding: 0.375rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}

.rol-admin {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.rol-territorial {
  background: rgba(139, 92, 246, 0.2);
  color: #c4b5fd;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.rol-facilitador {
  background: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.rol-tecnico_productivo {
  background: rgba(16, 185, 129, 0.2);
  color: #86efac;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.rol-tecnico_social {
  background: rgba(245, 158, 11, 0.2);
  color: #fcd34d;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.rol-usuario {
  background: rgba(16, 185, 129, 0.2);
  color: #86efac;
}

/* ========== CARDS (MOBILE) ========== */
.cards-wrapper {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.skeleton-card {
  padding: 1.25rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 12px;
  animation: pulse-loading 2s ease-in-out infinite;
}

.user-card {
  padding: 1.25rem;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
  border: 1px solid rgba(132, 204, 22, 0.15);
  border-radius: 14px;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
}

.user-card:hover {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border-color: rgba(132, 204, 22, 0.3);
  box-shadow: 0 8px 24px rgba(132, 204, 22, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.card-nombre {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex: 1;
}

.card-avatar {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, rgba(132, 204, 22, 0.2), rgba(132, 204, 22, 0.1));
  border: 2.5px solid #84cc16;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #84cc16;
  font-weight: 700;
  flex-shrink: 0;
  font-size: 0.9rem;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.5);
  box-shadow: 0 0 12px rgba(132, 204, 22, 0.2);
}

.card-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.card-nombre h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0;
  line-height: 1.2;
}

.card-email {
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0;
  line-height: 1.2;
}

.card-details {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(132, 204, 22, 0.1);
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
}

.detail-label {
  font-size: 0.7rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-value {
  font-size: 0.8rem;
  color: #e2e8f0;
  font-family: 'Courier New', monospace;
  text-align: right;
  flex: 1;
}

.card-actions {
  display: none;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #64748b;
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.25rem;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.empty-state p {
  font-size: 0.95rem;
}

/* ========== PAGINATION ========== */
.pagination-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  margin-bottom: 2rem;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
  padding: 0.75rem 1.25rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(16, 185, 129, 0.2) 100%);
  border-color: rgba(16, 185, 129, 0.5);
  transform: translateY(-2px);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-icon {
  width: 18px;
  height: 18px;
}

.pagination-info {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #cbd5e1;
}

.page-current {
  color: #10b981;
  font-size: 1.25rem;
}

.page-separator {
  color: #64748b;
}

.page-total {
  color: #94a3b8;
}

/* ========== STATS SECTION ========== */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 0.75rem;
}

.stat-card {
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
  padding: 0.9rem 0.75rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.4);
  transform: translateY(-2px);
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #10b981;
  margin-bottom: 0.3rem;
}

.stat-label {
  font-size: 0.7rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .usuarios-header {
    padding: 0.8rem 1rem;
  }

  .header-title {
    font-size: 0.85rem;
  }

  .header-icon-small {
    width: 28px;
    height: 28px;
  }

  .icon-stat {
    width: 18px;
    height: 18px;
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

  .usuarios-content {
    padding: 1.5rem 0.5rem;
  }

  .usuarios-card {
    padding: 1rem;
  }

  .search-section {
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
  }

  .results-info {
    order: -1;
    text-align: center;
    width: 100%;
    font-size: 0.75rem;
  }

  .pagination-section {
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .pagination-btn {
    flex: 1;
    min-width: 100px;
    font-size: 0.75rem;
  }

  .stats-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .usuarios-content {
    padding: 1.5rem 0.5rem;
  }

  .header-title {
    font-size: 0.8rem;
  }

  .header-subtitle {
    font-size: 0.7rem;
  }

  .usuarios-card {
    padding: 1rem;
  }

  .search-input {
    font-size: 16px; /* Previene zoom en iOS */
  }

  .pagination-section {
    padding: 1rem;
  }

  .pagination-btn {
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
  }

  .pagination-info {
    font-size: 0.85rem;
  }

  .page-current {
    font-size: 1.1rem;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .rol-badge {
    align-self: flex-start;
  }
}

@media (max-width: 480px) {
  .usuarios-header {
    padding: 0.6rem 0.8rem;
  }

  .back-button {
    width: 36px;
    height: 36px;
  }

  .back-icon {
    width: 18px;
    height: 18px;
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

  .reload-button {
    width: 34px;
    height: 34px;
  }

  .reload-icon {
    width: 18px;
    height: 18px;
  }

  .usuarios-content {
    padding: 1rem 0.5rem;
  }
}

/* ========== HEADER ACTIONS ========== */
.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* ========== CREATE BUTTON ========== */
.create-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 10px;
  padding: 0.5rem 1rem;
  color: white;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.create-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
}

.create-button:active {
  transform: translateY(0);
}

.create-icon {
  width: 18px;
  height: 18px;
}

.create-text {
  display: inline;
}

@media (max-width: 640px) {
  .create-text {
    display: none;
  }
  
  .create-button {
    padding: 0.5rem;
    border-radius: 50%;
    width: 36px;
    height: 36px;
  }
}

/* ========== MODAL OVERLAY ========== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

/* ========== MODAL CREAR USUARIO ========== */
.modal-crear-usuario {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 20px;
  padding: 0;
  max-width: 450px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  position: relative;
  padding: 1.5rem 1.5rem 1rem;
  text-align: center;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.modal-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
  border: 2px solid #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.modal-icon-svg {
  width: 28px;
  height: 28px;
  color: #10b981;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0 0 0.5rem;
}

.modal-subtitle {
  font-size: 0.85rem;
  color: #94a3b8;
  margin: 0;
  line-height: 1.4;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #ef4444;
}

.modal-close:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
}

.close-icon {
  width: 18px;
  height: 18px;
}

/* ========== MODAL FORM ========== */
.modal-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.label-icon {
  width: 16px;
  height: 16px;
  color: #10b981;
}

.form-input,
.form-select {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  color: #e2e8f0;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input::placeholder {
  color: #64748b;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
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
  background: #1e293b;
  color: #e2e8f0;
}

.password-wrapper {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.25rem;
  transition: color 0.3s ease;
}

.toggle-password:hover {
  color: #10b981;
}

.eye-icon {
  width: 18px;
  height: 18px;
}

.field-hint {
  display: block;
  font-size: 0.7rem;
  color: #64748b;
  margin-top: 0.3rem;
  font-style: italic;
}

.required-mark {
  color: #ef4444;
  font-weight: bold;
}

/* ========== FORM ACTIONS ========== */
.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancelar,
.btn-crear {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-cancelar {
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.3);
  color: #94a3b8;
}

.btn-cancelar:hover {
  background: rgba(148, 163, 184, 0.2);
  border-color: rgba(148, 163, 184, 0.5);
}

.btn-crear {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  color: white;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.btn-crear:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.btn-crear:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ========== RESPONSIVE MODAL ========== */
@media (max-width: 480px) {
  .modal-crear-usuario {
    max-height: 95vh;
    border-radius: 16px;
  }

  .modal-header {
    padding: 1.25rem 1.25rem 0.75rem;
  }

  .modal-icon {
    width: 50px;
    height: 50px;
  }

  .modal-icon-svg {
    width: 24px;
    height: 24px;
  }

  .modal-title {
    font-size: 1.1rem;
  }

  .modal-subtitle {
    font-size: 0.8rem;
  }

  .modal-form {
    padding: 1.25rem;
  }

  .form-actions {
    flex-direction: column;
  }
}

/* ========== MODAL OVERLAY ========== */
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
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(132, 204, 22, 0.2);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
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

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(132, 204, 22, 0.1);
  background: rgba(132, 204, 22, 0.05);
  border-radius: 16px 16px 0 0;
}

.modal-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #84cc16;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.3);
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
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.input-icon {
  width: 16px;
  height: 16px;
  color: #84cc16;
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
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 10px;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  color: #e2e8f0;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: #64748b;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #84cc16;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 3px rgba(132, 204, 22, 0.1);
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
  background: #1e293b;
  color: #e2e8f0;
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
  background: linear-gradient(135deg, #84cc16, #65a30d);
  border: 1px solid rgba(132, 204, 22, 0.5);
  border-radius: 8px;
  color: #0f172a;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 12px rgba(132, 204, 22, 0.2);
}

.btn-guardar:hover:not(:disabled) {
  background: linear-gradient(135deg, #a3e635, #84cc16);
  box-shadow: 0 6px 16px rgba(132, 204, 22, 0.3);
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
  border: 1.5px solid rgba(148, 163, 184, 0.4);
  background: rgba(15, 23, 42, 0.7);
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
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
  border: 1.5px solid rgba(239, 68, 68, 0.3) !important;
  border-radius: 16px !important;
  box-shadow: 0 20px 60px rgba(239, 68, 68, 0.2) !important;
  backdrop-filter: blur(12px) !important;
}

:deep(.swal-delete-title) {
  color: #fca5a5 !important;
  font-size: 1.4rem !important;
  font-weight: 700 !important;
  text-shadow: 0 0 8px rgba(239, 68, 68, 0.3) !important;
}

:deep(.swal-delete-html) {
  color: #cbd5e1 !important;
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
  color: #d1d5db !important;
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
  background: rgba(15, 23, 42, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(16, 185, 129, 0.15);
}

:deep(.swal-success-item) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0.8rem;
  background: rgba(30, 41, 59, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(71, 85, 105, 0.3);
}

:deep(.swal-success-label) {
  font-size: 0.85rem;
  color: #94a3b8;
  font-weight: 500;
}

:deep(.swal-success-value) {
  font-size: 0.9rem;
  color: #e2e8f0;
  font-weight: 600;
  text-align: right;
  max-width: 60%;
  word-break: break-word;
}

:deep(.swal-success-badge) {
  font-size: 0.75rem;
  padding: 0.3rem 0.75rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
  border: 1px solid rgba(16, 185, 129, 0.4);
  border-radius: 20px;
  color: #34d399;
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
