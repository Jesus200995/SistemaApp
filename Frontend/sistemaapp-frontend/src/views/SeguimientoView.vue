<template>
  <div class="seguimiento-container">
    <!-- Fondo decorativo con blobs -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header con botón de regreso -->
    <header class="header-seguimiento">
      <div class="header-wrapper">
        <div class="header-left">
          <router-link to="/dashboard" class="back-button" title="Volver al Dashboard">
            <ArrowLeft class="back-icon" />
          </router-link>
          <div class="header-icon-small">
            <Microscope class="icon-stat" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Seguimiento</h1>
            <p class="header-subtitle">Seguimiento de campo</p>
          </div>
        </div>
        <button @click="recargarSeguimientos" class="reload-button" title="Recargar">
          <svg class="reload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M3 21v-5h5"></path>
          </svg>
        </button>
      </div>
    </header>

    <!-- Tabs -->
    <div class="tabs-wrapper">
      <div class="tabs-container">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="activeTab = tab"
          :class="['tab', { active: activeTab === tab }]"
        >
          {{ tab }}
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <main class="seguimiento-main">
      <div class="seguimiento-content">
        <!-- Tab 1: Crear Seguimiento -->
        <section v-if="activeTab === 'Crear Seguimiento'" class="form-section">
          <div class="form-header">
            <h2 class="form-title">Registrar Seguimiento</h2>
            <p class="form-subtitle">Completa los detalles de tu visita</p>
          </div>

          <form @submit.prevent="crearSeguimiento" class="seguimiento-form">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label"><User :size="16" class="label-icon" /> Sembrador *</label>
                <span class="form-hint">Elige al sembrador que visitaste</span>
                <div class="input-wrapper">
                  <select 
                    v-model="formulario.sembrador_id" 
                    required 
                    class="form-input form-select"
                    :class="{ 'placeholder-selected': !formulario.sembrador_id }"
                  >
                    <option :value="null" disabled>Selecciona tu sembrador...</option>
                    <option v-for="sem in sembradores" :key="sem.id" :value="sem.id">
                      {{ sem.nombre }} - {{ sem.comunidad }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label"><Calendar :size="16" class="label-icon" /> Fecha de visita *</label>
                <span class="form-hint">¿Cuándo realizaste la visita?</span>
                <div class="input-wrapper">
                  <input v-model="formulario.fecha_visita" type="date" required class="form-input" />
                </div>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label"><Leaf :size="16" class="label-icon" /> Estado del cultivo *</label>
                <span class="form-hint">Etapa actual del crecimiento</span>
                <div class="input-wrapper">
                  <select 
                    v-model="formulario.estado_cultivo" 
                    required 
                    class="form-input form-select"
                    :class="{ 'placeholder-selected': !formulario.estado_cultivo }"
                  >
                    <option value="" disabled>Selecciona el estado...</option>
                    <option value="Germinando">Germinando</option>
                    <option value="Vegetativo">Vegetativo</option>
                    <option value="Floración">Floración</option>
                    <option value="Fructificación">Fructificación</option>
                    <option value="Cosecha">Cosecha</option>
                    <option value="Plagas">Plagas</option>
                    <option value="Enfermedad">Enfermedad</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label"><TrendingUp :size="16" class="label-icon" /> Avance del cultivo *</label>
                <span class="form-hint">Porcentaje de progreso (1-100%)</span>
                <div class="avance-container">
                  <div class="slider-wrapper">
                    <input 
                      v-model.number="formulario.avance_porcentaje" 
                      type="range" 
                      min="1" 
                      max="100" 
                      step="1"
                      required
                      class="avance-slider"
                    />
                    <div class="slider-track">
                      <div class="slider-fill" :style="{ width: formulario.avance_porcentaje + '%' }"></div>
                    </div>
                  </div>
                  <div class="avance-input-wrapper">
                    <input 
                      v-model.number="formulario.avance_porcentaje" 
                      type="number" 
                      min="1" 
                      max="100" 
                      required
                      class="avance-input"
                    />
                    <span class="avance-percent">%</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="form-group full-width">
              <label class="form-label"><FileText :size="16" class="label-icon" /> Observaciones *</label>
              <span class="form-hint">Describe lo que observaste en tu visita</span>
              <textarea v-model="formulario.observaciones" required placeholder="Escribe aquí tus observaciones, detalles del cultivo, problemas encontrados, recomendaciones..." class="form-input textarea-input" rows="3"></textarea>
            </div>

            <!-- Sección de Fotografía -->
            <div class="form-group full-width">
              <label class="form-label"><Camera :size="16" class="label-icon" /> Fotografía</label>
              <span class="form-hint">Captura una foto del cultivo (opcional)</span>
              <div class="foto-upload-container">
                <!-- Preview de la imagen -->
                <div v-if="fotoPreview" class="foto-preview">
                  <img :src="fotoPreview" alt="Preview" class="preview-image" />
                  <button type="button" @click="eliminarFoto" class="btn-remove-foto" title="Eliminar foto">
                    <X :size="16" />
                  </button>
                </div>
                
                <!-- Botones de acción cuando no hay foto -->
                <div v-else class="foto-actions">
                  <!-- Input oculto para seleccionar archivo -->
                  <input 
                    type="file" 
                    ref="fileInput" 
                    @change="onFileSelected" 
                    accept="image/jpeg,image/png,image/webp"
                    class="hidden-input"
                  />
                  
                  <!-- Input oculto para capturar con cámara -->
                  <input 
                    type="file" 
                    ref="cameraInput" 
                    @change="onFileSelected" 
                    accept="image/*"
                    capture="environment"
                    class="hidden-input"
                  />
                  
                  <!-- Botón subir desde galería -->
                  <button type="button" @click="triggerFileInput" class="btn-foto btn-gallery">
                    <ImageIcon :size="20" />
                    <span>Galería</span>
                  </button>
                  
                  <!-- Botón tomar foto -->
                  <button type="button" @click="triggerCameraInput" class="btn-foto btn-camera">
                    <Camera :size="20" />
                    <span>Cámara</span>
                  </button>
                </div>
                
                <!-- Estado de carga -->
                <div v-if="subiendoFoto" class="foto-loading">
                  <div class="loading-spinner-small"></div>
                  <span>Subiendo foto...</span>
                </div>
              </div>
            </div>

            <!-- Botón Guardar con efecto vidrio líquido -->
            <div class="btn-submit-wrapper">
              <button type="submit" :disabled="cargando || subiendoFoto" class="btn-submit-glass">
                <div class="btn-glass-bg"></div>
                <div class="btn-glass-content">
                  <span v-if="cargando" class="btn-loading">
                    <svg class="spin-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"/>
                    </svg>
                    Guardando...
                  </span>
                  <span v-else class="btn-text">
                    <svg class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M20 6L9 17l-5-5"/>
                    </svg>
                    Guardar Seguimiento
                  </span>
                </div>
                <div class="btn-glass-shine"></div>
              </button>
            </div>
          </form>
        </section>

        <!-- Tab 2: Mis Seguimientos -->
        <section v-if="activeTab === 'Mis Seguimientos'" class="historial-section">
          <div class="section-header">
            <h2 class="section-title">Historial</h2>
            <span class="badge-count">{{ seguimientos.length }}</span>
          </div>

          <div v-if="seguimientos.length === 0" class="empty-state">
            <p>Sin seguimientos</p>
          </div>

          <div v-else class="table-wrapper">
            <table class="seguimiento-table">
              <thead>
                <tr>
                  <th>Sembrador</th>
                  <th>Fecha</th>
                  <th>Estado</th>
                  <th>% Avance</th>
                  <th>Observaciones</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="seg in seguimientos" :key="seg.id" class="table-row">
                  <td><strong>{{ seg.sembrador_nombre }}</strong></td>
                  <td>{{ formatearFecha(seg.fecha_visita) }}</td>
                  <td>
                    <span class="estado-badge" :class="'estado-' + seg.estado_cultivo">
                      {{ seg.estado_cultivo }}
                    </span>
                  </td>
                  <td>
                    <div class="progress-cell">
                      <div class="progress-bar-small">
                        <div class="progress-fill-small" :style="{ width: seg.avance_porcentaje + '%' }"></div>
                      </div>
                      <span>{{ seg.avance_porcentaje }}%</span>
                    </div>
                  </td>
                  <td class="text-ellipsis">{{ seg.observaciones?.substring(0, 30) || 'N/A' }}</td>
                  <td>
                    <button @click="eliminarSeguimiento(seg.id)" class="btn-action btn-delete" title="Eliminar seguimiento">
                      <Trash2 :size="16" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Tab 3: Reportes -->
        <section v-if="activeTab === 'Reportes'" class="reportes-section">
          <div class="reportes-grid">
            <div class="reporte-card">
              <h3><Users :size="18" class="card-icon" /> Por Técnico</h3>
              <table v-if="reporteTecnico.length > 0" class="mini-table">
                <tr v-for="tech in reporteTecnico" :key="tech.tecnico_id">
                  <td>{{ tech.tecnico_nombre }}</td>
                  <td class="text-right">{{ tech.total_seguimientos }}</td>
                </tr>
              </table>
              <div v-else class="empty-state">Sin datos</div>
            </div>

            <div class="reporte-card">
              <h3><BarChart3 :size="18" class="card-icon" /> Por Cultivo</h3>
              <table v-if="reporteCultivo.length > 0" class="mini-table">
                <tr v-for="cul in reporteCultivo" :key="cul.cultivo">
                  <td>{{ cul.cultivo }}</td>
                  <td class="text-right">{{ cul.total_seguimientos }}</td>
                </tr>
              </table>
              <div v-else class="empty-state">Sin datos</div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import axios from 'axios'
import Swal from 'sweetalert2'
import { 
  ArrowLeft, 
  Microscope, 
  Trash2, 
  Calendar, 
  Camera, 
  Image as ImageIcon, 
  X,
  User,
  Leaf,
  TrendingUp,
  FileText,
  Users,
  BarChart3
} from 'lucide-vue-next'

const auth = useAuthStore()
const API_URL = getSecureApiUrl()

// Interfaces
interface Sembrador {
  id: number
  nombre: string
  comunidad: string
}

interface Seguimiento {
  id: number
  sembrador_id: number
  sembrador_nombre: string
  fecha_visita: string
  estado_cultivo: string
  avance_porcentaje: number
  observaciones: string
  foto_url?: string
  creado_en: string
  comunidad: string
  cultivo_principal: string
  tecnico_nombre: string
}

interface ReporteTecnico {
  tecnico_id: number
  tecnico_nombre: string
  total_seguimientos: number
  avance_promedio: number
  rol: string
}

interface ReporteCultivo {
  cultivo: string
  total_seguimientos: number
  total_sembradores: number
  avance_promedio: number
}

// Estado
const activeTab = ref('Crear Seguimiento')
const tabs = ['Crear Seguimiento', 'Mis Seguimientos', 'Reportes']
const cargando = ref(false)

// Datos
const sembradores: Ref<Sembrador[]> = ref([])
const seguimientos: Ref<Seguimiento[]> = ref([])
const reporteTecnico: Ref<ReporteTecnico[]> = ref([])
const reporteCultivo: Ref<ReporteCultivo[]> = ref([])

// Formulario
const formulario = ref({
  sembrador_id: null as number | null,
  fecha_visita: new Date().toISOString().split('T')[0],
  estado_cultivo: '',
  observaciones: '',
  avance_porcentaje: 1,
  foto_url: ''
})

// Referencias para inputs de archivo
const fileInput = ref<HTMLInputElement | null>(null)
const cameraInput = ref<HTMLInputElement | null>(null)

// Estado de foto
const fotoPreview = ref<string | null>(null)
const subiendoFoto = ref(false)

// Funciones para manejo de fotos
const triggerFileInput = () => {
  fileInput.value?.click()
}

const triggerCameraInput = () => {
  cameraInput.value?.click()
}

const onFileSelected = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  // Validar tipo
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    Swal.fire('Error', 'Solo se permiten imágenes JPG, PNG o WEBP', 'error')
    return
  }
  
  // Validar tamaño (10MB)
  if (file.size > 10 * 1024 * 1024) {
    Swal.fire('Error', 'La imagen es muy grande. Máximo 10MB', 'error')
    return
  }
  
  // Mostrar preview local
  const reader = new FileReader()
  reader.onload = (e) => {
    fotoPreview.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
  
  // Subir al servidor
  await subirFoto(file)
  
  // Limpiar input
  target.value = ''
}

