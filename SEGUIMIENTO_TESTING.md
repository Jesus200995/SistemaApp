# 🧪 Guía de Testing - Módulo Seguimiento de Campo

## Verificación de Implementación

### Checklist Backend

- [x] Modelo `Seguimiento` agregado a `models.py`
  - [x] Campo `sembrador_id` (Foreign Key)
  - [x] Campo `user_id` (Foreign Key)
  - [x] Campo `fecha_visita` (DateTime)
  - [x] Campo `estado_cultivo` (String)
  - [x] Campo `observaciones` (Text)
  - [x] Campo `avance_porcentaje` (Float)
  - [x] Campo `foto_url` (String, nullable)
  - [x] Timestamps: `creado_en`, `actualizado_en`

- [x] Archivo `routes/seguimientos.py` creado
  - [x] Función `get_current_user()` (JWT parsing)
  - [x] Endpoint `POST /seguimientos/crear`
  - [x] Endpoint `GET /seguimientos/`
  - [x] Endpoint `GET /seguimientos/{id}`
  - [x] Endpoint `PUT /seguimientos/{id}`
  - [x] Endpoint `DELETE /seguimientos/{id}`
  - [x] Endpoint `GET /seguimientos/reportes/por-tecnico`
  - [x] Endpoint `GET /seguimientos/reportes/por-cultivo`

- [x] Router registrado en `main.py`
  - [x] Importación de `seguimientos`
  - [x] Inclusión de router: `app.include_router(seguimientos.router)`

### Checklist Frontend

- [x] Vista `SeguimientoView.vue` creada
  - [x] Tab: "Crear Seguimiento" con formulario
  - [x] Tab: "Mis Seguimientos" con grid de tarjetas
  - [x] Tab: "Reportes" con dos tablas
  - [x] Styling: Dark theme + green accents (#10b981)
  - [x] Responsive design (móvil, tablet, desktop)

- [x] Router actualizado (`router/index.ts`)
  - [x] Ruta `/seguimiento` → `SeguimientoView.vue`
  - [x] Meta: `requiresAuth: true`

- [x] Navegación actualizada (`Navbar.vue`)
  - [x] Enlace "📊 Seguimiento" agregado
  - [x] Posicionado correctamente en la navbar

---

## 🚀 Testing Manual - Paso a Paso

### Paso 1: Verificar Backend

#### 1.1 Verificar que el servidor esté corriendo
```bash
# En terminal Backend
cd Backend
python -m uvicorn main:app --reload --port 8000

# Esperado: "Uvicorn running on http://127.0.0.1:8000"
```

#### 1.2 Verificar que la tabla se crea
```bash
# En PostgreSQL CLI o DBeaver
SELECT * FROM seguimientos LIMIT 1;

# Esperado: "0 rows returned" (tabla vacía pero existe)
```

#### 1.3 Obtener token JWT (para testing)
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"tecnico@example.com","password":"password123"}'

# Respuesta esperada:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "user": { "id": 5, "nombre": "Carlos", "rol": "tecnico_productivo" }
# }

# Guardar el token para los siguientes requests
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."
```

#### 1.4 Crear un seguimiento (POST)
```bash
curl -X POST "http://localhost:8000/seguimientos/crear" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sembrador_id": 1,
    "fecha_visita": "2024-11-18T14:30:00",
    "estado_cultivo": "Germinando",
    "observaciones": "Cultivo en buen estado",
    "avance_porcentaje": 25,
    "foto_url": null
  }'

# Respuesta esperada:
# {
#   "success": true,
#   "id": 1,
#   "mensaje": "Seguimiento creado exitosamente"
# }
```

#### 1.5 Listar seguimientos (GET)
```bash
curl -X GET "http://localhost:8000/seguimientos/" \
  -H "Authorization: Bearer $TOKEN"

# Respuesta esperada:
# {
#   "success": true,
#   "total": 1,
#   "items": [
#     {
#       "id": 1,
#       "sembrador_id": 1,
#       "sembrador_nombre": "Juan Perez",
#       "comunidad": "El Palmar",
#       "cultivo_principal": "Maíz",
#       "user_id": 5,
#       "tecnico_nombre": "Carlos García",
#       "fecha_visita": "2024-11-18T14:30:00",
#       "estado_cultivo": "Germinando",
#       "observaciones": "Cultivo en buen estado",
#       "avance_porcentaje": 25,
#       "foto_url": null,
#       "creado_en": "2024-11-18T14:30:00",
#       "actualizado_en": "2024-11-18T14:30:00"
#     }
#   ]
# }
```

#### 1.6 Obtener detalle de un seguimiento
```bash
curl -X GET "http://localhost:8000/seguimientos/1" \
  -H "Authorization: Bearer $TOKEN"

# Respuesta esperada: El seguimiento completo
```

#### 1.7 Actualizar seguimiento (PUT)
```bash
curl -X PUT "http://localhost:8000/seguimientos/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "estado_cultivo": "Vegetativo",
    "avance_porcentaje": 45
  }'

