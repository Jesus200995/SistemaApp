from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from routes import auth, layers, chat, notificaciones, sembradores, seguimientos, solicitudes
from database import Base, engine
import traceback

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SistemaApp API (FastAPI + PostgreSQL)")

# ✅ Lista de orígenes permitidos
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "https://sistemaapp.sembrandodatos.com",
    "https://www.sistemaapp.sembrandodatos.com",
]


def add_cors_headers_to_response(response, origin: str):
    """Añadir headers CORS a cualquier respuesta"""
    if origin in ALLOWED_ORIGINS or origin == "":
        allowed_origin = origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[3]  # default producción
        response.headers["Access-Control-Allow-Origin"] = allowed_origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept, Origin, X-Requested-With"
        response.headers["Access-Control-Expose-Headers"] = "*"
    return response


# 🛡️ Middleware personalizado que SIEMPRE añade CORS, incluso en errores
class CORSErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin", "")
        
        # Manejar preflight OPTIONS
        if request.method == "OPTIONS":
            response = JSONResponse(content={"status": "ok"}, status_code=200)
            return add_cors_headers_to_response(response, origin)
        
        try:
            response = await call_next(request)
            return add_cors_headers_to_response(response, origin)
        except Exception as exc:
            # Capturar CUALQUIER error y devolver con headers CORS
            print(f"❌ Error interno: {str(exc)}")
            traceback.print_exc()
            error_response = JSONResponse(
                status_code=500,
                content={"detail": f"Error interno del servidor: {str(exc)}"}
            )
            return add_cors_headers_to_response(error_response, origin)


# Añadir middleware personalizado PRIMERO (se ejecuta último, envuelve todo)
app.add_middleware(CORSErrorMiddleware)

# Middleware CORS estándar como respaldo
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
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


# 🛡️ Manejador global de excepciones con CORS
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejar todas las excepciones no capturadas con CORS"""
    origin = request.headers.get("origin", "")
    print(f"❌ Excepción global: {str(exc)}")
    traceback.print_exc()
    
    response = JSONResponse(
        status_code=500,
        content={"detail": f"Error interno: {str(exc)}"}
    )
    return add_cors_headers_to_response(response, origin)
