import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.core.domain.models import FileMetadata as FileMetadataDomain
from .models import File as FileORM

class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_hash(self, hash_value: str) -> Optional[FileORM]:
        return self.db.query(FileORM).filter(FileORM.hash == hash_value).first()

    def get_by_id(self, file_id: uuid.UUID) -> Optional[FileORM]:
        return self.db.query(FileORM).filter(FileORM.id == file_id).first()

    def save(self, file_meta: FileMetadataDomain) -> FileORM:
        db_file = FileORM(
            id=file_meta.id,
            name=file_meta.name,
            hash=file_meta.hash,
            location=file_meta.location
        )
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)
        return db_file