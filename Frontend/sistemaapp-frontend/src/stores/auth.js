import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    error: null,
  }),

  actions: {
    async login(email, password) {
      try {
        const { data } = await axios.post(
          `${import.meta.env.VITE_API_URL}/auth/login`,
          { email, password }
        )
        this.user = data.user
        this.token = data.token
        localStorage.setItem('token', data.token)
        this.error = null
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al iniciar sesión'
        return false
      }
    },

    async register(nombre, email, password, rol = 'usuario') {
      try {
        await axios.post(`${import.meta.env.VITE_API_URL}/auth/register`, {
          nombre,
          email,
          password,
          rol,
        })
        this.error = null
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al registrar usuario'
        return false
      }
    },

    /**
     * Crear usuario jerárquicamente (solo para admin, territorial, facilitador)
     */
    async createUserHierarchical(nombre, email, password, rol) {
      try {
        const { data } = await axios.post(
          `${import.meta.env.VITE_API_URL}/auth/create-user`,
          { nombre, email, password, rol },
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        )
        this.error = null
        return { success: true, data }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al crear usuario'
        return { success: false, error: this.error }
      }
    },

    /**
     * Obtener roles permitidos para crear según el rol actual
     */
    async getRolesPermitidos() {
      try {
        const { data } = await axios.get(
          `${import.meta.env.VITE_API_URL}/auth/roles-permitidos`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        )
        return data
      } catch (err) {
        console.error('Error al obtener roles permitidos:', err)
        return { puede_crear: false, roles_permitidos: [] }
      }
    },

    async fetchProfile() {
      if (!this.token) return
      try {
        const { data } = await axios.get(
          `${import.meta.env.VITE_API_URL}/auth/me`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        )
        this.user = data
        this.error = null
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al obtener perfil'
        // Si el token es inválido, limpiar la sesión
        if (err.response?.status === 401) {
          this.logout()
        }
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    },
  },
})
