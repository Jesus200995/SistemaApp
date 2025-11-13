# 🧪 Guía de Testing: Sembradores en el Mapa

## 1. Setup de Testing

### Requisitos

```bash
# Backend corriendo
python -m uvicorn BackendFastAPI.main:app --reload

# Frontend corriendo
cd Frontend/sistemaapp-frontend
npm run dev
```

### Credenciales de Prueba

```
🔐 Admin
  Email: admin@sistema.com
  Password: admin123

🔐 Territorial
  Email: territorial@sistema.com
  Password: territorial123

🔐 Facilitador
  Email: facilitador@sistema.com
  Password: facilitador123

🔐 Técnico Productivo
  Email: tecnico_prod@sistema.com
  Password: tecnico123

🔐 Técnico Social
  Email: tecnico_social@sistema.com
  Password: tecnico123
```

---

## 2. Test Cases Funcionales

### Test 2.1: Usuario Admin

**Objetivo**: Verificar que Admin ve todos los sembradores

**Pasos**:
1. Login con admin@sistema.com
2. Navega a "Mapa"
3. Observa la leyenda

**Verificaciones**:
```
✓ Leyenda muestra: "Mostrar sembradores (N)"
✓ N es el TOTAL de sembradores en el sistema (ej: 10)
✓ Markers aparecen distribuidos en el mapa
✓ Algunos marcadores son verdes (productivos)
✓ Algunos marcadores son azules (sociales)
✓ Al hacer click en marcador → popup con información
```

**Popup esperado**:
```
┌─────────────────────────┐
│ 🌱 Sembrador Productivo │ o 👥 Sembrador Social
├─────────────────────────┤
│ Nombre: [valor]         │
│ Comunidad: [valor]      │
│ Cultivo: [valor]        │
│ Técnico: [valor]        │
│ Ubicación: [-33, -51]   │
└─────────────────────────┘
```

**Resultado esperado**: ✅ PASS

---

### Test 2.2: Usuario Territorial

**Objetivo**: Verificar que Territorial ve solo subordinados

**Setup**:
- Crear estructura jerárquica:
  ```
  Territorial (id=2)
  ├─ Facilitador A (id=3)
  │  └─ Técnico (id=5) → 3 sembradores
  └─ Facilitador B (id=4)
     └─ Técnico (id=6) → 2 sembradores
  ```

**Pasos**:
1. Login con territorial@sistema.com
2. Navega a "Mapa"

**Verificaciones**:
```
✓ Leyenda muestra: "Mostrar sembradores (5)"  [3+2]
✓ SOLO ve 5 marcadores (no ve otros del sistema)
✓ Popup muestra técnicos de sus subordinados
```

**Resultado esperado**: ✅ PASS

---

### Test 2.3: Usuario Facilitador

**Objetivo**: Verificar que Facilitador ve solo sus técnicos

**Setup**:
```
Facilitador A (id=3)
├─ Técnico Productivo (id=5) → 3 sembradores (productivos)
└─ Técnico Social (id=6) → 2 sembradores (sociales)
```

**Pasos**:
1. Login con facilitador@sistema.com
2. Navega a "Mapa"

**Verificaciones**:
```
✓ Leyenda muestra: "Mostrar sembradores (5)"
✓ 3 marcadores verdes (técnico productivo)
✓ 2 marcadores azules (técnico social)
✓ Popup "Técnico: Juan Pérez" o similar
✓ NO ve sembradores de otros facilitadores
```

**Resultado esperado**: ✅ PASS

---

### Test 2.4: Usuario Técnico Productivo

**Objetivo**: Verificar que Técnico solo ve sus sembradores

**Setup**:
```
Técnico Productivo (id=5)
└─ 3 sembradores creados por él
```

**Pasos**:
1. Login con tecnico_prod@sistema.com
2. Navega a "Mapa"

**Verificaciones**:
```
✓ Leyenda muestra: "Mostrar sembradores (3)"
✓ SOLO 3 marcadores verdes
✓ Todos los marcadores son productivos
✓ Técnico es el usuario logueado
✓ NO ve sembradores de otros técnicos
```

**Resultado esperado**: ✅ PASS

---

## 3. Test Cases de UI

### Test 3.1: Toggle de Visibilidad

**Objetivo**: Verificar funcionamiento del checkbox

**Pasos**:
1. Abre mapa como usuario con sembradores
2. Leyenda muestra: "☑ Mostrar sembradores (5)"
3. Haz click en checkbox

