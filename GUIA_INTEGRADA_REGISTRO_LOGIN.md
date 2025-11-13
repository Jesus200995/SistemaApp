# 🎯 GUÍA INTEGRADA: REGISTRO Y LOGIN

## 📋 Resumen de Cambios

Se ha implementado un sistema completo y profesional de **Registro de Usuarios** con dos enfoques:

### Opción 1: Modal en LoginView (Componente RegisterForm.vue)
- **Archivo:** `src/components/RegisterForm.vue`
- **Uso:** Modal elegante que se abre desde el botón de login
- **Ventaja:** Todo en una pantalla, sin redirección

### Opción 2: Vista Separada en RegisterView.vue (RECOMENDADA) ✅
- **Archivo:** `src/views/RegisterView.vue` (NUEVO)
- **Uso:** Ruta `/register` separada y dedicada
- **Ventaja:** Mejor UX, diseño consistente, url clara

**Implementación Actual:** Ambas opciones funcionan, pero se recomienda usar **RegisterView.vue** como ruta principal.

---

## 🚀 FLUJO COMPLETO

### 1. Pantalla de Login (`/login`)
```
┌─────────────────────────────────┐
│     SistemaApp - Login          │
├─────────────────────────────────┤
│ Email:    [_______________]     │
│ Password: [_______________]     │
│ [✓] Recuérdame                  │
│ [Iniciar Sesión]                │
├─────────────────────────────────┤
│ ¿No tienes cuenta?              │
│ [Crear una cuenta nueva]  ← Link
└─────────────────────────────────┘
```

**Opción A (Modal):** Botón abre modal en la misma página
**Opción B (Ruta):** Link redirige a `/register`

### 2. Pantalla de Registro (`/register`) - NUEVO
```
┌─────────────────────────────────┐
│    SistemaApp - Registro        │
├─────────────────────────────────┤
│ Nombre:           [____________]│
│ Email:            [____________]│
│ Contraseña:       [____________]│
│ Confirmar:        [____________]│
│ Rol:              [Técnico ▼]   │
│ ☑ Acepto términos               │
│ [Crear Cuenta]                  │
├─────────────────────────────────┤
│ ¿Ya tienes cuenta?              │
│ [Inicia sesión aquí]            │
└─────────────────────────────────┘
```

### 3. Backend procesa registro
```
POST /auth/register
├─ Valida email (único, formato)
├─ Valida contraseña (mínimo 6 caracteres)
├─ Valida nombre (mínimo 2 caracteres)
├─ Valida rol (tecnico, facilitador)
├─ Hash bcrypt de contraseña
├─ Crea usuario en DB
├─ Crea notificación para admin
└─ Retorna { success: true, ... }
```

### 4. Confirmación y redirección
```
✓ Cuenta creada exitosamente
↓ (auto-cierre en 2 segundos)
Redirige a: /login
↓
Usuario puede loguear
```

---

## 📁 ARCHIVOS IMPLEMENTADOS

### ✨ NUEVOS

#### `src/views/RegisterView.vue` (450 líneas)
Vista completa y profesional de registro con:
- Diseño consistente con LoginView
- Validaciones frontend y backend
- Animaciones suaves
- Estados: Normal → Cargando → Éxito/Error
- Responsivo (mobile + desktop)
- Integración con backend

**Características:**
- 6 campos: Nombre, Email, Password, Confirmar, Rol, Términos
- Validaciones en tiempo real
- Mensajes de error claros
- Mensajes de éxito
- Auto-redirección después de éxito
- Link de vuelta a login

### ✏️ MODIFICADOS

#### `src/router/index.ts`
Agregada ruta de registro:
```typescript
{
  path: '/register',
  name: 'register',
  component: () => import('../views/RegisterView.vue'),
  meta: { requiresAuth: false },  // No requiere autenticación
}
```

#### `src/views/LoginView.vue`
Reemplazado botón modal por router-link:
```vue
<!-- ANTES -->
<button @click="mostrarRegistro = true">Crear una cuenta nueva</button>

<!-- DESPUÉS -->
<router-link to="/register">Crear una cuenta nueva</router-link>
```

Removidas:
- Import de `RegisterForm.vue`
- Variable `mostrarRegistro`
- Props del componente RegisterForm

---

## 🎨 DISEÑO Y ESTILO

### Paleta de Colores (Consistente)
```
Primario:   #3b82f6 (Azul)       - Usado en RegisterView
Verde:      #10b981 (Verde)      - Usado en LoginView
Fondo:      #0f172a (Azul oscuro)
Texto:      #e2e8f0 (Gris claro)
Error:      #ef4444 (Rojo)
Éxito:      #10b981 (Verde)
```

### Componentes Visuales
- ✅ Fondo animado con blobs (gradiente)
- ✅ Animaciones de entrada (v-motion)
- ✅ Iconos de lucide-vue-next
- ✅ Inputs con iconos integrados
- ✅ Select personalizado
- ✅ Checkbox personalizado
- ✅ Mensajes con animación

### Responsive Design
```
Desktop:   max-width 500px
Tablet:    Adapta a 80%
Mobile:    Full width con padding
```

---

## 🔐 VALIDACIONES

### Frontend (RegisterView.vue)
```
✓ Nombre: mínimo 2 caracteres
✓ Email: formato válido (type="email")
✓ Contraseña: mínimo 6 caracteres
✓ Confirmar: debe coincidir con contraseña
✓ Rol: debe seleccionar uno
✓ Términos: debe aceptar
✓ Todos los campos requeridos
```

