<template>
  <div class="h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-6 rounded shadow-md w-80">
      <h2 class="text-xl font-bold mb-4 text-center">Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <input
          v-model="email"
          type="email"
          placeholder="Correo"
          class="border p-2 w-full mb-3 rounded"
          required
        />
        <input
          v-model="password"
          type="password"
          placeholder="Contraseña"
          class="border p-2 w-full mb-3 rounded"
          required
        />
        <button
          type="submit"
          class="bg-green-500 text-white p-2 w-full rounded hover:bg-green-600"
        >
          Entrar
        </button>
      </form>
      <p v-if="auth.error" class="text-red-500 text-sm mt-3 text-center">
        {{ auth.error }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  const ok = await auth.login(email.value, password.value)
  if (ok) {
    router.push('/')
  }
}
</script>
