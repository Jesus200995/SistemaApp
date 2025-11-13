# 🆘 Troubleshooting & Referencia Rápida

## 1. Problemas Comunes y Soluciones

### ❌ Problema: No veo sembradores en el mapa

#### Diagnosis:

1. **¿API está devolviendo datos?**
   ```javascript
   // DevTools Console:
   const token = localStorage.getItem('token')
   fetch('http://localhost:8000/sembradores/map', {
     headers: { 'Authorization': `Bearer ${token}` }
   }).then(r => r.json()).then(console.log)
   ```
   
   - Si ves `"detail": "No se encuentra recurso"` → Error en URL
   - Si ves `"detail": "No autorizado"` → Token inválido
   - Si ves datos vacíos → Usuario sin sembradores (correcto)

2. **¿Frontend está cargando?**
   ```javascript
   // DevTools Console:
   // Busca si getSembradoresMapa se ejecutó
   console.log(sembradores.value) // Vue DevTools
   ```

3. **¿Mostrar es true?**
   ```javascript
   // DevTools Console Vue:
   console.log(mostrarSembradores.value) // Debe ser true
   ```

#### Soluciones por síntoma:

| Síntoma | Causa Probable | Solución |
|---------|---------------|----------|
| Network error en API | Backend no corriendo | Inicia `python -m uvicorn...` |
| 401 Unauthorized | Token vencido o inválido | Re-login |
| 400 Bad Request | Error en BD | Ver logs backend |
| Response vacío | User sin sembradores | Crea sembradores en SembradoresView |
| Marcadores no aparecen | `mostrarSembradores = false` | Haz click checkbox |
| Popup en blanco | Error en datos | Ver Network Response |

---

### ❌ Problema: Veo solo algunos sembradores

**Causa probable**: Filtrado jerárquico funciona correctamente

**Verificación**:
```
¿Eres Técnico? → Solo ves tus sembradores ✓
¿Eres Facilitador? → Solo ves de tus técnicos ✓
¿Eres Territorial? → Solo ves subordinados directos ✓
¿Eres Admin? → Ves TODOS ✓
```

**Si no coincide con arriba**:
1. Verifica rol en BD: `SELECT rol FROM users WHERE id=X`
2. Verifica jerarquía: `SELECT superior_id FROM users WHERE id=X`
3. Verifica sembradores: `SELECT COUNT(*) FROM sembradores WHERE user_id=X`

---

### ❌ Problema: Checkbox no funciona

**Posibles causas**:

1. **Checkbox no clickeable**:
   ```css
   /* Verifica que no haya eventos bloqueados */
   .legend-checkbox {
     pointer-events: auto !important;
     cursor: pointer;
   }
   ```

2. **v-model no actualiza**:
   ```vue
   <!-- Asegúrate que existe en template -->
   <input v-model="mostrarSembradores" type="checkbox">
   
   <!-- Y en script -->
   const mostrarSembradores = ref(true)
   ```

3. **Filtrado no funciona**:
   ```vue
   <!-- Verifica el filtro -->
   v-for="s in sembradores.filter(sem => 
     mostrarSembradores && 
     sem.tecnico_rol?.toLowerCase().includes('productivo')
   )"
   ```

**Solución rápida**:
```javascript
// DevTools Console:
// Simula click
mostrarSembradores.value = false
mostrarSembradores.value = true
```

---

### ❌ Problema: Popups se ven extraños

**Síntoma**: Texto cortado, colores incorrectos, posición mala

**Soluciones**:

1. **Borrar cache del navegador**:
   ```
   Ctrl+Shift+Delete → Borrar cache → Recarga
   ```

2. **Revisar estilos CSS en DevTools**:
   ```
   Click popup → F12 → Elements → Busca .popup-sembrador
   Verifica: width, max-width, padding, colors
   ```

3. **Si popup está fuera de pantalla**:
   ```javascript
   // Leaflet centra automaticamente, pero si no:
   map.panTo([lat, lng])
   ```

---

### ❌ Problema: "Error cargando sembradores" en consola

**Pasos para debug**:

1. Abre DevTools: F12
2. Tab Console
3. Busca: "Error cargando sembradores"
4. Expande el error (click en triángulo)
5. Nota qué dice

