<template>
  <div class="mapa-container">
    <!-- Menú hamburguesa global -->
    <HamburgerMenu />

    <!-- Fondo decorativo con blobs animados -->
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Header principal con botón de regreso -->
    <header class="header-mapa">
      <div class="header-wrapper">
        <div class="header-left">
          <router-link to="/dashboard" class="back-button" title="Volver al Dashboard">
            <ArrowLeft class="back-icon" />
          </router-link>
          <div class="icon-box">
            <Layers class="icon-header" />
          </div>
          <div class="header-text">
            <h1 class="header-title">Capas Temáticas</h1>
            <p class="header-subtitle">Ambiental, Social, Productiva e Infraestructura</p>
          </div>
        </div>
        <button @click="centerOnUser" class="btn-location">
          <MapPin class="btn-icon" />
          <span>Mi ubicación</span>
        </button>
      </div>
    </header>

    <!-- Panel lateral de capas -->
    <div class="layers-panel">
      <div class="panel-wrapper">
        <h3 class="panel-title">Capas disponibles:</h3>
        <div class="layers-list">
          <label v-for="c in capas" :key="c.value" class="layer-checkbox"
            :class="{ 'layer-active': activeLayers.includes(c.value) }"
          >
            <input type="checkbox" v-model="activeLayers" :value="c.value" class="checkbox-input" />
            <span class="checkbox-circle" :style="{ backgroundColor: c.colorBg }"></span>
            <span class="checkbox-label">{{ c.label }}</span>
          </label>
        </div>
        <hr class="panel-divider" />
        <p class="panel-hint">
          Selecciona las capas para mostrar información ambiental, social, productiva o de infraestructura.
        </p>
      </div>
    </div>

    <!-- Mapa principal -->
    <div id="map-container" class="map-section">
      <l-map ref="map" v-model:zoom="zoom" :center="center" style="height: 100%; width: 100%;" @click="onMapClick">
        <l-tile-layer :url="tileUrl" :attribution="tileAttr" />

        <!-- Capa ambiental -->
        <l-marker
          v-for="p in visibleCapas.ambiental"
          :key="'amb'+p.id"
          :lat-lng="p.latlng"
          :icon="greenIcon"
        >
          <l-popup class="popup-custom">
            <div class="popup-content">
              <strong class="popup-type">🌱 Zona Ambiental</strong><br />
              <span class="popup-name">{{ p.nombre }}</span>
            </div>
          </l-popup>
        </l-marker>

        <!-- Capa productiva -->
        <l-marker
          v-for="p in visibleCapas.productiva"
          :key="'prod'+p.id"
          :lat-lng="p.latlng"
          :icon="orangeIcon"
        >
          <l-popup class="popup-custom">
            <div class="popup-content">
              <strong class="popup-type">🌾 Área Productiva</strong><br />
              <span class="popup-name">{{ p.nombre }}</span>
            </div>
          </l-popup>
        </l-marker>

        <!-- Capa social -->
        <l-marker
          v-for="p in visibleCapas.social"
          :key="'soc'+p.id"
          :lat-lng="p.latlng"
          :icon="blueIcon"
        >
          <l-popup class="popup-custom">
            <div class="popup-content">
              <strong class="popup-type">👥 Proyecto Social</strong><br />
              <span class="popup-name">{{ p.nombre }}</span>
            </div>
          </l-popup>
        </l-marker>

        <!-- Capa infraestructura -->
        <l-marker
          v-for="p in visibleCapas.infraestructura"
          :key="'infra'+p.id"
          :lat-lng="p.latlng"
          :icon="grayIcon"
        >
          <l-popup class="popup-custom">
            <div class="popup-content">
              <strong class="popup-type">🏗️ Infraestructura</strong><br />
              <span class="popup-name">{{ p.nombre }}</span>
            </div>
          </l-popup>
        </l-marker>

        <!-- Sembradores Productivos -->
        <l-marker
          v-for="s in sembradores.filter(sem => mostrarSembradores && sem.tecnico_rol && sem.tecnico_rol.toLowerCase().includes('productivo'))"
          :key="'sembrador-prod-' + s.id"
          :lat-lng="[s.lat, s.lng]"
          :icon="sembradorProductivoIcon"
        >
          <l-popup class="popup-sembrador">
            <div class="popup-content-sembrador">
              <div class="popup-header-sembrador">
                <strong class="popup-type-sembrador">🌱 Sembrador Productivo</strong>
              </div>
              <div class="popup-body-sembrador">
                <p class="popup-field">
                  <span class="popup-label">Nombre:</span>
                  <span class="popup-value">{{ s.nombre }}</span>
                </p>
                <p class="popup-field">
                  <span class="popup-label">Comunidad:</span>
                  <span class="popup-value">{{ s.comunidad }}</span>
                </p>
                <p class="popup-field">
                  <span class="popup-label">Cultivo:</span>
                  <span class="popup-value">{{ s.cultivo }}</span>
                </p>
                <p class="popup-field">
                  <span class="popup-label">Técnico:</span>
                  <span class="popup-value">{{ s.tecnico_nombre }}</span>
                </p>
                <p class="popup-field text-xs">
                  <span class="popup-label">Ubicación:</span>
                  <span class="popup-value">{{ s.lat?.toFixed(4) }}, {{ s.lng?.toFixed(4) }}</span>
                </p>
              </div>
            </div>
          </l-popup>
        </l-marker>

        <!-- Sembradores Sociales -->
        <l-marker
          v-for="s in sembradores.filter(sem => mostrarSembradores && sem.tecnico_rol && sem.tecnico_rol.toLowerCase().includes('social'))"
          :key="'sembrador-soc-' + s.id"
          :lat-lng="[s.lat, s.lng]"
          :icon="sembradorSocialIcon"
        >
          <l-popup class="popup-sembrador">
            <div class="popup-content-sembrador">
              <div class="popup-header-sembrador">
                <strong class="popup-type-sembrador">👥 Sembrador Social</strong>
              </div>
              <div class="popup-body-sembrador">
                <p class="popup-field">
                  <span class="popup-label">Nombre:</span>
                  <span class="popup-value">{{ s.nombre }}</span>
                </p>
                <p class="popup-field">
                  <span class="popup-label">Comunidad:</span>
                  <span class="popup-value">{{ s.comunidad }}</span>
                </p>
                <p class="popup-field">
                  <span class="popup-label">Cultivo:</span>
                  <span class="popup-value">{{ s.cultivo }}</span>
                </p>
                <p class="popup-field">
                  <span class="popup-label">Técnico:</span>
                  <span class="popup-value">{{ s.tecnico_nombre }}</span>
                </p>
                <p class="popup-field text-xs">
                  <span class="popup-label">Ubicación:</span>
                  <span class="popup-value">{{ s.lat?.toFixed(4) }}, {{ s.lng?.toFixed(4) }}</span>
                </p>
              </div>
            </div>
          </l-popup>
        </l-marker>
      </l-map>
    </div>

    <!-- Leyenda flotante CON SEMBRADORES -->
    <div class="legend-box">
      <h3 class="legend-title">🗺️ Leyenda</h3>
      <div class="legend-items">
        <div class="legend-item">
          <div class="legend-marker" style="background: #10b981;"></div>
          <span>Ambiental</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker" style="background: #f97316;"></div>
          <span>Productiva</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker" style="background: #3b82f6;"></div>
          <span>Social</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker" style="background: #6b7280;"></div>
          <span>Infraestructura</span>
        </div>
        <hr class="legend-divider" />
        <div class="legend-item">
          <div class="legend-marker" style="background: #10b981; border-radius: 3px;"></div>
          <span>🌱 Sembrador</span>
        </div>
        <div class="legend-item">
          <div class="legend-marker" style="background: #3b82f6; border-radius: 3px;"></div>
          <span>👥 Sembrador Social</span>
        </div>
      </div>
      <div class="legend-controls">
        <label class="legend-checkbox">
          <input type="checkbox" v-model="mostrarSembradores" />
          <span>Mostrar sembradores ({{ contadorSembradores }})</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Layers, MapPin, ArrowLeft } from 'lucide-vue-next'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { getSecureApiUrl } from '../utils/api'
