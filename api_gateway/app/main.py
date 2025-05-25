from fastapi import FastAPI
from .services.router import router as api_router

app = FastAPI(
    title="API Gateway",
    description="Единая точка входа в систему.",
    version="1.0.0"
)

# Все публичные эндпоинты будут иметь префикс /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}