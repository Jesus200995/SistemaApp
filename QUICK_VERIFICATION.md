# 🔍 Verificación Rápida - Módulo Estadísticas

## ✅ Checklist de Verificación en 5 Minutos

### Paso 1: Verificar Backend (1 min)

```bash
# En la carpeta BackendFastAPI, verifica que el endpoint existe:
grep -n "def obtener_estadisticas" routes/seguimientos.py
# Deberías ver la línea ~451

# Prueba el endpoint (necesitas token):
curl -X GET http://localhost:8000/seguimientos/stats \
  -H "Authorization: Bearer tu_token_aqui"
```

**Esperado**: JSON con total_sembradores, total_seguimientos, promedio_avance, cultivos

---

### Paso 2: Verificar Frontend (2 min)

```bash
# En la carpeta Frontend/sistemaapp-frontend:

# Verifica que el archivo existe
ls -la src/views/EstadisticasView.vue
# Deberías ver el archivo (~850 líneas)

# Verifica que tiene las secciones principales
grep "stat-card\|chart-section\|table-section\|summary-section" src/views/EstadisticasView.vue | wc -l
# Deberías ver 4+ resultados
```

**Esperado**: Archivo existe y contiene todas las secciones

---

### Paso 3: Verificar Ruta (1 min)

```bash
# Verifica la ruta en router/index.ts
grep -n "estadisticas" src/router/index.ts
# Deberías ver:
# - path: '/estadisticas'
# - component: EstadisticasView
# - requiresAuth: true
```

**Esperado**: Ruta registrada correctamente

---

### Paso 4: Verificar Dashboard (1 min)

```bash
# Verifica el botón en Dashboard
grep -n "Reportes y Estadísticas\|/estadisticas" src/views/DashboardView.vue
# Deberías ver 3+ menciones
```

**Esperado**: Botón existe y enlaza a /estadisticas

---

## 🚀 Prueba Manual en Navegador

### Flujo de Prueba Completo (3 min)

1. **Inicia sesión**
   - URL: `http://localhost:3000/login`
   - Usuario: Tu admin / facilitador / territorial
   - Contraseña: Tu contraseña

2. **Navega al Dashboard**
   - URL: `http://localhost:3000/dashboard`
   - Verifica que ves el botón "📊 Reportes y Estadísticas"

3. **Haz clic en el botón**
   - Deberías ir a `/estadisticas`
   - Espera a que carguen los datos (< 1 segundo)

4. **Verifica los componentes**
   ```
   ☐ Header: "📊 Reportes y Estadísticas"
   ☐ 3 Tarjetas KPI con números
   ☐ Gráfico de barras (Chart.js)
   ☐ Tabla con cultivos
   ☐ Resumen general
   ☐ Footer
   ```

5. **Prueba interactividad**
   ```
   ☐ Pasa mouse sobre tarjetas (hover effect)
   ☐ Pasa mouse sobre gráfico (tooltip)
   ☐ Pasa mouse sobre tabla (fondo verde)
   ☐ Haz scroll (todo debe funcionar)
   ```

6. **Verifica responsive**
   ```
   ☐ Press F12 (DevTools)
   ☐ Selecciona "Toggle Device Toolbar"
   ☐ Prueba en Mobile (375px)
   ☐ Todo debe verse bien
   ```

---

## 🔐 Prueba de Seguridad (RBAC)

### Test 1: Admin ve todo
```
1. Login como admin
2. Ve /estadisticas
3. Verifica: TODOS los sembradores del sistema
```

### Test 2: Técnico bloqueado
```
1. Login como técnico
2. Ve /estadisticas directamente en URL
3. Espera: Redirección a login o error 401
```

### Test 3: Botón visible solo para roles correctos
```
1. Inicia como técnico
2. Ve a /dashboard
3. Busca botón "Reportes y Estadísticas"
4. Resultado: NO DEBE ESTAR VISIBLE
```

---

## 📊 Validación de Datos

### Backend JSON Response

```bash
# La respuesta del backend debería ser:
{
  "total_sembradores": <número>,
  "total_seguimientos": <número>,
  "promedio_avance": <0-100>,
  "cultivos": {
    "Maíz": <número>,
    "Frijol": <número>,
    ...
  }
}
```

**Verificación**:
```bash
curl -X GET http://localhost:8000/seguimientos/stats \
  -H "Authorization: Bearer token" | jq .

# Deberías ver JSON válido sin errores
```

---

### Frontend Data Binding

**En DevTools (Network tab)**:
1. Abre `/estadisticas`
2. Ve a Network
3. Busca request a `/seguimientos/stats`
4. Verifica:
   - Status: 200 ✅
   - Response: JSON válido ✅
   - Headers: Authorization presente ✅

