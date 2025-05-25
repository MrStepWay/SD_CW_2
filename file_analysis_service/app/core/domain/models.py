import uuid
from dataclasses import dataclass
from typing import Optional

@dataclass
class AnalysisResult:
    """Доменная модель результата анализа."""
    file_id: uuid.UUID
    paragraphs: int
    words: int
    symbols: int
    word_cloud_location: Optional[str] = None