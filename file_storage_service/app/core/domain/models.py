import uuid
from dataclasses import dataclass

@dataclass
class FileMetadata:
    """Доменная модель, описывающая метаданные файла."""
    id: uuid.UUID
    name: str
    hash: str
    location: str