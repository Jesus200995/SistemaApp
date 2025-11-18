# 🧪 Guía de Prueba - Módulo Estadísticas

## Pruebas Funcionales

### Test 1: Acceso al Módulo desde Dashboard

**Escenario**: Usuario Admin accediendo a estadísticas
```
1. Inicia sesión con usuario admin
2. Navega al Dashboard (/dashboard)
3. En la sección "Módulos Especializados", busca el botón "📊 Reportes y Estadísticas"
4. Haz clic en el botón
5. Espera a que cargue la vista
```

**Resultado Esperado**:
- ✅ El botón es visible
- ✅ La ruta cambia a `/estadisticas`
- ✅ Se carga EstadisticasView.vue
- ✅ Se hace una petición GET a `/seguimientos/stats`
- ✅ Los datos se renderizan correctamente

---

### Test 2: Visualización de Tarjetas KPI

**Escenario**: Ver las 3 tarjetas principales

```
En la vista de estadísticas, verifica:
1. Tarjeta 1: Total Sembradores 🌱
2. Tarjeta 2: Seguimientos Realizados 📋
3. Tarjeta 3: Promedio de Avance 📈
```

**Resultado Esperado**:
- ✅ 3 tarjetas visibles con números
- ✅ Gradientes de colores diferentes (verde, azul, naranja)
- ✅ Badges informativos en cada tarjeta
- ✅ Barra de progreso en la tercera tarjeta
- ✅ Hover effects suaves

---

### Test 3: Gráfico de Barras

**Escenario**: Visualizar distribución de cultivos

```
1. Desplázate hasta la sección "Distribución de Cultivos 🌾"
2. Observa el gráfico de barras
3. Pasa el mouse sobre las barras
```

**Resultado Esperado**:
- ✅ Gráfico Chart.js renderizado
- ✅ Barras de colores diferentes
- ✅ Tooltip al pasar mouse
- ✅ Eje Y con números
- ✅ Eje X con nombres de cultivos
- ✅ Responsive: se ajusta al tamaño de pantalla

---

### Test 4: Tabla de Cultivos

**Escenario**: Ver desglose detallado de cultivos

```
1. Sigue hacia la sección "Detalle por Cultivo"
2. Verifica las columnas: Tipo, Cantidad, Porcentaje, Barra Visual
3. Interactúa con las filas
```

**Resultado Esperado**:
- ✅ Tabla completa visible
- ✅ 4 columnas con headers
- ✅ Filas con datos de cultivos
- ✅ Badges de cantidad (azul)
- ✅ Barras visuales con progreso
- ✅ Hover effect en filas (fondo verde)
- ✅ Datos ordenados de mayor a menor cantidad

---

### Test 5: Resumen General

**Escenario**: Ver información resumen

```
1. Desplázate hasta "Resumen General"
2. Lee los 4 items informativos
```

**Resultado Esperado**:
- ✅ Fondo con gradiente verde
- ✅ 4 items con iconos (📊, 📋, 🌾, 📈)
- ✅ Texto descriptivo con valores destacados
- ✅ Layout responsive (grid 1-4 columnas según pantalla)

---

## Pruebas de Seguridad (RBAC)

### Test 6: Admin ve todo

**Usuario**: `admin`

```
1. Inicia sesión como admin
2. Accede a /estadisticas
3. Verifica que ves TODOS los datos del sistema
```

**Resultado Esperado**:
- ✅ Total sembradores = suma de todos
- ✅ Seguimientos = todos los registros
- ✅ Cultivos = todos los tipos del sistema

---

### Test 7: Territorial ve subordinados

**Usuario**: `territorial` (o similar)

```
1. Inicia sesión como territorial
2. Accede a /estadisticas
3. Verifica que ves datos de tu territorio
```

**Resultado Esperado**:
- ✅ Datos filtrados por territorio
- ✅ Solo subordinados visibles
- ✅ Números menores que admin

---

### Test 8: Facilitador ve técnicos asignados

**Usuario**: `facilitador`

```
1. Inicia sesión como facilitador
2. Accede a /estadisticas
3. Verifica que ves datos de tus técnicos
```

**Resultado Esperado**:
- ✅ Datos filtrados por técnicos asignados
- ✅ Solo sus sembradores visibles
- ✅ Seguimientos de sus técnicos

---

### Test 9: Técnico NO ve botón

**Usuario**: `tecnico`

```
1. Inicia sesión como técnico
2. Navega al Dashboard
3. Busca el botón "📊 Reportes y Estadísticas"
```

**Resultado Esperado**:
- ❌ Botón NO visible en Dashboard
- ✅ O si accede directamente a /estadisticas, recibe error 401
- ✅ Es redirigido a login

---

## Pruebas de Responsividad

### Test 10: Desktop (1200px+)

```
1. Abre el navegador en 1200px o más
2. Navega a /estadisticas
3. Observa el layout
```

**Resultado Esperado**:
- ✅ 3 tarjetas en fila
- ✅ Gráfico grande (altura 400px)
- ✅ Tabla con todas las columnas
- ✅ Resumen en 4 columnas

---

### Test 11: Tablet (768px)

