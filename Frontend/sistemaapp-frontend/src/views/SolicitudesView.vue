<template>
  <div class="solicitudes-container">
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
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
          class="form-section"
        >
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

                <!-- Usuario Destino - Dropdown mejorado -->
                <div class="form-group">
                  <label class="form-label">
                    <UserCheck :size="14" class="label-icon" />
                    Enviar a *
                  </label>
                  <div class="select-wrapper">
                    <select 
                      v-model="form.destino_id" 
                      class="form-select"
                      :class="{ 'loading-select': loadingUsuarios }"
                      required
                    >
                      <option value="">-- Selecciona destinatario --</option>
                      <optgroup 
                        v-for="grupo in usuariosAgrupados" 
                        :key="grupo.rol" 
                        :label="formatRol(grupo.rol)"
                      >
                        <option 
                          v-for="usuario in grupo.usuarios" 
                          :key="usuario.id" 
                          :value="usuario.id"
                        >
                          {{ usuario.nombre }} ({{ usuario.territorio }})
                        </option>
                      </optgroup>
                    </select>
                    <div v-if="loadingUsuarios" class="select-loading">
                      <div class="mini-spinner"></div>
                    </div>
                  </div>
                  <p class="form-hint">
                    <span v-if="usuariosDisponibles.length === 0 && !loadingUsuarios">
                      No hay usuarios disponibles
                    </span>
                    <span v-else>
                      {{ usuariosDisponibles.length }} usuario(s) disponible(s)
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

        <!-- Sección de solicitudes -->
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200, duration: 600 } }"
          class="solicitudes-section"
        >
          <div class="section-header">
            <h2 class="section-title">Historial de Solicitudes</h2>
            <div class="section-stats">
              <div class="stat-item">
                <span class="stat-label">Total:</span>
                <span class="stat-value">{{ solicitudes.length }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Pendientes:</span>
                <span class="stat-value pending">{{ countByStatus('pendiente') }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Aprobadas:</span>
                <span class="stat-value approved">{{ countByStatus('aprobada') }}</span>
              </div>
            </div>
          </div>

          <!-- Lista de solicitudes -->
          <div v-if="solicitudes.length > 0" class="solicitudes-table-wrapper">
            <div class="table-responsive">
              <table class="solicitudes-table">
                <thead>
                  <tr>
                    <th>Tipo</th>
                    <th>Descripción</th>
                    <th>Estado</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="solicitud in solicitudes" :key="solicitud.id" class="solicitud-row">
                    <td class="cell-tipo">
                      <span class="badge" :class="getBadgeClass(solicitud.tipo)">
                        {{ formatTipo(solicitud.tipo) }}
                      </span>
                    </td>
                    <td class="cell-descripcion">{{ solicitud.descripcion }}</td>
                    <td class="cell-estado">
                      <span class="status-badge" :class="`status-${solicitud.estado}`">
                        {{ formatEstado(solicitud.estado) }}
                      </span>
                    </td>
                    <td class="cell-fecha">{{ formatFecha(solicitud.fecha) }}</td>
                    <td class="cell-acciones">
                      <button
                        v-if="canApprove(solicitud) && solicitud.estado === 'pendiente'"
                        @click="actualizarEstado(solicitud.id, 'aprobada')"
                        class="action-btn approve-btn"
                        title="Aprobar"
                      >
                        <Check class="action-icon" />
                      </button>
                      <button
                        v-if="canApprove(solicitud) && solicitud.estado === 'pendiente'"
                        @click="actualizarEstado(solicitud.id, 'rechazada')"
                        class="action-btn reject-btn"
                        title="Rechazar"
                      >
                        <X class="action-icon" />
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Estado vacío -->
          <div v-else class="empty-state">
            <FileText class="empty-icon" />
            <p class="empty-title">No hay solicitudes</p>
            <p class="empty-text">Crea una nueva solicitud para comenzar</p>
          </div>
        </section>
      </div>
    </main>

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
import { FileText, Send, Check, X, ArrowLeft, UserCheck, MessageSquare } from 'lucide-vue-next'

const auth = useAuthStore()
const form = ref({ tipo: '', destino_id: null as number | null, descripcion: '' })
const solicitudes = ref([])
const loading = ref(false)

// Usuarios disponibles para enviar solicitud
const usuariosDisponibles = ref<any[]>([])
const loadingUsuarios = ref(false)

// Agrupar usuarios por rol
const usuariosAgrupados = computed(() => {
  const grupos: { [key: string]: any[] } = {}
  
  usuariosDisponibles.value.forEach(usuario => {
    if (!grupos[usuario.rol]) {
      grupos[usuario.rol] = []
    }
    grupos[usuario.rol].push(usuario)
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
    admin: '👑 Administradores',
    territorial: '🌍 Territoriales',
    facilitador: '🤝 Facilitadores',
    tecnico: '🔧 Técnicos'
  }
  return roles[rol] || rol
}

// Cargar usuarios disponibles
const cargarUsuariosDisponibles = async () => {
  loadingUsuarios.value = true
  try {
    const apiUrl = getSecureApiUrl()
    const res = await axios.get(`${apiUrl}/users/superiores`, {
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

const countByStatus = (estado: string) => {
  return solicitudes.value.filter(s => s.estado === estado).length
}

const canApprove = (solicitud: any) => {
  // Admin puede aprobar todas
  if (auth.user?.rol === 'admin') return true
  // Territorial/Facilitador puede aprobar las dirigidas a él
  if (auth.user?.rol === 'territorial' || auth.user?.rol === 'facilitador') {
    return solicitud.destino_id === auth.user?.id
  }
  return false
}

// API calls
const getSolicitudes = async () => {
  try {
    const apiUrl = getSecureApiUrl()
    const res = await axios.get(`${apiUrl}/solicitudes`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    solicitudes.value = res.data
  } catch (err) {
    console.error('Error al obtener solicitudes:', err)
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
  --color-primary: #10b981;
  --color-primary-dark: #059669;
  --color-bg-primary: #0f172a;
  --color-bg-secondary: #1e293b;
  --color-bg-tertiary: #111827;
  --color-text-primary: #f1f5f9;
  --color-text-secondary: #cbd5e1;
  --color-text-dim: #94a3b8;
  --color-border: rgba(148, 163, 184, 0.1);
  --color-blue: #3b82f6;
  --color-red: #ef4444;
  --color-yellow: #f59e0b;
  --color-purple: #8b5cf6;
}

/* ========== LAYOUT ========== */
.solicitudes-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
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
  opacity: 0.08;
  filter: blur(120px);
  mix-blend-mode: screen;
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
  background: rgba(132, 204, 22, 0.12);
  border-bottom: 1px solid rgba(132, 204, 22, 0.1);
  backdrop-filter: blur(12px);
  padding: 1rem 1.2rem;
  box-shadow: 0 4px 20px rgba(132, 204, 22, 0.1);
  width: 100%;
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
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.form-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.form-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #84cc16;
  margin: 0 0 0.3rem 0;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.3);
}

.form-subtitle {
  font-size: 0.8rem;
  color: #cbd5e1;
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
  color: #e2e8f0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.form-select,
.form-input,
.form-textarea {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #f1f5f9;
  font-size: 0.9rem;
  font-family: inherit;
  transition: all 0.3s ease;
  width: 100%;
}

.form-select:focus,
.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
  background: rgba(15, 23, 42, 0.7);
}

.form-input,
.form-select {
  height: 42px;
}

/* ========== SELECT MEJORADO ========== */
.select-wrapper {
  position: relative;
}

.form-select optgroup {
  background: #1e293b;
  color: #84cc16;
  font-weight: 600;
  padding: 0.5rem;
}

.form-select option {
  background: #0f172a;
  color: #f1f5f9;
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
  color: #84cc16;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-hint {
  font-size: 0.75rem;
  color: #cbd5e1;
  margin-top: 0.25rem;
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
  color: #f1f5f9;
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
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #f1f5f9;
}

.stat-value.pending {
  color: #f59e0b;
}

.stat-value.approved {
  color: #10b981;
}

/* ========== TABLE ========== */
.solicitudes-table-wrapper {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.table-responsive {
  overflow-x: auto;
}

.solicitudes-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.solicitudes-table thead {
  background: rgba(16, 185, 129, 0.12);
  border-bottom: 2px solid rgba(16, 185, 129, 0.2);
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

.solicitud-row {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  transition: all 0.3s ease;
}

.solicitud-row:hover {
  background: rgba(16, 185, 129, 0.05);
}

.solicitudes-table td {
  padding: 0.85rem;
  color: #e2e8f0;
}

.cell-tipo {
  width: 15%;
}

.cell-descripcion {
  width: 35%;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cell-estado {
  width: 12%;
}

.cell-fecha {
  width: 20%;
  font-size: 0.85rem;
}

.cell-acciones {
  width: 18%;
  display: flex;
  gap: 0.5rem;
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
  color: #cbd5e1;
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
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.status-aprobada {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.status-rechazada {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
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
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.reject-btn:hover {
  background: rgba(239, 68, 68, 0.3);
  transform: translateY(-2px);
}

.action-icon {
  width: 18px;
  height: 18px;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  background: rgba(30, 41, 59, 0.5);
  border: 1px dashed rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  text-align: center;
}

.empty-icon {
  width: 36px;
  height: 36px;
  color: #10b981;
  margin-bottom: 0.75rem;
  opacity: 0.8;
}

.empty-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0 0 0.35rem 0;
}

.empty-text {
  font-size: 0.8rem;
  color: #cbd5e1;
  margin: 0;
}

/* ========== FOOTER ========== */
.solicitudes-footer {
  position: relative;
  z-index: 5;
  text-align: center;
  padding: 1.25rem;
  border-top: 1px solid rgba(148, 163, 184, 0.15);
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(10px);
  font-size: 0.8rem;
  color: #cbd5e1;
}

.footer-highlight {
  color: #10b981;
  font-weight: 700;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
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

  .solicitudes-table {
    font-size: 0.75rem;
  }

  .solicitudes-table th,
  .solicitudes-table td {
    padding: 0.6rem 0.5rem;
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
  }

  .solicitudes-table th,
  .solicitudes-table td {
    padding: 0.5rem 0.4rem;
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
  }

  .solicitudes-table th,
  .solicitudes-table td {
    padding: 0.4rem 0.3rem;
  }
}
</style>
