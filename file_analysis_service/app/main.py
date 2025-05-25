from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="File Analysis Service",
    description="Сервис анализа текста и генерации облаков слов",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}