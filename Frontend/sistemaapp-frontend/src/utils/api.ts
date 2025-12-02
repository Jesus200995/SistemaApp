/**
 * Utilidades para configuración de API
 * Centraliza la construcción de URLs para evitar problemas de CORS y trailing slashes
 */

/**
 * Obtiene la URL base del API sin trailing slash
 */
export const getApiUrl = (): string => {
  const url = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  return url.replace(/\/$/, '')
}

/**
 * Construye una URL completa del API con el endpoint dado
 * @param endpoint - El endpoint (con o sin leading slash)
 * @returns URL completa
 */
export const buildApiUrl = (endpoint: string): string => {
  const baseUrl = getApiUrl()
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  // Asegurar trailing slash para evitar redirects
  const finalEndpoint = cleanEndpoint.endsWith('/') ? cleanEndpoint : `${cleanEndpoint}/`
  return `${baseUrl}${finalEndpoint}`
}

/**
 * Construye la URL del WebSocket basada en la URL del API
 * @param endpoint - El endpoint del WebSocket
 * @returns URL completa del WebSocket
 */
export const buildWsUrl = (endpoint: string): string => {
  const apiUrl = getApiUrl()
  // Determinar protocolo basado en la URL del API, no en window.location
  const isSecure = apiUrl.startsWith('https')
  const protocol = isSecure ? 'wss:' : 'ws:'
  const host = apiUrl.replace(/^(https?:\/\/)/, '')
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  return `${protocol}//${host}${cleanEndpoint}`
}

/**
 * Obtiene los headers de autenticación
 * @param token - Token opcional, si no se proporciona se busca en localStorage
 * @returns Headers con Authorization
 */
export const getAuthHeaders = (token?: string | null): Record<string, string> => {
  const authToken = token || localStorage.getItem('token')
  return authToken ? { Authorization: `Bearer ${authToken}` } : {}
}

export default {
  getApiUrl,
  buildApiUrl,
  buildWsUrl,
  getAuthHeaders,
}
