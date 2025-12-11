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
  
  // Debug info para PWA móvil
  console.log('🚀 App inicializada')
  console.log('📱 PWA standalone:', window.matchMedia('(display-mode: standalone)').matches)
  console.log('🔑 Token en store:', auth.token ? 'Sí' : 'No')
  
  // Si hay token guardado, cargar el perfil del usuario
  if (auth.token && !auth.user) {
    console.log('🔄 Cargando perfil de usuario...')
    try {
      await auth.fetchProfile()
      if (auth.user) {
        console.log('✅ Perfil cargado:', auth.user?.nombre || auth.user?.email)
      }
    } catch (error) {
      console.error('❌ Error al cargar perfil inicial:', error)
    }
  } else if (!auth.token) {
    console.log('⚠️ No hay token guardado - usuario no autenticado')
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


