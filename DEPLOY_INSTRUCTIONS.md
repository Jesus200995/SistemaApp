# 🚀 Instrucciones de Despliegue - Backend

## El problema actual

El servidor remoto (`sistemaapi.sembrandodatos.com`) tiene una versión antigua del backend que:
1. No tiene la configuración CORS actualizada
2. Está devolviendo errores 500 en `/notificaciones/`

## Solución: Desplegar el backend actualizado

### Opción 1: Por SSH (recomendado)

```bash
# Conectar al servidor
ssh root@31.97.8.51

# Navegar al directorio del backend
cd /ruta/al/backend

# Hacer pull de los cambios
git pull origin main

# Reiniciar el servicio
systemctl restart sistemaapp
# o si usas uvicorn directamente:
# pkill -f uvicorn && uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### Opción 2: Copiar archivos manualmente

Si no tienes git configurado en el servidor:

```bash
# Desde tu máquina local, copiar los archivos actualizados
scp -r BackendFastAPI/* root@31.97.8.51:/ruta/al/backend/
```

### Opción 3: Actualizar directamente en el servidor

Conecta por SSH y edita `main.py`:

```python
# Cambiar la configuración CORS a:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

## Verificar que funciona

Después de desplegar, prueba:

```bash
curl -X GET "https://sistemaapi.sembrandodatos.com/notificaciones/" \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Origin: http://localhost:5173"
```

Debería devolver los headers CORS:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: *`

## Archivos modificados que necesitan desplegarse

1. `BackendFastAPI/main.py` - Configuración CORS mejorada
2. (Opcional) `BackendFastAPI/routes/notificaciones.py` - Si hay errores en la BD

## Nota importante

El error 500 puede ser causado por:
1. La tabla `notificaciones` no existe en la BD del servidor
2. Faltan columnas en la tabla (como `user_destino`, `solicitud_id`)

Para verificar y crear la tabla:

```sql
-- En PostgreSQL
CREATE TABLE IF NOT EXISTS notificaciones (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    rol_destino VARCHAR(50),
    user_destino INTEGER REFERENCES users(id),
    leido BOOLEAN DEFAULT FALSE,
    usuario_id INTEGER REFERENCES users(id),
    solicitud_id INTEGER REFERENCES solicitudes(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    actualizado_en TIMESTAMP WITH TIME ZONE
);
```

O simplemente reinicia la API con:
```python
Base.metadata.create_all(bind=engine)
```