import HamburgerMenu from '../components/HamburgerMenu.vue'
import { addOfflinePoint, getOfflinePoints, clearOfflinePoints } from '../utils/db'
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'

const auth = useAuthStore()

// Íconos personalizados para capas temáticas
const greenIcon = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/609/609803.png',
  iconSize: [30, 30],
})
const orangeIcon = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/609/609814.png',
  iconSize: [30, 30],
})
const blueIcon = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
  iconSize: [30, 30],
})
const grayIcon = new L.Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/861/861128.png',
  iconSize: [30, 30],
})

// Íconos para sembradores (productivo y social)
const sembradorProductivoIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%2310b981" %3E%3Cpath d="M12 2c-5.52 5.52-8 8-8 11 0 4.41 3.59 8 8 8s8-3.59 8-8c0-3-2.48-5.48-8-11z"/%3E%3Ccircle cx="12" cy="13" r="3" fill="white"/%3E%3C/svg%3E',
  iconSize: [32, 40],
  iconAnchor: [16, 40],
  popupAnchor: [0, -40]
})

const sembradorSocialIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%233b82f6" %3E%3Cpath d="M12 2c-5.52 5.52-8 8-8 11 0 4.41 3.59 8 8 8s8-3.59 8-8c0-3-2.48-5.48-8-11z"/%3E%3Ccircle cx="12" cy="13" r="3" fill="white"/%3E%3C/svg%3E',
  iconSize: [32, 40],
  iconAnchor: [16, 40],
  popupAnchor: [0, -40]
})

