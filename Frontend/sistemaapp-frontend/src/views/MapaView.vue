<template>
  <div class="mapa-container">
    <!-- Fondo decorativo con blobs animados -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header principal -->
    <header class="header-mapa">
      <div class="header-wrapper">
        <div class="header-left">
          <div class="icon-box">
            <MapPin class="icon-header" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Mapa Territorial</h1>
            <p class="header-subtitle">Localización de usuarios en tiempo real</p>
          </div>
        </div>
        <button @click="centerOnUser" class="btn-location">
          <MapPin class="btn-icon" />
          <span>Mi ubicación</span>
        </button>
      </div>
    </header>

    <!-- Filtros por rol -->
    <div class="filters-section">
      <div class="filters-wrapper">
        <h3 class="filters-title">Filtrar por rol:</h3>
        <div class="filters-grid">
          <label
            v-for="r in roles"
            :key="r.value"
            class="filter-checkbox"
            :class="{ 'filter-active': selectedRoles.includes(r.value) }"
          >
            <input
              type="checkbox"
              v-model="selectedRoles"
              :value="r.value"
              class="checkbox-input"
            />
            <span class="checkbox-label">{{ r.label }}</span>
            <span class="checkbox-count">({{ roleCount(r.value) }})</span>
          </label>
        </div>
      </div>
    </div>

    <!-- Estadísticas -->
    <div class="stats-section">
      <div class="stats-wrapper">
        <div class="stat-item">
          <span class="stat-emoji">📍</span>
          <span class="stat-label">Total:</span>
          <span class="stat-value">{{ markers.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-emoji">👁️</span>
          <span class="stat-label">Mostrados:</span>
          <span class="stat-value">{{ filteredMarkers.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-emoji">🔍</span>
          <span class="stat-label">Zoom:</span>
          <span class="stat-value">{{ zoom }}</span>
        </div>
      </div>
    </div>

    <!-- Mapa -->
    <div class="map-section">
      <l-map ref="map" v-model:zoom="zoom" :center="center" class="map-container-leaflet">
        <l-tile-layer :url="tileUrl" :attribution="tileAttr" layer-type="base" name="OpenStreetMap" />

        <l-marker
          v-for="marker in filteredMarkers"
          :key="marker.id"
          :lat-lng="marker.latlng"
          :icon="getMarkerIcon(marker.rol)"
        >
          <l-popup class="marker-popup-custom">
            <div class="popup-card">
              <div class="popup-nombre">{{ marker.nombre }}</div>
              <div class="popup-rol" :class="`rol-${marker.rol}`">{{ marker.rol }}</div>
              <div class="popup-email">{{ marker.email }}</div>
              <div class="popup-coords">{{ marker.latlng[0].toFixed(4) }}, {{ marker.latlng[1].toFixed(4) }}</div>
            </div>
          </l-popup>
        </l-marker>
      </l-map>

      <!-- Loading -->
      <div v-if="loading" class="loading-overlay">
        <div class="loading-content">
          <div class="spinner"></div>
          <p>Cargando ubicaciones...</p>
        </div>
      </div>

      <!-- Sin resultados -->
      <div v-if="!loading && filteredMarkers.length === 0" class="empty-state">
        <div class="empty-content">
          <MapPin class="empty-icon" />
          <p class="empty-title">No hay usuarios para mostrar</p>
          <p class="empty-text">Intenta cambiar los filtros</p>
        </div>
      </div>
    </div>

    <!-- Leyenda -->
    <div class="legend-box">
      <h3 class="legend-title">Leyenda de Roles</h3>
      <div class="legend-items">
        <div class="legend-item">
          <div class="legend-marker admin"></div>
          <span>Admin</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker territorial"></div>
          <span>Territorial</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker facilitador"></div>
          <span>Facilitador</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker tecnico"></div>
          <span>Técnico</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { MapPin } from 'lucide-vue-next'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

// Referencias del mapa
const map = ref(null)
const center = ref([19.4326, -99.1332]) // CDMX
const zoom = ref(6)

// URLs de mapas
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const tileAttr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

// Datos
const markers = ref([])
const loading = ref(true)

// Filtros por rol
const roles = [
  { label: 'Admin', value: 'admin' },
  { label: 'Territorial', value: 'territorial' },
  { label: 'Facilitador', value: 'facilitador' },
  { label: 'Técnico', value: 'tecnico' },
]
const selectedRoles = ref(['admin', 'territorial', 'facilitador', 'tecnico'])

// Computed
const filteredMarkers = computed(() =>
  markers.value.filter(m => selectedRoles.value.includes(m.rol))
)

const roleCount = (role) => markers.value.filter(m => m.rol === role).length

// Íconos personalizados por rol
const getRoleColor = (rol) => {
  const colors = {
    admin: '#ef4444',
    territorial: '#3b82f6',
    facilitador: '#10b981',
    tecnico: '#eab308',
  }
  return colors[rol] || '#6b7280'
}

const getMarkerIcon = (rol) => {
  const color = getRoleColor(rol)
  return L.icon({
    iconUrl: `data:image/svg+xml;base64,${btoa(`
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="40" viewBox="0 0 24 24">
        <circle cx="12" cy="8" r="4" fill="${color}"/>
        <path d="M12 14c-4 0-6 2-6 5v3c0 .55.45 1 1 1h10c.55 0 1-.45 1-1v-3c0-3-2-5-6-5z" fill="${color}"/>
      </svg>
    `)}`,
    iconSize: [32, 40],
    iconAnchor: [16, 40],
    popupAnchor: [0, -40],
  })
}

// Cargar marcadores
const fetchMarkers = async () => {
  try {
    loading.value = true
    const { data } = await axios.get(`${import.meta.env.VITE_API_URL}/auth/users?limit=100`, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })

    markers.value = data.users.map(u => ({
      id: u.id,
      nombre: u.nombre,
      email: u.email,
      rol: u.rol || 'usuario',
      latlng: [
        u.lat || 19.4326 + (Math.random() * 4 - 2),
        u.lng || -99.1332 + (Math.random() * 4 - 2),
      ],
    }))
    loading.value = false
  } catch (err) {
    console.error('Error al cargar marcadores:', err)
    loading.value = false
  }
}

// Centrar en ubicación actual
const centerOnUser = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        center.value = [pos.coords.latitude, pos.coords.longitude]
        zoom.value = 13
      },
      err => console.warn('Geolocalización no disponible:', err)
    )
  }
}

