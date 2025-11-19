<script setup lang="ts">
import { RouterView } from 'vue-router'
import PWAInstall from './components/PWAInstall.vue'
import FaviconManager from './components/FaviconManager.vue'
import UpdateModal from './components/UpdateModal.vue'
import { usePWAUpdate } from './composables/usePWAUpdate'

// Inicializar actualización automática de PWA
usePWAUpdate()
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


