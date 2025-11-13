# ⚡ Guía Rápida - Prueba de Nuevos Roles Técnicos

## 🎯 En 10 Minutos

### 1. Iniciar Backend
```bash
cd BackendFastAPI
python -m uvicorn main:app --reload
# La app correrá en http://localhost:8000
```

### 2. Iniciar Frontend
```bash
cd Frontend/sistemaapp-frontend
npm run dev
# La app correrá en http://localhost:5173
```

---

## 📋 Test Rápido en Frontend

### Paso 1: Registro de Técnico Productivo
1. Ve a `http://localhost:5173/register`
2. Completa el formulario:
   - **Nombre:** Juan Productivo
   - **Email:** juan@productivo.com
   - **Contraseña:** 123456
   - **Rol:** Técnico Productivo ← *Selecciona esta opción*
   - Acepta términos
3. Click en "Crear Cuenta"
4. Verás: `¡Cuenta creada exitosamente! Bienvenido Juan Productivo`
5. Espera 2 segundos → Te redirige a login

### Paso 2: Login y Prueba
1. Login con credenciales:
   - Email: juan@productivo.com
   - Contraseña: 123456
2. Irás al dashboard
3. Si tienes acceso al mapa, intenta crear un punto:
   - Haz clic en el mapa
   - Selecciona tipo: `productiva`
   - Dale nombre: "Cultivo de maíz"
   - Se debe guardar sin problemas

### Paso 3: Registro de Técnico Social
1. Logout (botón superior derecho)
2. Ve a `/register` de nuevo
3. Completa con:
   - **Nombre:** María Social
   - **Email:** maria@social.com
   - **Contraseña:** 123456
   - **Rol:** Técnico Social ← *Selecciona esta opción*
4. Login con estas credenciales
5. En el mapa, intenta crear un punto:
   - Tipo: `social`
   - Nombre: "Centro comunitario"
   - Debe guardarse exitosamente

---

## 🧪 Test en Backend (Postman/cURL)

### Test 1: Verificar Rol por Defecto
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test User",
    "email": "test@test.com",
    "password": "123456"
  }'

# Resultado esperado:
# "rol": "tecnico_productivo"  ✅
```

### Test 2: Registrar con Rol Específico
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos Social",
    "email": "carlos@social.com",
    "password": "123456",
    "rol": "tecnico_social"
  }'

# Resultado esperado:
# "rol": "tecnico_social"  ✅
```

### Test 3: Verificar Rol Inválido Rechazado
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Invalid",
    "email": "invalid@test.com",
    "password": "123456",
    "rol": "superadmin"
  }'

# Resultado esperado:
# "detail": "Rol inválido. Permite: tecnico_productivo, tecnico_social, facilitador, territorial, admin"
# Status: 400  ✅
```

### Test 4: Técnico Productivo vs. Capas Sociales
```bash
# 1. Login y obtener token como técnico_productivo
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@productivo.com",
    "password": "123456"
  }'
# Copiar el "token" de la respuesta

# 2. Intentar ver capas sociales
curl http://localhost:8000/layers/social \
  -H "Authorization: Bearer {token_tecnico_productivo}"

# Resultado esperado:
# "total": 0, "items": []  ✅ (Vacío, sin acceso)
```

### Test 5: Técnico Social vs. Capas Productivas
```bash
# 1. Login como técnico_social
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "maria@social.com",
    "password": "123456"
  }'

# 2. Intentar ver capas productivas
curl http://localhost:8000/layers/productiva \
  -H "Authorization: Bearer {token_tecnico_social}"

# Resultado esperado:
# "total": 0, "items": []  ✅ (Vacío, sin acceso)
```

### Test 6: Facilitador Ve Ambas Capas
```bash
# Asumir que existe un facilitador con token {token_facilitador}

# 1. Ver capas productivas
curl http://localhost:8000/layers/productiva \
  -H "Authorization: Bearer {token_facilitador}"

# 2. Ver capas sociales
curl http://localhost:8000/layers/social \
  -H "Authorization: Bearer {token_facilitador}"

# Resultado esperado:
# Ambas retornan items de sus técnicos subordinados  ✅
```

---

## ✅ Checklist de Verificación

### Backend
- [ ] `tecnico_productivo` es el rol por defecto en `/auth/register`
- [ ] Los nuevos roles se aceptan en validación
- [ ] Facilitador filtra con `.like("tecnico%")`
- [ ] Técnico productivo no puede ver capas sociales (retorna vacío)
- [ ] Técnico social no puede ver capas productivas (retorna vacío)
- [ ] Admin ve todas las capas sin restricción

### Frontend
- [ ] RegisterView.vue muestra 3 opciones de rol
- [ ] Se puede seleccionar "Técnico Productivo"
- [ ] Se puede seleccionar "Técnico Social"
- [ ] El formulario valida correctamente

### Integración
- [ ] Registro → Login funciona para ambos tipos
- [ ] Las capas se crean en el tipo correcto
- [ ] El mapa muestra datos según el rol actual

---

## 🐛 Troubleshooting

### Problema: "Rol inválido"
**Solución:** Verifica que estés usando `tecnico_productivo` o `tecnico_social` exactamente, sin espacios.

### Problema: El técnico productivo sigue viendo capas sociales
**Solución:** Reinicia el backend (`uvicorn main:app --reload`). Los cambios en `layers.py` requieren reinicio.

### Problema: Las opciones de rol no aparecen en RegisterView
**Solución:** Limpia caché del navegador (Ctrl+Shift+Delete) y recarga.

### Problema: No puedo registrar con nuevo rol
**Solución:** Verifica que la API está corriendo en `http://localhost:8000`. Revisa la consola del navegador (F12).

---

## 📊 Datos de Prueba Recomendados

```
Admin (login test):
  Email: admin@test.com
  Password: 123456
  Rol: admin

Territorial (login test):
  Email: territorial@test.com
  Password: 123456
  Rol: territorial

Facilitador:
  Email: facilitador@test.com
  Password: 123456
  Rol: facilitador

Técnico Productivo (nuevo):
  Email: juan@productivo.com
  Password: 123456
  Rol: tecnico_productivo

Técnico Social (nuevo):
  Email: maria@social.com
  Password: 123456
  Rol: tecnico_social
```

---

## 🚀 Resumen de lo que Cambió

| Aspecto | Antes | Después |
|--------|-------|---------|
| Rol por defecto | `tecnico` | `tecnico_productivo` |
| Opciones de rol | tecnico, facilitador | tecnico_productivo, tecnico_social, facilitador |
| Filtrado facilitador | ❌ No había | ✅ Usa `.like("tecnico%")` |
| Especialización de capas | ❌ No había | ✅ Productiva solo para tech_productivo, Social solo para tech_social |
| Jerarquía en /users | Solo admin | ✅ Admin, Territorial, Facilitador con filtros jerárquicos |

---

## 💡 Notas Importantes

1. **Rol por defecto:** Si registras sin especificar rol, será `tecnico_productivo`
2. **Especialización:** Un técnico productivo NO puede ver/crear capas sociales
3. **Facilitador flexible:** Puede ver ambos tipos de capas (de sus técnicos)
4. **Admin omnipotente:** Ve y puede todo sin restricciones
5. **Jerarquía:** Territorial y facilitador solo ven subordinados

---

**Última actualización:** 13 de noviembre de 2025
**Estado:** ✅ Listo para pruebas
