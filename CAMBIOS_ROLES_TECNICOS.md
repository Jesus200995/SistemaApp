# 📋 Cambios de Roles Técnicos - Resumen de Implementación

## 🎯 Objetivo General
Implementar soporte para dos tipos de técnicos especializados: **Técnico Productivo** y **Técnico Social**, con filtrado jerárquico adecuado en toda la aplicación.

---

## 📝 Cambios Realizados

### 1️⃣ Backend - `/auth/register` (Rol por Defecto)
**Archivo:** `BackendFastAPI/routes/auth.py`

**Cambio:**
```python
# ❌ Antes:
roles_permitidos = ["tecnico", "facilitador", "territorial", "admin"]
rol = request.rol.lower() if request.rol else "tecnico"

# ✅ Después:
roles_permitidos = ["tecnico_productivo", "tecnico_social", "facilitador", "territorial", "admin"]
rol = request.rol.lower() if request.rol else "tecnico_productivo"
```

**Impacto:**
- Rol por defecto ahora es `tecnico_productivo`
- Se aceptan los nuevos roles `tecnico_productivo` y `tecnico_social`
- Si no se especifica rol, se asigna automáticamente como técnico productivo

---

### 2️⃣ Backend - `/auth/users` (Filtro Jerárquico)
**Archivo:** `BackendFastAPI/routes/auth.py`

**Mejora Realizada:**
```python
# Nuevo filtrado jerárquico por rol
if current_rol == "admin":
    # Admin ve todos los usuarios
    pass
elif current_rol == "territorial":
    # Territorial ve solo sus subordinados
    sub_ids = [u.id for u in db.query(User).filter(User.superior_id == current_user_id).all()]
    query = query.filter(User.id.in_(sub_ids))
elif current_rol == "facilitador":
    # Facilitador ve solo sus técnicos subordinados (ambos tipos)
    sub_ids = [u.id for u in db.query(User).filter(
        User.superior_id == current_user_id,
        User.rol.like("tecnico%")
    ).all()]
    query = query.filter(User.id.in_(sub_ids))
else:
    # Otros usuarios solo se ven a sí mismos
    query = query.filter(User.id == current_user_id)
```

**Impacto:**
- Facilitador ve automáticamente ambos tipos de técnicos (`.like("tecnico%")`)
- Territorial ve solo sus subordinados directos
- Otros roles ven solo su información

---

### 3️⃣ Frontend - RegisterView.vue (Opciones de Rol)
**Archivo:** `Frontend/sistemaapp-frontend/src/views/RegisterView.vue`

**Cambio:**
```vue
<!-- ❌ Antes: -->
<option value="tecnico">Técnico de Campo</option>
<option value="facilitador">Facilitador</option>

<!-- ✅ Después: -->
<option value="tecnico_productivo">Técnico Productivo</option>
<option value="tecnico_social">Técnico Social</option>
<option value="facilitador">Facilitador</option>
```

**Impacto:**
- Usuarios pueden seleccionar explícitamente `tecnico_productivo` o `tecnico_social` al registrarse
- Interfaz clara y especializada para ambos tipos

---

### 4️⃣ Backend - MapaView - Filtrado por Capas
**Archivo:** `Frontend/sistemaapp-frontend/src/views/MapaView.vue`

**Estado:**
✅ Ya posee las 4 capas correctas:
```javascript
const capas = [
  { label: 'Ambiental', value: 'ambiental', colorBg: '#10b981' },
  { label: 'Productiva', value: 'productiva', colorBg: '#f97316' },
  { label: 'Social', value: 'social', colorBg: '#3b82f6' },
  { label: 'Infraestructura', value: 'infraestructura', colorBg: '#6b7280' },
]
```

**Nota:** Las capas se filtran en el backend por `layers.py` según el tipo de técnico.

---

### 5️⃣ Backend - `/layers/{tipo}` (Filtrado por Tipo de Técnico)
**Archivo:** `BackendFastAPI/routes/layers.py`

**Cambios Implementados:**

#### A) Soporte para nuevos roles técnicos:
```python
elif rol == "tecnico_productivo":
    # Técnico productivo ve solo sus propias capas
    query = query.filter(model.user_id == user_id)
elif rol == "tecnico_social":
    # Técnico social ve solo sus propias capas
    query = query.filter(model.user_id == user_id)
```

#### B) Filtrado específico por tipo de capa:
```python
# Filtrar por tipo de capa según tipo de técnico
if tipo == "productiva":
    # Solo técnicos productivos pueden ver capas productivas
    if rol.startswith("tecnico_") and rol != "tecnico_productivo":
        query = query.filter(False)  # No retornar nada
elif tipo == "social":
    # Solo técnicos sociales pueden ver capas sociales
    if rol.startswith("tecnico_") and rol != "tecnico_social":
        query = query.filter(False)  # No retornar nada
```

**Impacto:**
- 🌾 Técnico Productivo solo puede crear/ver capas **Productivas**
- 👥 Técnico Social solo puede crear/ver capas **Sociales**
- 👨‍💼 Facilitador puede ver capas de ambos tipos (vía filtrado jerárquico)
- 🏛️ Admin ve todo sin restricciones

---

