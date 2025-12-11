import { defineStore } from 'pinia'
import axios from 'axios'
import { getSecureApiUrl } from '../utils/api'

// Helper para obtener token de forma segura
const getStoredToken = () => {
  try {
    const token = localStorage.getItem('token')
    if (token && token !== 'null' && token !== 'undefined') {
      console.log('🔑 Token recuperado del localStorage')
      return token
    }
  } catch (e) {
    console.error('⚠️ Error al leer token del localStorage:', e)
  }
  return null
}

// Helper para guardar token de forma segura
const saveToken = (token) => {
  try {
    if (token) {
      localStorage.setItem('token', token)
      console.log('💾 Token guardado en localStorage')
      return true
    }
  } catch (e) {
    console.error('⚠️ Error al guardar token en localStorage:', e)
  }
  return false
}

// Helper para eliminar token
const removeToken = () => {
  try {
    localStorage.removeItem('token')
    console.log('🗑️ Token eliminado del localStorage')
  } catch (e) {
    console.error('⚠️ Error al eliminar token:', e)
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: getStoredToken(),
    error: null,
  }),

  actions: {
    async login(email, password) {
      try {
        this.error = null
        // Normalizar email a minúsculas
        const emailNormalizado = email.trim().toLowerCase()
        const API_URL = getSecureApiUrl()
        console.log('🔐 Intentando login en:', API_URL)
        
        const { data } = await axios.post(
          `${API_URL}/auth/login`,
          { email: emailNormalizado, password }
        )
        this.user = data.user
        this.token = data.token
        saveToken(data.token)
        this.error = null
        console.log('✅ Login exitoso para:', emailNormalizado)
        return true
      } catch (err) {
        console.error('❌ Error en login:', err.response?.data || err.message)
        this.error = err.response?.data?.detail || 'Error al iniciar sesión'
        return false
      }
    },

    async register(nombre, email, password, rol = 'usuario') {
      try {
        const API_URL = getSecureApiUrl()
        await axios.post(`${API_URL}/auth/register`, {
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
    async createUserHierarchical(nombre, email, password, rol, curp = null, telefono = null, territorio = null) {
      try {
        const API_URL = getSecureApiUrl()
        const { data } = await axios.post(
          `${API_URL}/auth/create-user`,
          { nombre, email, password, rol, curp, telefono, territorio },
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
        const API_URL = getSecureApiUrl()
        const { data } = await axios.get(
          `${API_URL}/auth/roles-permitidos`,
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
      if (!this.token) {
        console.log('⚠️ fetchProfile: No hay token disponible')
        return
      }
      try {
        const API_URL = getSecureApiUrl()
        console.log('📡 fetchProfile: Solicitando perfil a:', API_URL)
        const { data } = await axios.get(
          `${API_URL}/auth/me`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        )
        this.user = data
        this.error = null
        console.log('✅ fetchProfile: Perfil cargado para:', data?.nombre || data?.email)
      } catch (err) {
        console.error('❌ fetchProfile Error:', err.response?.status, err.response?.data?.detail || err.message)
        this.error = err.response?.data?.detail || 'Error al obtener perfil'
        // Si el token es inválido, limpiar la sesión
        if (err.response?.status === 401) {
          console.log('🔒 Token inválido (401), cerrando sesión...')
          this.logout()
        }
      }
    },

    logout() {
      this.user = null
      this.token = null
      removeToken()
    },

    // Verificar si el token es válido (útil para debugging en PWA)
    async verifyToken() {
      if (!this.token) {
        console.log('⚠️ No hay token para verificar')
        return false
      }
      try {
        const API_URL = getSecureApiUrl()
        console.log('🔍 Verificando token en:', API_URL)
        const { data } = await axios.get(
          `${API_URL}/auth/me`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        )
        this.user = data
        console.log('✅ Token válido para usuario:', data?.nombre || data?.email)
        return true
      } catch (err) {
        console.error('❌ Token inválido:', err.response?.status, err.response?.data?.detail)
        if (err.response?.status === 401) {
          this.logout()
        }
        return false
      }
    },
  },
})
