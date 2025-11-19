<template>
  <transition name="fade">
    <div v-if="isVisible" class="update-modal-overlay">
      <div class="update-modal">
        <!-- Icono de actualización animado -->
        <div class="update-icon">
          <svg viewBox="0 0 24 24" class="spinner">
            <path
              d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"
              fill="#10b981"
            />
          </svg>
        </div>

        <!-- Contenido -->
        <h2 class="update-title">{{ title }}</h2>
        <p class="update-message">{{ message }}</p>

        <!-- Progress bar -->
        <div class="progress-bar">
          <div class="progress-fill"></div>
        </div>

        <!-- Texto informativo -->
        <p class="update-info">{{ infoText }}</p>

        <!-- Botones -->
        <div class="update-actions" v-if="showButton">
          <button @click="handleUpdate" class="update-button">
            Actualizar Ahora
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)
const title = ref('Actualizando App...')
const message = ref('Se está descargando la última versión')
const infoText = ref('Por favor no cierres la app')
const showButton = ref(false)
let updateTimer: ReturnType<typeof setTimeout> | null = null

const handleUpdate = () => {
  window.location.reload()
}

const showUpdateModal = (config: any = {}) => {
  title.value = config.title || 'Actualizando App...'
  message.value = config.message || 'Se está descargando la última versión'
  infoText.value = config.infoText || 'Por favor no cierres la app'
  showButton.value = config.showButton || false
  isVisible.value = true
}

const hideUpdateModal = () => {
  isVisible.value = false
  if (updateTimer) {
    clearTimeout(updateTimer)
  }
}

const closeModal = () => {
  hideUpdateModal()
}

// Exponer funciones para uso global
window.__updateModal = {
  show: showUpdateModal,
  hide: hideUpdateModal,
}

onMounted(() => {
  // Escuchar eventos de actualización desde el Service Worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('message', (event: any) => {
      const messageData = event.data || {}
      
      if (messageData.type === 'UPDATE_AVAILABLE') {
        showUpdateModal({
          title: '✨ Nueva Versión Disponible',
          message: 'Se está descargando la actualización...',
          infoText: 'La app se actualizará automáticamente',
          showButton: false,
        })

        // Auto-reload después de 3 segundos
        updateTimer = setTimeout(() => {
          window.location.reload()
        }, 3000)
      } else if (messageData.type === 'UPDATE_ACTIVATED') {
        showUpdateModal({
          title: '✅ App Actualizada',
          message: 'La aplicación se ha actualizado correctamente',
          infoText: 'Se recargará en 2 segundos...',
          showButton: false,
        })

        // Auto-reload después de 2 segundos
        updateTimer = setTimeout(() => {
          window.location.reload()
        }, 2000)
      }
    })
  }
})

onUnmounted(() => {
  if (updateTimer) {
    clearTimeout(updateTimer)
  }
})
</script>

<style scoped>
.update-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}

.update-modal {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 20px;
  padding: 2rem 1.5rem;
  max-width: 320px;
  width: 90%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 1px rgba(16, 185, 129, 0.2);
  backdrop-filter: blur(10px);
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.update-icon {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.spinner {
  width: 60px;
  height: 60px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.update-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #22c55e;
  margin: 1rem 0 0.5rem 0;
  letter-spacing: -0.01em;
}

.update-message {
  font-size: 0.95rem;
  color: #cbd5e1;
  margin: 0.5rem 0 1rem 0;
  line-height: 1.5;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 10px;
  overflow: hidden;
  margin: 1rem 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #22c55e);
  border-radius: 10px;
  animation: progressAnimation 2s ease-in-out infinite;
}

@keyframes progressAnimation {
  0% {
    width: 0%;
  }
  50% {
    width: 100%;
  }
  100% {
    width: 0%;
  }
}

.update-info {
  font-size: 0.85rem;
  color: #94a3b8;
  margin: 0.75rem 0 1rem 0;
}

.update-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.update-button {
  flex: 1;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
}

.update-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
}

.update-button:active {
  transform: translateY(0);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 480px) {
  .update-modal {
    padding: 1.5rem 1rem;
    max-width: 90%;
  }

  .update-title {
    font-size: 1.1rem;
  }

  .update-message {
    font-size: 0.9rem;
  }
}

@media (max-width: 320px) {
  .update-modal {
    padding: 1rem 0.8rem;
    margin: 1rem;
  }

  .update-title {
    font-size: 1rem;
  }

  .update-message {
    font-size: 0.85rem;
  }

  .spinner {
    width: 50px;
    height: 50px;
  }
}
</style>