# Respuesta esperada:
# {
#   "success": true,
#   "mensaje": "Seguimiento actualizado"
# }
```

#### 1.8 Ver reportes por técnico
```bash
curl -X GET "http://localhost:8000/seguimientos/reportes/por-tecnico" \
  -H "Authorization: Bearer $TOKEN"

# Respuesta esperada:
# {
#   "success": true,
#   "total": 1,
#   "items": [
#     {
#       "tecnico_id": 5,
#       "tecnico_nombre": "Carlos García",
#       "rol": "tecnico_productivo",
#       "total_seguimientos": 1,
#       "avance_promedio": 45.0,
#       "ultimo_seguimiento": "2024-11-18T14:30:00"
#     }
#   ]
# }
```

#### 1.9 Ver reportes por cultivo
```bash
curl -X GET "http://localhost:8000/seguimientos/reportes/por-cultivo" \
  -H "Authorization: Bearer $TOKEN"

# Respuesta esperada:
# {
#   "success": true,
#   "total": 1,
#   "items": [
#     {
#       "cultivo": "Maíz",
#       "total_sembradores": 1,
#       "total_seguimientos": 1,
#       "avance_promedio": 45.0
#     }
#   ]
# }
```

#### 1.10 Eliminar seguimiento (DELETE)
```bash
curl -X DELETE "http://localhost:8000/seguimientos/1" \
  -H "Authorization: Bearer $TOKEN"

# Respuesta esperada:
# {
#   "success": true,
#   "mensaje": "Seguimiento eliminado"
# }

# Verificar que fue eliminado:
curl -X GET "http://localhost:8000/seguimientos/" \
  -H "Authorization: Bearer $TOKEN"
# Total debe ser 0
```

### Paso 2: Verificar Frontend

#### 2.1 Verificar que el frontend está corriendo
```bash
# En terminal Frontend
cd Frontend/sistemaapp-frontend
npm install  # Si es la primera vez
npm run dev

# Esperado: "VITE v4.x.x  ready in xxx ms"
# Navegar a http://localhost:5173
```

#### 2.2 Verificar login
1. Ir a http://localhost:5173
2. Inicia sesión con credenciales de técnico
3. Verifica que seas redirigido a home ✅

#### 2.3 Verificar navbar
1. En el home, busca la navbar en la parte superior
2. Verifica que aparezca el enlace "📊 Seguimiento" ✅
3. Haz clic en él

#### 2.4 Verificar vista SeguimientoView
1. Después de hacer clic, deberías ver la vista
2. Verifica que existan 3 tabs:
   - ✅ "Crear Seguimiento"
   - ✅ "Mis Seguimientos"
   - ✅ "Reportes"
3. Verifica el estilo (dark theme, green accents)

#### 2.5 Verificar Tab: Crear Seguimiento
1. La tab "Crear Seguimiento" debe estar activa por defecto
2. Verifica los campos:
   - ✅ Selector de sembrador (dropdown)
   - ✅ Date/time picker
   - ✅ Dropdown estado cultivo
   - ✅ Range slider para progreso
   - ✅ Textarea observaciones
   - ✅ Input URL foto
3. Verifica los botones:
   - ✅ Botón "✅ Guardar Seguimiento"
   - ✅ Botón "🔄 Limpiar Formulario"

#### 2.6 Crear un seguimiento desde UI
1. Rellena el formulario:
   - **Sembrador**: Selecciona uno de la lista
   - **Fecha**: Hoy
   - **Estado**: "Germinando"
   - **Avance**: Mueve slider a 25%
   - **Observaciones**: "Cultivo en buen estado"
   - **Foto**: Deja vacío
2. Haz clic en "✅ Guardar Seguimiento"
3. Verifica:
   - ✅ Modal de confirmación
   - ✅ Se redirige a "Mis Seguimientos"
   - ✅ El nuevo seguimiento aparece en la lista

#### 2.7 Verificar Tab: Mis Seguimientos
1. Deberías ver al menos 1 tarjeta
2. Verifica que la tarjeta muestre:
   - ✅ Nombre del sembrador
   - ✅ Estado del cultivo (con badge)
   - ✅ Comunidad
   - ✅ Cultivo
   - ✅ Fecha de visita
   - ✅ Técnico (tu nombre)
   - ✅ Barra de progreso
   - ✅ Sección de observaciones
3. Verifica los botones:
   - ✅ Botón ✏️ (editar)
   - ✅ Botón 🗑️ (eliminar)

#### 2.8 Eliminar un seguimiento
1. En una tarjeta, haz clic en 🗑️
2. Verifica confirmación
3. Confirma
4. Verifica que la tarjeta desaparezca

#### 2.9 Verificar Tab: Reportes
1. Cambia a la tab "Reportes"
2. Verifica 2 secciones:

**Sección 1: Reporte por Técnico**
- ✅ Tabla con columnas: Técnico, Rol, Seguimientos, Avance %, Último
- ✅ Deberías ver tu nombre
- ✅ Mini barras de progreso

**Sección 2: Reporte por Cultivo**
- ✅ Tabla con columnas: Cultivo, Sembradores, Seguimientos, Avance %
- ✅ Deberías ver "Maíz" (o el cultivo del sembrador seleccionado)
- ✅ Mini barras de progreso

---

## 📋 Test Cases - Validación de Errores

### Test: Sin JWT Token
```bash
curl -X GET "http://localhost:8000/seguimientos/"

