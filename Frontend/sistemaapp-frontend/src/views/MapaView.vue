<template>
  <div class="mapa-container">
    <!-- Fondo decorativo -->
    <div class="background-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header moderno -->
    <header class="mapa-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">
            <MapPin class="logo-svg" />
          </div>
          <div class="logo-text">
            <h1 class="app-title">Mapa Territorial</h1>
            <p class="app-subtitle">Localización de usuarios</p>
          </div>
        </div>
        <button @click="centerOnUser" class="location-button">
          <Navigation class="button-icon" />
          <span class="button-text">Mi ubicación</span>
        </button>
      </div>
    </header>

    <!-- Controles e información -->
    <div class="mapa-info-bar">
      <div class="info-items">
        <div class="info-item">
          <span class="info-label">📍 Ubicaciones:</span>
          <span class="info-value">{{ markers.length }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">🔍 Zoom:</span>
          <span class="info-value">{{ zoom }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">👥 Admins:</span>
          <span class="info-value admin">{{ adminCount }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">� Usuarios:</span>
          <span class="info-value regular">{{ userCount }}</span>
        </div>
      </div>
    </div>

    <!-- Contenedor del mapa -->
    <div class="map-wrapper">
      <l-map
        ref="mapInstance"
        v-model:zoom="zoom"
        :center="center"
        class="leaflet-map"
        @ready="onMapReady"
      >
        <l-tile-layer
          :url="tileUrl"
          :attribution="tileAttr"
          layer-type="base"
          name="OpenStreetMap"
        />
        <l-marker
          v-for="marker in markers"
          :key="marker.id"
          :lat-lng="marker.latlng"
          :icon="getMarkerIcon(marker.rol)"
        >
          <l-popup class="marker-popup">
            <div class="popup-content">
              <h3 class="popup-nombre">{{ marker.nombre }}</h3>
              <div class="popup-item">
                <span class="popup-label">Rol:</span>
                <span :class="['popup-value', `rol-${marker.rol}`]">
                  {{ marker.rol.toUpperCase() }}
                </span>
              </div>
              <div class="popup-item">
                <span class="popup-label">Email:</span>
                <span class="popup-email">{{ marker.email }}</span>
              </div>
              <div class="popup-item">
                <span class="popup-label">Coords:</span>
                <span class="popup-coords"
                  >{{ marker.latlng[0].toFixed(4) }}, {{ marker.latlng[1].toFixed(4) }}</span
                >
              </div>
            </div>
          </l-popup>
        </l-marker>
      </l-map>

      <!-- Loading state -->
      <div v-if="loading" class="map-loading">
        <div class="loading-spinner"></div>
        <p>Cargando ubicaciones...</p>
      </div>

      <!-- Error state -->
      <div v-if="error" class="map-error">
        <p>⚠️ {{ error }}</p>
      </div>
    </div>

    <!-- Leyenda flotante -->
    <div class="map-legend">
      <h3 class="legend-title">Leyenda</h3>
      <div class="legend-items">
        <div class="legend-item">
          <div class="legend-icon admin-marker"></div>
          <span>Administrador</span>
        </div>
        <div class="legend-item">
          <div class="legend-icon user-marker"></div>
          <span>Usuario Regular</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { MapPin, Navigation } from 'lucide-vue-next'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

// Estado del mapa
const mapInstance = ref(null)
const center = ref([20.0, -100.0]) // Centro aproximado de México
const zoom = ref(5)
const markers = ref([])
const loading = ref(true)
const error = ref(null)

// URLs y atribuciones
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const tileAttr =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

// Contadores
const adminCount = computed(() => markers.value.filter(m => m.rol === 'admin').length)
const userCount = computed(() => markers.value.filter(m => m.rol !== 'admin').length)
const adminIcon = L.icon({
  iconUrl:
    'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgdmlld0JveD0iMCAwIDI0IDI0Ij48cmVjdCBmaWxsPSIjZWY0NDQ0IiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHJ4PSI0Ii8+PHRleHQgeD0iMTIiIHk9IjE4IiBmb250LXNpemU9IjE2IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn4yP</tZT48L3N2Zz4=',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
})

const userIcon = L.icon({
  iconUrl:
    'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgdmlld0JveD0iMCAwIDI0IDI0Ij48cmVjdCBmaWxsPSIjMTBiOTgxIiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHJ4PSI0Ii8+PHRleHQgeD0iMTIiIHk9IjE4IiBmb250LXNpemU9IjE2IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn4y7PC90ZXh0Pjwvc3ZnPg==',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
})

const getMarkerIcon = (rol) => {
  return rol === 'admin' ? adminIcon : userIcon
}

const onMapReady = () => {
  // El mapa está listo
}

// Cargar usuarios como puntos en el mapa
const fetchMarkers = async () => {
  try {
    loading.value = true
    error.value = null

    const { data } = await axios.get(`${import.meta.env.VITE_API_URL}/auth/users`, {
      params: { page: 1, limit: 100 },
      headers: { Authorization: `Bearer ${auth.token}` },
    })

    // Generar posiciones aleatorias en México (dentro de límites reales)
    markers.value = data.users.map((u, idx) => {
      // Distribución aleatoria en México
      const latBase = 22
      const lngBase = -102
      return {
        id: u.id,
        nombre: u.nombre,
        email: u.email,
        rol: u.rol,
        latlng: [
          latBase + (Math.random() * 12 - 6), // Lat: 16-28
          lngBase + (Math.random() * 12 - 6), // Lng: -108 a -96
        ],
      }
    })

    loading.value = false
  } catch (err) {
    console.error('Error al cargar marcadores:', err)
    error.value = 'No se pudieron cargar las ubicaciones'
    loading.value = false
  }
}

// Centrar en ubicación del usuario actual
const centerOnUser = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        center.value = [pos.coords.latitude, pos.coords.longitude]
        zoom.value = 13
      },
      (err) => {
        console.warn('No se pudo obtener ubicación:', err)
        error.value = 'No se pudo acceder a tu ubicación'
        setTimeout(() => {
          error.value = null
        }, 3000)
      }
    )
  }
}

