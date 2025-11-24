<template>
  <div class="sembradores-container">
    <!-- Fondo decorativo con blobs animados -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header principal con botón de regreso -->
    <header class="header-sembradores">
      <div class="header-wrapper">
        <div class="header-left">
          <router-link to="/dashboard" class="back-button" title="Volver al Dashboard">
            <ArrowLeft class="back-icon" />
          </router-link>
          <div class="header-icon-small">
            <Sprout class="icon-stat" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Sembradores</h1>
            <p class="header-subtitle">Registro y gestión</p>
          </div>
        </div>
        <button @click="recargarSembradores" class="reload-button" title="Recargar">
          <svg class="reload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8M21 3v5h-5M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16M3 21v-5h5"></path>
          </svg>
        </button>
      </div>
    </header>

    <!-- Contenido principal -->
    <main class="sembradores-main">
      <div class="sembradores-content">
        <!-- Formulario de registro -->
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
          class="form-section"
        >
          <div class="form-header">
            <h2 class="form-title">Registrar Nuevo Sembrador</h2>
            <p class="form-subtitle">Completa los datos del sembrador</p>
          </div>

          <form @submit.prevent="crearSembrador" class="sembrador-form">
            <!-- Fila 1: Nombre y Comunidad -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Nombre Completo *</label>
                <div class="input-wrapper">
                  <User class="input-icon" />
                  <input
                    v-model="form.nombre"
                    type="text"
                    placeholder="Juan Pérez García"
                    class="form-input"
                    required
                    minlength="2"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Comunidad *</label>
                <div class="input-wrapper">
                  <MapPin class="input-icon" />
                  <input
                    v-model="form.comunidad"
                    type="text"
                    placeholder="La Esperanza"
                    class="form-input"
                    required
                  />
                </div>
              </div>
            </div>

            <!-- Fila 2: Cultivo y Teléfono -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Cultivo Principal *</label>
                <div class="input-wrapper">
                  <Leaf class="input-icon" />
                  <input
                    v-model="form.cultivo_principal"
                    type="text"
                    placeholder="Maíz, Papa, etc."
                    class="form-input"
                    required
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Teléfono *</label>
                <div class="input-wrapper">
                  <Phone class="input-icon" />
                  <input
                    v-model="form.telefono"
                    type="tel"
                    placeholder="+56912345678"
                    class="form-input"
                    required
                  />
                </div>
              </div>
            </div>

            <!-- Fila 3: Latitud y Longitud -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Latitud</label>
                <div class="input-wrapper">
                  <Navigation class="input-icon" />
                  <input
                    v-model="form.lat"
                    type="number"
                    placeholder="-33.8688"
                    step="0.0001"
                    class="form-input"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Longitud</label>
                <div class="input-wrapper">
                  <Navigation class="input-icon" />
                  <input
                    v-model="form.lng"
                    type="number"
                    placeholder="-51.2093"
                    step="0.0001"
                    class="form-input"
                  />
                </div>
              </div>
            </div>

            <!-- Botón de envío -->
            <button type="submit" class="submit-btn" :disabled="loading">
              <Sprout class="btn-icon" v-if="!loading" />
              <span class="btn-text">{{ loading ? 'Guardando...' : 'Guardar Sembrador' }}</span>
            </button>
          </form>
        </section>

        <!-- Sección de lista de sembradores -->
        <section
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200, duration: 600 } }"
          class="list-section"
        >
          <div class="list-header">
            <h2 class="list-title">
              <span class="count-badge">{{ sembradores.length }}</span>
              Sembradores Registrados
            </h2>
            <p class="list-subtitle">Gestión de sembradores en tu jurisdicción</p>
          </div>

          <!-- Estado vacío -->
          <div v-if="sembradores.length === 0" class="empty-state">
            <div class="empty-icon">
              <Sprout />
            </div>
            <h3 class="empty-title">Sin sembradores aún</h3>
            <p class="empty-text">Registra el primer sembrador para comenzar</p>
          </div>

          <!-- Tabla de sembradores -->
          <div v-else class="table-wrapper">
            <div class="table-container">
              <table class="sembradores-table">
                <thead>
                  <tr class="table-header-row">
                    <th class="table-header-cell">Nombre</th>
                    <th class="table-header-cell">Comunidad</th>
                    <th class="table-header-cell">Cultivo</th>
                    <th class="table-header-cell">Teléfono</th>
                    <th class="table-header-cell">Ubicación</th>
                    <th class="table-header-cell">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(sembrador, index) in sembradores"
                    :key="sembrador.id"
                    class="table-body-row"
                    :style="{
                      animation: `slideIn 0.3s ease ${index * 0.05}s`
                    }"
                  >
                    <td class="table-cell">
                      <div class="cell-content">
                        <div class="cell-icon">
                          <User class="icon-small" />
                        </div>
                        <span class="cell-text">{{ sembrador.nombre }}</span>
                      </div>
                    </td>
                    <td class="table-cell">
                      <div class="cell-location">
                        <MapPin class="icon-tiny" />
                        {{ sembrador.comunidad }}
                      </div>
                    </td>
                    <td class="table-cell">
                      <span class="cell-badge">{{ sembrador.cultivo_principal }}</span>
                    </td>
                    <td class="table-cell">
                      <a :href="`tel:${sembrador.telefono}`" class="cell-phone">
                        {{ sembrador.telefono }}
                      </a>
                    </td>
                    <td class="table-cell">
                      <div class="cell-location-small">
                        {{ sembrador.lat ? `${sembrador.lat.toFixed(4)}°` : 'N/A' }}
                        {{ sembrador.lng ? `${sembrador.lng.toFixed(4)}°` : '' }}
                      </div>
                    </td>
                    <td class="table-cell">
                      <div class="cell-actions">
                        <button
                          @click="editarSembrador(sembrador)"
                          class="action-btn edit-btn"
                          title="Editar"
                        >
                          <Edit2 class="action-icon" />
                        </button>
                        <button
                          @click="eliminarSembrador(sembrador.id)"
                          class="action-btn delete-btn"
                          title="Eliminar"
                        >
                          <Trash2 class="action-icon" />
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import {
  Sprout,
  User,
  MapPin,
  Leaf,
  Phone,
  Navigation,
  Edit2,
  Trash2,
  ArrowLeft
} from 'lucide-vue-next'
import Swal from 'sweetalert2'

