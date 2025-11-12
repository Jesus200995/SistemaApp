# 🏗️ Arquitectura - API de Capas Temáticas

## Flujo de datos

```
┌─────────────────┐
│  Frontend Vue   │
│  (MapaView.vue) │
└────────┬────────┘
         │
         │ HTTP Request + JWT Token
         │
         ▼
┌─────────────────────────────────┐
│      FastAPI Server             │
│      (puerto 9000)              │
│                                 │
│  ┌───────────────────────────┐  │
│  │  CORS Middleware          │  │
│  │  - localhost:5173         │  │
│  │  - sistemaapp.com         │  │
│  └───────────────────────────┘  │
│                                 │
│  ┌───────────────────────────┐  │
│  │  Rutas / Routers          │  │
│  │  - /auth (autenticación)  │  │
│  │  - /layers (capas)  ◄─── NEW
│  │  - /users (usuarios)      │  │
│  └───────────────────────────┘  │
└────────┬────────────────────────┘
         │
         │ Queries SQL
         │
         ▼
┌─────────────────────────────────┐
│   PostgreSQL Database           │
│   (31.97.8.51:5432)            │
│                                 │
│  Tables:                        │
│  ├── users                      │
│  ├── ambiental      ◄─── NEW
│  ├── productiva     ◄─── NEW
│  ├── social         ◄─── NEW
│  └── infraestructura ◄─── NEW
└─────────────────────────────────┘
```

---

## Estructura de carpetas

```
BackendFastAPI/
│
├── main.py                      ← Entrada principal de la app
│   └── include_router(auth)
│   └── include_router(layers)   ← NEW
│
├── database.py                  ← Conexión PostgreSQL
│   └── SessionLocal
│   └── get_db()
│
├── models.py                    ← Modelos SQLAlchemy
│   ├── User
│   ├── Ambiental       ◄─── NEW
│   ├── Productiva      ◄─── NEW
│   ├── Social          ◄─── NEW
│   └── Infraestructura ◄─── NEW
│
├── requirements.txt             ← Dependencias Python
│
└── routes/                      ← Routers / Endpoints
    ├── __init__.py
    ├── auth.py                  ← /auth/login, /auth/register, etc.
    ├── users.py                 ← /auth/users, /auth/users/{id}
    └── layers.py        ◄─── NEW
        ├── GET    /layers/{tipo}
        ├── POST   /layers/{tipo}
        ├── GET    /layers/{tipo}/{id}
        ├── PUT    /layers/{tipo}/{id}
        └── DELETE /layers/{tipo}/{id}
```

---

## Modelos de datos

