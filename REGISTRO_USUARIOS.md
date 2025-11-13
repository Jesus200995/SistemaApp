# 📝 GUÍA DE REGISTRO DE USUARIOS

## 🎯 Objetivo General

Implementar un sistema completo de registro de usuarios que permita:
1. **Crear nuevas cuentas** desde la pantalla de login
2. **Validar datos** de manera segura
3. **Notificar al admin** cuando se registra un nuevo usuario
4. **Asignar jerarquía** (se hará manualmente por el admin)

---

## 🏗️ Arquitectura Implementada

### Backend (FastAPI)

#### Endpoint: `POST /auth/register`

**Ubicación:** `BackendFastAPI/routes/auth.py`

**Funcionalidad:**
```python
@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
```

**Datos requeridos:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "password": "miPassword123",
  "rol": "tecnico"  // o "facilitador"
}
```

**Validaciones implementadas:**

1. **Email válido** (formato correcto)
2. **Nombre mínimo** (2 caracteres)
3. **Contraseña mínima** (6 caracteres)
4. **Email único** (no puede estar registrado)
5. **Rol permitido** (tecnico, facilitador, territorial, admin)

**Respuesta exitosa:**
```json
{
  "success": true,
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "rol": "tecnico",
  "message": "Usuario registrado exitosamente. Un administrador revisará tu solicitud."
}
```

#### Notificaciones al Admin

Cuando se registra un usuario, se crea automáticamente una notificación:

```python
notificacion = Notificacion(
  titulo="Nuevo usuario registrado",
  mensaje="Juan Pérez (juan@ejemplo.com) se registró como TECNICO",
  tipo="info",
  rol_destino="admin"
)
```

### Frontend (Vue 3)

#### Componente: `RegisterForm.vue`

**Ubicación:** `Frontend/sistemaapp-frontend/src/components/RegisterForm.vue`

**Características:**

1. **Modal elegante** con fondo de desenfoque
2. **Validaciones locales:**
   - Email válido
   - Contraseñas coinciden
   - Términos aceptados
   - Campos requeridos

3. **Estados:**
   - **Cargando:** Mientras se envía la solicitud
   - **Error:** Si hay problema (email duplicado, validación, etc.)
   - **Éxito:** Confirmación y redirección al login

4. **UX mejorada:**
   - Animaciones suaves
   - Mensajes claros
   - Responsivo (mobile y desktop)
   - Auto-cierre después de éxito

#### Integración en LoginView

**Antes:**
```vue
<button @click="goToRegister">Crear una cuenta nueva</button>
```

**Después:**
```vue
<!-- Botón que abre el modal -->
<button @click="mostrarRegistro = true">Crear una cuenta nueva</button>

<!-- Modal de registro -->
<RegisterForm :mostrar="mostrarRegistro" @close="mostrarRegistro = false" />
```

---

## 🔐 Seguridad Implementada

### Contraseñas
- ✅ Hash con **bcrypt** (gensalt automático)
- ✅ Nunca se almacena contraseña en plano

### Validaciones
- ✅ Email duplicado rechazado
- ✅ Datos requeridos validados
- ✅ Rol restringido a valores permitidos

### Roles Disponibles
```
- tecnico       → Técnico de campo
- facilitador   → Facilitador territorial
- territorial   → Territorial (asignado por admin)
- admin         → Administrador (asignado por admin)
```

### Jerarquía
- **Por defecto:** `superior_id = None` (sin superior)
- **Asignación:** El admin asigna el `superior_id` manualmente
- **Validación:** Controlada en endpoints de layers.py

---

## 📋 Modelos Actualizado

### User Model

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Hash bcrypt
    rol = Column(String, nullable=False)       # tecnico, facilitador, etc.
    activo = Column(Boolean, default=True)
    superior_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # ← NUEVO
    created_at = Column(DateTime, server_default=func.now())
```

### Notificacion Model

```python
class Notificacion(Base):
    __tablename__ = "notificaciones"
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    mensaje = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # info, warning, error, success
    rol_destino = Column(String(50))           # admin, usuario, all
    leido = Column(Boolean, default=False)
    usuario_id = Column(Integer)               # Para notificaciones personales
    created_at = Column(DateTime, server_default=func.now())
```

---

## 🚀 Flujo Completo

### 1️⃣ Usuario accede a Login
```
LoginView.vue carga
↓
Lee token del localStorage (si existe)
↓
Muestra botón "Crear una cuenta nueva"
```

### 2️⃣ Usuario abre el formulario de registro
```
Hace clic en "Crear una cuenta nueva"
↓
Se abre RegisterForm.vue (modal)
↓
Usuario completa el formulario
```

### 3️⃣ Usuario envía datos
```
Validación local (contraseñas, términos, etc.)
↓
POST /auth/register
↓
Backend valida:
  - Email no duplicado
  - Contraseña ≥ 6 caracteres
  - Nombre ≥ 2 caracteres
  - Rol válido
↓
Se crea Usuario con rol "tecnico" por defecto
↓
Se crea Notificación para admins
↓
Retorna: { success: true, id, nombre, email }
```

