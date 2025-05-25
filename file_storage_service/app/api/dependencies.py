from sqlalchemy.orm import Session
from fastapi import Depends

from app.core.config import settings
from app.infrastructure.database.session import get_db
from app.infrastructure.database.repository import FileRepository
from app.infrastructure.storage.file_storage import FileSystemStorage
from app.services.file_service import FileService

def get_file_service(db: Session = Depends(get_db)) -> FileService:
    """Провайдер зависимости для FileService."""
    repo = FileRepository(db)
    storage = FileSystemStorage(base_path=settings.FILE_STORAGE_PATH)
    return FileService(repository=repo, storage=storage)