from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import auth, layers, chat, notificaciones, sembradores, seguimientos, solicitudes
from database import Base, engine
import traceback

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SistemaApp API (FastAPI + PostgreSQL)")

# ✅ Configuración CORS correcta - permitir todos los orígenes de desarrollo
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:5177",
    "http://localhost:5178",
    "http://localhost:5179",
    "http://localhost:5180",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:5176",
    "http://127.0.0.1:5177",
    "https://sistemaapp.sembrandodatos.com",
    "http://sistemaapp.sembrandodatos.com",
    "https://sistema.sembrandodatos.com",
    "http://sistema.sembrandodatos.com",
    "*",  # Permitir todos los orígenes temporalmente para debugging
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ✅ Manejador de excepciones global para mantener CORS en errores
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"❌ Error global: {exc}")
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "error": "Internal Server Error"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
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