const subirFoto = async (file: File) => {
  subiendoFoto.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await axios.post(`${API_URL}/seguimientos/upload-foto`, formData, {
      headers: {
        Authorization: `Bearer ${auth.token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.data.success) {
      formulario.value.foto_url = response.data.foto_url
      console.log('✅ Foto subida:', response.data.foto_url)
    }
  } catch (error: any) {
    console.error('Error subiendo foto:', error)
    Swal.fire('Error', error.response?.data?.detail || 'No se pudo subir la foto', 'error')
    fotoPreview.value = null
  } finally {
    subiendoFoto.value = false
  }
}

const eliminarFoto = () => {
  fotoPreview.value = null
  formulario.value.foto_url = ''
}

// Funciones
const obtenerSembradores = async () => {
  try {
    const response = await axios.get(`${API_URL}/sembradores/`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    sembradores.value = response.data.items || response.data || []
  } catch (error) {
    console.error('Error cargando sembradores:', error)
  }
}

const obtenerSeguimientos = async () => {
  try {
    const response = await axios.get(`${API_URL}/seguimientos/`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    seguimientos.value = response.data.items || response.data || []
  } catch (error) {
    console.error('Error cargando seguimientos:', error)
  }
}

const crearSeguimiento = async () => {
  if (!formulario.value.sembrador_id) {
    alert('Por favor selecciona un sembrador')
    return
  }

  cargando.value = true
  try {
    await axios.post(`${API_URL}/seguimientos/crear`, formulario.value, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    
    alert('✅ Seguimiento creado exitosamente')
    
    // Limpiar formulario y foto
    formulario.value = {
      sembrador_id: null,
      fecha_visita: new Date().toISOString().split('T')[0],
      estado_cultivo: '',
      observaciones: '',
      avance_porcentaje: 1,
      foto_url: ''
    }
    fotoPreview.value = null
    
    await obtenerSeguimientos()
    activeTab.value = 'Mis Seguimientos'
  } catch (error) {
    console.error('Error:', error)
    alert('❌ Error al crear seguimiento')
  } finally {
    cargando.value = false
  }
}

const eliminarSeguimiento = async (id: number) => {
  if (!confirm('¿Estás seguro de que deseas eliminar este seguimiento?')) return

  try {
    await axios.delete(`${API_URL}/seguimientos/${id}`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    
    alert('✅ Seguimiento eliminado')
    await obtenerSeguimientos()
  } catch (error) {
    console.error('Error:', error)
    alert('❌ Error al eliminar')
  }
}

const cargarReportes = async () => {
  try {
    const respTecnico = await axios.get(`${API_URL}/seguimientos/reportes/por-tecnico`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    reporteTecnico.value = respTecnico.data.items || []

    const respCultivo = await axios.get(`${API_URL}/seguimientos/reportes/por-cultivo`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    reporteCultivo.value = respCultivo.data.items || []
  } catch (error) {
    console.error('Error cargando reportes:', error)
  }
}

const formatearFecha = (fecha: string): string => {
  if (!fecha) return 'N/A'
  const date = new Date(fecha)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const recargarSeguimientos = async () => {
  try {
    await obtenerSeguimientos()
    await Swal.fire('✅ Recargado', 'Los seguimientos se han actualizado', 'success')
  } catch (err) {
    await Swal.fire('❌ Error', 'No se pudo recargar los seguimientos', 'error')
  }
}

onMounted(() => {
  obtenerSembradores()
  obtenerSeguimientos()
  cargarReportes()
})
</script>

<style scoped>
/* Forzar esquema de color oscuro siempre */
:root {
  --color-primary: #10b981;
  --color-primary-dark: #059669;
  --color-bg: #0f172a;
  --color-bg-dark: #0a0f1e;
  --color-card: #1e293b;
  --color-input: #1a2332;
  --color-border: #334155;
  --color-text: #f1f5f9;
  --color-text-sec: #cbd5e1;
  --color-text-dim: #94a3b8;
  color-scheme: dark;
}

/* Forzar colores en toda la vista */
.seguimiento-container,
.seguimiento-container * {
  color-scheme: dark;
}

.seguimiento-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* Blobs */
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

/* Header */
.header-seguimiento {
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

/* Main */
.seguimiento-main {
  position: relative;
  z-index: 5;
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.seguimiento-content {
  display: grid;
  gap: 2rem;
}

/* Tabs */
.tabs-wrapper {
  position: relative;
  z-index: 9;
  background: rgba(30, 41, 59, 0.3);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.tabs-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 0;
  padding: 0 1rem;
}

.tab {
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: #cbd5e1;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.tab:hover {
  color: #e2e8f0;
  background: rgba(16, 185, 129, 0.05);
}

.tab.active {
  color: #10b981;
  border-bottom-color: #10b981;
}

/* Form Section */
.form-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.form-header {
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #84cc16;
  margin: 0 0 0.3rem 0;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.3);
}

.form-subtitle {
  color: #cbd5e1;
  margin: 0;
  font-size: 0.8rem;
}

.seguimiento-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0;
}

.label-icon {
  color: #10b981;
  flex-shrink: 0;
}

.form-hint {
  font-size: 0.72rem;
  color: #94a3b8;
  margin-top: 0;
  margin-bottom: 0.4rem;
  font-style: italic;
  line-height: 1.2;
}

.input-wrapper {
  position: relative;
}

/* Select wrapper con icono */
.select-wrapper {
  position: relative;
}

.select-icon {
  position: absolute;
  right: 2.5rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
  pointer-events: none;
  z-index: 1;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(148, 163, 184, 0.3);
  border-radius: 8px;
  color: #f1f5f9 !important;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  font-family: inherit;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.form-input:hover {
  border-color: rgba(148, 163, 184, 0.5);
}

.form-input:focus {
  outline: none;
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.9) !important;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

/* ========== SELECT STYLES ========== */
.form-select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2310b981' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  padding-right: 2.5rem;
  color: #f1f5f9 !important;
  background-color: rgba(15, 23, 42, 0.8) !important;
  cursor: pointer;
}

/* Clase para cuando está el placeholder seleccionado */
.form-select.placeholder-selected {
  color: #9ca3af !important;
}

/* Opciones del select */
.form-select option {
  background: #1e293b !important;
  color: #f1f5f9 !important;
  padding: 0.5rem;
}

.form-select option:disabled {
  color: #9ca3af !important;
}

.textarea-input {
  resize: vertical;
  min-height: 100px;
}

/* ========== AVANCE SLIDER MODERNO ========== */
.avance-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0;
}

.slider-wrapper {
  flex: 1;
  position: relative;
  height: 24px;
  display: flex;
  align-items: center;
}

.avance-slider {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 10;
}

.slider-track {
  position: absolute;
  width: 100%;
  height: 10px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider-fill {
  height: 100%;
  background: linear-gradient(90deg, #22c55e, #10b981, #059669);
  border-radius: 10px;
  transition: width 0.15s ease-out;
  position: relative;
  overflow: hidden;
}

.slider-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.3) 0%, transparent 100%);
}

.avance-input-wrapper {
  display: flex;
  align-items: center;
  background: rgba(15, 23, 42, 0.6);
  border: 2px solid rgba(16, 185, 129, 0.4);
  border-radius: 12px;
  padding: 0.5rem 0.75rem;
  gap: 0.25rem;
  transition: all 0.3s ease;
}

.avance-input-wrapper:focus-within {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2), 0 0 20px rgba(16, 185, 129, 0.2);
}

.avance-input {
  width: 50px;
  background: transparent;
  border: none;
  color: #10b981;
  font-size: 1.1rem;
  font-weight: 700;
  text-align: center;
  outline: none;
  font-family: inherit;
}

.avance-input::-webkit-inner-spin-button,
.avance-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.avance-input[type='number'] {
  -moz-appearance: textfield;
}

.avance-percent {
  color: #10b981;
  font-weight: 700;
  font-size: 1rem;
}

/* ========== BOTÓN GUARDAR VIDRIO LÍQUIDO ========== */
.btn-submit-wrapper {
  width: 100%;
  margin-top: 1.5rem;
}

.btn-submit-glass {
  width: 100%;
  position: relative;
  padding: 1rem 2rem;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  background: transparent;
}

.btn-glass-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, 
    rgba(16, 185, 129, 0.9) 0%, 
    rgba(5, 150, 105, 0.95) 50%,
    rgba(4, 120, 87, 0.9) 100%
  );
  border-radius: 16px;
  z-index: 1;
}

.btn-glass-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.2) 0%, 
    transparent 50%,
    rgba(0, 0, 0, 0.1) 100%
  );
  border-radius: 16px;
}

.btn-glass-bg::after {
  content: '';
  position: absolute;
  inset: 2px;
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-bottom-color: transparent;
  border-right-color: transparent;
}

.btn-glass-content {
  position: relative;
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-text, .btn-loading {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.check-icon {
  width: 24px;
  height: 24px;
  stroke: currentColor;
}

.spin-icon {
  width: 22px;
  height: 22px;
  stroke: currentColor;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.btn-glass-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 40%,
    rgba(255, 255, 255, 0.15) 50%,
    transparent 60%
  );
  z-index: 2;
  transition: transform 0.5s ease;
  transform: translateX(-100%) rotate(45deg);
}

.btn-submit-glass:hover:not(:disabled) .btn-glass-shine {
  transform: translateX(50%) rotate(45deg);
}

.btn-submit-glass:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 
    0 10px 40px rgba(16, 185, 129, 0.4),
    0 6px 20px rgba(16, 185, 129, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.btn-submit-glass:active:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 
    0 5px 20px rgba(16, 185, 129, 0.3),
    0 3px 10px rgba(16, 185, 129, 0.2);
}

.btn-submit-glass:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-submit-glass:disabled .btn-glass-bg {
  background: linear-gradient(135deg, 
    rgba(148, 163, 184, 0.5) 0%, 
    rgba(100, 116, 139, 0.5) 100%
  );
}

/* Historial */
.historial-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

.badge-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  border-radius: 50%;
  font-size: 0.85rem;
  font-weight: 700;
}

/* Table */
.table-wrapper {
  overflow-x: auto;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.seguimiento-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.seguimiento-table thead {
  background: rgba(16, 185, 129, 0.1);
  border-bottom: 2px solid rgba(16, 185, 129, 0.2);
}

.seguimiento-table th {
  padding: 1rem;
  text-align: left;
  color: var(--color-text-sec);
  font-weight: 600;
}

.seguimiento-table tbody tr {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  transition: background-color 0.2s ease;
}

.seguimiento-table tbody tr:hover {
  background-color: rgba(16, 185, 129, 0.05);
}

.table-row td {
  padding: 1rem;
  color: var(--color-text-dim);
}

.estado-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.estado-Germinando { background: rgba(34, 197, 94, 0.1); color: #86efac; }
.estado-Vegetativo { background: rgba(34, 197, 94, 0.15); color: #10b981; }
.estado-Floración { background: rgba(245, 158, 11, 0.1); color: #fbbf24; }
.estado-Fructificación { background: rgba(239, 68, 68, 0.1); color: #fca5a5; }
.estado-Cosecha { background: rgba(59, 130, 246, 0.1); color: #93c5fd; }
.estado-Plagas { background: rgba(239, 68, 68, 0.15); color: #fca5a5; }
.estado-Enfermedad { background: rgba(168, 85, 247, 0.1); color: #d8b4fe; }

.progress-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.progress-bar-small {
  flex: 1;
  height: 6px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 3px;
  overflow: hidden;
  min-width: 40px;
}

.progress-fill-small {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-dark));
  transition: width 0.3s ease;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: transparent;
}

.btn-delete {
  color: #f87171;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.1);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-dim);
}

/* Reportes */
.reportes-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.reportes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.reporte-card {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
}

.reporte-card h3 {
  color: var(--color-text);
  margin-top: 0;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-icon {
  color: #10b981;
}

.mini-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.mini-table tr {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
}

.mini-table tr:last-child {
  border-bottom: none;
}

.mini-table td {
  padding: 0.75rem 0;
  color: var(--color-text-dim);
}

.text-right {
  text-align: right;
  color: var(--color-primary);
  font-weight: 600;
}

@media (max-width: 768px) {
  .header-seguimiento {
    padding: 0.8rem 1rem;
  }

  /* Responsivo slider y botón */
  .avance-container {
    flex-direction: column;
    gap: 0.75rem;
    align-items: stretch;
  }

  .slider-wrapper {
    width: 100%;
  }

  .avance-input-wrapper {
    align-self: center;
    padding: 0.6rem 1rem;
  }

  .avance-input {
    width: 55px;
    font-size: 1.2rem;
  }

  .btn-submit-glass {
    padding: 1.1rem 1.5rem;
    border-radius: 14px;
  }

  .btn-glass-content {
    font-size: 1rem;
  }

  .check-icon, .spin-icon {
    width: 22px;
    height: 22px;
  }

  .form-hint {
    font-size: 0.7rem;
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

  .seguimiento-container {
    padding: 0;
  }

  .form-title {
    font-size: 1.1rem;
  }

  .seguimiento-main {
    padding: 1rem 0.5rem;
  }

  .form-section,
  .historial-section,
  .reportes-section {
    padding: 1.5rem 1rem;
    border-radius: 12px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .tabs-container {
    flex-wrap: wrap;
  }

  .table-wrapper {
    overflow-x: auto;
  }

  .seguimiento-table {
    font-size: 0.75rem;
  }

  .seguimiento-table th,
  .seguimiento-table td {
    padding: 0.6rem 0.5rem;
  }

  .reportes-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .header-seguimiento {
    padding: 0.75rem 0.9rem;
  }

  /* Responsivo para 640px */
  .btn-submit-glass {
    padding: 1rem 1.25rem;
    border-radius: 12px;
  }

  .btn-glass-content {
    font-size: 0.95rem;
    gap: 0.5rem;
  }

  .check-icon, .spin-icon {
    width: 20px;
    height: 20px;
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

  .seguimiento-table {
    font-size: 0.7rem;
  }

  .seguimiento-table th,
  .seguimiento-table td {
    padding: 0.5rem 0.4rem;
  }
}

@media (max-width: 480px) {
  .header-seguimiento {
    padding: 0.7rem 0.8rem;
  }

  /* Responsivo para 480px */
  .btn-submit-glass {
    padding: 0.9rem 1rem;
    border-radius: 12px;
  }

  .btn-glass-content {
    font-size: 0.9rem;
    gap: 0.5rem;
  }

  .check-icon, .spin-icon {
    width: 18px;
    height: 18px;
  }

  .avance-input-wrapper {
    padding: 0.5rem 0.75rem;
  }

  .avance-input {
    width: 45px;
    font-size: 1rem;
  }

  .avance-percent {
    font-size: 0.9rem;
  }

  .slider-track {
    height: 8px;
  }

  .form-hint {
    font-size: 0.65rem;
  }

  .form-label {
    font-size: 0.85rem;
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

  .form-title {
    font-size: 1rem;
  }

  .section-title {
    font-size: 1rem;
  }

  .tabs-container {
    overflow-x: auto;
  }

  .seguimiento-table {
    font-size: 0.65rem;
  }

  .seguimiento-table th,
  .seguimiento-table td {
    padding: 0.4rem 0.3rem;
  }
}

/* ========== FOTO UPLOAD STYLES ========== */
.foto-upload-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.foto-preview {
  position: relative;
  width: 100%;
  max-width: 300px;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid rgba(132, 204, 22, 0.3);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.preview-image {
  width: 100%;
  height: auto;
  max-height: 250px;
  object-fit: cover;
  display: block;
}

.btn-remove-foto {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.9);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.btn-remove-foto:hover {
  background: #ef4444;
  transform: scale(1.1);
}

.foto-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.hidden-input {
  display: none;
}

.btn-foto {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 10px;
  border: 2px dashed rgba(132, 204, 22, 0.4);
  background: rgba(132, 204, 22, 0.05);
  color: #84cc16;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 120px;
  justify-content: center;
}

.btn-foto:hover {
  background: rgba(132, 204, 22, 0.15);
  border-color: rgba(132, 204, 22, 0.6);
  transform: translateY(-2px);
}

.btn-gallery {
  border-color: rgba(59, 130, 246, 0.4);
  background: rgba(59, 130, 246, 0.05);
  color: #3b82f6;
}

.btn-gallery:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.6);
}

.btn-camera {
  border-color: rgba(16, 185, 129, 0.4);
  background: rgba(16, 185, 129, 0.05);
  color: #10b981;
}

.btn-camera:hover {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.6);
}

.foto-loading {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: rgba(132, 204, 22, 0.1);
  border-radius: 8px;
  color: #84cc16;
  font-size: 0.85rem;
}

.loading-spinner-small {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(132, 204, 22, 0.3);
  border-top-color: #84cc16;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Responsive para foto upload */
@media (max-width: 480px) {
  .foto-actions {
    flex-direction: column;
  }

  .btn-foto {
    width: 100%;
    padding: 0.65rem 1rem;
    font-size: 0.85rem;
  }

  .foto-preview {
    max-width: 100%;
  }

  .preview-image {
    max-height: 200px;
  }
}
</style>
