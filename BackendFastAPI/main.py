from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, layers
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SistemaApp API (FastAPI + Uvicorn)")

# ✅ Configuración correcta de CORS
origins = [
    "http://localhost:5173",                 # Frontend local (desarrollo)
    "https://sistemaapp.sembrandodatos.com", # Frontend en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 👈 no uses ["*"] ni combines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 Rutas
app.include_router(auth.router)
app.include_router(layers.router)

@app.get("/")
def root():
    return {"message": "✅ API SistemaApp con FastAPI funcionando correctamente 🚀"}
