/**
 * Helper para obtener la URL segura de la API
 * Fuerza HTTPS cuando la página está cargada sobre HTTPS
 * para evitar errores de "Mixed Content"
 */
export const getSecureApiUrl = (): string => {
  let apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  
  // Si la página está en HTTPS, forzar que la API también use HTTPS
  if (typeof window !== 'undefined' && window.location.protocol === 'https:' && apiUrl.startsWith('http://')) {
    apiUrl = apiUrl.replace('http://', 'https://')
  }
  
  return apiUrl
}

/**
 * Helper para obtener la URL de WebSocket segura
 * Usa WSS cuando la página está en HTTPS
 */
export const getSecureWsUrl = (path: string): string => {
  const protocol = typeof window !== 'undefined' && window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const apiUrl = getSecureApiUrl()
  
  if (apiUrl.startsWith('/')) {
    return `${protocol}//${window.location.host}${apiUrl}${path}`
  } else {
    const host = apiUrl.replace(/^(https?:\/\/)/, '').replace(/\/$/, '')
    return `${protocol}//${host}${path}`
  }
}

export default {
  getSecureApiUrl,
  getSecureWsUrl
}
