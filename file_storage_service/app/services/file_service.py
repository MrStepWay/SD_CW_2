# file_storage_service/app/services/file_service.py
import uuid
from typing import Optional, Tuple
from app.core.domain.models import FileMetadata
from app.infrastructure.database.repository import FileRepository
from app.infrastructure.database.models import File as FileORM
from app.infrastructure.storage.file_storage import FileSystemStorage

class FileService:
    def __init__(self, repository: FileRepository, storage: FileSystemStorage):
        self.repository = repository
        self.storage = storage


    def _map_orm_to_domain(self, file_orm: FileORM) -> FileMetadata:
        """Преобразует ORM-модель в доменную модель."""
        return FileMetadata(
            id=file_orm.id,
            name=file_orm.name,
            hash=file_orm.hash,
            location=file_orm.location
        )

    def upload_file(self, filename: str, content: bytes) -> FileMetadata:
        """
        Обрабатывает загрузку файла: проверяет на дубликат по хэшу,
        сохраняет на диск и в БД, если файл новый.
        """
        file_hash = self.storage.get_hash(content)
        
        existing_file_orm = self.repository.get_by_hash(file_hash)
        if existing_file_orm:
            return self._map_orm_to_domain(existing_file_orm)
            
        new_id = uuid.uuid4()
        storage_filename = f"{new_id}.txt"
        
        saved_location = self.storage.save(content, storage_filename)
        
        new_file_metadata = FileMetadata(
            id=new_id,
            name=filename,
            hash=file_hash,
            location=saved_location
        )
        self.repository.save(new_file_metadata)
        
        return new_file_metadata

    def get_file_content(self, file_id: uuid.UUID) -> Optional[Tuple[FileMetadata, bytes]]:
        """Получает метаданные файла и его содержимое."""
        file_orm = self.repository.get_by_id(file_id)
        if not file_orm:
            return None
        
        content = self.storage.read(file_orm.location)
        metadata = self._map_orm_to_domain(file_orm)
        
        return metadata, content