// ========== DATOS Y REFERENCIAS ==========
const center = ref([19.4326, -99.1332])
const zoom = ref(6)
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const tileAttr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'

const capas = [
  { label: 'Ambiental', value: 'ambiental', colorBg: '#10b981' },
  { label: 'Productiva', value: 'productiva', colorBg: '#f97316' },
  { label: 'Social', value: 'social', colorBg: '#3b82f6' },
  { label: 'Infraestructura', value: 'infraestructura', colorBg: '#6b7280' },
]

const activeLayers = ref(['ambiental', 'productiva'])
const dataCapas = ref({
  ambiental: [],
  productiva: [],
  social: [],
  infraestructura: [],
})

// ========== SEMBRADORES ==========
const sembradores = ref([])
const mostrarSembradores = ref(true)
const contadorSembradores = computed(() => sembradores.value.length)

const visibleCapas = computed(() => {
  const visible = {}
  for (const c of capas) {
    visible[c.value] = activeLayers.value.includes(c.value)
      ? dataCapas.value[c.value]
      : []
  }
  return visible
})

// ========== FUNCIONES PARA SEMBRADORES ==========
const getSembradoresMapa = async () => {
  try {
    const apiUrl = getSecureApiUrl()
    const { data } = await axios.get(`${apiUrl}/sembradores/map`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    sembradores.value = data.items || data || []
  } catch (err) {
    console.error('Error al cargar sembradores para mapa:', err)
  }
}

const getIconSembrador = (s) => {
  // Determinar icono según rol del técnico
  if (s.tecnico_rol && s.tecnico_rol.toLowerCase().includes('social')) {
    return sembradorSocialIcon
  }
  return sembradorProductivoIcon
}

const centerOnUser = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        center.value = [pos.coords.latitude, pos.coords.longitude]
        zoom.value = 12
      },
      err => console.warn('No se pudo obtener ubicación:', err)
    )
  }
}

const loadLayers = async () => {
  try {
    const apiUrl = getSecureApiUrl()
    for (const c of capas) {
      const { data } = await axios.get(`${apiUrl}/layers/${c.value}`, {
        headers: { Authorization: `Bearer ${auth.token}` },
      })
      dataCapas.value[c.value] = data.items.map(p => ({
        id: p.id,
        nombre: p.nombre,
        latlng: [p.lat, p.lng],
      }))
    }
  } catch (err) {
    console.error('Error al cargar capas:', err)
  }
}

