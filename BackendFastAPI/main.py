from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, layers, chat, notificaciones, sembradores, seguimientos, solicitudes
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SistemaApp API (FastAPI + PostgreSQL)")

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