**Verificaciones - Estado Checked**:
```
✓ Checkbox marcado ☑
✓ Todos los marcadores visibles
✓ Mapa se ve normal
```

**Verificaciones - Estado Unchecked**:
```
✓ Checkbox desmarcado ☐
✓ TODOS los marcadores desaparecen
✓ Mapa se ve limpio (sin marcadores)
✓ Contador sigue mostrando "(5)"
```

**Verificaciones - Volver a Checked**:
```
✓ Al rehacer click, marcadores reaparecen
✓ En la MISMA posición que antes
✓ No hace nueva petición HTTP
```

**Resultado esperado**: ✅ PASS

---

### Test 3.2: Popups Interactivos

**Objetivo**: Verificar información en popups

**Pasos**:
1. Abre mapa
2. Haz click en un marcador verde (productivo)

**Verificaciones**:
```
✓ Popup aparece cerca del marcador
✓ Header dice: "🌱 Sembrador Productivo"
✓ Header es de color verde oscuro
✓ Popup tiene estos campos:
  - Nombre: [nombre del sembrador]
  - Comunidad: [comunidad]
  - Cultivo: [cultivo]
  - Técnico: [nombre técnico]
  - Ubicación: [lat, lng]
✓ Toda información es legible
✓ Sin errores de datos
```

**Pasos 2 - Click en marcador azul**:
1. Haz click en un marcador azul (social)

**Verificaciones**:
```
✓ Popup aparece
✓ Header dice: "👥 Sembrador Social"
✓ Header es de color azul oscuro
✓ Mismo formato que productivo
```

**Pasos 3 - Click fuera popup**:
1. Haz click en zona vacía del mapa

**Verificaciones**:
```
✓ Popup se cierra
✓ Vuelve a ver el mapa limpio
```

**Resultado esperado**: ✅ PASS

---

### Test 3.3: Leyenda Visual

**Objetivo**: Verificar que leyenda se vea correcta

**Verificaciones**:
```
✓ Leyenda visible en esquina inferior derecha
✓ Estructura:
  - Capas temáticas (existentes)
  - Línea separadora
  - 🌱 Sembrador Productivo (verde)
  - 👥 Sembrador Social (azul)
  - Línea separadora
  - ☑ Mostrar sembradores (X)
✓ Colores correctos (verde y azul)
✓ Contador actualizado correctamente
✓ Checkbox accesible (clickeable)
✓ Estilos oscuros consistentes
```

**Resultado esperado**: ✅ PASS

---

## 4. Test Cases de API

### Test 4.1: Endpoint Responde Correctamente

**Objetivo**: Verificar que API devuelve datos válidos

**Pasos**:
1. Abre DevTools: F12
2. Tab "Network"
3. Filtra por: "sembradores"
4. Recarga página del mapa

**Verificaciones**:
```
✓ REQUEST:
  - URL: /sembradores/map
  - Method: GET
  - Headers incluye: Authorization: Bearer [token]
  
✓ RESPONSE:
  - Status: 200 OK
  - Content-Type: application/json
  
✓ PAYLOAD:
  - success: true
  - total: [número > 0]
  - items: [array de objetos]
```

