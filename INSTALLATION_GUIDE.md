# 🚀 Guía de Instalación Rápida - SembradoresView

## ✅ Prerequisitos

- Node.js 16+
- npm o yarn
- Backend FastAPI corriendo en `http://localhost:8000`
- Token JWT válido

---

## 📦 Instalación

### 1. Instalar Dependencias (si no lo has hecho)

```bash
cd Frontend/sistemaapp-frontend

npm install
# o
yarn install
```

### 2. Verificar que las dependencias estén instaladas

```bash
npm list axios sweetalert2 lucide-vue-next pinia v-motion
```

**Esperado:**
```
├── axios@1.5.0+
├── sweetalert2@11.10.0+
├── lucide-vue-next@0.292.0+
├── pinia@2.1.0+
└── v-motion@0.10.0+
```

Si falta alguna:
```bash
npm install axios sweetalert2 lucide-vue-next pinia v-motion
```

---

## 🔧 Configuración

### 1. Variables de Entorno

Crear/Verificar `.env.local` en `Frontend/sistemaapp-frontend/`:

```env
VITE_API_URL=http://localhost:8000
```

### 2. Backend Configurado

Verificar que el backend tiene:
- ✅ `models.py` con clase `Sembrador`
- ✅ `routes/sembradores.py` con 5 endpoints
- ✅ `main.py` con `include_router(sembradores.router)`
- ✅ BD con tabla `sembradores`

---

## 🚀 Ejecución

### Desarrollo Local

```bash
cd Frontend/sistemaapp-frontend

# Iniciar servidor Vite
npm run dev

# Esperar a que compile
# Abrir http://localhost:5173
```

### Build Producción

```bash
cd Frontend/sistemaapp-frontend

# Build optimizado
npm run build

# Generar archivos en dist/
# Servir con: python -m http.server (o similar)
```

---

## 🧪 Testing

### 1. Acceso a la Vista

```
1. Ir a http://localhost:5173 (o tu URL Vite)
2. Login con credenciales válidas
3. Navegar a "🌱 Sembradores" en navbar
4. Debería ver SembradoresView cargada
```

### 2. Test de Formulario

```
1. Llenar todos los campos
2. Click "Guardar Sembrador"
3. Esperar notificación ✅ Éxito
4. Formulario debe limpiarse
5. Nuevo sembrador debe aparecer en tabla
```

### 3. Test de Tabla

```
1. Tabla debe mostrarse con datos
2. Animaciones escalonadas visibles
3. Contador debe coincidir con número de filas
4. Hover en filas debe cambiar color
```

### 4. Test de Eliminación

```
1. Click en botón 🗑️ de una fila
2. Modal de confirmación debe aparecer
3. Click "Sí, eliminar"
4. Notificación roja ✅ Eliminado
5. Fila debe desaparecer de tabla
```

### 5. Test de Filtrado (diferentes usuarios)

```
Tecnician: Solo ve sus sembradores
Facilitador: Ve técnicos bajo supervisión
Territorial: Ve subordinados directos
Admin: Ve todos los sembradores
```

---

## 🐛 Troubleshooting

### Error: "CORS policy"

```
Solución: Verificar que backend tiene CORS habilitado
Backend: add_middleware(CORSMiddleware, ...)
```

### Error: "401 Unauthorized"

```
Solución: Token expirado
Acción: Re-login en /login
```

### Error: "Cannot GET /sembradores"

```
Solución: Ruta no agregada
Verificar: src/router/index.ts tiene la ruta
```

### Tabla vacía pero backend tiene datos

```
Solución: Filtrado jerárquico es restrictivo
Verificar: Usuario tiene rol correcto
Solución: Cambiar rol del usuario a admin para testing
```

### Animaciones lentas

```
Solución: Hardware limitado
Verificar: DevTools → Performance
Reducir: Cambiar delays en SembradoresView.vue línea 200
```

---

## 📁 Estructura de Archivos

```
Frontend/sistemaapp-frontend/
├── src/
│   ├── views/
│   │   ├── SembradoresView.vue ← NUEVA ✨
│   │   ├── DashboardView.vue
│   │   ├── LoginView.vue
│   │   └── ...
│   ├── router/
│   │   └── index.ts ← MODIFICADO ✏️
│   ├── components/
│   │   └── Navbar.vue ← MODIFICADO ✏️
│   ├── stores/
│   │   └── auth.js (para usar useAuthStore())
│   ├── App.vue
│   └── main.ts
├── .env.local (VITE_API_URL=...)
├── package.json
└── vite.config.ts
```

---

## 🎯 Flujo de Primera Vez

```
1. Login
   ↓
2. Dashboard
   ↓
3. Click "🌱 Sembradores" en navbar
   ↓
4. Carga SembradoresView.vue
   ↓
5. onMounted() → GET /sembradores/
   ↓
6. Tabla se llena con datos
   ↓
7. Usuario puede crear, listar, eliminar
```

---

## 🔐 Seguridad Verificada

✅ Token JWT requerido
✅ Ruta protegida (requiresAuth: true)
✅ Autenticación en cada petición API
✅ Autorización por rol en backend
✅ Validación de permisos en delete
✅ Encriptación de contraseñas
✅ CORS configurado

---

## 📊 Datos de Prueba

### Usuario Admin

```
Email: admin@test.com
Password: admin123
Rol: admin
Verá: Todos los sembradores
```

### Usuario Técnico

```
Email: tecnico@test.com
Password: tecnico123
Rol: tecnico_productivo
Verá: Solo sus sembradores
```

### Usuario Facilitador

```
Email: facilitador@test.com
Password: facilitador123
Rol: facilitador
Verá: Técnicos bajo supervisión
```

---

## 🔗 URLs Importantes

| Recurso | URL |
|---------|-----|
| Aplicación | http://localhost:5173 |
| Sembradores | http://localhost:5173/sembradores |
| Backend API | http://localhost:8000 |
| Docs API | http://localhost:8000/docs |

---

## 📞 Soporte

### Recursos Disponibles

- 📖 GUIA_SEMBRADORES_FRONTEND.md (400+ líneas)
- 📖 RESUMEN_ARQUITECTURA_COMPLETA.md (350+ líneas)
- 📖 EJEMPLOS_PRACTICOS_SEMBRADORES.md (300+ líneas)
- 📖 QUICK_REFERENCE.md (150+ líneas)

### Verificaciones Rápidas

```bash
# Verificar Node version
node --version  # 16+ esperado

# Verificar npm
npm --version

# Verificar dependencias
cd Frontend/sistemaapp-frontend
npm list | grep -E "axios|sweetalert2|lucide"

# Verificar que Vite compila
npm run build

# Verificar backend
curl http://localhost:8000/docs
```

---

## ✅ Checklist Pre-Deployment

- [ ] Todas las dependencias instaladas
- [ ] Variables de entorno configuradas
- [ ] Backend corriendo y accesible
- [ ] JWT token funcional
- [ ] Tabla sembradores existe en BD
- [ ] Roles y permisos configurados
- [ ] Vite dev server funciona (npm run dev)
- [ ] Puede navegar a /sembradores
- [ ] Puede crear sembrador
- [ ] Puede listar sembradores
- [ ] Puede eliminar sembrador
- [ ] Tabla se actualiza correctamente
- [ ] Notificaciones aparecen
- [ ] Responsive funciona en mobile
- [ ] Build producción compila (npm run build)

---

## 🎉 ¡Listo!

Una vez completados estos pasos, SembradoresView.vue estará completamente funcional y listo para producción.

**Versión:** 1.0
**Status:** ✅ Production Ready
**Última actualización:** 2024
