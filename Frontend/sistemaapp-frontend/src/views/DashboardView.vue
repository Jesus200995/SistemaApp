<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center py-10">
    <div class="bg-white shadow-md rounded-lg p-6 w-96 text-center">
      <h2 class="text-2xl font-bold text-gray-700 mb-4">
        Bienvenido, {{ auth.user?.nombre || 'Usuario' }} 👋
      </h2>

      <p class="text-gray-600">Rol: <strong>{{ auth.user?.rol }}</strong></p>
      <p class="text-gray-600 mt-1">Correo: <strong>{{ auth.user?.email }}</strong></p>

      <button
        @click="logout"
        class="mt-6 bg-red-500 hover:bg-red-600 text-white font-semibold px-4 py-2 rounded-lg"
      >
        Cerrar sesión
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
const auth = useAuthStore()

onMounted(() => {
  auth.fetchProfile()
})

const logout = () => {
  auth.logout()
  window.location.href = '/login'
}
</script>
