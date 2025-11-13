# 🚀 Guía Rápida - CRUD Sembradores

## ✅ Implementación Completada

Se ha agregado un sistema completo de gestión de **Sembradores** con:

- ✅ Modelo en BD (`Sembrador`)
- ✅ 5 Endpoints CRUD (POST, GET, GET by ID, PUT, DELETE)
- ✅ Jerarquía de permisos (admin, territorial, facilitador, técnico)
- ✅ Validaciones y seguridad
- ✅ Geolocalización (lat/lng)

---

## 📝 Cambios Realizados

### 1. Modelo Agregado (models.py)

```python
class Sembrador(Base):
    __tablename__ = "sembradores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    comunidad = Column(String(100))
    cultivo_principal = Column(String(100))
    telefono = Column(String(30))
    lat = Column(Float)
    lng = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
```

**Status:** ✅ Agregado a `models.py`

### 2. Rutas CRUD Creadas (sembradores.py)

- ✅ `POST /sembradores/` - Crear
- ✅ `GET /sembradores/` - Listar (con filtrado jerárquico)
- ✅ `GET /sembradores/{id}` - Obtener uno
- ✅ `PUT /sembradores/{id}` - Actualizar
- ✅ `DELETE /sembradores/{id}` - Eliminar

**Status:** ✅ Archivo creado: `routes/sembradores.py`

### 3. Ruta Registrada (main.py)

**Cambios:**
- Línea 2: Importación de `sembradores`
- Línea 26: `app.include_router(sembradores.router)`

**Status:** ✅ Registrado en `main.py`

---

## 📊 Endpoints Disponibles

| Método | URL | Descripción | Auth |
|--------|-----|-------------|------|
| POST | `/sembradores/` | Crear sembrador | ✅ |
| GET | `/sembradores/` | Listar sembradores | ✅ |
| GET | `/sembradores/{id}` | Obtener uno | ✅ |
| PUT | `/sembradores/{id}` | Actualizar | ✅ |
| DELETE | `/sembradores/{id}` | Eliminar | ✅ |

---

## 🔐 Jerarquía de Acceso

```
┌─────────────┐
│    Admin    │  Ve TODOS los sembradores
└─────────────┘
      │
      ├─────────────────────────────────┐
      │                                 │
┌─────▼──────────┐           ┌──────────▼──────┐
│ Territorial    │           │ Facilitador     │
│ Ve subordinados│           │ Ve sus técnicos │
└────────────────┘           └─────────────────┘
      │                              │
      ├──────────────────────────────┤
      │                              │
┌─────▼──────────────────┐  ┌────────▼──────────────────┐
│ Técnico Productivo     │  │ Técnico Social           │
│ Ve solo sus sembradores│  │ Ve solo sus sembradores  │
└────────────────────────┘  └──────────────────────────┘
```

---

## 🧪 Test Rápido

### 1. Crear un Sembrador

```bash
curl -X POST http://localhost:8000/sembradores/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{\n    "nombre": "Juan Pérez",\n    "comunidad": "La Esperanza",\n    "cultivo_principal": "Maíz",\n    "telefono": "+56912345678",\n    "lat": -33.8688,\n    "lng": -51.2093\n  }'\n\n# Esperado: Status 200\n# Response: {"success": true, "id": 1, "nombre": "Juan Pérez", "message": "..."}
```

### 2. Listar Sembradores

```bash
curl -X GET http://localhost:8000/sembradores/ \
  -H "Authorization: Bearer {token}"\n\n# Esperado: Status 200\n# Response: {"total": 1, "items": [...]}\n```

### 3. Obtener Sembrador Específico

```bash
curl -X GET http://localhost:8000/sembradores/1 \
  -H "Authorization: Bearer {token}"\n\n# Esperado: Status 200\n# Response: {id, nombre, comunidad, ...}\n```

### 4. Actualizar Sembrador

```bash
curl -X PUT http://localhost:8000/sembradores/1 \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{\"nombre\": \"Juan Carlos Pérez\"}'\n\n# Esperado: Status 200\n```

### 5. Eliminar Sembrador

```bash
curl -X DELETE http://localhost:8000/sembradores/1 \
  -H "Authorization: Bearer {token}"\n\n# Esperado: Status 200\n# Response: {"success": true, "message": "..."}\n```

---

## ✨ Características

✅ **CRUD Completo** - Crear, leer, actualizar, eliminar
✅ **Jerarquía** - Permisos según rol del usuario
✅ **Geolocalización** - Latitud y longitud
✅ **Contacto** - Teléfono del sembrador
✅ **Timestamps** - Fecha de creación automática
✅ **Validaciones** - Campos requeridos verificados
✅ **Seguridad** - JWT + filtrado por usuario_id

---

## 📁 Archivos Modificados

| Archivo | Cambios | Status |
|---------|---------|--------|
| `models.py` | Agregado clase Sembrador | ✅ |
| `routes/sembradores.py` | Creado (nuevo archivo) | ✅ |
| `main.py` | Agregada importación y router | ✅ |

---

## 🚀 Próximos Pasos

### Inmediato (Hoy)
1. ✅ Reiniciar backend
2. ✅ Probar endpoints con Postman/cURL
3. ✅ Verificar que se crea tabla en BD

### Corto Plazo (Esta Semana)
1. Crear migración de BD (Alembic)
2. Crear vista de sembradores en frontend
3. Agregar formulario de captura

### Mediano Plazo
1. Dashboard de sembradores
2. Mapa interactivo
3. Reportes

---

## 📚 Documentación Completa

Para más detalles, revisa:
- `SEMBRADORES_CRUD_DOCUMENTACION.md` - Documentación técnica completa

---

## ✅ Checklist de Verificación

- [x] Modelo `Sembrador` agregado a `models.py`
- [x] 5 Endpoints CRUD implementados
- [x] Jerarquía de permisos configurable
- [x] Ruta registrada en `main.py`
- [x] Validaciones de campos
- [x] Manejo de errores
- [x] Documentación generada

---

**Status:** ✅ IMPLEMENTADO Y LISTO
**Fecha:** 13 de noviembre de 2025