| Error | Significado | Solución |
|-------|-------------|----------|
| `TypeError: Cannot read properties of undefined` | Datos llegan mal formados | Verifica response backend |
| `NetworkError: Failed to fetch` | Conexión rechazada | Backend no corriendo |
| `401 Unauthorized` | Token inválido | Re-login |
| `CORS error` | Configuración servidor | Agregar CORS headers |

---

### ❌ Problema: Marcadores en posición incorrecta

**Causa**: Coordenadas lat/lng invertidas

**Verificación**:
```javascript
// Leaflet espera [lat, lng]
// Verificar que backend devuelva en ese orden
{
  "lat": -33.8688,  // ✓ Correcto
  "lng": -51.2093   // ✓ Correcto
}

// En template:
<l-marker :lat-lng="[s.lat, s.lng]" /> <!-- ✓ Correcto -->
```

**Si está invertido**:
```vue
<!-- Cambiar a -->
<l-marker :lat-lng="[s.lng, s.lat]" /> <!-- ✗ MALO -->
```

---

### ❌ Problema: Token expira en mapa

**Síntoma**: Después de 30 minutos, marcadores desaparecen

**Solución**:
```typescript
// Agregar refresh automático
setInterval(() => {
  if (mostrarSembradores.value) {
    getSembradoresMapa()
  }
}, 5 * 60 * 1000) // Cada 5 minutos
```

---

### ❌ Problema: Mapa muy lento con muchos sembradores

**Síntoma**: Lag al zoom, pan lento, UI congelada

**Optimizaciones**:

1. **Implementar clustering**:
   ```bash
   npm install leaflet.markercluster
   ```

2. **Paginar datos**:
   ```typescript
   GET /sembradores/map?limit=50&offset=0
   // Cargar más con scroll
   ```

3. **Virtualizar markers**:
   - Solo renderizar visible en viewport
   - Eliminar fuera del rango

---

## 2. Referencia Rápida de Comandos

### Backend - Verificaciones

```bash
# ¿Backend corriendo?
netstat -an | findstr :8000

# ¿Endpoint existe?
curl -X GET http://localhost:8000/sembradores/map \
  -H "Authorization: Bearer YOUR_TOKEN"

# ¿Base de datos conectada?
# En python repl:
python -c "
from sqlalchemy import create_engine
engine = create_engine('postgresql://...')
print('Conexión OK' if engine.execute('SELECT 1') else 'Error')
"

# ¿Sembradores existen en BD?
# En psql:
SELECT COUNT(*) FROM sembradores;
SELECT * FROM sembradores LIMIT 5;
```

### Frontend - Verificaciones

```bash
# ¿Frontend corriendo?
netstat -an | findstr :5173

# ¿Dev server corriendo?
ps aux | grep vite

# ¿Compilar sin errores?
cd Frontend/sistemaapp-frontend
npm run build
```

### DevTools - Console Snippets

```javascript
// Ver todos los sembradores cargados
console.table(window.__VUE_APP__.sembradores)

// Ver estado del toggle
console.log('Mostrar:', mostrarSembradores.value)

// Refrescar datos manualmente
getSembradoresMapa()

// Ver número de marcadores en pantalla
console.log(document.querySelectorAll('.sembrador-marker').length)

// Simular click en checkbox
document.querySelector('.legend-checkbox input').click()
```

---

## 3. Checklist de Deployment

### Pre-Producción

- [ ] Backend endpoint `/sembradores/map` funciona
- [ ] Datos filtrados correctamente por rol
- [ ] Frontend carga datos sin errores
- [ ] Marcadores aparecen en posiciones correctas
- [ ] Popups muestran información completa
- [ ] Toggle checkbox funciona
- [ ] Mobile responsive
- [ ] Performance: < 500ms carga
- [ ] No hay console errors
- [ ] JWT validation funciona
- [ ] CORS configurado correctamente

### Database

- [ ] Índices en `sembradores.user_id`
- [ ] Índices en `users.superior_id`
- [ ] Datos de prueba migrados
- [ ] Jerarquía de usuarios correcta
- [ ] Backup antes de deploy

### Environment

- [ ] `VITE_API_URL` correcto
- [ ] Backend URL en producción
- [ ] JWT secret seguro
- [ ] CORS headers correctos
- [ ] HTTPS habilitado

---

## 4. Estado de Archivos

### Archivos Modificados ✏️

