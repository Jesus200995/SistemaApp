# ⚡ Quick Reference - SembradoresView

## 📂 Archivos Modificados/Creados

```
✨ NUEVO:
   src/views/SembradoresView.vue (750 líneas)
   └─ Componente completo con CRUD UI

✏️  MODIFICADO:
   src/router/index.ts
   └─ +1 ruta: /sembradores (protegida)
   
✏️  MODIFICADO:
   src/components/Navbar.vue
   └─ +1 enlace: 🌱 Sembradores
```

---

## 🔌 API Endpoints

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|------------|
| POST | `/sembradores/` | ✅ Requerida | Crear nuevo |
| GET | `/sembradores/` | ✅ Requerida | Listar (filtrado) |
| GET | `/sembradores/{id}` | ✅ Requerida | Obtener uno |
| PUT | `/sembradores/{id}` | ✅ Requerida | Actualizar |
| DELETE | `/sembradores/{id}` | ✅ Requerida | Eliminar |

---

## 🔐 Seguridad

**Token:** `Authorization: Bearer {token}`

**Filtrados por rol:**
- Admin: Todo
- Territorial: Subordinados directos
- Facilitador: Técnicos bajo supervisión
- Técnico: Solo propios

---

## 📝 Campos Obligatorios

| Campo | Tipo | Validación |
|-------|------|-----------|
| `nombre` * | String | min: 2, required |
| `comunidad` * | String | required |
| `cultivo_principal` * | String | required |
| `telefono` * | String | required |
| `lat` | Number | opcional, step: 0.0001 |
| `lng` | Number | opcional, step: 0.0001 |

---

## 🎨 Colores

```
Verde principal:    #10b981
Verde oscuro:       #059669
Fondo oscuro:       #0f172a
Texto:              #e2e8f0
Gris secundario:    #94a3b8
Rojo error:         #ef4444
```

---

## 💻 Métodos Principales

```typescript
// Obtener lista
getSembradores()

// Crear nuevo
crearSembrador()

// Editar (placeholder)
editarSembrador(sembrador)

// Eliminar con confirmación
eliminarSembrador(id)
```

---

## 📊 Data Structure

```typescript
interface Sembrador {
  id: number
  nombre: string
  comunidad: string
  cultivo_principal: string
  telefono: string
  lat: number | null
  lng: number | null
  user_id: number
  creado_en: string
}
```

---

## ⚙️ Variables Reactivas

```typescript
// Lista de sembradores
sembradores: ref([])

// Estado de carga
loading: ref(false)

// Datos del formulario
form: ref({
  nombre: '',
  comunidad: '',
  cultivo_principal: '',
  telefono: '',
  lat: null,
  lng: null
})
```

---

## 🚀 Acceso Rápido

```
URL: http://localhost:3000/sembradores
Nav: 🌱 Sembradores (en navbar)
Auth: ✅ Requerida (protegida)
Load: onMounted() ejecuta getSembradores()
```

---

## 🎯 Validaciones Frontend

✅ Campos obligatorios
✅ Confirmación de eliminación
✅ Input number para lat/lng
✅ Minlength en nombre

---

## 📱 Responsive Breakpoints

```
Mobile: < 480px  → 1 columna
Tablet: 480-768px → 1 columna
Desktop: > 768px  → 2 columnas
```

---

## 🔔 Notificaciones

```typescript
// Éxito
Swal.fire('✅ Éxito', 'Mensaje', 'success')

// Error
Swal.fire('❌ Error', 'Mensaje', 'error')

// Confirmación
Swal.fire({...mostrar modal...})
```

---

## 🔍 Debugging

**Console logs:**
```
✅ Conectado a notificaciones en navbar
❌ Error procesando notificación
Error al cargar sembradores
Error procesando notificación
```

**Network tab:**
- Authorization header presente
- Status 200 OK en GET
- Status 201 en POST
- Status 403 si no tienes permiso

---

## 🛠️ Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| 401 Unauthorized | Re-login |
| 403 Forbidden | Permisos insuficientes |
| Tabla vacía | Filtrado jerárquico es restrictivo |
| No carga | Verificar token |
| Lento | Network lento o BD grande |

---

## 📦 Dependencias Requeridas

```json
{
  "axios": "^1.5.0",
  "sweetalert2": "^11.10.0",
  "lucide-vue-next": "^0.292.0",
  "pinia": "^2.1.0",
  "v-motion": "^0.10.0"
}
```

---

## 📡 Environment Variables

```
VITE_API_URL=http://localhost:8000
```

---

## 🧩 Componentes Usados

- Sprout (icon)
- User (icon)
- MapPin (icon)
- Leaf (icon)
- Phone (icon)
- Navigation (icon)
- Edit2 (icon)
- Trash2 (icon)

---

## 📈 Performance Tips

✅ Lazy loading activado
✅ Scoped styles
✅ Animaciones transform/opacity
✅ Iconos SVG ligeros

---

## 📞 Endpoints Base

```
GET   http://localhost:8000/sembradores/
POST  http://localhost:8000/sembradores/
DELETE http://localhost:8000/sembradores/1
```

---

## ✅ Checklist Deployment

- [ ] Variables de entorno configuradas
- [ ] Token JWT funcional
- [ ] API backend corriendo
- [ ] BD con tabla sembradores
- [ ] Permisos de rol correctos
- [ ] CORS habilitado
- [ ] Build production: `npm run build`
- [ ] Servir dist/ con servidor

---

## 🔗 Relacionados

- DashboardView.vue (diseño matching)
- auth.js (Pinia store)
- router/index.ts (rutas)
- Navbar.vue (navegación)
- Backend/routes/sembradores.py (API)

---

## 📝 Notas

- Editar estará disponible en próxima versión
- Paginación recomendada para listas > 100
- Mapa de sembradores en desarrollo
- Exportación a PDF planeada

---

**Version:** 1.0
**Status:** ✅ Production Ready
**Last Updated:** 2024
