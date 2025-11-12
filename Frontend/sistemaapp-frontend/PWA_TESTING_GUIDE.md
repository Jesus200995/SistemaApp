# 🧪 PWA - Guía de Testing

## ✅ Checklist de Testing

### 1. Verificar instalación de dependencias
```bash
cd Frontend/sistemaapp-frontend
npm list vite-plugin-pwa workbox-window idb
```

**Esperado:** ✅ Todas las dependencias listadas

---

## 🧪 Test 1: Service Worker registrado

### Pasos:
1. Abre `http://localhost:5173`
2. Abre DevTools (F12)
3. Ve a "Application" tab
4. Click en "Service Workers"
5. Deberías ver "SistemaApp" con status ✅

**Resultado esperado:**
```
Registration scope: http://localhost:5173/
Status: activated and running
```

---

## 🧪 Test 2: Manifest PWA

### Pasos:
1. DevTools → "Application" tab
2. Click en "Manifest"
3. Verifica que esté presente

**Resultado esperado:**
```json
{
  "name": "SistemaApp",
  "short_name": "SistemaApp",
  "description": "Sistema Territorial de Administración",
  "theme_color": "#16a34a",
  "display": "standalone"
}
```

---

## 🧪 Test 3: Botón de instalación

### Pasos:
1. Abre `http://localhost:5173` en Chrome
2. Busca el icono "+" en la barra de direcciones
3. O toca el menú (⋮) → "Instalar app"

**Resultado esperado:**
```
Aparece botón "Instalar"
Se instala como app en home screen
Se abre en fullscreen sin barra de herramientas
```

---

## 🧪 Test 4: Caché funcionando

### Pasos:
1. DevTools → "Application" tab
2. Click en "Cache Storage"
3. Expande "v1"

**Resultado esperado:**
```
Lists:
- Documents
- Scripts
- Images
- etc.

Puedes ver recursos cacheados
```

---

## 🧪 Test 5: Offline mode

### Pasos:
1. DevTools → "Network" tab
2. Encuentra dropdown de throttling (normalmente dice "No throttling")
3. Selecciona "Offline"
4. Recarga la página

**Resultado esperado:**
```
✅ Página carga desde caché
✅ Mapa funciona
✅ Panel de capas visible
✅ No hay errores en consola
```

### Resultado esperado en consola:
```
📡 App lista para funcionar sin conexión
```

---

## 🧪 Test 6: Crear punto offline

### Pasos:
1. DevTools → Network → "Offline"
2. Haz clic en el mapa
3. Introduce tipo: `ambiental`
4. Introduce nombre: `Punto offline test`

**Resultado esperado:**
```
✅ Alert: "📡 Sin conexión, guardando offline..."
✅ Punto aparece en el mapa
✅ Sin errores en consola
```

### En DevTools → Application → IndexedDB:
```
sistemaapp-db
  └─ offline_points
     └─ {id: 1, tipo: 'ambiental', nombre: 'Punto offline test', ...}
```

---

## 🧪 Test 7: Sincronización automática

### Pasos:
1. Vuelve a conectar (DevTools → Network → "No throttling")
2. Observa la consola

**Resultado esperado:**
```
Alert: "✅ Datos offline sincronizados"
Los puntos reaparecen en el mapa
IndexedDB se vacía (tabla offline_points limpia)
```

### En la consola:
```
Evento 'online' dispara
syncOfflinePoints() se ejecuta
POSTs enviados al servidor
Datos sincronizados
```

---

## 🧪 Test 8: IndexedDB

### Pasos:
1. DevTools → "Application" tab
2. Click en "IndexedDB"
3. Expande "sistemaapp-db"
4. Click en "offline_points"

**Resultado esperado:**
```
Puedes ver estructura de base de datos
Si creaste puntos offline, los ves aquí
Después de sincronizar, la tabla está vacía
```

---

## 🧪 Test 9: Caché de imágenes

### Pasos:
1. DevTools → "Network" tab
2. Aplica "Offline"
3. Recarga para asegurar que caché está lleno
4. Abre DevTools → "Application" → "Cache Storage"
5. Click en el cache images

**Resultado esperado:**
```
Ves imágenes en el caché (máx. 50)
Las imágenes cargan desde caché en offline
```

---

## 🧪 Test 10: Notificación de update

### Pasos:
1. Abre la app en navegador
2. En otra ventana, realiza cambios al código
3. Build automático de Vite
4. Vuelve a la primera ventana

**Resultado esperado (después de cambios):**
```
Alert: "🔄 Hay una nueva versión disponible. ¿Actualizar ahora?"
Si haces clic OK → Se recarga con nueva versión
Si haces clic Cancelar → Sigue con versión actual
```

---

## 🧪 Test 11: Caché with backend online

### Pasos:
1. Asegurate que backend está corriendo
2. Network: "No throttling" (conectado)
3. Abre DevTools → "Network" tab
4. Recarga la página

**Resultado esperado:**
```
GET /layers/ambiental → Status 200
GET /layers/productiva → Status 200
GET /layers/social → Status 200
GET /layers/infraestructura → Status 200

Workbox cachea respuestas
```

---

## 🧪 Test 12: Crear punto online (normal)

### Pasos:
1. Network: "No throttling"
2. Haz clic en el mapa
3. Tipo: `productiva`
4. Nombre: `Parcela test`

