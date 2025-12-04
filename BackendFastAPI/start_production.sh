#!/bin/bash
# Script para iniciar el backend FastAPI en producción con soporte de proxy HTTPS
# Uso: ./start_production.sh

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# ✅ IMPORTANTE: --proxy-headers habilita el soporte para X-Forwarded-Proto
# Esto es NECESARIO cuando FastAPI está detrás de Nginx con HTTPS
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --proxy-headers \
    --forwarded-allow-ips="*"