const auth = useAuthStore()
const sembradores = ref([])
const loading = ref(false)

const form = ref({
  nombre: '',
  comunidad: '',
  cultivo_principal: '',
  telefono: '',
  lat: null,
  lng: null
})

// Obtener sembradores
const getSembradores = async () => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const res = await axios.get(`${apiUrl}/sembradores/`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    sembradores.value = res.data.items || res.data
  } catch (err: any) {
    console.error('Error al cargar sembradores:', err)
    Swal.fire('⚠️ Advertencia', 'No se pudieron cargar los sembradores', 'warning')
  }
}

// Crear sembrador
const crearSembrador = async () => {
  try {
    // Validar campos obligatorios
    if (!form.value.nombre || !form.value.comunidad || !form.value.cultivo_principal || !form.value.telefono) {
      Swal.fire('❌ Error', 'Por favor completa todos los campos obligatorios', 'error')
      return
    }

    loading.value = true
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

    await axios.post(`${apiUrl}/sembradores/`, form.value, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })

    Swal.fire('✅ Éxito', 'Sembrador registrado correctamente', 'success')
    
    // Limpiar formulario
    form.value = {
      nombre: '',
      comunidad: '',
      cultivo_principal: '',
      telefono: '',
      lat: null,
      lng: null
    }

    // Recargar lista
    await getSembradores()
  } catch (err: any) {
    const errorMsg = err.response?.data?.detail || 'No se pudo registrar el sembrador'
    Swal.fire('❌ Error', errorMsg, 'error')
  } finally {
    loading.value = false
  }
}

// Editar sembrador (placeholder para futura implementación)
const editarSembrador = (sembrador: any) => {
  form.value = { ...sembrador }
  Swal.fire('ℹ️ Información', 'La edición estará disponible pronto', 'info')
}

// Eliminar sembrador
const eliminarSembrador = async (id: number) => {
  const result = await Swal.fire({
    title: '⚠️ Confirmar eliminación',
    text: '¿Estás seguro de que deseas eliminar este sembrador?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#6b7280',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  })

  if (result.isConfirmed) {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      await axios.delete(`${apiUrl}/sembradores/${id}`, {
        headers: { Authorization: `Bearer ${auth.token}` }
      })

      Swal.fire('✅ Eliminado', 'Sembrador eliminado correctamente', 'success')
      await getSembradores()
    } catch (err: any) {
      Swal.fire('❌ Error', 'No se pudo eliminar el sembrador', 'error')
    }
  }
}

