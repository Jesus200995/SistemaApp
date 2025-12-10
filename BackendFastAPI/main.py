from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from routes import auth, layers, chat, notificaciones, sembradores, seguimientos, solicitudes, users
from database import Base, engine
import os

Base.metadata.create_all(bind=engine)

# 🔄 Ejecutar migraciones al iniciar
try:
    from migrations.add_user_fields import run_migration
    run_migration()
except Exception as e:
    print(f"⚠️ Error ejecutando migraciones: {str(e)}")

# 📁 Crear carpeta de uploads si no existe
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads", "seguimientos")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="SistemaApp API (FastAPI + PostgreSQL)")

# ✅ Configuración CORS PERMISIVA - Permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir TODOS los orígenes
    allow_credentials=False,  # No se puede usar True con "*"
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight por 1 hora
)

# 🔧 Middleware adicional para manejar OPTIONS manualmente si es necesario
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    # Manejar preflight OPTIONS explícitamente
    if request.method == "OPTIONS":
        response = JSONResponse(content={"status": "ok"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Max-Age"] = "3600"
        return response
    
    response = await call_next(request)
    
    # Agregar headers CORS a todas las respuestas
    response.headers["Access-Control-Allow-Origin"] = "*"
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
app.include_router(users.router)

# 📁 Servir archivos estáticos (uploads)
app.mount("/uploads", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "uploads")), name="uploads")

@app.get("/")
def root():
    return {"status": "✅ API corriendo correctamente"}
