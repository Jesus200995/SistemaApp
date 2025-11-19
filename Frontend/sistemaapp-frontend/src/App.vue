<script setup lang="ts">
import { RouterView } from 'vue-router'
import PWAInstall from './components/PWAInstall.vue'
import FaviconManager from './components/FaviconManager.vue'
</script>

<template>
  <div id="app">
    <!-- Gestor del Favicon con animaciones -->
    <FaviconManager />
    
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
}</style>


