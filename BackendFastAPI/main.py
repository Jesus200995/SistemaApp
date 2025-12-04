from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from routes import auth, layers, chat, notificaciones, sembradores, seguimientos, solicitudes
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SistemaApp API (FastAPI + PostgreSQL)",
    # ✅ CRÍTICO: Deshabilitar redirección automática de trailing slash
    # Esto evita el problema de CORS cuando se redirige /path a /path/
    redirect_slashes=False,
    # ✅ Configuración para proxy reverso (Nginx con HTTPS)
    root_path="",
    servers=[
        {"url": "https://sistemaapi.sembrandodatos.com", "description": "Producción HTTPS"},
        {"url": "http://localhost:8000", "description": "Desarrollo local"}
    ]
)


# ✅ Middleware para manejar X-Forwarded-Proto y forzar HTTPS en producción
class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware que corrige el esquema de URL cuando está detrás de un proxy HTTPS.
    Esto asegura que FastAPI genere URLs con https:// cuando el proxy usa HTTPS.
    """
    async def dispatch(self, request: Request, call_next):
        # Leer X-Forwarded-Proto del proxy Nginx
        forwarded_proto = request.headers.get("x-forwarded-proto", "").lower()
        
        # Si el proxy indica HTTPS, actualizar el scope
        if forwarded_proto == "https":
            # Modificar el scope para que FastAPI use https://
            request.scope["scheme"] = "https"
        
        response = await call_next(request)
        return response


# ✅ Agregar middleware de proxy ANTES de CORS
app.add_middleware(ProxyHeadersMiddleware)

# ✅ Configuración CORS correcta
origins = [
    "http://localhost:5173",                 # desarrollo local
    "http://localhost:5174",                 # desarrollo local (puerto alternativo)
    "http://localhost:5175",                 # desarrollo local (puerto alternativo)
    "http://localhost:5176",                 # desarrollo local (puerto alternativo)
    "http://localhost:5177",                 # desarrollo local (puerto alternativo)
    "http://127.0.0.1:5173",                 # desarrollo local (IP)
    "http://127.0.0.1:5174",                 # desarrollo local (IP)
    "http://127.0.0.1:5177",                 # desarrollo local (IP)
    "https://sistemaapp.sembrandodatos.com", # frontend desplegado
    "http://sistemaapp.sembrandodatos.com",  # frontend sin SSL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 Rutas
app.include_router(auth.router)
app.include_router(layers.router)
app.include_router(chat.router)
app.include_router(notificaciones.router)
app.include_router(sembradores.router)
app.include_router(seguimientos.router)
app.include_router(solicitudes.router)

@app.get("/")
def root():
    return {"status": "✅ API corriendo correctamente"}