// Evento para crear nuevos puntos al hacer clic en el mapa
const onMapClick = async (event) => {
  const { lat, lng } = event.latlng
  const tipo = prompt("¿Qué tipo de capa deseas agregar? (ambiental/productiva/social/infraestructura)")
  const nombre = prompt("Nombre del punto:")

  if (!tipo || !nombre) return

  const point = { tipo, nombre, lat, lng }

  try {
    const apiUrl = getSecureApiUrl()
    await axios.post(`${apiUrl}/layers/${tipo}`, point, {
      headers: { Authorization: `Bearer ${auth.token}` },
    })
    alert("✅ Punto guardado en servidor")
    loadLayers()
  } catch {
    alert("📡 Sin conexión, guardando offline...")
    await addOfflinePoint(point)
  }
}

// Sincronizar puntos guardados offline cuando vuelva la conexión
const syncOfflinePoints = async () => {
  const offlinePoints = await getOfflinePoints()
  if (offlinePoints.length === 0) return

  const apiUrl = getSecureApiUrl()
  for (const p of offlinePoints) {
    try {
      await axios.post(`${apiUrl}/layers/${p.tipo}`, p, {
        headers: { Authorization: `Bearer ${auth.token}` },
      })
    } catch {
      console.warn('Aún sin conexión, reintentaré más tarde.')
      return
    }
  }

  await clearOfflinePoints()
  alert("✅ Datos offline sincronizados con el servidor.")
  loadLayers()
}

window.addEventListener('online', syncOfflinePoints)

onMounted(() => {
  loadLayers()
  getSembradoresMapa()
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
  width: 100vw;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #f0fdf4 100%);
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  margin: 0;
  padding: 0;
}

/* ========== BACKGROUND BLOBS ========== */
.background-blobs {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.blob {
  position: absolute;
  opacity: 0.3;
  filter: blur(120px);
  mix-blend-mode: multiply;
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
  background: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(22, 163, 74, 0.2);
  backdrop-filter: blur(12px);
  padding: 0.65rem 1rem;
  box-shadow: 0 4px 20px rgba(22, 163, 74, 0.1);
  width: 100%;
}

.header-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 50px; /* Espacio para el menú hamburguesa */
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

/* ========== BACK BUTTON ========== */
.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
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
  width: 16px;
  height: 16px;
  stroke-width: 2.5;
}

.icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 5px;
  background: transparent;
  flex-shrink: 0;
}

.icon-header {
  width: 16px;
  height: 16px;
  color: #16a34a;
  stroke-width: 2;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-text h1,
.header-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: #15803d;
  margin: 0;
  background: none;
  -webkit-background-clip: unset;
  -webkit-text-fill-color: unset;
  background-clip: unset;
}

.header-text p,
.header-subtitle {
  font-size: 0.65rem;
  color: #64748b;
  margin: 0;
  margin-top: 0.15rem;
}

.btn-location {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255, 255, 255, 0.9);
  color: #16a34a;
  border: 1.5px solid rgba(22, 163, 74, 0.4);
  border-radius: 16px;
  padding: 0.35rem 0.75rem;
  font-size: 0.7rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  white-space: nowrap;
}

.btn-location:hover {
  background: rgba(22, 163, 74, 0.1);
  box-shadow: 0 4px 15px rgba(22, 163, 74, 0.3);
  border-color: rgba(22, 163, 74, 0.6);
}

.btn-location:active {
  transform: scale(0.98);
}

.btn-icon {
  width: 14px;
  height: 14px;
}

/* ========== LAYERS PANEL ========== */
.layers-panel {
  position: absolute;
  top: 65px;
  left: 0;
  width: 240px;
  max-height: calc(100vh - 65px);
  z-index: 20;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
  border-right: 1px solid rgba(22, 163, 74, 0.15);
  border-bottom: 1px solid rgba(22, 163, 74, 0.15);
  border-radius: 0 0 12px 0;
  overflow-y: auto;
  box-shadow: 0 6px 24px rgba(22, 163, 74, 0.12);
}

.panel-wrapper {
  padding: 1rem;
}

