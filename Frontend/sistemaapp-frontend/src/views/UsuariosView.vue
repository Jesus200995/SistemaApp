<template>
  <div class="usuarios-container">
    <!-- Fondo decorativo -->
    <div class="background-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <!-- Contenido principal -->
    <div class="usuarios-content">
      <!-- Header -->
      <div
        v-motion
        :initial="{ opacity: 0, y: -50 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
        class="usuarios-header"
      >
        <div class="header-title">
          <Users class="header-icon" />
          <h1>Gestión de Usuarios</h1>
        </div>
        <button @click="fetchUsuarios" class="reload-button">
          <RotateCw class="reload-icon" />
          <span>Recargar</span>
        </button>
      </div>

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

        <!-- Tabla responsiva -->
        <div class="table-wrapper">
          <table class="users-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Email</th>
                <th>Rol</th>
              </tr>
            </thead>
            <tbody>
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
                    <div class="nombre-avatar">{{ u.nombre.charAt(0).toUpperCase() }}</div>
                    <span>{{ u.nombre }}</span>
                  </div>
                </td>
                <td class="cell-email">{{ u.email }}</td>
                <td class="cell-rol">
                  <span :class="['rol-badge', `rol-${u.rol}`]">
                    {{ u.rol.toUpperCase() }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Estado vacío -->
          <div v-if="filteredUsuarios.length === 0" class="empty-state">
            <Search class="empty-icon" />
            <h3>No se encontraron usuarios</h3>
            <p>Intenta con otros términos de búsqueda</p>
          </div>
        </div>

        <!-- Estadísticas -->
        <div class="stats-section">
          <div class="stat-card">
            <div class="stat-number">{{ adminCount }}</div>
            <div class="stat-label">Administradores</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ usuarioCount }}</div>
            <div class="stat-label">Usuarios</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ usuarios.length }}</div>
            <div class="stat-label">Total</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { Users, RotateCw, Search } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const usuarios = ref([])
const search = ref('')

const filteredUsuarios = computed(() =>
  usuarios.value.filter(u =>
    u.nombre.toLowerCase().includes(search.value.toLowerCase()) ||
    u.email.toLowerCase().includes(search.value.toLowerCase())
  )
)

const adminCount = computed(() => usuarios.value.filter(u => u.rol === 'admin').length)
const usuarioCount = computed(() => usuarios.value.filter(u => u.rol === 'usuario').length)

const fetchUsuarios = async () => {
  try {
    const { data } = await axios.get(`${import.meta.env.VITE_API_URL}/auth/users`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    usuarios.value = data
  } catch (err) {
    console.error('Error al cargar usuarios:', err)
  }
}

onMounted(() => {
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
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 2rem 0;
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
  z-index: 10;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* ========== HEADER ========== */
.usuarios-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 32px;
  height: 32px;
  color: #10b981;
}

.usuarios-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #e2e8f0;
}

.reload-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.75rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.reload-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4);
}

.reload-button:active {
  transform: translateY(0);
}

.reload-icon {
  width: 18px;
  height: 18px;
  animation: rotate 0.6s ease;
}

.reload-button:active .reload-icon {
  animation: rotate 0.6s ease;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ========== USUARIOS CARD ========== */
.usuarios-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 20px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  color: #e2e8f0;
  font-size: 0.95rem;
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

/* ========== TABLE ========== */
.table-wrapper {
  overflow-x: auto;
  margin-bottom: 2rem;
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.users-table thead {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
  border-bottom: 2px solid rgba(16, 185, 129, 0.3);
}

.users-table thead th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #10b981;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.8rem;
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
  padding: 1rem;
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
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
}

.cell-email {
  color: #94a3b8;
  font-size: 0.9rem;
}

.cell-rol {
  text-align: center;
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
}

.rol-usuario {
  background: rgba(16, 185, 129, 0.2);
  color: #86efac;
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

/* ========== STATS SECTION ========== */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

.stat-card {
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
  padding: 1.25rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.4);
  transform: translateY(-2px);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #10b981;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .usuarios-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .header-title {
    width: 100%;
    justify-content: center;
  }

  .usuarios-header h1 {
    font-size: 1.5rem;
  }

  .reload-button {
    width: 100%;
    justify-content: center;
  }

  .usuarios-card {
    padding: 1.5rem;
  }

  .search-section {
    flex-direction: column;
  }

  .results-info {
    order: -1;
    text-align: center;
    width: 100%;
  }

  .users-table {
    font-size: 0.85rem;
  }

  .users-table thead th,
  .users-table td {
    padding: 0.75rem;
  }

  .nombre-content {
    flex-direction: column;
    text-align: center;
  }

  .cell-nombre {
    text-align: center;
  }

  .stats-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .usuarios-container {
    padding: 1rem 0;
  }

  .usuarios-content {
    padding: 0 1rem;
  }

  .usuarios-header {
    padding: 1rem;
    gap: 0.75rem;
  }

  .header-icon {
    width: 24px;
    height: 24px;
  }

  .usuarios-header h1 {
    font-size: 1.25rem;
  }

  .usuarios-card {
    padding: 1rem;
  }

  .users-table {
    font-size: 0.8rem;
  }

  .users-table thead th {
    padding: 0.5rem;
  }

  .users-table td {
    padding: 0.5rem;
  }

  .nombre-avatar {
    width: 30px;
    height: 30px;
    font-size: 0.8rem;
  }

  .search-input {
    font-size: 16px; /* Previene zoom en iOS */
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
