from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import auth, layers, chat, notificaciones, sembradores, seguimientos, solicitudes
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SistemaApp API (FastAPI + PostgreSQL)")

# ✅ Configuración CORS - IMPORTANTE: debe estar ANTES de las rutas
origins = [
    "http://localhost:5173",                  # desarrollo local Vite
    "http://localhost:3000",                  # desarrollo alternativo
    "http://127.0.0.1:5173",                  # desarrollo local IP
    "https://sistemaapp.sembrandodatos.com",  # frontend en producción
    "https://www.sistemaapp.sembrandodatos.com",  # con www
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # Cache preflight requests por 10 minutos
)

# 🛡️ Middleware adicional para asegurar headers CORS en todas las respuestas
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    origin = request.headers.get("origin", "")
    if origin in origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "*"
    return response

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

# 🛡️ Endpoint para verificar CORS
@app.options("/{full_path:path}")
async def preflight_handler(request: Request, full_path: str):
    """Manejar preflight requests (OPTIONS) explícitamente"""
    origin = request.headers.get("origin", "")
    if origin in origins:
        return JSONResponse(
            content={"status": "ok"},
            headers={
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "600",
            }
        )
    return JSONResponse(content={"status": "forbidden"}, status_code=403)