const recargarSembradores = async () => {
  try {
    await getSembradores()
    await Swal.fire('✅ Recargado', 'Los sembradores se han actualizado', 'success')
  } catch (err) {
    await Swal.fire('❌ Error', 'No se pudo recargar los sembradores', 'error')
  }
}

onMounted(getSembradores)
// Cargar sembradores al montar
onMounted(getSembradores)
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ========== CONTAINER ========== */
.sembradores-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
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
  50% { transform: translate(30px, -50px); }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== HEADER ========== */
.header-sembradores {
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
.sembradores-main {
  position: relative;
  z-index: 5;
  min-height: calc(100vh - 100px);
  padding: 2rem;
}

.sembradores-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* ========== FORM SECTION ========== */
.form-section {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.form-header {
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #84cc16;
  margin-bottom: 0.3rem;
  text-shadow: 0 0 8px rgba(132, 204, 22, 0.3);
}

.form-subtitle {
  font-size: 0.8rem;
  color: #94a3b8;
}

.sembrador-form {
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
  gap: 0.5rem;
}

.form-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  width: 20px;
  height: 20px;
  color: #10b981;
  pointer-events: none;
}

.form-input {
  width: 100%;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 10px;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.form-input::placeholder {
  color: #64748b;
}

.form-input:focus {
  outline: none;
  border-color: #10b981;
  background: rgba(15, 23, 42, 0.7);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

/* ========== SUBMIT BUTTON ========== */
.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.875rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  margin-top: 1rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.btn-text {
  font-weight: 600;
}

/* ========== LIST SECTION ========== */
.list-section {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.list-header {
  margin-bottom: 2rem;
}

.list-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #e2e8f0;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.875rem;
}

.list-subtitle {
  font-size: 0.95rem;
  color: #94a3b8;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  color: #10b981;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.empty-text {
  font-size: 0.95rem;
  color: #94a3b8;
}

/* ========== TABLE ========== */
.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.table-container {
  min-width: 100%;
}

.sembradores-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header-row {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
  border-bottom: 2px solid rgba(16, 185, 129, 0.2);
}

.table-header-cell {
  padding: 1rem;
  text-align: left;
  font-size: 0.875rem;
  font-weight: 600;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.table-body-row {
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  transition: all 0.3s ease;
}

.table-body-row:hover {
  background: rgba(16, 185, 129, 0.05);
}

.table-cell {
  padding: 1rem;
  color: #e2e8f0;
  font-size: 0.9rem;
}

.cell-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.cell-icon {
  width: 32px;
  height: 32px;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-small {
  width: 16px;
  height: 16px;
  color: #10b981;
}

.cell-text {
  font-weight: 500;
}

.cell-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #cbd5e1;
}

.icon-tiny {
  width: 14px;
  height: 14px;
  color: #10b981;
  flex-shrink: 0;
}

.cell-badge {
  display: inline-block;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
  color: #a7f3d0;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.875rem;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.cell-phone {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.cell-phone:hover {
  color: #60a5fa;
}

.cell-location-small {
  font-size: 0.85rem;
  color: #94a3b8;
  font-family: 'Courier New', monospace;
}

.cell-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(15, 23, 42, 0.5);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
}

.action-icon {
  width: 18px;
  height: 18px;
}

.edit-btn .action-icon {
  color: #3b82f6;
}

.delete-btn .action-icon {
  color: #ef4444;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .header-sembradores {
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

  .sembradores-main {
    padding: 1rem;
  }

  .form-title {
    font-size: 1.1rem;
  }

  .form-label {
    font-size: 0.7rem;
  }

  .list-title {
    font-size: 1rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.6rem 0.5rem;
    font-size: 0.75rem;
  }

  .table-header-cell {
    font-size: 0.7rem;
  }

  .form-input {
    font-size: 16px;
  }
}

@media (max-width: 640px) {
  .header-sembradores {
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

  .form-label {
    font-size: 0.65rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.5rem 0.4rem;
    font-size: 0.7rem;
  }
}

@media (max-width: 480px) {
  .header-sembradores {
    padding: 0.7rem 0.8rem;
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

  .header-title {
    font-size: 0.75rem;
  }

  .header-subtitle {
    font-size: 0.65rem;
  }

  .form-section,
  .list-section {
    padding: 1rem;
    border-radius: 12px;
  }

  .form-title,
  .list-title {
    font-size: 1rem;
  }

  .form-label {
    font-size: 0.6rem;
  }

  .table-header-cell,
  .table-cell {
    padding: 0.4rem 0.3rem;
    font-size: 0.65rem;
  }

  .submit-btn {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}
</style>
