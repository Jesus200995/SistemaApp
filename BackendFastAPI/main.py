from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, layers, chat, notificaciones
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SistemaApp API (FastAPI + PostgreSQL)")

# ✅ Configuración CORS correcta
origins = [
    "http://localhost:5173",                 # desarrollo local
    "https://sistemaapp.sembrandodatos.com", # frontend desplegado
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

@app.get("/")
def root():
    return {"status": "✅ API corriendo correctamente"}