onMounted(() => {
  fetchMarkers()
})
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
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
  background: linear-gradient(135deg, #10b981, #06b6d4);
  border-radius: 50%;
  top: -200px;
  left: -200px;
  animation: blob-animate 8s ease-in-out infinite;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-radius: 50%;
  top: 50%;
  right: -150px;
  animation: blob-animate 10s ease-in-out infinite reverse;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #ec4899, #f59e0b);
  border-radius: 50%;
  bottom: -100px;
  left: 50%;
  animation: blob-animate 12s ease-in-out infinite;
}

@keyframes blob-animate {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -50px); }
}

/* ========== HEADER ========== */
.mapa-header {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding: 1rem 0;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.logo-svg {
  width: 28px;
  height: 28px;
  color: white;
}

.logo-text h1 {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981, #6ee7b7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-text p {
  font-size: 0.85rem;
  color: #94a3b8;
  font-weight: 500;
}

.location-button {
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

.location-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4);
}

.location-button:active {
  transform: translateY(0);
}

.button-icon {
  width: 18px;
  height: 18px;
}

.button-text {
  display: none;
}

@media (min-width: 640px) {
  .button-text {
    display: inline;
  }
}

/* ========== INFO BAR ========== */
.mapa-info-bar {
  background: rgba(30, 41, 59, 0.4);
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
  padding: 1rem 1.5rem;
  backdrop-filter: blur(10px);
}

.info-items {
  display: flex;
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-label {
  font-size: 0.9rem;
  color: #94a3b8;
  font-weight: 500;
}

.info-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #10b981;
}

.info-value.admin {
  color: #ef4444;
}

.info-value.regular {
  color: #3b82f6;
}

/* ========== MAP WRAPPER ========== */
.map-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
}

.leaflet-map {
  width: 100%;
  height: 100%;
  z-index: 2;
}

/* ========== LOADING STATE ========== */
.map-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  background: rgba(30, 41, 59, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 2rem;
  border-radius: 16px;
  z-index: 100;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(16, 185, 129, 0.2);
  border-top: 4px solid #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.map-loading p {
  font-size: 1rem;
  color: #cbd5e1;
  font-weight: 500;
}

/* ========== ERROR STATE ========== */
.map-error {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 1rem;
  border-radius: 8px;
  z-index: 100;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* ========== POPUP STYLES ========== */
.popup-content {
  padding: 0.5rem 0;
  color: #374151;
}

.popup-nombre {
  font-size: 1rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.popup-item {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
  font-size: 0.85rem;
}

.popup-label {
  font-weight: 600;
  color: #6b7280;
}

.popup-value {
  font-weight: 600;
}

.popup-value.rol-admin {
  color: #ef4444;
}

.popup-value.rol-usuario {
  color: #10b981;
}

.popup-email {
  color: #6b7280;
  font-style: italic;
}

.popup-coords {
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  color: #9ca3af;
}

/* ========== LEGEND ========== */
.map-legend {
  position: absolute;
  bottom: 1.5rem;
  left: 1.5rem;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1.25rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  z-index: 100;
  max-width: 250px;
}

.legend-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 0.75rem;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  color: #cbd5e1;
}

.legend-icon {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 2px solid rgba(148, 163, 184, 0.2);
}

.admin-marker {
  background: #ef4444;
  border-color: #dc2626;
}

.user-marker {
  background: #10b981;
  border-color: #059669;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .logo-section {
    width: 100%;
  }

  .logo-text h1 {
    font-size: 1.25rem;
  }

  .location-button {
    width: 100%;
    justify-content: center;
  }

  .info-items {
    gap: 1rem;
  }

  .map-legend {
    bottom: 1rem;
    left: 1rem;
    right: 1rem;
    max-width: none;
  }
}

@media (max-width: 640px) {
  .header-content {
    padding: 0 1rem;
  }

  .logo-icon {
    width: 40px;
    height: 40px;
  }

  .logo-svg {
    width: 24px;
    height: 24px;
  }

  .logo-text h1 {
    font-size: 1.1rem;
  }

  .logo-text p {
    font-size: 0.8rem;
  }

  .location-button {
    padding: 0.6rem 1rem;
    font-size: 0.8rem;
  }

  .mapa-info-bar {
    padding: 0.75rem 1rem;
  }

  .info-items {
    gap: 0.75rem;
    flex-direction: column;
  }

  .info-label {
    font-size: 0.85rem;
  }

  .info-value {
    font-size: 1rem;
  }

  .map-legend {
    padding: 1rem;
    bottom: 0.75rem;
    left: 0.75rem;
    right: 0.75rem;
  }

  .legend-title {
    font-size: 0.9rem;
  }

  .legend-item {
    font-size: 0.85rem;
  }
}

/* ========== LEAFLET OVERRIDES ========== */
:deep(.leaflet-popup-content-wrapper) {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

:deep(.leaflet-popup-tip) {
  border-top-color: white;
}

:deep(.leaflet-container) {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

:deep(.leaflet-control-attribution) {
  background: rgba(255, 255, 255, 0.8) !important;
  font-size: 0.75rem;
}
</style>
