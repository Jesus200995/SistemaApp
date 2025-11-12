<script setup lang="ts">
import Navbar from '../components/Navbar.vue'
import TheWelcome from '../components/TheWelcome.vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
</script>

<template>
  <div class="home-container">
    <!-- Navbar con notificaciones -->
    <Navbar />
    
    <!-- Contenido principal -->
    <main class="main-content">
      <TheWelcome />
    </main>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
}

.main-content {
  flex: 1;
  overflow-y: auto;
}
</style>
