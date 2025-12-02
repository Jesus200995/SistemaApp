import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    VitePWA({
      registerType: 'prompt',
      injectRegister: 'auto',
      includeAssets: ['favicon.ico', 'robots.txt', 'pwa-192x192.png', 'pwa-512x512.png'],
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,jpg,jpeg,gif,svg,woff,woff2,ttf,eot}'],
        cleanupOutdatedCaches: true,
        sourcemap: false,
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/sistemaapi\.sembrandodatos\.com\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              networkTimeoutSeconds: 10,
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24, // 1 día
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp|ico)$/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'images-cache',
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 * 24 * 7, // 7 días
              },
            },
          },
          {
            urlPattern: /\.(?:js|css)$/i,
            handler: 'StaleWhileRevalidate',
            options: {
              cacheName: 'static-resources',
            },
          },
        ],
        skipWaiting: true,
        clientsClaim: true,
      },
      manifest: {
        name: 'SistemaApp - Panel de Control',
        short_name: 'SistemaApp',
        description: 'Sistema Territorial de Administración',
        theme_color: '#10b981',
        background_color: '#0f172a',
        display: 'standalone',
        scope: '/',
        start_url: '/',
        orientation: 'portrait-primary',
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
      },
      devOptions: {
        enabled: false,
      },
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
