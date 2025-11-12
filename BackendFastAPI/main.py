from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SistemaApp API (FastAPI + Uvicorn)")

# ✅ Configuración de CORS
origins = [
    "http://localhost:5173",                 # Frontend local (dev)
    "http://localhost:5174",                 # Frontend local (dev - puerto alternativo)
    "https://sistemaapp.sembrandodatos.com", # Tu dominio (producción)
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

@app.get("/")
def root():
    return {"message": "✅ API SistemaApp con FastAPI funcionando correctamente 🚀"}
