/// <reference lib="webworker" />
declare const self: ServiceWorkerGlobalScope;

import { cleanupOutdatedCaches, precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, NetworkOnly, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

// Versión del SW para detectar cambios
const SW_VERSION = 'v2.0.' + Date.now();

// Precache archivos generados por Vite PWA
precacheAndRoute(self.__WB_MANIFEST);

// Limpiar cachés antiguos
cleanupOutdatedCaches();

// ========== DETECCIÓN DE ACTUALIZACIONES ==========

// Verificar actualizaciones cada 30 segundos
setInterval(() => {
  self.registration.update();
}, 30000);

// ========== ESTRATEGIAS DE CACHÉ ==========

// 1. Documentos HTML: Network First (intentar red primero)
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({
    cacheName: 'pages-cache',
    networkTimeoutSeconds: 3,
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// 2. Scripts y estilos: Stale While Revalidate
registerRoute(
  ({ request }) => request.destination === 'script' || request.destination === 'style',
  new StaleWhileRevalidate({
    cacheName: 'static-resources',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// 3. Imágenes: Cache First
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images-cache',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 7 * 24 * 60 * 60, // 7 días
      }),
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// 4. API requests: NETWORK ONLY - NUNCA CACHEAR datos de la API
registerRoute(
  ({ url }) => url.pathname.startsWith('/api') || 
               url.pathname.startsWith('/solicitudes') ||
               url.pathname.startsWith('/usuarios') ||
               url.pathname.startsWith('/auth') ||
               url.pathname.startsWith('/notificaciones') ||
               url.pathname.startsWith('/sembradores') ||
               url.pathname.startsWith('/seguimientos'),
  new NetworkOnly()
);

// 5. Cualquier otra llamada a API externa: Network Only
registerRoute(
  ({ url }) => url.origin !== self.location.origin && 
               (url.pathname.includes('/api') || url.pathname.includes('/solicitudes')),
  new NetworkOnly()
);

// ========== EVENTOS DEL SERVICE WORKER ==========

// Activación del Service Worker
self.addEventListener('activate', (event: ExtendableEvent) => {
  console.log('[SW] Activando Service Worker:', SW_VERSION);
  
  event.waitUntil(
    Promise.all([
      // LIMPIAR TODOS LOS CACHÉS al activar nueva versión
      caches.keys().then((cacheNames) => {
        console.log('[SW] Limpiando TODOS los cachés:', cacheNames);
        return Promise.all(
          cacheNames.map((cacheName) => {
            console.log('[SW] Eliminando caché:', cacheName);
            return caches.delete(cacheName);
          })
        );
      }),
      // Notificar a todos los clientes sobre la activación
      self.clients.matchAll({ type: 'window' }).then((clients) => {
        clients.forEach((client) => {
          client.postMessage({
            type: 'SW_ACTIVATED',
            version: SW_VERSION,
          });
        });
      }),
    ])
  );
  
  // Tomar control de todas las páginas inmediatamente
  self.clients.claim();
});

// Instalación del Service Worker
self.addEventListener('install', (event: ExtendableEvent) => {
  console.log('[SW] Instalando Service Worker:', SW_VERSION);
  
  // Forzar que se convierta en activo inmediatamente - NO ESPERAR
  self.skipWaiting();
  
  event.waitUntil(
    // Limpiar cachés antiguos durante la instalación también
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => caches.delete(cacheName))
      );
    })
  );
});

// Actualización del registro del Service Worker
self.addEventListener('controllerchange', () => {
  console.log('[SW] Nuevo Service Worker tomó control');
});

// Mensaje desde el cliente
self.addEventListener('message', (event: ExtendableMessageEvent) => {
  console.log('[SW] Mensaje recibido:', event.data?.type);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('[SW] SKIP_WAITING ejecutado');
    self.skipWaiting();
  }

  // Sincronización de notificaciones
  if (event.data && event.data.type === 'SYNC_NOTIFICATIONS') {
    event.waitUntil(syncNotifications());
  }

  // Limpiar caché
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    console.log('[SW] Limpiando todo el caché');
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => caches.delete(cacheName))
        );
      })
    );
  }

  // Forzar actualización
  if (event.data && event.data.type === 'FORCE_UPDATE') {
    console.log('[SW] Fuerza de actualización activada');
    self.registration.update();
  }
});

// Sincronización de notificaciones en background
async function syncNotifications() {
  try {
    const response = await fetch('/notificaciones/');
    if (response.ok) {
      const notifications = await response.json();
      // Mostrar notificaciones de escritorio
      notifications.forEach((notification: any) => {
        self.registration.showNotification(notification.titulo, {
          body: notification.mensaje,
          icon: '/pwa-192x192.png',
          tag: `notification-${notification.id}`,
          data: {
            url: '/',
            id: notification.id,
          },
        });
      });
    }
  } catch (error) {
    console.error('[SW] Error sincronizando notificaciones:', error);
  }
}

// Notificaciones push
self.addEventListener('push', (event: PushEvent) => {
  const data = event.data?.json() || {};
  
  self.registration.showNotification(data.titulo || 'Nueva notificación', {
    body: data.mensaje || 'Tienes una nueva notificación',
    icon: '/pwa-192x192.png',
    badge: '/pwa-192x192.png',
    tag: `push-${Date.now()}`,
    data: {
      url: data.url || '/',
      id: data.id,
    },
  });
});

// Click en notificación
self.addEventListener('notificationclick', (event: NotificationEvent) => {
  event.notification.close();
  
  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then((clientList: readonly WindowClient[]) => {
      // Si hay una ventana abierta, enfocarse en ella
      for (let client of clientList) {
        if (client.url === event.notification.data.url && 'focus' in client) {
          return client.focus();
        }
      }
      // Si no hay ventana, abrir una nueva
      if (self.clients.openWindow) {
        return self.clients.openWindow(event.notification.data.url);
      }
    })
  );
});

export {};