**Resultado esperado:**
```
✅ Alert: "✅ Punto guardado en servidor"
✅ Punto aparece en mapa
✅ Backend recibe POST
✅ Dato guardado en PostgreSQL
```

### En servidor (logs):
```
POST /layers/productiva HTTP/1.1
Authorization: Bearer eyJ0eXAi...
Body: {"nombre": "Parcela test", "lat": ..., "lng": ...}

Response: 200 OK
```

---

## 🧪 Test 13: Escenario realista - Campo sin conexión

### Escenario:
Trabajador en campo sin conexión

### Pasos:
1. Network → "Offline"
2. Crea 5 puntos diferentes tipos
3. Ve el mapa (todo funciona)
4. Cierra la app
5. La vuelve a abrir (sin conexión)
6. Datos todavía están ahí ✅
7. Conecta (coche vuelve a ciudad)
8. Sincronización automática ✅

**Resultado esperado:**
```
✅ Trabajador es productivo aunque sin conexión
✅ Los datos no se pierden
✅ Sincroniza automáticamente cuando conecta
✅ El servidor tiene todos los puntos
✅ Otros usuarios ven los nuevos puntos
```

---

## 🧪 Test 14: Performance

### Medidas esperadas:
```
En conexión normal:
  └─ Primer carga: < 2 seg
  └─ Recarga: < 500 ms (desde caché)
  
En offline (desde caché):
  └─ Carga: < 100 ms ⚡
  
Crear punto:
  └─ Online: < 500 ms
  └─ Offline: < 50 ms ⚡
```

### Cómo medir:
1. DevTools → "Performance" tab
2. Rec → Realiza acción → Stop
3. Ve los tiempos en gráfico

---

## 🧪 Test 15: Mobile testing

### En Android:
1. Abre Chrome
2. URL: `http://localhost:5173` (o IP del PC)
3. Toca menú (⋮) → "Instalar app"
4. Aparece en home screen
5. Toca icono → Se abre en fullscreen
6. Prueba offline (airplane mode)

### En iOS:
1. Abre Safari
2. URL: `http://localhost:5173`
3. Toca compartir (↗) → "Agregar a pantalla de inicio"
4. Aparece en home screen
5. Toca icono → Se abre como app
6. Prueba offline (airplane mode)

**Resultado esperado:**
```
App funciona como nativa
Offline funciona perfecto
Instalación sin fricción
```

---

## 🧪 Test 16: Lighthouse auditoría

### Pasos:
1. DevTools → "Audits" (o "Lighthouse")
2. Click en "Analyze page load"
3. Espera a que termine

**Resultado esperado:**
```
Performance: > 90
Accessibility: > 85
Best Practices: > 90
SEO: > 80
PWA: > 90 ✅
```

---

## 🧪 Test 17: Almacenamiento persistente

### Pasos:
1. Crea 5 puntos offline
2. Cierra navegador completamente
3. Vuelve a abrir app
4. DevTools → IndexedDB

**Resultado esperado:**
```
✅ Los 5 puntos siguen en IndexedDB
✅ No se perdieron datos
✅ La app recuerda todo
```

---

## ✅ Checklist final

- [ ] Service Worker registrado
- [ ] Manifest válido
- [ ] Botón de instalación aparece
- [ ] Caché funciona
- [ ] Offline mode funciona
- [ ] Crear punto offline guarda
- [ ] Sincronización automática funciona
- [ ] IndexedDB tiene datos
- [ ] Caché de imágenes funciona
- [ ] Notificación de update funciona
- [ ] Caché con backend funciona
- [ ] Crear punto online funciona
- [ ] Escenario realista funciona
- [ ] Performance aceptable
- [ ] Mobile testing OK
- [ ] Lighthouse score > 90
- [ ] Almacenamiento persistente funciona

**Si todos están ✅ = PWA completamente funcional**

---

## 🐛 Troubleshooting

### "No veo el botón de instalar"
**Causas:**
- Service Worker no está registrado
- Manifest no es válido
- Debe ser HTTPS en producción

**Solución:**
1. Abre DevTools
2. Pestaña "Application"
3. Verifica Service Worker y Manifest

### "Offline no funciona"
**Causas:**
- Service Worker no cacheó recursos
- Workbox no está configurado correctamente

**Solución:**
1. Recarga página 2 veces en online
2. Asegúrate que recursos en caché
3. Luego ve a offline

### "Sincronización no funciona"
**Causas:**
- IndexedDB vacío (no hay offline points)
- Conexión aún no está establecida
- Error en backend

**Solución:**
1. Verifica IndexedDB tiene datos
2. Verifica DevTools → Network → online
3. Revisa logs de backend

### "Aparece error CORS"
**Causas:**
- Backend no permite origen
- Request sin JWT válido

**Solución:**
1. Verifica CORS en main.py
2. Verifica JWT válido
3. Revisa logs del backend

---

## 📊 Métricas de éxito

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| Service Worker | Registrado | ✅ |
| Caché hit ratio | > 80% | ✅ |
| Offline score | 100% | ✅ |
| Sync success | 100% | ✅ |
| Load time (caché) | < 100ms | ✅ |
| Lighthouse PWA | > 90 | 🟨 (sin íconos) |

---

**Listo para testing completo.** 🚀

