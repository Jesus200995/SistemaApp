# 🚀 Despliegue - Sistema de Notificaciones

**Versión:** 1.0  
**Fecha:** 12 de noviembre de 2025  
**Entorno:** Producción (VPS)

---

## 📋 Pre-requisitos

- [ ] VPS con IP: 31.97.8.51
- [ ] PostgreSQL corriendo en puerto 5432
- [ ] Python 3.9+
- [ ] Node.js 18+
- [ ] Git actualizado
- [ ] HTTPS configurado (para WSS)

---

## 🔧 Despliegue Backend

### Paso 1: Actualizar código en VPS

```bash
# Conectar al servidor
ssh root@31.97.8.51

# Ir a carpeta del proyecto
cd /var/www/SistemaApp/BackendFastAPI

# Actualizar desde git (o copiar archivos)
git pull origin main
# O: scp -r . root@31.97.8.51:/var/www/SistemaApp/BackendFastAPI/
```

### Paso 2: Instalar dependencias nuevas

```bash
source venv/bin/activate
pip install broadcaster[postgresql] python-socketio

# Verificar que todo está OK
python -c "from routes import notificaciones; print('✅ OK')"
```

### Paso 3: Actualizar base de datos

```bash
# Las tablas se crean automáticamente al iniciar FastAPI
python -c "from database import Base, engine; from models import *; Base.metadata.create_all(bind=engine); print('✅ BD actualizada')"
```

### Paso 4: Verificar configuración

```bash
# Revisar .env
cat .env | grep -E "DATABASE_URL|JWT_SECRET"

# Esperado:
# DATABASE_URL=postgresql://jesus:2025@31.97.8.51:5432/SistemaApp
# JWT_SECRET=tu_clave_secreta
```

### Paso 5: Reiniciar servicio

```bash
# Si usa pm2
pm2 restart SistemaAppFast
pm2 status

# Si usa systemd
systemctl restart sistemapp-backend
systemctl status sistemapp-backend

# Verificar que está corriendo
curl https://sistemaapi.sembrandodatos.com/notificaciones/status/info
```

**Esperado:**
```json
{
  "clientes_conectados": 0,
  "status": "✅ Sistema de notificaciones funcionando correctamente"
}
```

---

## 🎨 Despliegue Frontend

### Paso 1: Actualizar código

```bash
# Conectar al servidor
ssh root@31.97.8.51

# Ir a carpeta del proyecto
cd /var/www/SistemaApp/Frontend/sistemaapp-frontend

# Actualizar desde git
git pull origin main
```

### Paso 2: Instalar dependencias (si las hay nuevas)

```bash
npm install
```

### Paso 3: Build para producción

```bash
npm run build

# Esperado: Carpeta dist/ creada
ls -la dist/
```

### Paso 4: Configurar .env producción

```bash
# Editar archivo .env
cat > .env.production << EOF
VITE_API_URL=https://sistemaapi.sembrandodatos.com
VITE_APP_NAME=SistemaApp
EOF

# O actualizar existente
sed -i 's|VITE_API_URL=.*|VITE_API_URL=https://sistemaapi.sembrandodatos.com|' .env
```

### Paso 5: Desplegar en servidor web

```bash
# Si usa Nginx
cp -r dist/* /var/www/html/sistemaapp/

# Si usa Apache
cp -r dist/* /var/www/sistemaapp/

# Verificar permisos
chmod -R 755 /var/www/html/sistemaapp/
```

### Paso 6: Recargar servidor web

```bash
# Nginx
nginx -t && systemctl reload nginx

# Apache
apache2ctl configtest && systemctl reload apache2
```

---

## 🔐 Configuración HTTPS/WSS

### Nginx (recomendado)

```nginx
# /etc/nginx/sites-available/sistemaapi.sembrandodatos.com

upstream fastapi {
    server 127.0.0.1:9000;
}

server {
    listen 443 ssl http2;
    server_name sistemaapi.sembrandodatos.com;

    ssl_certificate /etc/letsencrypt/live/sistemaapi.sembrandodatos.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sistemaapi.sembrandodatos.com/privkey.pem;

    # WebSocket
    location /notificaciones/ws {
        proxy_pass http://fastapi;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }

    # Chat WebSocket
    location /chat/ws {
        proxy_pass http://fastapi;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }

    # API REST
    location /api/ {
        proxy_pass http://fastapi;
        proxy_set_header Host $host;
    }
}

# Redireccionar HTTP a HTTPS
server {
    listen 80;
    server_name sistemaapi.sembrandodatos.com;
    return 301 https://$server_name$request_uri;
}
```

### Verificar SSL

```bash
# Probar certificado
curl https://sistemaapi.sembrandodatos.com/notificaciones/status/info

# Verificar WSS
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
  https://sistemaapi.sembrandodatos.com/notificaciones/ws
```