// Ciclo de vida
onMounted(fetchMarkers)
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ========== CONTAINER ========== */
.mapa-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* ========== BACKGROUND BLOBS ========== */
.background-blobs {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
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

/* ========== HEADER ========== */
.header-mapa {
  position: relative;
  z-index: 30;
  backdrop-filter: blur(12px);
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 1px solid rgba(148, 163, 184, 0.15);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
  padding: 1.25rem 1.5rem;
}

.header-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.icon-box {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
  flex-shrink: 0;
}

.icon-header {
  width: 28px;
  height: 28px;
  color: white;
  stroke-width: 2;
}

.header-text h1 {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.25rem;
}

.header-text p {
  font-size: 0.85rem;
  color: #94a3b8;
  font-weight: 500;
}

.btn-location {
  display: flex;
  align-items: center;
  gap: 0.75rem;
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
  white-space: nowrap;
}

.btn-location:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4);
}

.btn-location:active {
  transform: translateY(0);
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* ========== FILTERS SECTION ========== */
.filters-section {
  position: relative;
  z-index: 20;
  backdrop-filter: blur(10px);
  background: rgba(30, 41, 59, 0.4);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding: 1.25rem 1.5rem;
}

.filters-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

.filters-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filters-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.875rem;
  background: rgba(71, 85, 105, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.filter-checkbox:hover {
  background: rgba(71, 85, 105, 0.7);
  border-color: rgba(148, 163, 184, 0.4);
}

.filter-checkbox.filter-active {
  background: rgba(16, 185, 129, 0.2);
  border-color: rgba(16, 185, 129, 0.5);
}

.checkbox-input {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #10b981;
}

.checkbox-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #cbd5e1;
}

.checkbox-count {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 400;
}

/* ========== STATS SECTION ========== */
.stats-section {
  position: relative;
  z-index: 20;
  backdrop-filter: blur(10px);
  background: rgba(30, 41, 59, 0.3);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding: 0.875rem 1.5rem;
}

.stats-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.stat-emoji {
  font-size: 1.2rem;
}

.stat-label {
  color: #94a3b8;
  font-weight: 500;
}

.stat-value {
  color: #10b981;
  font-weight: 700;
  font-size: 1.1rem;
}

/* ========== MAP SECTION ========== */
.map-section {
  flex: 1;
  position: relative;
  z-index: 10;
  overflow: hidden;
}

.map-container-leaflet {
  width: 100%;
  height: 100%;
}

/* ========== LOADING STATE ========== */
.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 100;
}

