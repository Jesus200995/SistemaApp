import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'https://sistemaapi.sembrandodatos.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        secure: true,
        ws: true, // Habilitar proxy de WebSocket
      },
    },
  },
  plugins: [
    vue(),
    vueDevTools(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'robots.txt', 'apple-touch-icon.png'],
      workbox: {
        // Forzar actualización del SW al cambiar archivos
        cleanupOutdatedCaches: true,
        skipWaiting: true,
        clientsClaim: true,
        globPatterns: ['**/*.{js,css,html,ico,png,jpg,jpeg,gif,svg,woff,woff2,ttf,eot}'],
        // IMPORTANTE: Excluir archivos de API del precache
        navigateFallbackDenylist: [/^\/api/, /^\/auth/, /^\/solicitudes/, /^\/usuarios/],
        runtimeCaching: [
          {
            urlPattern: ({ request }) => request.destination === 'document',
            handler: 'NetworkFirst',
            options: {
              cacheName: 'pages-cache',
              networkTimeoutSeconds: 3,
            },
          },
          {
            urlPattern: ({ request }) =>
              ['style', 'script', 'worker'].includes(request.destination),
            handler: 'StaleWhileRevalidate',
            options: {
              cacheName: 'static-resources',
            },
          },
          {
            urlPattern: ({ request }) => request.destination === 'image',
            handler: 'CacheFirst',
            options: {
              cacheName: 'images-cache',
              expiration: { maxEntries: 100, maxAgeSeconds: 7 * 24 * 60 * 60 },
            },
          },
          // NETWORK ONLY para TODAS las rutas de API - NUNCA CACHEAR
          {
            urlPattern: ({ url }) => 
              url.pathname.startsWith('/api') ||
              url.pathname.startsWith('/auth') ||
              url.pathname.startsWith('/solicitudes') ||
              url.pathname.startsWith('/usuarios') ||
              url.pathname.startsWith('/notificaciones') ||
              url.pathname.startsWith('/sembradores') ||
              url.pathname.startsWith('/seguimientos'),
            handler: 'NetworkOnly',
          },
          // NETWORK ONLY para API externa (otro dominio)
          {
            urlPattern: ({ url }) => url.origin.includes('sistemaapi.sembrandodatos.com'),
            handler: 'NetworkOnly',
          },
        ],
      },
      manifest: {
        name: 'SistemaApp - Panel de Control',
        short_name: 'SistemaApp',
        description: 'Sistema Territorial de Administración - Panel de control completo con notificaciones en tiempo real',
        theme_color: '#10b981',
        background_color: '#0f172a',
        display: 'standalone',
        scope: '/',
        start_url: '/',
        orientation: 'portrait-primary',
        categories: ['business', 'productivity'],
        icons: [
          {
            src: '/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'any',
          },
          {
            src: '/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any',
          },
          {
            src: '/pwa-192x192-maskable.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'maskable',
          },
          {
            src: '/pwa-512x512-maskable.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
        ],
        screenshots: [
          {
            src: '/pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png',
            form_factor: 'narrow',
          },
          {
            src: '/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            form_factor: 'wide',
          },
        ],
        shortcuts: [
          {
            name: 'Dashboard',
            short_name: 'Dashboard',
            description: 'Ir al panel de control',
            url: '/dashboard',
            icons: [
              {
                src: '/pwa-192x192.png',
                sizes: '192x192',
                type: 'image/png',
              },
            ],
          },
          {
            name: 'Chat',
            short_name: 'Chat',
            description: 'Abrir chat',
            url: '/chat',
            icons: [
              {
                src: '/pwa-192x192.png',
                sizes: '192x192',
                type: 'image/png',
              },
            ],
          },
          {
            name: 'Mapa',
            short_name: 'Mapa',
            description: 'Ver mapa',
            url: '/mapa',
            icons: [
              {
                src: '/pwa-192x192.png',
                sizes: '192x192',
                type: 'image/png',
              },
            ],
          },
        ],
      },
      devOptions: {
        enabled: false, // Deshabilitado en desarrollo para evitar conflictos
        navigateFallback: 'index.html',
        suppressWarnings: true,
        type: 'module',
      },
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