---

## ✅ Verificación Post-despliegue

### 1. Backend funcionando

```bash
curl https://sistemaapi.sembrandodatos.com/notificaciones/status/info
```

### 2. WebSocket conectando

```bash
# Usar websocat si está instalado
websocat wss://sistemaapi.sembrandodatos.com/notificaciones/ws

# O desde navegador console:
const ws = new WebSocket('wss://sistemaapi.sembrandodatos.com/notificaciones/ws')
console.log(ws)
```

### 3. REST API funcionando

```bash
TOKEN="tu_token_aqui"

curl -X GET https://sistemaapi.sembrandodatos.com/notificaciones/ \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Frontend cargando

```bash
curl https://sistemaapp.sembrandodatos.com/
```

### 5. Notificación end-to-end

```bash
# 1. Abrir frontend
# 2. Login en navegador
# 3. Ejecutar:
TOKEN="tu_token"
curl -X POST https://sistemaapi.sembrandodatos.com/notificaciones/crear \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Test","mensaje":"Test","tipo":"success","rol_destino":"all"}'

# 4. Ver notificación en navegador (debería aparecer inmediatamente)
```

---

## 📊 Monitoreo

### Logs backend

```bash
# Ver logs en tiempo real
pm2 logs SistemaAppFast

# O si usa systemd
journalctl -u sistemapp-backend -f

# Buscar errores
grep -i error /var/log/systemapp/*.log
```

### Logs frontend

```bash
# Ver logs del servidor web
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Monitoreo de conexiones WebSocket

```bash
# Contar conexiones activas
netstat -tuln | grep 9000

# Ver procesos Python
ps aux | grep uvicorn

# Ver estado en tiempo real
pm2 monit
```

---

## 🐛 Troubleshooting

### "Connection refused"

```bash
# Backend no está corriendo
pm2 restart SistemaAppFast
pm2 status

# Verificar puerto
lsof -i :9000
netstat -tuln | grep 9000
```

### "SSL certificate problem"

```bash
# Renovar certificado Let's Encrypt
certbot renew

# Verificar certificado
openssl s_client -connect sistemaapi.sembrandodatos.com:443
```

### "WebSocket handshake failed"

```bash
# Verificar Nginx config
nginx -t

# Recargar Nginx
systemctl reload nginx

# Verificar que WebSocket está permitido en proxy
grep "Connection.*upgrade" /etc/nginx/sites-available/sistemaapi.sembrandodatos.com
```

### "Database connection error"

```bash
# Verificar DATABASE_URL en .env
cat /var/www/SistemaApp/BackendFastAPI/.env

# Probar conexión a PostgreSQL
psql postgresql://jesus:2025@31.97.8.51:5432/SistemaApp -c "SELECT 1"
```

---

## 🔄 Rollback en caso de error

### Si algo sale mal

```bash
# 1. Revertir cambios
git checkout HEAD~1 BackendFastAPI/
git checkout HEAD~1 Frontend/sistemaapp-frontend/

# 2. Reinstalar dependencias antiguas
pip install -r requirements.txt.bak

# 3. Reiniciar servicios
pm2 restart SistemaAppFast
systemctl restart nginx

# 4. Verificar que todo funciona
curl https://sistemaapi.sembrandodatos.com/
```

---

## 📈 Optimización producción

### Nginx cache

```nginx
# Cache static assets
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### FastAPI workers

```bash
# Aumentar workers para más concurrencia
gunicorn -w 4 -b 0.0.0.0:9000 main:app

# O con uvicorn
uvicorn main:app --workers 4 --host 0.0.0.0 --port 9000
```

### PostgreSQL optimization

```sql
-- Crear índices para mejor performance
CREATE INDEX idx_notificaciones_leido ON notificaciones(leido);
CREATE INDEX idx_notificaciones_created_at ON notificaciones(created_at DESC);
CREATE INDEX idx_notificaciones_tipo ON notificaciones(tipo);
```

---

## 🔍 Checklist final

- [ ] Backend corriendo sin errores
- [ ] WebSocket conecta correctamente
- [ ] JWT autenticación funciona
- [ ] PostgreSQL accesible
- [ ] HTTPS/WSS funcionando
- [ ] Frontend cargando
- [ ] NotificationCenter visible
- [ ] Notificaciones en tiempo real
- [ ] Logs limpios sin errores
- [ ] Certificados SSL válidos

---

## 📞 Contacto y soporte

En caso de problemas, verificar:

1. Logs en `/var/log/`
2. DevTools (F12) en navegador
3. Documentación en `*.md`
4. Comandos de verificación arriba

---

**Despliegue completado exitosamente.** 🎉

