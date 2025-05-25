from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.infrastructure.database.session import get_db
from app.infrastructure.database.repository import AnalysisRepository
from app.infrastructure.clients.file_storage_client import FileStorageClient
from app.infrastructure.clients.word_cloud_client import WordCloudClient
from app.infrastructure.storage.image_storage import ImageStorage
from app.services.analysis_service import AnalysisService

# Это, если что, так DI в FastAPI выглядит. Отвратительно, не правда ли? Я вообще как-то в питоне разочаровываюсь пока это всё пишу.
def get_analysis_service(db: Session = Depends(get_db)) -> AnalysisService:
    repo = AnalysisRepository(db)
    file_client = FileStorageClient(base_url=settings.FILE_STORAGE_SERVICE_URL)
    word_cloud_client = WordCloudClient(api_url=settings.WORD_CLOUD_API_URL)
    image_storage = ImageStorage(base_path=settings.IMAGE_STORAGE_PATH)
    
    return AnalysisService(
        repository=repo,
        file_storage_client=file_client,
        word_cloud_client=word_cloud_client,
        image_storage=image_storage,
    )