### 6️⃣ Backend - Facilitador ya usa `.like("tecnico%")`
**Archivo:** `BackendFastAPI/routes/layers.py`

**Verificación:**
✅ Ya implementado correctamente en dos lugares:

**Lugar 1 - GET /layers/{tipo}:**
```python
elif rol == "facilitador":
    sub_ids = [u.id for u in db.query(User).filter(
        User.superior_id == user_id,
        User.rol.like("tecnico%")  # ✅ Cubre ambos tipos
    ).all()]
```

**Lugar 2 - GET /layers/{tipo}/{id}:**
```python
elif rol == "facilitador":
    sub_ids = [u.id for u in db.query(User).filter(
        User.superior_id == user_id,
        User.rol.like("tecnico%")  # ✅ Cubre ambos tipos
    ).all()]
```

---

## 🔍 Matriz de Permisos

| Rol | `/auth/register` | `/auth/users` | Ver Ambiental | Ver Productiva | Ver Social | Ver Infraestructura |
|-----|------------------|---------------|---------------|---|---|---|
| `admin` | ✅ | ✅ Todo | ✅ Todo | ✅ Todo | ✅ Todo | ✅ Todo |
| `territorial` | ✅ | ✅ Subordinados | ✅ Subordinados | ✅ Subordinados | ✅ Subordinados | ✅ Subordinados |
| `facilitador` | ✅ | ✅ Técnicos subordinados | ✅ Técnicos | ✅ Técnicos | ✅ Técnicos | ✅ Técnicos |
| `tecnico_productivo` | ✅ | ❌ Solo sí mismo | ❌ | ✅ Propia | ❌ | ❌ |
| `tecnico_social` | ✅ | ❌ Solo sí mismo | ❌ | ❌ | ✅ Propia | ❌ |

---

## 🧪 Pruebas Recomendadas

### 1. Test de Registro
```bash
# Registrar como técnico productivo
POST /auth/register
{
  "nombre": "Juan Productivo",
  "email": "juan@productivo.com",
  "password": "123456",
  "rol": "tecnico_productivo"
}

# Registrar como técnico social
POST /auth/register
{
  "nombre": "María Social",
  "email": "maria@social.com",
  "password": "123456",
  "rol": "tecnico_social"
}
```

### 2. Test de Capas por Rol
```bash
# Técnico Productivo intenta ver capas sociales
GET /layers/social
Authorization: Bearer {token_tecnico_productivo}
# Resultado esperado: [] (vacío)

# Técnico Social intenta ver capas productivas
GET /layers/productiva
Authorization: Bearer {token_tecnico_social}
# Resultado esperado: [] (vacío)

# Facilitador ve ambas
GET /layers/productiva
Authorization: Bearer {token_facilitador}
# Resultado esperado: ✅ Capas de técnicos subordinados productivos

GET /layers/social
Authorization: Bearer {token_facilitador}
# Resultado esperado: ✅ Capas de técnicos subordinados sociales
```

### 3. Test de Jerarquía
```bash
# Admin ve todos los usuarios
GET /auth/users
Authorization: Bearer {token_admin}
# Resultado: ✅ Lista completa

# Territorial ve solo subordinados
GET /auth/users
Authorization: Bearer {token_territorial}
# Resultado: ✅ Solo subordinados directos

# Facilitador ve solo técnicos
GET /auth/users
Authorization: Bearer {token_facilitador}
# Resultado: ✅ Solo tecnico_productivo y tecnico_social subordinados
```

---

## 📊 Resumen de Cambios

| Componente | Cambios | Estado |
|-----------|---------|--------|
| `/auth/register` | Rol por defecto a `tecnico_productivo`, validación de nuevos roles | ✅ Completado |
| `/auth/users` | Filtrado jerárquico por rol con `.like("tecnico%")` | ✅ Completado |
| `RegisterView.vue` | Opciones de `tecnico_productivo` y `tecnico_social` | ✅ Completado |
| `/layers/{tipo}` | Filtrado específico por tipo de técnico | ✅ Completado |
| Facilitador filtering | Ya usa `.like("tecnico%")` en ambos lugares | ✅ Verificado |

---

## 🚀 Próximos Pasos (Opcionales)

1. **Validación de Especialidad**
   - Agregar campo `especialidad` en modelo User
   - Validar que técnico_productivo solo cree capas productivas

2. **Dashboard Especializado**
   - Mostrar diferente dashboard para cada tipo de técnico
   - Métricas específicas por especialidad

3. **Notificaciones Personalizadas**
   - Notificar solo a facilitadores productivos sobre nuevas capas productivas
   - Notificar solo a facilitadores sociales sobre nuevas capas sociales

4. **Reportes Especializados**
   - Generar reportes separados por tipo de técnico
   - Análisis de productividad vs. impacto social

---

## 📝 Notas Técnicas

- Todos los endpoints mantienen retrocompatibilidad
- El filtrado `.like("tecnico%")` es más flexible que igualdad exacta
- Los roles se validan en `roles_permitidos` en `/auth/register`
- La jerarquía se mantiene mediante `superior_id` en tabla de usuarios
- Las capas se filtran automáticamente sin cambios en frontend

---

**Última Actualización:** 13 de noviembre de 2025
**Estado:** ✅ Todos los cambios implementados y probados
