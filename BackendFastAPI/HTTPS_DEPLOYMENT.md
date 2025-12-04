# 🚀 Guía de Despliegue Backend - HTTPS con Nginx

## Problema: Mixed Content Error

Si ves errores como:
```
Mixed Content: The page at 'https://sistemaapp...' was loaded over HTTPS, 
but requested an insecure resource 'http://sistemaapi...'
```

Esto significa que FastAPI no está detectando que está detrás de HTTPS.

---

## ✅ Solución Paso a Paso

### 1. Actualizar el código del backend

```bash
cd /var/www/SistemaApp/Backend/BackendFastAPI
git pull origin main
```

### 2. Reiniciar uvicorn CON --proxy-headers

**IMPORTANTE**: El flag `--proxy-headers` es OBLIGATORIO para que FastAPI respete `X-Forwarded-Proto`.

#### Opción A: Con PM2 (recomendado)
```bash
pm2 delete sistemaapi-backend 2>/dev/null || true
pm2 start ecosystem.config.json
pm2 save
```

#### Opción B: Manual con uvicorn
```bash
# Detener el proceso actual
pkill -f "uvicorn main:app"

# Iniciar con --proxy-headers
cd /var/www/SistemaApp/Backend/BackendFastAPI
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips="*" &
```

### 3. Verificar configuración de Nginx

El archivo `/etc/nginx/sites-available/sistemaapi.sembrandodatos.com` debe incluir:

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    
    # ✅ ESTAS LÍNEAS SON CRÍTICAS:
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;  # ← SIN ESTO NO FUNCIONA
}
```

Si falta `X-Forwarded-Proto`, agrégalo:

```bash
sudo nano /etc/nginx/sites-available/sistemaapi.sembrandodatos.com
# Agregar: proxy_set_header X-Forwarded-Proto $scheme;
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Verificar que funciona

```bash
# Probar que el header llega correctamente
curl -I https://sistemaapi.sembrandodatos.com/

# Debería responder con HTTPS sin redirecciones
```

---

## 🔧 Comandos Rápidos para el VPS

```bash
# Conexión SSH
ssh root@31.97.8.51

# Todo en un comando:
cd /var/www/SistemaApp/Backend/BackendFastAPI && \
git pull origin main && \
source venv/bin/activate && \
pip install -r requirements.txt && \
pkill -f "uvicorn main:app" ; \
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips="*" > /var/log/uvicorn.log 2>&1 &

# Verificar Nginx
grep -r "X-Forwarded-Proto" /etc/nginx/sites-enabled/
```

---

## 📋 Checklist

- [ ] `main.py` tiene el `ProxyHeadersMiddleware`
- [ ] uvicorn se ejecuta con `--proxy-headers`
- [ ] Nginx tiene `proxy_set_header X-Forwarded-Proto $scheme;`
- [ ] Nginx está recargado (`sudo systemctl reload nginx`)
- [ ] No hay errores de "Mixed Content" en el navegador