.loading-content {
  text-align: center;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(16, 185, 129, 0.2);
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-overlay p {
  color: #cbd5e1;
  font-weight: 500;
  font-size: 1rem;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  z-index: 100;
}

.empty-content {
  text-align: center;
  background: rgba(30, 41, 59, 0.9);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.empty-icon {
  width: 56px;
  height: 56px;
  color: #64748b;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-title {
  color: #cbd5e1;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.empty-text {
  color: #94a3b8;
  font-size: 0.9rem;
}

/* ========== LEGEND ========== */
.legend-box {
  position: absolute;
  bottom: 1.5rem;
  left: 1.5rem;
  z-index: 40;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1rem;
  backdrop-filter: blur(12px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  max-width: 280px;
}

.legend-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #cbd5e1;
}

.legend-marker {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  flex-shrink: 0;
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

.legend-marker.admin {
  background: #ef4444;
  border-color: #dc2626;
}

.legend-marker.territorial {
  background: #3b82f6;
  border-color: #1d4ed8;
}

.legend-marker.facilitador {
  background: #10b981;
  border-color: #059669;
}

.legend-marker.tecnico {
  background: #eab308;
  border-color: #ca8a04;
}

/* ========== POPUP STYLES ========== */
:deep(.leaflet-popup-content-wrapper) {
  border-radius: 10px;
  background: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

:deep(.leaflet-popup-tip) {
  border-top-color: white;
}

.popup-card {
  padding: 0.5rem 0;
  min-width: 200px;
}

.popup-nombre {
  font-size: 1rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.popup-rol {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.625rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.popup-rol.rol-admin {
  background: #fee2e2;
  color: #991b1b;
}

.popup-rol.rol-territorial {
  background: #dbeafe;
  color: #1e3a8a;
}

.popup-rol.rol-facilitador {
  background: #dcfce7;
  color: #166534;
}

.popup-rol.rol-tecnico {
  background: #fef3c7;
  color: #854d0e;
}

.popup-email {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
  font-style: italic;
}

.popup-coords {
  font-size: 0.75rem;
  color: #9ca3af;
  font-family: 'Courier New', monospace;
  margin-top: 0.25rem;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .header-wrapper {
    gap: 1rem;
  }

  .header-text h1 {
    font-size: 1.5rem;
  }

  .legend-box {
    bottom: 1rem;
    left: 1rem;
    max-width: 260px;
  }
}

@media (max-width: 768px) {
  .header-mapa {
    padding: 1rem;
  }

  .header-wrapper {
    flex-direction: column;
  }

  .btn-location {
    width: 100%;
    justify-content: center;
  }

  .filters-section {
    padding: 0.875rem 1rem;
  }

  .filters-grid {
    gap: 0.5rem;
  }

  .filter-checkbox {
    padding: 0.4rem 0.75rem;
    font-size: 0.85rem;
  }

  .stats-wrapper {
    gap: 1rem;
  }

  .legend-box {
    bottom: 0.75rem;
    left: 0.75rem;
    right: 0.75rem;
    max-width: none;
  }
}

@media (max-width: 640px) {
  .header-left {
    gap: 0.75rem;
  }

  .icon-box {
    width: 44px;
    height: 44px;
  }

  .icon-header {
    width: 24px;
    height: 24px;
  }

  .header-text h1 {
    font-size: 1.25rem;
  }

  .header-text p {
    font-size: 0.8rem;
  }

  .btn-location {
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
  }

  .filters-grid {
    gap: 0.4rem;
  }

  .filter-checkbox {
    padding: 0.35rem 0.625rem;
    font-size: 0.8rem;
  }

  .checkbox-label {
    font-size: 0.85rem;
  }

  .stat-item {
    font-size: 0.8rem;
  }

  .legend-box {
    padding: 0.75rem;
  }

  .legend-title {
    font-size: 0.8rem;
  }

  .legend-item {
    font-size: 0.8rem;
    gap: 0.5rem;
  }

  .legend-marker {
    width: 16px;
    height: 16px;
  }
}

/* ========== LEAFLET OVERRIDES ========== */
:deep(.leaflet-container) {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

:deep(.leaflet-control-attribution) {
  background: rgba(15, 23, 42, 0.9) !important;
  color: #94a3b8 !important;
  font-size: 0.7rem;
  backdrop-filter: blur(10px);
  border: none;
  border-top: 1px solid rgba(148, 163, 184, 0.1);
}

:deep(.leaflet-control-attribution a) {
  color: #10b981 !important;
  text-decoration: none;
}

:deep(.leaflet-control-attribution a:hover) {
  text-decoration: underline;
}
</style>