**En DevTools (Console)**:
```javascript
// En la consola puedes inspeccionar:
// El store de auth
JSON.stringify(useAuthStore())

// Los datos cargados
// (Verifica que no hay errores de red)
```

---

## 🎨 Validación Visual

### Colores
```
✓ Fondo oscuro (#0f172a)
✓ Tarjetas con glassmorphism
✓ Acento verde (#10b981)
✓ Texto claro (#f1f5f9)
✓ Bordes suaves
```

### Animaciones
```
✓ Entrada fade + slide suave
✓ Hover effects en tarjetas
✓ Hover effects en tabla
✓ Smooth transitions (300ms)
✓ Blobs de fondo flotantes (opcional)
```

### Tipografía
```
✓ Título grande y legible
✓ Subtítulos con contraste
✓ Números destacados
✓ Labels pequeños
✓ Monoespaciado en números
```

---

## 🧪 Teste Automáticos (Opcional)

### Frontend Tests

```bash
# Si existe configuración Vitest/Jest:
npm run test

# Deberías ver tests pasar para EstadisticasView
```

### Backend Tests

```bash
# Si existe pytest:
pytest tests/test_seguimientos.py::test_stats_endpoint

# Deberías ver tests pasar
```

---

## ⚡ Performance Check

### Network Performance
```
1. Abre DevTools → Network
2. Recarga /estadisticas
3. Verifica:
   - HTML: < 100ms
   - JS: < 500ms
   - CSS: < 100ms
   - Data (/stats): < 500ms
   - Total: < 1.5s
```

### Memory Usage
```
1. DevTools → Memory
2. Toma snapshot inicial
3. Interactúa con página
4. Toma snapshot final
5. Verifica: No hay leaks (< +50MB)
```

### Chart.js Performance
```
1. DevTools → Performance
2. Graba mientras entra a /estadisticas
3. Verifica:
   - FCP < 1s
   - LCP < 2s
   - CLS < 0.1
```

---

## 📱 Breakpoints Responsive

### Desktop (1920px)
```
✓ 3 tarjetas en una fila
✓ Gráfico ancho (800px)
✓ Tabla con todas las columnas
✓ Resumen en 4 columnas
```

### Tablet (768px)
```
✓ 1-2 tarjetas por fila
✓ Gráfico mediano (400px)
✓ Tabla scrolleable
✓ Resumen en 2 columnas
```

### Mobile (375px)
```
✓ 1 tarjeta por fila
✓ Gráfico pequeño (300px)
✓ Tabla horizontal scrolleable
✓ Resumen en 1 columna
✓ Botones táctiles grandes
```

---

## 🐛 Debug Rápido

### Si no ves datos

```javascript
// En consola, ejecuta:
const response = await fetch('/seguimientos/stats', {
  headers: {'Authorization': 'Bearer ' + localStorage.getItem('token')}
});
console.log(await response.json());
```

### Si la ruta no funciona

```javascript
// Verifica el router
import router from '@/router';
console.log(router.getRoutes());
// Busca path: 'estadisticas'
```

### Si el gráfico no renderiza

```javascript
// Verifica Chart.js
console.log(window.Chart);
// Debería mostrar la clase ChartJS
```

---

## 📋 Checklist Final

```
FUNCIONALIDAD:
☐ Endpoint /stats responde
☐ Datos JSON válidos
☐ Frontend carga datos
☐ Gráfico renderiza
☐ Tabla muestra cultivos
☐ Números correctos

SEGURIDAD:
☐ Admin ve todo
☐ Territorial filtrado
☐ Facilitador filtrado
☐ Técnico bloqueado

DISEÑO:
☐ Colores correctos
☐ Responsive funciona
☐ Animaciones suaves
☐ Tipografía legible

PERFORMANCE:
☐ Carga < 2s
☐ Sin errores console
☐ Sin memory leaks
☐ Scroll suave

NAVEGACIÓN:
☐ Router funciona
☐ Botón en Dashboard
☐ Breadcrumb correcto
☐ Links funcionales

DOCUMENTACIÓN:
☐ Guía técnica presente
☐ Guía usuario presente
☐ Guía pruebas presente
☐ Este checklist presente
```

---

## 🎉 ¡Listo!

Si todo el checklist está completo ✅, el módulo está **listo para producción**.

**Próximos pasos**:
1. Deploy a staging para QA
2. Pruebas de usuario final
3. Deploy a producción
4. Monitoreo 24/7

---

**Tiempo estimado de verificación**: 5-10 minutos
**Última actualización**: 2025
**Versión**: 1.0.0
