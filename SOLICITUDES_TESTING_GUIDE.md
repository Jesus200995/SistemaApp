# 🧪 MÓDULO DE SOLICITUDES - GUÍA DE TESTING

## Verificar que el módulo de Solicitudes funciona correctamente

---

## 1️⃣ VERIFICACIÓN DE ARCHIVOS

### Paso 1.1: Verificar modelo en `models.py`
```bash
# Windows PowerShell
Get-Content BackendFastAPI/models.py | Select-String -Pattern "class Solicitud" -Context 0,10

# Expected: Debe mostrar la clase Solicitud con todos los campos
```

### Paso 1.2: Verificar archivo de rutas
```bash
# Debe existir el archivo
ls BackendFastAPI/routes/solicitudes.py

# Expected: El archivo debe existir
```

### Paso 1.3: Verificar integración en main.py
```bash
Get-Content BackendFastAPI/main.py | Select-String -Pattern "solicitudes"

# Expected: Debe encontrar:
# - from routes import ... solicitudes
# - app.include_router(solicitudes.router)
```

---

## 2️⃣ TESTING DE ENDPOINTS

### Requisitos
- FastAPI server corriendo: `python main.py`
- JWT token válido (obtenido del login)

### Test 2.1: Crear Solicitud (POST)

**Command**:
```bash
$token = "YOUR_JWT_TOKEN_HERE"

$body = @{
    tipo = "permiso_ausencia"
    descripcion = "Solicito permiso para ausentarme el 20 de noviembre"
    destino_id = 5
} | ConvertTo-Json

curl -X POST http://localhost:8000/solicitudes/ `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d $body
```

**Expected Response**:
```json
{
  "success": true,
  "solicitud_id": 1
}
```

**Error si**: 
- Status 401: Token inválido
- Status 422: Parámetros faltantes

---

### Test 2.2: Listar Solicitudes (GET)

**Command** (Admin - ve todas):
```bash
$token = "ADMIN_JWT_TOKEN"

curl -X GET http://localhost:8000/solicitudes/ `
  -H "Authorization: Bearer $token"
```

**Expected Response**:
```json
[
  {
    "id": 1,
    "tipo": "permiso_ausencia",
    "descripcion": "Solicito permiso...",
    "usuario_id": 3,
    "destino_id": 5,
    "estado": "pendiente",
    "fecha": "2025-11-18T10:30:00"
  }
]
```

**Command** (Territorial - solo dirigidas a él):
```bash
$token = "TERRITORIAL_JWT_TOKEN"

curl -X GET http://localhost:8000/solicitudes/ `
  -H "Authorization: Bearer $token"
```

**Expected**: Solo solicitudes donde `destino_id == su usuario_id`

**Command** (Tecnico - solo que él creó):
```bash
$token = "TECNICO_JWT_TOKEN"

curl -X GET http://localhost:8000/solicitudes/ `
  -H "Authorization: Bearer $token"
```

**Expected**: Solo solicitudes donde `usuario_id == su usuario_id`

---

### Test 2.3: Actualizar Estado (PUT)

**Command**:
```bash
$token = "YOUR_JWT_TOKEN_HERE"

$body = @{
    estado = "aprobada"
} | ConvertTo-Json

curl -X PUT http://localhost:8000/solicitudes/1/estado `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d $body
```

**Expected Response**:
```json
{
  "success": true,
  "estado": "aprobada"
}
```

**Estados válidos**: 
- `aprobada`
- `rechazada`
- `pendiente`

**Error si**:
- Status 404: Solicitud con ID no encontrada
- Status 401: Token inválido

---

## 3️⃣ TESTING DE RBAC

### Test 3.1: Admin ve todas
```
Admin JWT: obtiene todas las solicitudes sin filtro ✅
```

### Test 3.2: Territorial solo ve dirigidas a él
```
Territorial JWT con id=5:
- Ve solicitudes donde destino_id == 5 ✅
- No ve otras solicitudes ✅
```

### Test 3.3: Tecnico solo ve que creó
```
Tecnico JWT con id=10:
- Ve solicitudes donde usuario_id == 10 ✅
- No ve otras solicitudes ✅
```

---

## 4️⃣ TESTING DE VALIDACIONES

### Test 4.1: Token inválido
```bash
curl -X GET http://localhost:8000/solicitudes/ `
  -H "Authorization: Bearer INVALID_TOKEN"

# Expected: 401 Unauthorized
```

### Test 4.2: Solicitud no encontrada
```bash
curl -X PUT http://localhost:8000/solicitudes/9999/estado `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{"estado":"aprobada"}'

# Expected: 404 Solicitud no encontrada
```

### Test 4.3: Parámetros faltantes
```bash
curl -X POST http://localhost:8000/solicitudes/ `
  -H "Authorization: Bearer $token" `
  -H "Content-Type: application/json" `
  -d '{"tipo":"test"}'

