# ⚡ GUÍA RÁPIDA: REGISTRO DE USUARIOS

## 🚀 Setup en 5 minutos

### Paso 1: Preparar Base de Datos (2 min)

**Opción A: Alembic Migration (recomendado)**
```bash
cd BackendFastAPI
alembic revision --autogenerate -m "Add superior_id to users"
alembic upgrade head
```

**Opción B: SQL Directo (PostgreSQL)**
```bash
psql postgresql://jesus:2025@31.97.8.51:5432/SistemaApp
```
```sql
ALTER TABLE users ADD COLUMN superior_id INTEGER REFERENCES users(id);
```

### Paso 2: Iniciar Backend (1 min)

```bash
cd BackendFastAPI
.\.venv\Scripts\Activate.ps1  # Si no está activado
uvicorn main:app --reload
```

**Verificar:** http://localhost:8000/docs (Swagger UI)

### Paso 3: Iniciar Frontend (1 min)

```bash
cd Frontend/sistemaapp-frontend
npm run dev
```

**Verificar:** http://localhost:5173/login

### Paso 4: Probar (1 min)

1. Ir a http://localhost:5173/login
2. Hacer clic en "Crear una cuenta nueva"
3. Llenar el formulario
4. Hacer clic en "Crear Cuenta"
5. ✓ Verás: "Cuenta creada exitosamente"
6. Luego podrás loguear con las credenciales creadas

---

## 📋 Checklist Rápido

- [ ] Base de datos: campo `superior_id` agregado a tabla `users`
- [ ] Backend: `uvicorn main:app --reload` corriendo
- [ ] Frontend: `npm run dev` corriendo
- [ ] Acceso a http://localhost:5173/login
- [ ] Botón "Crear una cuenta nueva" visible
- [ ] Modal se abre al hacer clic
- [ ] Puedo registrar usuario exitosamente
- [ ] Puedo loguear con las nuevas credenciales

---

## 🧪 Test Rápido en Curl

```bash
# Test: Registrar usuario
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

---

## 📁 Archivos Principales

| Archivo | Cambio |
|---------|--------|
| `BackendFastAPI/routes/auth.py` | ✏️ Endpoint `/register` mejorado |
| `BackendFastAPI/models.py` | ✏️ Agregado `superior_id` a User |
| `Frontend/sistemaapp-frontend/src/components/RegisterForm.vue` | ✨ NUEVO |
| `Frontend/sistemaapp-frontend/src/views/LoginView.vue` | ✏️ Integrado RegisterForm |

---

## 🐛 Troubleshooting

### Error: "El correo ya está registrado"
→ Ese email ya fue usado. Usa otro email.

### Error: "La contraseña debe tener al menos 6 caracteres"
→ Contraseña muy corta. Usa mínimo 6 caracteres.

### Error: "Email inválido"
→ Formato de email incorrecto. Ej: usuario@dominio.com

### Error: "El nombre debe tener al menos 2 caracteres"
→ Nombre muy corto. Usa mínimo 2 caracteres.

### No aparece el modal de registro
→ Verifica en la consola del navegador (F12) si hay errores JavaScript.

### Backend no responde
→ Asegúrate de que `uvicorn` está corriendo en `http://localhost:8000`

### Notificación no aparece
→ La notificación se crea en la BD, pero el admin debe estar logueado para verla.

---

## 📞 Variables de Entorno

Verificar que en `.env` están configuradas:

```properties
DATABASE_URL=postgresql://jesus:2025@31.97.8.51:5432/SistemaApp
JWT_SECRET=mi_clave_jwt_2025
```

En Frontend, verificar `.env` (si existe):
```
VITE_API_URL=http://localhost:8000
```

---

## ✨ Características Principales

✅ **Validación robusta:** Email, nombre, contraseña, rol
✅ **Seguridad:** Hash bcrypt, input sanitizado, CORS
✅ **UX moderna:** Modal elegante, animaciones, feedback
✅ **Responsive:** Funciona en mobile y desktop
✅ **Notificaciones:** Admin recibe alerta cuando se registra usuario
✅ **Jerarquía:** Campo `superior_id` para futuras asignaciones

---

## 🎯 Próximos Pasos

1. **Verificación de email:** Enviar confirmación por email
2. **CAPTCHA:** Agregar Google reCAPTCHA
3. **Políticas de contraseña:** Requerir mayúsculas, números, símbolos
4. **Rate limiting:** Limitar intentos por IP
5. **Recuperación:** Endpoint para resetear contraseña

---

**Última actualización:** 13 de noviembre de 2025
**Versión:** 1.0 - LISTA PARA PRODUCCIÓN