```
1. Abre DevTools
2. Selecciona viewport tablet
3. Recarga la página
```

**Resultado Esperado**:
- ✅ 1-2 tarjetas por fila
- ✅ Gráfico mediano (altura 300px)
- ✅ Tabla scrollable horizontalmente
- ✅ Resumen en 1-2 columnas

---

### Test 12: Mobile (480px)

```
1. Selecciona viewport mobile
2. Recarga la página
3. Verifica todos los elementos
```

**Resultado Esperado**:
- ✅ 1 tarjeta por fila
- ✅ Tarjetas en layout vertical
- ✅ Gráfico pequeño (altura 250px)
- ✅ Tabla en vista comprimida
- ✅ Resumen en 1 columna
- ✅ Todo scrolleable verticalmente

---

## Pruebas de Performance

### Test 13: Tiempo de Carga

```
1. Abre DevTools (Pestaña Network)
2. Recarga la página de estadísticas
3. Observa el tiempo de carga
```

**Resultado Esperado**:
- ✅ Primera pintura < 500ms
- ✅ Chart.js renderiza < 200ms
- ✅ Tabla renderiza < 100ms

---

### Test 14: Sin Datos

```
1. Crea un usuario nuevo sin sembradores
2. Inicia sesión
3. Accede a /estadisticas
```

**Resultado Esperado**:
- ✅ Valores muestran 0 en tarjetas
- ✅ Gráfico muestra "No hay datos suficientes"
- ✅ Tabla muestra "Sin datos de cultivos"
- ✅ No hay errores en consola

---

## Pruebas de Animaciones

### Test 15: Entrada de Elementos

```
1. Abre la página de estadísticas
2. Observa la entrada de elementos
```

**Resultado Esperado**:
- ✅ Tarjetas entran con fade + slide (opacity + transform)
- ✅ Cada elemento con delay escalonado
- ✅ Animaciones suaves (duración ~600ms)

---

### Test 16: Hover Effects

```
1. En Desktop, pasa el mouse sobre:
   - Tarjetas KPI
   - Filas de tabla
   - Botones (si aplica)
2. Observa los efectos
```

**Resultado Esperado**:
- ✅ Tarjetas: translateY(-4px) + sombra
- ✅ Tarjetas: border-color cambia a verde
- ✅ Tabla: fondo verde suave
- ✅ Transiciones smooth (300ms)

---

## Pruebas de Integraciones

### Test 17: Conexión Backend

```
1. Abre DevTools (Network tab)
2. Accede a /estadisticas
3. Busca la request GET /seguimientos/stats
```

**Resultado Esperado**:
- ✅ Request enviada con Authorization header
- ✅ Response status 200
- ✅ JSON response contiene: total_sembradores, total_seguimientos, promedio_avance, cultivos
- ✅ Tiempo de respuesta < 500ms

---

### Test 18: Manejo de Errores

```
1. Desconecta el Backend
2. Recarga /estadisticas
3. Observa el comportamiento
```

**Resultado Esperado**:
- ✅ Error se captura en try-catch
- ✅ No crash de la aplicación
- ✅ Mensaje de error en consola
- ✅ UI muestra estado vacío

---

### Test 19: Token Expirado

```
1. Inicia sesión
2. Espera a que expire el token (o simula)
3. Accede a /estadisticas
```

**Resultado Esperado**:
- ✅ Error 401 desde backend
- ✅ Redirige a login
- ✅ Mensaje de sesión expirada

---

## Pruebas de Navegación

### Test 20: Links Funcionales

```
1. En la vista de estadísticas
2. Usa breadcrumb/navbar para navegar
3. Vuelve a /estadisticas
```

**Resultado Esperado**:
- ✅ Navegación funciona
- ✅ Los datos se recargan
- ✅ Sin errores de routing

---

## Checklist Final

```
FUNCIONALIDAD:
☐ Tarjetas KPI muestran números correctos
☐ Gráfico renderiza correctamente
☐ Tabla muestra todos los cultivos
☐ Resumen general visible

DISEÑO:
☐ Colores coinciden con tema
☐ Responsive en móvil/tablet/desktop
☐ Animaciones suaves
☐ Iconos visibles

SEGURIDAD:
☐ RBAC funciona (roles ven datos correctos)
☐ Técnico no ve el botón
☐ Token se valida
☐ Errores manejados

PERFORMANCE:
☐ Carga rápida
☐ Sin lag en animaciones
☐ Gráfico no consume recursos
☐ Sin memory leaks

INTEGRACIONES:
☐ Backend endpoint responde
☐ Axios hace requests correctos
☐ Auth store funciona
☐ Router navega correctamente
```

---

## Reportar Bugs

Si encuentras algún problema durante las pruebas, reporta:

1. **Paso a reproducir**: Qué hiciste
2. **Resultado esperado**: Qué debería pasar
3. **Resultado actual**: Qué pasó realmente
4. **Capturas**: Screenshots o videos
5. **Rol/Usuario**: Con qué rol lo viste
6. **Navegador/Dispositivo**: En qué dispositivo

---

**Última actualización**: 2025
**Versión de pruebas**: 1.0.0