### Tabla: `ambiental`
```sql
CREATE TABLE ambiental (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  lat FLOAT NOT NULL,
  lng FLOAT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Tabla: `productiva`
```sql
CREATE TABLE productiva (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  lat FLOAT NOT NULL,
  lng FLOAT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Tabla: `social`
```sql
CREATE TABLE social (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  lat FLOAT NOT NULL,
  lng FLOAT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Tabla: `infraestructura`
```sql
CREATE TABLE infraestructura (
  id INTEGER PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  lat FLOAT NOT NULL,
  lng FLOAT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Flujo de autenticación

```
┌────────────────────────────────────────┐
│  1. Usuario ingresa credenciales       │
│     POST /auth/login                   │
│     Body: {"email": "...", "pwd": "..."}
└────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│  2. Backend valida credenciales        │
│     - Busca usuario en DB              │
│     - Verifica contraseña con bcrypt   │
└────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│  3. Genera JWT Token                   │
│     jwt.encode({                       │
│       "sub": user_id,                  │
│       "email": email,                  │
│       "iat": timestamp                 │
│     }, SECRET, algorithm="HS256")      │
└────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│  4. Retorna token al frontend          │
│     Response: {"access_token": "..."}  │
└────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│  5. Frontend almacena token            │
│     localStorage.setItem("token", ...)│
└────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│  6. En cada request a /layers:         │
│     GET /layers/ambiental              │
│     Headers: {                         │
│       "Authorization": "Bearer <token>"│
│     }                                  │
└────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│  7. Backend valida token               │
│     jwt.decode(token, SECRET)          │
│     ¿Token válido?                     │
│     ├─ Sí → Procesa la solicitud       │
│     └─ No → 401 Unauthorized           │
└────────────────────────────────────────┘
```

---

## Flujo de operaciones CRUD

### CREATE (POST /layers/{tipo})

```
Cliente                    Backend                    DB
  │                          │                        │
  ├─ POST /layers/ambiental  │                        │
  │ + JWT Token              │                        │
  │ + {nombre, lat, lng}     │                        │
  ├────────────────────────>│                        │
  │                          ├─ Valida token         │
  │                          │                        │
  │                          ├─ Valida datos         │
  │                          │                        │
  │                          ├─ INSERT INTO ambiental│
  │                          ├───────────────────────>│
  │                          │                        ├─ INSERT OK
  │                          │ <───────────────────────┤
  │                          │                        │
  │ <200 OK                  │                        │
  │ {success, id}            │                        │
  │<────────────────────────┤                        │
```

### READ (GET /layers/{tipo})

```
Cliente                    Backend                    DB
  │                          │                        │
  ├─ GET /layers/ambiental   │                        │
  │ + JWT Token              │                        │
  ├────────────────────────>│                        │
  │                          ├─ Valida token         │
  │                          │                        │
  │                          ├─ SELECT * FROM ambiental
  │                          ├───────────────────────>│
  │                          │ <────────────────────────┤ rows
  │                          │                        │
  │ <200 OK                  │                        │
  │ {items: []}              │                        │
  │<────────────────────────┤                        │
```

### UPDATE (PUT /layers/{tipo}/{id})

```
Cliente                    Backend                    DB
  │                          │                        │
  ├─ PUT /layers/ambiental/1 │                        │
  │ + JWT Token              │                        │
  │ + {nombre, descripción}  │                        │
  ├────────────────────────>│                        │
  │                          ├─ Valida token         │
  │                          │                        │
  │                          ├─ UPDATE ambiental     │
  │                          ├───────────────────────>│
  │                          │                        ├─ UPDATE OK
  │                          │ <───────────────────────┤
  │                          │                        │
  │ <200 OK                  │                        │
  │ {success, item}          │                        │
  │<────────────────────────┤                        │
```

### DELETE (DELETE /layers/{tipo}/{id})

```
Cliente                    Backend                    DB
  │                          │                        │
  ├─ DELETE /layers/ambiental/1
  │ + JWT Token              │                        │
  ├────────────────────────>│                        │
  │                          ├─ Valida token         │
  │                          │                        │
  │                          ├─ DELETE FROM ambiental│
  │                          ├───────────────────────>│
  │                          │                        ├─ DELETE OK
  │                          │ <───────────────────────┤
  │                          │                        │
  │ <200 OK                  │                        │
  │ {success}                │                        │
  │<────────────────────────┤                        │
```

---

## Stack tecnológico

```
┌──────────────────────────────────────┐
│           Frontend                   │
│  Vue 3 + TypeScript + Leaflet Maps   │
│  (MapaView.vue)                      │
└────────────────┬─────────────────────┘
                 │ HTTP/JSON
┌────────────────▼─────────────────────┐
│           Backend                    │
│  FastAPI + Uvicorn                   │
│  - Async/Await                       │
│  - JWT Authentication                │
│  - CORS Middleware                   │
│  - REST API                          │
└────────────────┬─────────────────────┘
                 │ SQL Queries
┌────────────────▼─────────────────────┐
│           Database                   │
│  PostgreSQL 12+                      │
│  (31.97.8.51:5432)                   │
└──────────────────────────────────────┘
```

---

## Variables de entorno requeridas

```env
# Database
DATABASE_URL=postgresql://usuario:password@31.97.8.51:5432/SistemaApp

# Security
SECRET_KEY=tu_secret_key_muy_seguro_aleatorio_12345

# API
API_HOST=0.0.0.0
API_PORT=9000
```

---

## Seguridad implementada

✅ **CORS** - Solo se permiten requests de dominios autorizados
✅ **JWT** - Tokens firmados con SECRET_KEY
✅ **HTTPBearer** - Validación de tokens en headers
✅ **Password Hashing** - bcrypt para contraseñas
✅ **SQL Injection Prevention** - SQLAlchemy ORM
✅ **HTTPS Ready** - Funciona con SSL/TLS en producción

---

## Monitoreo y debugging

```bash
# Ver logs en tiempo real
tail -f uvicorn.log

# Ver Swagger API docs
http://localhost:9000/docs

# Ver ReDoc API docs
http://localhost:9000/redoc

# Ver health check
curl http://localhost:9000/
```

---

## Performance

- **FastAPI** → Muy rápido (ASGI async)
- **PostgreSQL** → Índices en IDs
- **Caching potencial** → RedisCache en futuro
- **Paginación** → Implementable en futuro