**Estructura esperada de item**:
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "comunidad": "La Esperanza",
  "cultivo": "Maíz",
  "lat": -33.8688,
  "lng": -51.2093,
  "user_id": 5,
  "tecnico_nombre": "Juan Pérez",
  "tecnico_rol": "tecnico_productivo",
  "creado_en": "2024-01-15T10:30:00"
}
```

**Resultado esperado**: ✅ PASS

---

### Test 4.2: Filtrado Jerárquico Funciona

**Objetivo**: Verificar que cada rol ve correctamente

**Setup**:
- En base de datos, asegúrate de tener:
  - 3+ sembradores de técnico A
  - 2+ sembradores de técnico B
  - Técnicos bajo distintos facilitadores

**Pasos por cada rol**:

1. **Admin**:
   ```
   Login → Mapa → DevTools Network
   Response total = TODAS los sembradores del sistema
   ```

2. **Territorial**:
   ```
   Login → Mapa → DevTools Network
   Response total = solo de subordinados directos
   ≠ Admin total
   ```

3. **Facilitador**:
   ```
   Login → Mapa → DevTools Network
   Response total = solo de sus técnicos
   < Territorial total
   ```

4. **Técnico**:
   ```
   Login → Mapa → DevTools Network
   Response total = solo sus sembradores (ej: 3)
   < Facilitador total
   ```

**Verificaciones**:
```
✓ Cada rol ve cantidad diferente
✓ Orden: Admin ≥ Territorial ≥ Facilitador ≥ Técnico
✓ Datos son realmente distintos (diferente ids)
✓ Sin exposición de datos de otros usuarios
```

**Resultado esperado**: ✅ PASS

---

### Test 4.3: Error Handling

**Objetivo**: Verificar que errores se manejen correctamente

**Test 4.3.1 - Sin token**:
1. Abre DevTools Console
2. Ejecuta:
   ```javascript
   fetch('http://localhost:8000/sembradores/map', {
     headers: { 'Authorization': 'Bearer INVALID' }
   })
   ```

**Verificaciones**:
```
✓ Response status: 401
✓ Response detalle: "Usuario no encontrado" o similar
✓ Frontend: Marcadores NO aparecen (array vacío)
```

**Test 4.3.2 - Usuario sin sembradores**:
1. Login con usuario técnico que nunca ha creado sembradores

**Verificaciones**:
```
✓ API Response: total = 0
✓ Frontend: items = []
✓ Leyenda: "Mostrar sembradores (0)"
✓ Mapa: Sin marcadores
```

**Resultado esperado**: ✅ PASS

---

## 5. Test Cases de Performance

### Test 5.1: Carga Rápida

**Objetivo**: Verificar que datos cargan rápidamente

**Pasos**:
1. Abre DevTools: F12 → Tab "Network"
2. Recarga página del mapa
3. Cronometra tiempo de `/sembradores/map`

**Verificaciones**:
```
✓ Tiempo de respuesta < 500ms (ideal < 200ms)
✓ Tamaño JSON < 100KB (para 100 items)
✓ Markers aparecen inmediatamente después
✓ UI no se congela
```

**Resultado esperado**: ✅ PASS

---

### Test 5.2: Toggle es Instantáneo

**Objetivo**: Verificar que checkbox funciona sin delay

**Pasos**:
1. Mapa cargado con sembradores visibles
2. Haz click en checkbox "Mostrar sembradores"
3. Mira si marcadores desaparecen inmediatamente

**Verificaciones**:
```
✓ Desaparición es instantánea (< 50ms)
✓ No hay lag o bloqueo
✓ Puedes hacer click de nuevo sin delay
✓ UI responde fluidamente
```

**Resultado esperado**: ✅ PASS

---

### Test 5.3: Muchos Sembradores

**Objetivo**: Verificar comportamiento con muchos items

**Setup**:
- Crea 100+ sembradores en base de datos

**Pasos**:
1. Login como Admin
2. Abre mapa
3. Observa performance

**Verificaciones**:
```
✓ Carga completa en < 1 segundo
✓ Mapa mantiene 60 FPS al pan/zoom
✓ Popups abren sin delay
✓ Toggle sigue siendo instantáneo
✓ Navegador no se cuelga
```

**Resultado esperado**: ✅ PASS (o nota si hay lag)

---

## 6. Test Cases de Responsividad

### Test 6.1: Desktop (1920x1080)

**Verificaciones**:
```
✓ Mapa ocupa todo el espacio
✓ Leyenda en esquina inferior derecha
✓ Popups se ven completos
✓ Todas las capas visibles
✓ Checkbox claramente clickeable
```

**Resultado esperado**: ✅ PASS

---

### Test 6.2: Tablet (768x1024)

**Pasos**:
1. Abre DevTools
2. Click icono dispositivo (mobile)
3. Selecciona "iPad" o equivalente

**Verificaciones**:
```
✓ Mapa sigue siendo funcional
✓ Leyenda visible (puede ser compacta)
✓ Popups caben en pantalla
✓ Checkbox accesible
✓ Sin scroll horizontal
```

**Resultado esperado**: ✅ PASS

---

### Test 6.3: Mobile (375x667)

**Pasos**:
1. DevTools → Mobile: iPhone
2. Prueba interacciones

**Verificaciones**:
```
✓ Mapa visible sin scroll horizontal
✓ Tap en marcador abre popup
✓ Popup es legible (puede ser más pequeño)
✓ Checkbox funciona en mobile
✓ Zoom/pan funciona normalmente
✓ Sin texto cortado
```

**Resultado esperado**: ✅ PASS

---

## 7. Test Cases de Seguridad

### Test 7.1: No hay exposición de datos

**Objetivo**: Verificar que cada usuario SOLO ve sus datos

**Setup en BD**:
```sql
-- Técnico A: 3 sembradores
-- Técnico B: 3 sembradores
-- Facilitador A supervisa a ambos
-- Facilitador B supervisa a técnico B solo
```

**Pasos**:
1. Login como Técnico A
2. Abre DevTools → Network
3. Carga mapa
4. Observa response de `/sembradores/map`

**Verificaciones**:
```
✓ Response contiene SOLO ids: [1,2,3] (propios)
✓ NO contiene ids de Técnico B
✓ user_id en todos = su ID
```

**Pasos 2 - Login como Facilitador A**:
1. Repite proceso

**Verificaciones**:
```
✓ Response contiene: [1,2,3,4,5,6] (de ambos técnicos)
✓ NO contiene sembradores de otros facilitadores
✓ user_id varía (pertenecen a técnicos)
```

**Resultado esperado**: ✅ PASS

---

### Test 7.2: Token Inválido Rechaza

**Pasos**:
1. Devtools → Application → Cookies
2. Busca token JWT
3. Modifica 1 caracter del token
4. Recarga página

**Verificaciones**:
```
✓ API devuelve error 401
✓ Mapa carga pero sin marcadores
✓ Leyenda muestra: "Mostrar sembradores (0)"
✓ Sin exposición de datos
✓ Usuario puede ver pero no sus datos
```

**Resultado esperado**: ✅ PASS

---

## 8. Test Cases de Integración

### Test 8.1: Con SembradoresView

**Objetivo**: Verificar que mapa y tabla funcionan juntos

**Pasos**:
1. Login como técnico
2. Ve a SembradoresView → ve sus 3 sembradores
3. Ve a MapaView → ve los mismos 3 en el mapa
4. Compara ids

**Verificaciones**:
```
✓ Mismo número de items
✓ Mismos ids en ambas vistas
✓ Mismo nombre en ambas vistas
✓ Coordenadas coinciden en popup
```

**Resultado esperado**: ✅ PASS

---

### Test 8.2: Crear nuevo Sembrador → Aparece en Mapa

**Objetivo**: Verificar que data es consistente

**Pasos**:
1. En SembradoresView → Crear nuevo sembrador
2. Llenar formulario con coordenadas
3. Guardar
4. Ve a MapaView
5. Busca el nuevo marcador

**Verificaciones**:
```
✓ Nuevo marcador aparece en posición correcta
✓ Popup muestra información exacta
✓ Coordenadas coinciden
✓ No requiere reload completo
```

**Resultado esperado**: ✅ PASS

---

## 9. Matriz de Testing

| Test Case | Admin | Territorial | Facilitador | Técnico | Status |
|-----------|-------|------------|------------|---------|--------|
| Ver todos | ✓ | ✓ | ✓ | ✓ | |
| Toggle visibilidad | ✓ | ✓ | ✓ | ✓ | |
| Popup información | ✓ | ✓ | ✓ | ✓ | |
| Leyenda visual | ✓ | ✓ | ✓ | ✓ | |
| API responde | ✓ | ✓ | ✓ | ✓ | |
| Filtrado correcto | ✓ | - | - | - | |
| Performance | ✓ | ✓ | ✓ | ✓ | |
| Mobile responsive | ✓ | ✓ | ✓ | ✓ | |
| Sin exposición datos | ✓ | ✓ | ✓ | ✓ | |

---

## 10. Resumen de Testing

### Checklist Pre-Producción

**Funcionalidad**:
- [ ] Admin ve todos los sembradores
- [ ] Territorial ve solo subordinados
- [ ] Facilitador ve solo sus técnicos
- [ ] Técnico ve solo propios
- [ ] Popups muestran información correcta
- [ ] Toggle funciona correctamente
- [ ] Leyenda visible y completa

**API**:
- [ ] Endpoint responde 200 OK
- [ ] Response tiene estructura correcta
- [ ] Filtrado jerárquico funciona
- [ ] Errores se manejan correctamente
- [ ] Sin exposición de datos

**UX**:
- [ ] Interfaz clara e intuitiva
- [ ] Responsiva en mobile/tablet/desktop
- [ ] Carga rápida
- [ ] Sin lag en interacciones
- [ ] Colores diferenciados

**Seguridad**:
- [ ] Requiere autenticación
- [ ] Sin bypass de filtros
- [ ] Datos seguros
- [ ] Tokens validados

### Estado Final

**Todos los tests**: ✅ PASS = **LISTO PARA PRODUCCIÓN**

