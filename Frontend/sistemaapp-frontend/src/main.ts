import './assets/main.css'
import './assets/favicon-animations.css'
import './registerSW'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { MotionPlugin } from '@vueuse/motion'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(MotionPlugin)

app.mount('#app')

// Escuchar mensajes del Service Worker para recargar automáticamente
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.addEventListener('message', (event) => {
    if (event.data?.type === 'SW_ACTIVATED') {
      console.log('🔄 Nueva versión del SW activada, recargando...')
      window.location.reload()
    }
  })
  
  // Detectar cuando un nuevo SW toma control
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    console.log('🔄 Nuevo Service Worker tomó control, recargando...')
    window.location.reload()
  })
}