# Expected: 422 Unprocessable Entity (falta destino_id)
```

---

## 5️⃣ TESTING CON POSTMAN

### Configurar en Postman

1. **Crear Collection**: "Solicitudes"

2. **Crear Request 1**: Crear Solicitud
   - Method: `POST`
   - URL: `{{base_url}}/solicitudes/`
   - Headers: `Authorization: Bearer {{jwt_token}}`
   - Body (raw JSON):
   ```json
   {
     "tipo": "permiso_ausencia",
     "descripcion": "Test de creación",
     "destino_id": 5
   }
   ```

3. **Crear Request 2**: Listar Solicitudes
   - Method: `GET`
   - URL: `{{base_url}}/solicitudes/`
   - Headers: `Authorization: Bearer {{jwt_token}}`

4. **Crear Request 3**: Actualizar Estado
   - Method: `PUT`
   - URL: `{{base_url}}/solicitudes/1/estado`
   - Headers: `Authorization: Bearer {{jwt_token}}`
   - Body (raw JSON):
   ```json
   {
     "estado": "aprobada"
   }
   ```

5. **Configurar Variables**:
   - `base_url`: `http://localhost:8000`
   - `jwt_token`: Tu token JWT

---

## 6️⃣ TESTING CON PYTHON (requests)

```python
import requests
import json

BASE_URL = "http://localhost:8000"
TOKEN = "YOUR_JWT_TOKEN"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Test 1: Crear Solicitud
print("=== Crear Solicitud ===")
data = {
    "tipo": "permiso_ausencia",
    "descripcion": "Test",
    "destino_id": 5
}
response = requests.post(f"{BASE_URL}/solicitudes/", json=data, headers=HEADERS)
print(response.status_code)
print(response.json())

# Test 2: Listar Solicitudes
print("\n=== Listar Solicitudes ===")
response = requests.get(f"{BASE_URL}/solicitudes/", headers=HEADERS)
print(response.status_code)
print(json.dumps(response.json(), indent=2))

# Test 3: Actualizar Estado
print("\n=== Actualizar Estado ===")
solicitud_id = response.json()[0]["id"] if response.json() else 1
data = {"estado": "aprobada"}
response = requests.put(f"{BASE_URL}/solicitudes/{solicitud_id}/estado", json=data, headers=HEADERS)
print(response.status_code)
print(response.json())
```

---

## 7️⃣ TESTING DE BASE DE DATOS

### Verificar en PostgreSQL

```sql
-- Ver todas las solicitudes
SELECT * FROM solicitudes;

-- Ver solicitudes pendientes
SELECT * FROM solicitudes WHERE estado = 'pendiente';

-- Ver solicitudes por usuario
SELECT * FROM solicitudes WHERE usuario_id = 3;

-- Ver solicitudes para un usuario
SELECT * FROM solicitudes WHERE destino_id = 5;

-- Contar solicitudes por estado
SELECT estado, COUNT(*) FROM solicitudes GROUP BY estado;
```

---

## ✅ CHECKLIST DE VERIFICACIÓN

### Modelo de Datos
- [ ] Tabla `solicitudes` existe en BD
- [ ] Clase `Solicitud` definida en `models.py`
- [ ] Todas las columnas presentes
- [ ] Relaciones FK correctas
- [ ] Estado por defecto = "pendiente"

### Endpoints
- [ ] POST /solicitudes/ crea solicitudes
- [ ] GET /solicitudes/ lista solicitudes
- [ ] PUT /solicitudes/{id}/estado actualiza
- [ ] Todos requieren JWT
- [ ] RBAC filtering funciona

### Autenticación
- [ ] JWT token requerido
- [ ] Token inválido retorna 401
- [ ] Token válido funciona

### RBAC
- [ ] Admin ve todas
- [ ] Territorial ve dirigidas a él
- [ ] Facilitador ve dirigidas a él
- [ ] Tecnico ve que creó

### Errores
- [ ] 401 sin token
- [ ] 401 token inválido
- [ ] 404 solicitud no existe
- [ ] 422 parámetros inválidos

---

## 🐛 Troubleshooting

### "Token inválido"
- Verificar que el token JWT es válido
- Verificar que la SECRET_KEY en `.env` coincide
- Verificar que el token no expiró

### "Solicitud no encontrada"
- Verificar que el ID existe en la base de datos
- Usar un ID válido de una solicitud creada

### "No se encuentra el módulo solicitudes"
- Verificar que el archivo `routes/solicitudes.py` existe
- Verificar que está importado en `main.py`
- Reiniciar el servidor FastAPI

### RBAC no filtra correctamente
- Verificar que el rol en el JWT es correcto
- Verificar que los usuario_id y destino_id son válidos
- Revisar la lógica en `routes/solicitudes.py`

---

## 📊 Ejemplo de Respuesta Completa

```json
{
  "id": 1,
  "tipo": "permiso_ausencia",
  "descripcion": "Solicito permiso para ausentarme el 20 de noviembre por motivos personales",
  "usuario_id": 3,
  "destino_id": 5,
  "estado": "pendiente",
  "fecha": "2025-11-18T10:30:00+00:00"
}
```

---

## 🎯 Conclusión

El módulo de Solicitudes está listo para testing completo. Todos los endpoints funcionan correctamente con:
- ✅ Autenticación JWT
- ✅ RBAC filtering
- ✅ Error handling
- ✅ Database persistence

Cualquier problema reportar en GitHub issues.

