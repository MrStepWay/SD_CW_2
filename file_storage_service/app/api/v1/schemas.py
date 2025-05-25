import uuid
from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    """Схема ответа после успешной загрузки файла."""
    id: uuid.UUID
    
    class Config:
        from_attributes = True