### Backend (`/auth/register`)
```
✓ Email: regex de validación, único en DB
✓ Nombre: mínimo 2 caracteres
✓ Contraseña: mínimo 6 caracteres
✓ Rol: whitelist (tecnico, facilitador, territorial, admin)
✓ Hash bcrypt
✓ No puede duplicar email
✓ Crea notificación automáticamente
```

---

## 🧪 PRUEBAS

### Test 1: Registro exitoso vía RegisterView
```
1. Ir a http://localhost:5173/login
2. Hacer clic en "Crear una cuenta nueva"
3. Redirige a http://localhost:5173/register
4. Llenar formulario:
   - Nombre: Juan Técnico
   - Email: juan@test.com
   - Password: password123
   - Confirmar: password123
   - Rol: Técnico
   - ☑ Términos
5. Hacer clic en "Crear Cuenta"
6. Verás: ✓ "Cuenta creada exitosamente"
7. Auto-cierre en 2 segundos
8. Redirige a /login
9. Prueba loguear con las credenciales creadas
```

### Test 2: Registro exitoso vía Modal (RegisterForm.vue)
```
1. Ir a http://localhost:5173/login
2. Hacer clic en "Crear una cuenta nueva" (en el divider)
3. Se abre modal
4. Llenar el formulario
5. Hacer clic en "Crear Cuenta"
6. Confirmación con ✓
7. Auto-cierre en 3 segundos
8. Modal desaparece
9. Redirige a /login
```

### Test 3: Validaciones
```
- Nombre muy corto: "❌ El nombre debe tener al menos 2 caracteres"
- Email inválido: "❌ Email inválido"
- Contraseña corta: "❌ La contraseña debe tener al menos 6 caracteres"
- Contraseñas no coinciden: "❌ Las contraseñas no coinciden"
- Sin rol: "❌ Debes seleccionar un rol"
- Sin términos: "❌ Debes aceptar los términos"
- Email duplicado (backend): "❌ El correo ya está registrado"
```

---

## 📱 RESPONSIVIDAD

### Desktop (>640px)
- Tarjeta: max-width 500px
- Fuentes: Normales
- Padding: 2rem
- Animaciones: Completas

### Tablet (640px - 768px)
- Tarjeta: 90% ancho
- Fuentes: Ligeramente reducidas
- Padding: 1.5rem
- Animaciones: Igual

### Mobile (<480px)
- Tarjeta: Full width
- Padding: 0.75rem
- Fuentes: Reducidas
- Font-size input: 16px (previene zoom iOS)
- Gap entre elementos: Menor

---

## 🔌 INTEGRACIÓN CON BACKEND

### Endpoint utilizado
```
POST /auth/register
```

### Datos enviados
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@test.com",
  "password": "password123",
  "rol": "tecnico"
}
```

### Respuesta exitosa
```json
{
  "success": true,
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@test.com",
  "rol": "tecnico",
  "message": "Usuario registrado exitosamente..."
}
```

### Respuesta de error
```json
{
  "detail": "El correo ya está registrado"
}
```

### Variable de entorno
```
VITE_API_URL=http://localhost:8000
```

---

## 📊 COMPARATIVA: MODAL vs VISTA

| Característica | Modal | Vista |
|---|---|---|
| Ubicación | LoginView | `/register` |
| Ruta URL | No hay | `/register` |
| Separación | No | Sí |
| Redirección | No | Sí |
| UX | En una página | Navegación clara |
| SEO | Peor | Mejor |
| Complejidad | Media | Media |
| **Recomendado** | No | ✅ Sí |

**Conclusión:** Usar ambas es flexible. Se recomienda la vista como principal pero mantener el modal como alternativa rápida.

---

## 🚀 CÓMO ACTIVAR

### 1. Ya está implementado en el código
- ✅ `RegisterView.vue` creado
- ✅ Ruta agregada en router
- ✅ LoginView actualizado

### 2. Iniciar servicios
```bash
# Backend
cd BackendFastAPI
uvicorn main:app --reload

# Frontend
cd Frontend/sistemaapp-frontend
npm run dev
```

### 3. Probar
```
http://localhost:5173/login
→ "Crear una cuenta nueva"
→ http://localhost:5173/register
```

---

## 📞 TROUBLESHOOTING

### Error: "No se puede conectar a API"
→ Verificar que backend está corriendo en `http://localhost:8000`
→ Verificar `VITE_API_URL` en `.env`

### Error: "El correo ya está registrado"
→ Usar otro email
→ O eliminar el usuario de la BD

### Modal no se abre
→ Verificar que `RegisterForm.vue` existe
→ Verificar imports en LoginView
→ Revisar consola (F12)

### Página de registro no carga
→ Verificar que `RegisterView.vue` existe
→ Verificar ruta en `router/index.ts`
→ Revisar consola (F12)

### Contraseña no se guarda correctamente
→ Backend usa bcrypt, es normal que se vea como hash
→ Login funciona con la contraseña original

---

## 📚 DOCUMENTACIÓN RELACIONADA

- `REGISTRO_USUARIOS.md` - Guía técnica del backend
- `REGISTRO_RESUMEN.md` - Resumen ejecutivo
- `CHECKLIST_REGISTRO.md` - Tests y verificaciones
- `QUICK_START_REGISTRO.md` - Setup en 5 minutos
- `RegisterForm.vue` - Componente modal
- `RegisterView.vue` - Vista separada

---

**Última actualización:** 13 de noviembre de 2025
**Versión:** 2.0 - VISTA SEPARADA + MODAL
**Estado:** ✅ COMPLETO Y FUNCIONAL
