<template>
  <div v-if="showInstallButton" class="install-pwa-container">
    <!-- Banner de instalación -->
    <div class="install-banner">
      <div class="banner-content">
        <div class="banner-icon">
          📱
        </div>
        <div class="banner-text">
          <h3>Instala SistemaApp</h3>
          <p>Accede rápidamente desde tu pantalla de inicio</p>
        </div>
        <button @click="install" class="install-btn">
          <span>Instalar</span>
        </button>
        <button @click="dismiss" class="dismiss-btn" aria-label="Cerrar">
          ✕
        </button>
      </div>
    </div>

    <!-- Indicador de estado -->
    <div v-if="isOnline === false" class="offline-indicator">
      ⚠️ Sin conexión - Los datos se sincronizarán cuando haya conexión
    </div>

    <!-- Botón flotante de instalación -->
    <button 
      v-if="pwa.isInstallable.value && !dismissed"
      @click="install" 
      class="install-fab"
      title="Instalar aplicación"
    >
      <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
        <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePWA } from '../composables/usePWA'

const pwa = usePWA()
const dismissed = ref(false)

const showInstallButton = computed(() => {
  return pwa.isInstallable.value && !pwa.isInstalled.value && !dismissed.value
})

const isOnline = computed(() => pwa.isOnline.value)

const install = async () => {
  await pwa.installApp()
  dismissed.value = true
}

const dismiss = () => {
  dismissed.value = true
}
</script>

<style scoped>
.install-pwa-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  pointer-events: none;
}

/* ========== BANNER DE INSTALACIÓN ========== */
.install-banner {
  pointer-events: all;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 -4px 20px rgba(22, 163, 74, 0.15);
  animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.banner-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.banner-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.banner-text {
  flex: 1;
  color: white;
}

.banner-text h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  font-weight: 600;
}

.banner-text p {
  margin: 0;
  font-size: 0.85rem;
  opacity: 0.9;
}

.install-btn {
  flex-shrink: 0;
  background: white;
  color: #16a34a;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.2);
}

.install-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

.install-btn:active {
  transform: translateY(0);
}

.dismiss-btn {
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.dismiss-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* ========== INDICADOR OFFLINE ========== */
.offline-indicator {
  pointer-events: all;
  background: #f59e0b;
  color: #78350f;
  padding: 0.75rem 1rem;
  text-align: center;
  font-size: 0.875rem;
  font-weight: 500;
  animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ========== BOTÓN FLOTANTE ========== */
.install-fab {
  pointer-events: all;
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(22, 163, 74, 0.4);
  transition: all 0.3s ease;
  animation: fadeInScale 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 99;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.install-fab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 24px rgba(22, 163, 74, 0.5);
}

.install-fab:active {
  transform: scale(0.95);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 640px) {
  .banner-content {
    padding: 0.75rem 1rem;
    gap: 0.75rem;
  }

  .banner-icon {
    font-size: 1.5rem;
  }

  .banner-text h3 {
    font-size: 0.95rem;
  }

  .banner-text p {
    font-size: 0.8rem;
  }

  .install-btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }

  .install-fab {
    width: 48px;
    height: 48px;
    bottom: 70px;
    right: 16px;
  }

  .install-fab svg {
    width: 20px;
    height: 20px;
  }
}
</style>