# Esperado: 401 Unauthorized
# Respuesta: {"detail":"Not authenticated"}
```

### Test: Token Inválido
```bash
curl -X GET "http://localhost:8000/seguimientos/" \
  -H "Authorization: Bearer invalid_token"

# Esperado: 401 Unauthorized
```

### Test: Sembrador No Existe
```bash
curl -X POST "http://localhost:8000/seguimientos/crear" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sembrador_id": 99999,
    "fecha_visita": "2024-11-18T14:30:00",
    "estado_cultivo": "Germinando",
    "observaciones": "Test",
    "avance_porcentaje": 25
  }'

# Esperado: 404 Not Found
# Respuesta: {"success": false, "mensaje": "Sembrador no encontrado"}
```

### Test: Intentar Eliminar Seguimiento Ajeno
```bash
# Crear seguimiento como usuario A
# Cambiar token a usuario B
# Intentar eliminar:

curl -X DELETE "http://localhost:8000/seguimientos/1" \
  -H "Authorization: Bearer TOKEN_B"

# Esperado: 403 Forbidden
# Respuesta: {"success": false, "mensaje": "No tienes permiso..."}
```

### Test: Porcentaje Fuera de Rango (Optional - si hay validación)
```bash
curl -X POST "http://localhost:8000/seguimientos/crear" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sembrador_id": 1,
    "fecha_visita": "2024-11-18T14:30:00",
    "estado_cultivo": "Germinando",
    "observaciones": "Test",
    "avance_porcentaje": 150
  }'

# Esperado: 400 Bad Request o aceptado (depende de validación)
```

---

## 📊 Test Cases - Filtrado Jerárquico

### Test: Admin ve todos los seguimientos
```bash
# Login como admin
# Crear 3 seguimientos como diferentes técnicos
# Listar como admin

curl -X GET "http://localhost:8000/seguimientos/" \
  -H "Authorization: Bearer ADMIN_TOKEN"

# Esperado: 3 seguimientos
```

### Test: Técnico ve solo sus seguimientos
```bash
# Crear 3 seguimientos como tecnico A
# Crear 3 seguimientos como tecnico B
# Listar como tecnico A

curl -X GET "http://localhost:8000/seguimientos/" \
  -H "Authorization: Bearer TECNICO_A_TOKEN"

# Esperado: 3 seguimientos (solo los de tecnico A)
```

### Test: Facilitador ve seguimientos de sus técnicos
```bash
# Admin asigna tecnico A y B a facilitador 1
# Tecnico C a facilitador 2
# Crear seguimientos de cada uno
# Listar como facilitador 1

curl -X GET "http://localhost:8000/seguimientos/" \
  -H "Authorization: Bearer FACILITADOR_1_TOKEN"

# Esperado: 6 seguimientos (3 de tecnico A + 3 de tecnico B)
# No ver: Seguimientos de tecnico C
```

---

## ✅ Validación Final

Cuando todos los tests pasen:

- [x] Backend crea registros correctamente
- [x] Frontend muestra los datos
- [x] Filtrado jerárquico funciona
- [x] Eliminación solo funciona para creador
- [x] Reportes se calculan correctamente
- [x] Interfaz es responsive
- [x] Estilos son consistentes

### Datos de Prueba Recomendados

Para testing completo, crea:
- 2-3 técnicos diferentes
- 4-5 sembradores
- 10-15 seguimientos variados
- Diferentes estados de cultivo
- Diferentes porcentajes de avance

---

## 🐛 Bugs Conocidos / En Desarrollo

- ⚠️ Edición de seguimientos: Botón ✏️ abre alert de "En desarrollo"
- ⚠️ Carga de fotos: Solo URLs externas (no upload directo)
- ⚠️ Filtros: No hay búsqueda por rango de fechas aún

---

## 📝 Notas de Testing

1. **Limpieza de datos**: Antes de cada sesión, considera limpiar:
   ```sql
   DELETE FROM seguimientos;
   ```

2. **Timezone**: Todos los timestamps en UTC. El frontend convierte a zona local.

3. **Cache**: Si ves datos viejos, limpia cache del navegador:
   - Ctrl+Shift+R (Windows/Linux)
   - Cmd+Shift+R (Mac)

4. **Console**: Abre Developer Tools (F12) para ver logs de errores

5. **Network**: Tab "Network" en DevTools para inspeccionar requests/responses

---

**Última Actualización**: 18 Noviembre 2024  
**Versión**: 1.0.0  
**Status**: ✅ Listo para Testing
