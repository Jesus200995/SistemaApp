/// <reference lib="webworker" />
declare const self: ServiceWorkerGlobalScope;

import { cleanupOutdatedCaches, precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

// Precache archivos generados por Vite PWA
precacheAndRoute(self.__WB_MANIFEST);

// Limpiar cachés antiguos
cleanupOutdatedCaches();

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

// 4. API requests: Network First con timeout
registerRoute(
  ({ url }) => url.origin === self.location.origin && url.pathname.startsWith('/api'),
  new NetworkFirst({
    cacheName: 'api-cache',
    networkTimeoutSeconds: 5,
    plugins: [
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 24 * 60 * 60, // 1 día
      }),
    ],
  })
);

// 5. WebSocket fallback (no se cachea)
registerRoute(
  ({ url }) => url.pathname.startsWith('/notificaciones') || url.pathname.startsWith('/chat'),
  new NetworkFirst({
    cacheName: 'realtime-cache',
    networkTimeoutSeconds: 2,
  })
);

// ========== EVENTOS DEL SERVICE WORKER ==========

// Activación del Service Worker
self.addEventListener('activate', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== 'pages-cache' && cacheName !== 'static-resources' && 
              cacheName !== 'images-cache' && cacheName !== 'api-cache' && 
              cacheName !== 'realtime-cache') {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Mensaje desde el cliente
self.addEventListener('message', (event: ExtendableMessageEvent) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  // Sincronización de notificaciones
  if (event.data && event.data.type === 'SYNC_NOTIFICATIONS') {
    event.waitUntil(syncNotifications());
  }

  // Limpiar caché
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => caches.delete(cacheName))
        );
      })
    );
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
    console.error('Error sincronizando notificaciones:', error);
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
