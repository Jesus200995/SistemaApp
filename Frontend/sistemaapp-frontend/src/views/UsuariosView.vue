<template>
  <div class="usuarios-container">
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
        <div 
          class="modal-crear-usuario"
          v-motion
          :initial="{ opacity: 0, scale: 0.9, y: -20 }"
          :enter="{ opacity: 1, scale: 1, y: 0, transition: { duration: 300 } }"
        >
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

    <!-- Contenido principal -->
    <div class="usuarios-content">
      <!-- Tarjeta principal -->
      <div
        v-motion
        :initial="{ opacity: 0, scale: 0.95, y: 30 }"
        :enter="{ opacity: 1, scale: 1, y: 0, transition: { delay: 200, duration: 700 } }"
        class="usuarios-card"
      >
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
                <th>Rol</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <!-- Skeleton loader -->
              <tr v-if="loading" v-for="n in limit" :key="'skeleton-' + n" class="skeleton-row">
                <td colspan="5">
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
                <td class="cell-rol">
                  <span :class="['rol-badge', `rol-${u.rol}`]">
                    {{ u.rol.toUpperCase() }}
                  </span>
                </td>
                <td class="cell-actions">
                  <button
                    @click="editUser(u)"
                    class="action-btn edit-btn"
                    title="Editar"
                  >
                    <Edit class="action-icon" />
                  </button>
                  <button
                    @click="deleteUser(u.id)"
                    class="action-btn delete-btn"
                    title="Eliminar"
                  >
                    <Trash2 class="action-icon" />
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
                <div>
                  <h3>{{ u.nombre }}</h3>
                  <p class="card-email">{{ u.email }}</p>
                </div>
              </div>
              <span :class="['rol-badge', `rol-${u.rol}`]">
                {{ u.rol.toUpperCase() }}
              </span>
            </div>
            <div class="card-actions">
              <button
                @click="editUser(u)"
                class="action-btn edit-btn"
                title="Editar"
              >
                <Edit class="action-icon" />
                <span>Editar</span>
              </button>
              <button
                @click="deleteUser(u.id)"
                class="action-btn delete-btn"
                title="Eliminar"
              >
                <Trash2 class="action-icon" />
                <span>Eliminar</span>
              </button>
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
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :enter="{ opacity: 1, transition: { delay: 600, duration: 600 } }"
        class="stats-section"
      >
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
      // Mostrar mensaje de éxito
      Swal.fire({
        icon: 'success',
        title: '✅ Usuario Creado',
        html: `
          <div style="text-align: left; padding: 10px;">
            <p><strong>Nombre:</strong> ${result.data?.nombre || nuevoUsuario.value.nombre}</p>
            <p><strong>Email:</strong> ${result.data?.email || nuevoUsuario.value.email}</p>
            <p><strong>Rol:</strong> ${(result.data?.rol || nuevoUsuario.value.rol).toUpperCase().replace('_', ' ')}</p>
          </div>
        `,
        confirmButtonColor: '#10b981'
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

const editUser = async (user) => {
  const { value: formValues } = await Swal.fire({
    title: 'Editar usuario',
    html:
      `<input id="nombre" class="swal2-input" placeholder="Nombre" value="${user.nombre}">` +
      `<input id="email" class="swal2-input" placeholder="Email" value="${user.email}">` +
      `<input id="rol" class="swal2-input" placeholder="Rol" value="${user.rol}">`,
    focusConfirm: false,
    showCancelButton: true,
    confirmButtonText: 'Guardar',
    preConfirm: () => {
      return {
        nombre: document.getElementById('nombre').value,
        email: document.getElementById('email').value,
        rol: document.getElementById('rol').value,
      }
    },
  })

  if (formValues) {
    try {
      const apiUrl = getSecureApiUrl()
      await axios.put(`${apiUrl}/auth/users/${user.id}`, formValues, {
        headers: { Authorization: `Bearer ${auth.token}` },
      })
      Swal.fire('✅ Actualizado', 'El usuario fue modificado correctamente.', 'success')
      fetchUsuarios()
    } catch (err) {
      Swal.fire('❌ Error', 'No se pudo actualizar el usuario.', 'error')
    }
  }
}

const deleteUser = async (id) => {
  const result = await Swal.fire({
    title: '¿Eliminar usuario?',
    text: 'Esta acción no se puede deshacer.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar',
  })

  if (result.isConfirmed) {
    try {
      const apiUrl = getSecureApiUrl()
      await axios.delete(`${apiUrl}/auth/users/${id}`, {
        headers: { Authorization: `Bearer ${auth.token}` },
      })
      Swal.fire('🗑️ Eliminado', 'El usuario ha sido eliminado.', 'success')
      fetchUsuarios()
    } catch (err) {
      Swal.fire('❌ Error', 'No se pudo eliminar el usuario.', 'error')
    }
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
  padding: 1rem 0.9rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.user-card:hover {
  background: rgba(15, 23, 42, 0.7);
  border-color: rgba(16, 185, 129, 0.3);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.card-nombre {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.card-avatar {
  width: 36px;
  height: 36px;
  background: transparent;
  border: 2px solid #84cc16;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #84cc16;
  font-weight: 600;
  flex-shrink: 0;
  font-size: 0.75rem;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.5);
}

.card-nombre h3 {
  font-size: 0.85rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.1rem;
  line-height: 1.2;
}

.card-email {
  font-size: 0.7rem;
  color: #94a3b8;
  line-height: 1.2;
}

.card-actions {
  display: flex;
  gap: 0.6rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.card-actions .action-btn {
  flex: 1;
  padding: 0.4rem 0.8rem;
  font-size: 0.7rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
}

.card-actions .edit-btn {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.card-actions .edit-btn:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.5);
  transform: scale(1.05);
}

.card-actions .delete-btn {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.card-actions .delete-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
  transform: scale(1.05);
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

/* ========== SCROLLBAR ========== */
</style>
