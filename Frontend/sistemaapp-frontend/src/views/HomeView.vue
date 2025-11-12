<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <main>
    <div class="header-container" style="padding: 1rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee;">
      <div>
        <h1 style="margin: 0; font-size: 1.5rem;">Bienvenido, {{ auth.user?.nombre || 'Usuario' }}</h1>
        <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">{{ auth.user?.email || '' }}</p>
      </div>
      <button
        @click="logout"
        style="background-color: #ef4444; color: white; padding: 0.5rem 1rem; border: none; border-radius: 0.375rem; cursor: pointer; font-size: 0.9rem; font-weight: 500;"
      >
        Cerrar sesión
      </button>
    </div>
    <TheWelcome />
  </main>
</template>