### 4️⃣ Usuario ve confirmación
```
Modal muestra ✓ "¡Cuenta creada!"
↓
Auto-cierre después de 3 segundos
↓
Redirige a Login
↓
Usuario ya puede iniciar sesión
```

### 5️⃣ Admin recibe notificación
```
En el dashboard aparece:
  "Nuevo usuario registrado"
  "Juan Pérez (juan@ejemplo.com) se registró como TECNICO"
↓
Admin puede:
  - Ver al usuario en /auth/users
  - Asignarle un superior_id
  - Cambiar su rol si es necesario
```

---

## 📱 Vista Previa del Frontend

### Pantalla de Login (Antes)
```
┌─────────────────────────┐
│   SistemaApp Login      │
├─────────────────────────┤
│ Email: [____]           │
│ Password: [____]        │
│ [Iniciar Sesión]        │
├─────────────────────────┤
│ ¿No tienes cuenta?      │
│ [Crear una cuenta nueva]│ ← Antes: alert
└─────────────────────────┘
```

### Pantalla de Login (Después)
```
┌─────────────────────────┐
│   SistemaApp Login      │
├─────────────────────────┤
│ Email: [____]           │
│ Password: [____]        │
│ [Iniciar Sesión]        │
├─────────────────────────┤
│ ¿No tienes cuenta?      │
│ [Crear una cuenta nueva]│ ← Después: abre modal
└─────────────────────────┘

Hace clic ↓

┌────────────────────────────┐
│ Modal: Crear Nueva Cuenta  │
├────────────────────────────┤
│ Nombre: [Juan Pérez]       │
│ Email: [juan@ejemplo.com]  │
│ Password: [••••••••]       │
│ Confirmar: [••••••••]      │
│ Rol: [Técnico ▼]          │
│ ☑ Acepto términos         │
├────────────────────────────┤
│ [Crear Cuenta] [Cancelar]  │
└────────────────────────────┘
```

---

## ⚙️ Instalación y Configuración

### Backend

1. **Importar las nuevas dependencias** en `requirements.txt`:
```
bcrypt==4.0.1
python-multipart==0.0.6
```

2. **Instalar:**
```bash
pip install -r requirements.txt
```

3. **Migrar la base de datos:**
```bash
# Agregar campo superior_id a tabla users
alembic revision --autogenerate -m "Add superior_id to users"
alembic upgrade head
```

O crear la tabla manualmente:
```sql
ALTER TABLE users ADD COLUMN superior_id INTEGER REFERENCES users(id);
```

### Frontend

1. **El componente ya está importado** en `LoginView.vue`
2. **Verificar que VITE_API_URL está correcta** en `.env`:
```
VITE_API_URL=http://localhost:8000
```

3. **Reiniciar Vite** si es necesario:
```bash
npm run dev
```

---

## 🧪 Pruebas

### Probar con curl (Backend)

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test User",
    "email": "test@ejemplo.com",
    "password": "password123",
    "rol": "tecnico"
  }'
```

**Respuesta esperada:**
```json
{
  "success": true,
  "id": 1,
  "nombre": "Test User",
  "email": "test@ejemplo.com",
  "rol": "tecnico",
  "message": "Usuario registrado exitosamente..."
}
```

### Casos de error

1. **Email duplicado:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test User",
    "email": "test@ejemplo.com",  # Ya existe
    "password": "password123",
    "rol": "tecnico"
  }'
```
Respuesta: `{ "detail": "El correo ya está registrado" }`

2. **Contraseña muy corta:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test",
    "email": "new@ejemplo.com",
    "password": "123",  # < 6 caracteres
    "rol": "tecnico"
  }'
```
Respuesta: `{ "detail": "La contraseña debe tener al menos 6 caracteres" }`

3. **Rol inválido:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test",
    "email": "new@ejemplo.com",
    "password": "password123",
    "rol": "superadmin"  # No permitido
  }'
```
Respuesta: `{ "detail": "Rol inválido. Permite: tecnico, facilitador, territorial, admin" }`

---

## 📊 Próximos Pasos (Futuro)

1. **Verificación de email:**
   - Enviar email de confirmación
   - Usuario debe confirmar antes de poder iniciar sesión

2. **Asignación automática de superior:**
   - Territorial más cercano se asigna automáticamente como superior

3. **Recuperación de contraseña:**
   - Endpoint `/auth/forgot-password`
   - Email de recuperación con token temporal

4. **Roles más avanzados:**
   - Roles personalizados por organización
   - Permisos granulares

5. **Multi-tenant:**
   - Cada organización con sus usuarios
   - Aislamiento de datos por tenant

---

## 📞 Contacto y Soporte

- **Backend Issues:** Revisar logs de FastAPI
- **Frontend Issues:** Revisar console del navegador
- **Database Issues:** Revisar logs de PostgreSQL

---

**Última actualización:** 13 de noviembre de 2025
**Estado:** ✅ COMPLETADO Y FUNCIONAL
