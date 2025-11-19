<script setup lang="ts">
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import PWAInstall from './components/PWAInstall.vue'
import FaviconManager from './components/FaviconManager.vue'
import UpdateModal from './components/UpdateModal.vue'
import { usePWAUpdate } from './composables/usePWAUpdate'
import { useAuthStore } from './stores/auth'

// Inicializar actualización automática de PWA
usePWAUpdate()

// 🔄 Inicializar autenticación al cargar la app
onMounted(async () => {
  const auth = useAuthStore()
  
  // Si hay token guardado, cargar el perfil del usuario
  if (auth.token && !auth.user) {
    try {
      await auth.fetchProfile()
    } catch (error) {
      console.error('Error al cargar perfil inicial:', error)
    }
  }
})
</script>

<template>
  <div id="app">
    <!-- Gestor del Favicon con animaciones -->
    <FaviconManager />
    
    <!-- Modal de Actualización de PWA -->
    <UpdateModal />
    
    <!-- Componente de instalación PWA -->
    <PWAInstall />
    
    <!-- Vistas del Router -->
    <RouterView />
  </div>
</template>

<style scoped>
#app {
  height: 100%;
  width: 100%;
}
</style>


