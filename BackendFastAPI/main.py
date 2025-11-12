from fastapi import FastAPI
from routes import auth
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SistemaApp API (FastAPI + Uvicorn)")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "✅ API SistemaApp con FastAPI funcionando correctamente 🚀"}
