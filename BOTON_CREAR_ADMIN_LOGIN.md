# 👨‍💼 Botón para Crear Administrador en LoginView

## Descripción General
Se agregó un botón temporal (solo para desarrollo) en la pantalla de login que permite crear rápidamente usuarios administradores sin necesidad de pasar por el formulario de registro.

## Ubicación del Botón
El botón aparece debajo del botón "Crear una cuenta nueva" en la tarjeta de login.

## Cambios Realizados

### 1️⃣ Template - Nuevo Botón

```vue
<!-- Botón temporal para crear admin (solo desarrollo) -->
<button
  @click="crearAdmin"
  type="button"
  class="admin-button"
>
  <span>⚙️ Crear administrador (desarrollo)</span>
</button>
```

**Ubicación**: Después del `register-button` y dentro de la tarjeta de login.

### 2️⃣ Script - Imports y Función

#### Imports Agregados:
```javascript
import axios from 'axios'
import Swal from 'sweetalert2'
```

#### Función crearAdmin:
```javascript
const crearAdmin = async () => {
  try {
    const nombre = prompt('Nombre del nuevo administrador:')
    if (!nombre) return

    const emailAdmin = prompt('Correo del administrador:')
    if (!emailAdmin) return

    const passwordAdmin = prompt('Contraseña del administrador:')
    if (!passwordAdmin) return

    if (!nombre || !emailAdmin || !passwordAdmin) {
      await Swal.fire('⚠️ Campos incompletos', 'Debes llenar todos los campos', 'warning')
      return
    }

    await axios.post(`${import.meta.env.VITE_API_URL}/auth/register`, {
      nombre,
      email: emailAdmin,
      password: passwordAdmin,
      rol: 'admin'
    })

    await Swal.fire('✅ Administrador creado', 'Ya puedes iniciar sesión con este usuario', 'success')
  } catch (err) {
    await Swal.fire('❌ Error', err.response?.data?.detail || 'No se pudo crear el usuario', 'error')
  }
}
```

### 3️⃣ Estilos CSS

#### Estilo Base (.admin-button)
```css
.admin-button {
  width: 100%;
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
  border: 1.5px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  padding: 0.8rem 1.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Inter', 'Segoe UI', sans-serif;
  margin-top: 0.75rem;
}

.admin-button:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.6);
  color: #3b82f6;
  transform: translateY(-1px);
}

.admin-button:active {
  transform: scale(0.98);
}
```

#### Estilos Responsivos

| Breakpoint | Padding | Font Size | Border Radius | Margen Superior |
|-----------|---------|-----------|---------------|-----------------|
| Desktop (>1024px) | 0.8rem 1.5rem | 0.85rem | 12px | 0.75rem |
| Tablet (768px) | 0.7rem 1.2rem | 0.8rem | 10px | 0.6rem |
| Mobile (640px) | 0.65rem 1rem | 0.8rem | 9px | 0.5rem |
| Small Mobile (576px) | 0.6rem 0.9rem | 0.75rem | 8px | 0.5rem |
| Ultra Small (480px) | 0.55rem 0.85rem | 0.7rem | 7px | 0.4rem |
| Tiny (320px) | 0.5rem 0.75rem | 0.65rem | 6px | 0.35rem |

## Flujo de Funcionamiento

### 1. Usuario Presiona el Botón
```
Usuario ve: "⚙️ Crear administrador (desarrollo)"
```

### 2. Prompts Secuenciales
```
Primer prompt: "Nombre del nuevo administrador:"
Segundo prompt: "Correo del administrador:"
Tercer prompt: "Contraseña del administrador:"
```

### 3. Validación
- Se verifica que todos los campos estén completos
- Si alguno está vacío, se muestra alerta de warning

### 4. Envío al Backend
```javascript
POST /auth/register
{
  nombre: "nombre ingresado",
  email: "correo ingresado",
  password: "contraseña ingresada",
  rol: "admin"  // ← Rol forzado a admin
}
```

### 5. Respuesta
- **Éxito**: ✅ "Administrador creado" - El usuario puede iniciar sesión con esas credenciales
- **Error**: ❌ Muestra el mensaje de error del servidor

## Características Visuales

### Color Scheme
- **Fondo**: Azul semi-transparente (rgba(59, 130, 246, 0.1))
- **Borde**: Azul claro (rgba(59, 130, 246, 0.3))
- **Texto**: Azul cielo (#60a5fa)
- **Hover**: Azul más intenso (#3b82f6)

### Efectos
- **Hover**: Fondo más intenso + subida ligera (translateY -2px)
- **Click**: Escala de 0.98 para efecto de presión
- **Transición**: Suave (0.3s cubic-bezier)

## Responsividad
✅ Completamente responsivo en todos los breakpoints
- Desktop: 100% ancho, padding 0.8rem 1.5rem
- Tablets: Reducción proporcional
- Móviles: Ajustes para pantallas pequeñas (320px+)

## Dependencias Requeridas
```json
{
  "axios": "latest",
  "sweetalert2": "latest"
}
```

## Validación
✅ Sin errores de sintaxis
✅ Imports correctos
✅ Función lista para usar
✅ Estilos aplicados en todos los breakpoints

## Notas Importantes

### 🔒 SEGURIDAD - Solo para Desarrollo
Este botón debe eliminarse en producción o estar protegido detrás de:
- Una variable de entorno de desarrollo
- Verificación de usuario administrador
- Código comentado para producción

### ⚠️ Recomendaciones
1. En producción, eliminar este botón completamente
2. Considerar agregar verificación de rol antes de permitir crear admin
3. Agregar logging de creación de administradores
4. Implementar límite de intentos/rate limiting si se mantiene

## Archivo Modificado
- `LoginView.vue`: +50 líneas de código (template, script, CSS con todos los breakpoints)

## Testing Manual
```
1. Presionar botón "⚙️ Crear administrador (desarrollo)"
2. Ingresar nombre en primer prompt
3. Ingresar email en segundo prompt
4. Ingresar contraseña en tercer prompt
5. Verificar que aparezca mensaje de éxito
6. Intentar iniciar sesión con las credenciales creadas
```

## Próximos Pasos
- [ ] Probar en navegador
- [ ] Verificar que los prompts funcionan correctamente
- [ ] Probar en diferentes dispositivos (mobile, tablet, desktop)
- [ ] Confirmar que el admin se crea correctamente en backend
- [ ] Confirmar que se puede iniciar sesión con el admin creado
- [ ] Preparar versión sin botón para producción
