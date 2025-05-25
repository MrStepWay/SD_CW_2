import uuid
from typing import Optional
from pydantic import BaseModel

class AnalysisResultResponse(BaseModel):
    file_id: uuid.UUID
    paragraphs: int
    words: int
    symbols: int
    word_cloud_location: Optional[str] = None

    class Config:
        from_attributes = True