```
BackendFastAPI/routes/sembradores.py
  ✓ GET /sembradores/map endpoint agregado
  ✓ Filtrado jerárquico implementado
  ✓ Respuesta JSON estructurada

Frontend/sistemaapp-frontend/src/views/MapaView.vue
  ✓ Íconos SVG para sembradores
  ✓ Estados reactivos (sembradores, mostrarSembradores)
  ✓ Función getSembradoresMapa()
  ✓ Marcadores productivos y sociales
  ✓ Popups informativos
  ✓ Leyenda actualizada
  ✓ Estilos CSS para popups
```

### Archivos Documentación ✍️

```
MODULO_SEMBRADORES_EN_MAPA.md          → Este archivo
GUIA_TECNICA_SEMBRADORES_MAPA.md        → Guía técnica detallada
GUIA_TESTING_SEMBRADORES_MAPA.md        → Casos de testing
TROUBLESHOOTING_REFERENCIA_RAPIDA.md    → Soluciones (ESTE)
```

---

## 5. Escalabilidad Futura

### Optimizaciones Sugeridas

**Performance**:
- [ ] Agregar paginación: `?limit=50&offset=0`
- [ ] Implementar clustering para 100+ marcadores
- [ ] Caché con Redis
- [ ] Compresión gzip de response

**Funcionalidad**:
- [ ] Filtros adicionales: cultivo, comunidad, rango fechas
- [ ] Exportar mapa a PDF/PNG
- [ ] Geolocalización en tiempo real
- [ ] Rutas entre sembradores
- [ ] Heatmap de densidad

**Seguridad**:
- [ ] Rate limiting en endpoint
- [ ] Auditoría de accesos
- [ ] Encriptación de coordenadas

---

## 6. Logging & Monitoring

### Logs Backend

```python
# Agregar logging
import logging
logger = logging.getLogger(__name__)

@router.get("/map")
def obtener_sembradores_mapa(...):
    logger.info(f"Solicitando sembradores para user: {user_id}, rol: {rol}")
    try:
        # ...
        logger.debug(f"Retornando {len(items)} sembradores")
        return response
    except Exception as e:
        logger.error(f"Error en /map: {str(e)}")
        raise
```

### Logs Frontend

```typescript
const getSembradoresMapa = async () => {
  console.log('[MAPA] Cargando sembradores...')
  try {
    const response = await axios.get(...)
    console.log('[MAPA] Sembradores cargados:', response.data.total)
    sembradores.value = response.data.items
  } catch (error) {
    console.error('[MAPA] Error:', error.message)
  }
}
```

---

## 7. Contacto & Soporte

### Datos de Referencia

**Endpoint**: `/sembradores/map`
**Método**: GET
**Autenticación**: Bearer Token
**Archivo Backend**: `BackendFastAPI/routes/sembradores.py`
**Archivo Frontend**: `Frontend/sistemaapp-frontend/src/views/MapaView.vue`

### Información Técnica

- **Lenguaje Backend**: Python (FastAPI)
- **Lenguaje Frontend**: TypeScript (Vue 3)
- **Base Datos**: PostgreSQL
- **Mapa**: Leaflet.js
- **HTTP Client**: Axios
- **Estado**: Pinia

---

## 8. Versión & Changelog

**Versión**: 1.0.0
**Estado**: ✅ Producción
**Fecha**: 2024-01-15

### Cambios en v1.0.0

- ✅ Backend endpoint `/sembradores/map`
- ✅ Filtrado jerárquico implementado
- ✅ Frontend integración con markers
- ✅ Íconos SVG diferenciados
- ✅ Popups informativos
- ✅ Leyenda actualizada
- ✅ Toggle visibilidad
- ✅ Documentación completa

### Próxima versión (v1.1)

- [ ] Paginación de datos
- [ ] Clustering de marcadores
- [ ] Filtros adicionales
- [ ] Exportar mapa

---

## ✅ Quick Status Check

Antes de decir que funciona, verifica:

```bash
# 1. Backend
curl -s http://localhost:8000/sembradores/map \
  -H "Authorization: Bearer TEST_TOKEN" | jq .

# 2. Frontend (DevTools Console)
console.log('Sembradores:', sembradores.value.length)
console.log('Mostrar:', mostrarSembradores.value)
console.log('Contador:', contadorSembradores.value)

# 3. Visualización
- ¿Ves marcadores? YES/NO
- ¿Checkbox funciona? YES/NO
- ¿Popups abren? YES/NO
- ¿Sin errores de consola? YES/NO
```

**Si todo = YES**: ✅ FUNCIONA CORRECTAMENTE

---

