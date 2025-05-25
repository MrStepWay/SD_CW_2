from fastapi import APIRouter
from .endpoints import files

api_router = APIRouter()
api_router.include_router(files.router, prefix="/files", tags=["Files"])