.panel-title {
  font-size: 0.7rem;
  font-weight: 700;
  color: #1e3a2f;
  margin-bottom: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.layers-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.layer-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(240, 253, 244, 0.8);
  border: 1px solid rgba(22, 163, 74, 0.2);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.layer-checkbox:hover {
  background: rgba(220, 252, 231, 0.9);
  border-color: rgba(22, 163, 74, 0.4);
}

.layer-checkbox.layer-active {
  background: rgba(22, 163, 74, 0.15);
  border-color: rgba(22, 163, 74, 0.5);
}

.checkbox-input {
  width: 14px;
  height: 14px;
  cursor: pointer;
  accent-color: #16a34a;
}

.checkbox-circle {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.checkbox-label {
  font-size: 0.75rem;
  font-weight: 500;
  color: #374151;
}

.panel-divider {
  border: none;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
  margin: 0.65rem 0;
}

.panel-hint {
  font-size: 0.65rem;
  color: #64748b;
  line-height: 1.35;
  font-style: italic;
}

/* ========== MAP SECTION ========== */
.map-section {
  flex: 1;
  position: relative;
  z-index: 10;
  overflow: hidden;
  margin-left: 240px;
}

/* ========== LEGEND BOX ========== */
.legend-box {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  z-index: 40;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(22, 163, 74, 0.3);
  border-radius: 10px;
  padding: 0.75rem;
  backdrop-filter: blur(12px);
  box-shadow: 0 6px 24px rgba(22, 163, 74, 0.12);
  max-width: 220px;
}

.legend-title {
  font-size: 0.7rem;
  font-weight: 700;
  color: #1e3a2f;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.7rem;
  color: #374151;
}

.legend-marker {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
}

/* ========== POPUP STYLES ========== */
:deep(.leaflet-popup-content-wrapper) {
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid rgba(22, 163, 74, 0.3);
  box-shadow: 0 8px 30px rgba(22, 163, 74, 0.12);
  backdrop-filter: blur(10px);
}

:deep(.leaflet-popup-tip) {
  border-top-color: rgba(255, 255, 255, 0.98);
}

:deep(.leaflet-popup-close-button) {
  color: #64748b;
}

:deep(.leaflet-popup-close-button:hover) {
  color: #16a34a;
}

.popup-custom {
  color: #374151;
}

.popup-content {
  padding: 0.35rem 0;
  min-width: 150px;
}

.popup-type {
  font-size: 0.8rem;
  font-weight: 600;
  color: #16a34a;
  display: block;
  margin-bottom: 0.35rem;
}

.popup-name {
  font-size: 0.75rem;
  color: #1e3a2f;
  display: block;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .header-wrapper {
    gap: 0.75rem;
  }

  .header-text h1 {
    font-size: 0.8rem;
  }

  .layers-panel {
    width: 220px;
    top: 60px;
  }

  .map-section {
    margin-left: 220px;
  }

  .legend-box {
    bottom: 0.75rem;
    right: 0.75rem;
    max-width: 200px;
  }
}

@media (max-width: 768px) {
  .header-mapa {
    padding: 0.55rem 0.85rem;
  }

  .back-button {
    width: 30px;
    height: 30px;
  }

  .back-icon {
    width: 14px;
    height: 14px;
  }

  .header-wrapper {
    flex-direction: column;
    gap: 0.5rem;
    padding-right: 50px;
  }

  .header-text h1 {
    font-size: 0.75rem;
  }

  .header-text p {
    font-size: 0.6rem;
  }

  .btn-location {
    width: 100%;
    justify-content: center;
    padding: 0.35rem 0.65rem;
    font-size: 0.65rem;
  }

  .layers-panel {
    width: 100%;
    height: auto;
    max-height: none;
    position: relative;
    top: auto;
    border-radius: 0;
    border-right: none;
    margin-bottom: 0;
  }

  .panel-wrapper {
    padding: 0.75rem;
  }

  .panel-title {
    font-size: 0.65rem;
    margin-bottom: 0.5rem;
  }

  .layers-list {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .layer-checkbox {
    padding: 0.4rem 0.5rem;
    flex: 1;
    min-width: 100px;
  }

  .checkbox-label {
    font-size: 0.65rem;
  }

  .panel-hint {
    display: none;
  }

  .panel-divider {
    display: none;
  }

  .map-section {
    margin-left: 0;
  }

  .legend-box {
    bottom: 0.5rem;
    right: 0.5rem;
    max-width: none;
    width: auto;
    padding: 0.5rem;
  }

  .legend-title {
    font-size: 0.6rem;
    margin-bottom: 0.35rem;
  }

  .legend-item {
    font-size: 0.6rem;
    gap: 0.35rem;
  }

  .legend-marker {
    width: 12px;
    height: 12px;
  }
}

@media (max-width: 640px) {
  .header-mapa {
    padding: 0.5rem 0.75rem;
  }

  .header-left {
    gap: 0.4rem;
  }

  .back-button {
    width: 28px;
    height: 28px;
  }

  .back-icon {
    width: 14px;
    height: 14px;
  }

  .icon-box {
    display: none;
  }

  .header-text h1,
  .header-title {
    font-size: 0.75rem;
  }

  .header-text p,
  .header-subtitle {
    font-size: 0.55rem;
  }

  .btn-location {
    padding: 0.3rem 0.6rem;
    font-size: 0.6rem;
  }

  .btn-icon {
    width: 12px;
    height: 12px;
  }

  .panel-title {
    font-size: 0.6rem;
  }

  .layer-checkbox {
    padding: 0.35rem 0.45rem;
    gap: 0.35rem;
  }

  .checkbox-input {
    width: 12px;
    height: 12px;
  }

  .checkbox-circle {
    width: 10px;
    height: 10px;
  }

  .checkbox-label {
    font-size: 0.6rem;
  }

  .legend-box {
    padding: 0.4rem;
    bottom: 0.35rem;
    right: 0.35rem;
    border-radius: 8px;
  }

  .legend-title {
    font-size: 0.55rem;
    margin-bottom: 0.3rem;
  }

  .legend-items {
    gap: 0.25rem;
  }

  .legend-item {
    font-size: 0.55rem;
    gap: 0.3rem;
  }

  .legend-marker {
    width: 10px;
    height: 10px;
  }

  .legend-divider {
    margin: 0.25rem 0;
  }

  .legend-controls {
    padding-top: 0.35rem;
    margin-top: 0.35rem;
  }

  .legend-checkbox {
    font-size: 0.55rem;
    gap: 0.3rem;
  }

  .legend-checkbox input {
    width: 12px;
    height: 12px;
  }
}

/* ========== LEAFLET OVERRIDES ========== */
:deep(.leaflet-container) {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

:deep(.leaflet-control-attribution) {
  background: rgba(255, 255, 255, 0.9) !important;
  color: #64748b !important;
  font-size: 0.7rem;
  backdrop-filter: blur(10px);
  border: none;
  border-top: 1px solid rgba(22, 163, 74, 0.2);
}

:deep(.leaflet-control-attribution a) {
  color: #16a34a !important;
  text-decoration: none;
}

:deep(.leaflet-control-attribution a:hover) {
  text-decoration: underline;
}

/* ========== ESTILOS POPUP SEMBRADORES ========== */
.popup-sembrador {
  color: #374151;
}

.popup-content-sembrador {
  padding: 0;
  min-width: 180px;
}

.popup-header-sembrador {
  padding: 0.5rem 0.6rem 0.35rem 0.6rem;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
  border-bottom: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 6px 6px 0 0;
}

.popup-type-sembrador {
  font-size: 0.75rem;
  font-weight: 700;
  color: #10b981;
  display: block;
}

.popup-body-sembrador {
  padding: 0.5rem 0.6rem;
}

.popup-field {
  margin: 0 0 0.35rem 0;
  font-size: 0.7rem;
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.35rem;
  background: rgba(71, 85, 105, 0.3);
  border-radius: 3px;
}

.popup-field:last-child {
  margin-bottom: 0;
}

.popup-label {
  font-weight: 600;
  color: #64748b;
  white-space: nowrap;
  font-size: 0.65rem;
}

.popup-value {
  color: #1e3a2f;
  text-align: right;
  word-break: break-word;
  font-size: 0.65rem;
}

.popup-field.text-xs {
  font-size: 0.6rem;
}

/* ========== LEGEND CONTROLS ========== */
.legend-divider {
  border: none;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
  margin: 0.35rem 0;
}

.legend-controls {
  padding-top: 0.5rem;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
  margin-top: 0.5rem;
}

.legend-checkbox {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  cursor: pointer;
  font-size: 0.65rem;
  color: #374151;
  user-select: none;
}

.legend-checkbox input {
  width: 12px;
  height: 12px;
  cursor: pointer;
  accent-color: #16a34a;
}

.legend-checkbox:hover {
  color: #1e3a2f;
}

@media (max-width: 480px) {
  .header-mapa {
    padding: 0.45rem 0.6rem;
  }

  .back-button {
    width: 26px;
    height: 26px;
  }

  .back-icon {
    width: 12px;
    height: 12px;
  }

  .header-left {
    gap: 0.35rem;
  }

  .header-text h1 {
    font-size: 0.7rem;
  }

  .header-text p {
    font-size: 0.5rem;
  }

  .btn-location {
    padding: 0.25rem 0.5rem;
    font-size: 0.55rem;
    border-radius: 12px;
  }

  .panel-wrapper {
    padding: 0.5rem;
  }

  .layer-checkbox {
    padding: 0.3rem 0.4rem;
    min-width: 80px;
  }

  .legend-box {
    padding: 0.35rem;
    border-radius: 6px;
  }

  .legend-title {
    font-size: 0.5rem;
  }

  .legend-item {
    font-size: 0.5rem;
  }

  .legend-marker {
    width: 8px;
    height: 8px;
  }

  .legend-checkbox {
    font-size: 0.5rem;
  }

  .legend-checkbox input {
    width: 10px;
    height: 10px;
  }
}

/* ========== 360px - Pantallas muy pequeñas ========== */
@media (max-width: 360px) {
  .header-mapa {
    padding: 0.4rem 0.5rem;
  }

  .back-button {
    width: 24px;
    height: 24px;
  }

  .header-text h1 {
    font-size: 0.65rem;
  }

  .header-text p {
    font-size: 0.45rem;
  }

  .btn-location {
    padding: 0.2rem 0.4rem;
    font-size: 0.5rem;
  }

  .btn-icon {
    width: 10px;
    height: 10px;
  }

  .panel-wrapper {
    padding: 0.4rem;
  }

  .panel-title {
    font-size: 0.55rem;
  }

  .layer-checkbox {
    padding: 0.25rem 0.35rem;
    min-width: 70px;
  }

  .checkbox-input {
    width: 10px;
    height: 10px;
  }

  .checkbox-circle {
    width: 8px;
    height: 8px;
  }

  .checkbox-label {
    font-size: 0.55rem;
  }

  .legend-box {
    padding: 0.3rem;
    border-radius: 5px;
    bottom: 0.25rem;
    right: 0.25rem;
  }

  .legend-title {
    font-size: 0.45rem;
  }

  .legend-item {
    font-size: 0.45rem;
    gap: 0.2rem;
  }

  .legend-marker {
    width: 7px;
    height: 7px;
  }
}

/* ========== Landscape mobile ========== */
@media (max-height: 500px) and (orientation: landscape) {
  .mapa-container {
    height: 100vh;
  }

  .header-mapa {
    padding: 0.35rem 0.65rem;
  }

  .header-wrapper {
    flex-direction: row;
    gap: 0.5rem;
  }

  .header-text h1 {
    font-size: 0.7rem;
  }

  .header-text p {
    font-size: 0.5rem;
  }

  .back-button {
    width: 26px;
    height: 26px;
  }

  .btn-location {
    padding: 0.25rem 0.5rem;
    font-size: 0.55rem;
  }

  .layers-panel {
    position: absolute;
    top: 50px;
    left: 0;
    width: 180px;
    max-height: calc(100vh - 50px);
  }

  .panel-wrapper {
    padding: 0.5rem;
  }

  .panel-title {
    font-size: 0.55rem;
    margin-bottom: 0.35rem;
  }

  .layers-list {
    flex-direction: column;
    gap: 0.3rem;
  }

  .layer-checkbox {
    padding: 0.3rem 0.4rem;
  }

  .checkbox-label {
    font-size: 0.55rem;
  }

  .map-section {
    margin-left: 180px;
  }

  .legend-box {
    bottom: 0.35rem;
    right: 0.35rem;
    padding: 0.35rem;
    max-width: 160px;
  }

  .legend-title {
    font-size: 0.5rem;
  }

  .legend-item {
    font-size: 0.5rem;
  }

  .legend-marker {
    width: 8px;
    height: 8px;
  }

  .legend-checkbox {
    font-size: 0.5rem;
  }
}
</style>
