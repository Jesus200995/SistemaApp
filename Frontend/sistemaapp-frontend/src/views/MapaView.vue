<template>
  <div class="mapa-container">
    <!-- Fondo decorativo (solo en header) -->
    <div class="background-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <!-- Header -->
    <header
      v-motion
      :initial="{ opacity: 0, y: -50 }"
      :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
      class="mapa-header"
    >
      <div class="header-content">
        <div class="header-title">
          <MapPin class="header-icon" />
          <h1>Mapa Territorial</h1>
        </div>
        <button @click="centerOnUser" class="location-button">
          <Navigation class="button-icon" />
          <span>Mi ubicación</span>
        </button>
      </div>
    </header>

    <!-- Controles secundarios -->
    <div class="map-controls">
      <div class="controls-info">
        <span class="info-badge">📍 {{ markers.length }} ubicaciones</span>
        <span class="info-badge zoom-level">🔍 Zoom: {{ zoom }}</span>
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
                <span class="popup-label">Ubicación:</span>
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
        <p>⚠️ Error: {{ error }}</p>
      </div>
    </div>

    <!-- Leyenda -->
    <div class="map-legend">
      <h3 class="legend-title">Leyenda</h3>
      <div class="legend-items">
        <div class="legend-item">
          <div class="legend-icon admin-marker"></div>
          <span>Administradores</span>
        </div>
        <div class="legend-item">
          <div class="legend-icon user-marker"></div>
          <span>Usuarios</span>
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

// Íconos personalizados para marcadores
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
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f3f4f6;
  position: relative;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ========== BACKGROUND DECORATION ========== */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100px;
  overflow: hidden;
  z-index: 1;
}

.blob {
  position: absolute;
  opacity: 0.08;
  filter: blur(80px);
  mix-blend-mode: screen;
}

.blob-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #10b981, #06b6d4);
  border-radius: 50%;
  top: -100px;
  left: -100px;
}

.blob-2 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  border-radius: 50%;
  top: -80px;
  right: -80px;
}

/* ========== HEADER ========== */
.mapa-header {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-bottom: 1px solid #e2e8f0;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: relative;
  z-index: 10;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
  gap: 1rem;
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

.mapa-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
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
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.location-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.location-button:active {
  transform: translateY(0);
}

.button-icon {
  width: 18px;
  height: 18px;
}

/* ========== MAP CONTROLS ========== */
.map-controls {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 0.75rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.controls-info {
  display: flex;
  gap: 1rem;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.info-badge {
  display: inline-block;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
  color: #059669;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.zoom-level {
  margin-left: auto;
}

/* ========== MAP WRAPPER ========== */
.map-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
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
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
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
  color: #6b7280;
  font-weight: 500;
}

/* ========== ERROR STATE ========== */
.map-error {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #fecaca;
  border: 1px solid #f87171;
  color: #991b1b;
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
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  z-index: 100;
  max-width: 250px;
}

.legend-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1f2937;
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
  color: #4b5563;
}

.legend-icon {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 2px solid #e5e7eb;
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

  .header-title {
    width: 100%;
  }

  .mapa-header h1 {
    font-size: 1.5rem;
  }

  .location-button {
    width: 100%;
    justify-content: center;
  }

  .map-legend {
    bottom: 1rem;
    left: 1rem;
    right: 1rem;
    max-width: none;
  }

  .controls-info {
    flex-direction: column;
    gap: 0.5rem;
  }

  .zoom-level {
    margin-left: 0;
  }
}

@media (max-width: 640px) {
  .map-controls {
    padding: 0.5rem 1rem;
  }

  .info-badge {
    font-size: 0.8rem;
    padding: 0.35rem 0.6rem;
  }

  .map-legend {
    padding: 1rem;
    bottom: 0.75rem;
    left: 0.75rem;
    right: 0.75rem;
  }

  .mapa-header {
    padding: 1rem;
  }

  .mapa-header h1 {
    font-size: 1.25rem;
  }

  .location-button {
    padding: 0.6rem 1rem;
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
