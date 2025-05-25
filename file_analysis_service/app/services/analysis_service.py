import uuid
from typing import Optional
from app.core.domain.models import AnalysisResult
from app.infrastructure.database.repository import AnalysisRepository
from app.infrastructure.database.models import Analysis as AnalysisORM
from app.infrastructure.clients.file_storage_client import FileStorageClient
from app.infrastructure.clients.word_cloud_client import WordCloudClient
from app.infrastructure.storage.image_storage import ImageStorage

class AnalysisService:
    def __init__(
        self,
        repository: AnalysisRepository,
        file_storage_client: FileStorageClient,
        word_cloud_client: WordCloudClient,
        image_storage: ImageStorage,
    ):
        self.repository = repository
        self.file_storage_client = file_storage_client
        self.word_cloud_client = word_cloud_client
        self.image_storage = image_storage

    def _calculate_stats(self, text: str) -> tuple[int, int, int]:
        paragraphs = len([p for p in text.split('\n') if p.strip()])
        words = len(text.split())
        symbols = len(text)
        return paragraphs, words, symbols

    def _map_orm_to_domain(self, orm_obj: AnalysisORM) -> AnalysisResult:
        return AnalysisResult(
            file_id=orm_obj.file_id,
            paragraphs=orm_obj.paragraphs,
            words=orm_obj.words,
            symbols=orm_obj.symbols,
            word_cloud_location=orm_obj.word_cloud_location,
        )

    async def analyze_file(self, file_id: uuid.UUID) -> AnalysisResult:
        existing_analysis = self.repository.get_by_file_id(file_id)
        if existing_analysis:
            return self._map_orm_to_domain(existing_analysis)

        content_bytes = await self.file_storage_client.get_file_content(file_id)
        if content_bytes is None:
            raise FileNotFoundError(f"File with ID {file_id} not found in storage service")
        
        text = content_bytes.decode('utf-8', errors='ignore')

        paragraphs, words, symbols = self._calculate_stats(text)

        word_cloud_location = None
        cloud_image_bytes = await self.word_cloud_client.generate_word_cloud(text)
        if cloud_image_bytes:
            word_cloud_location = self.image_storage.save(cloud_image_bytes, file_id)

        analysis_result = AnalysisResult(
            file_id=file_id,
            paragraphs=paragraphs,
            words=words,
            symbols=symbols,
            word_cloud_location=word_cloud_location,
        )
        self.repository.save(analysis_result)
        return analysis_result

    def get_analysis_by_file_id(self, file_id: uuid.UUID) -> Optional[AnalysisResult]:
        analysis_orm = self.repository.get_by_file_id(file_id)
        if not analysis_orm:
            return None
        return self._map_orm_to_domain(analysis_orm)