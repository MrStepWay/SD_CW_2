import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.core.domain.models import AnalysisResult as AnalysisResultDomain
from .models import Analysis as AnalysisORM

class AnalysisRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_file_id(self, file_id: uuid.UUID) -> Optional[AnalysisORM]:
        return self.db.query(AnalysisORM).filter(AnalysisORM.file_id == file_id).first()

    def save(self, analysis: AnalysisResultDomain) -> AnalysisORM:
        db_analysis = AnalysisORM(
            file_id=analysis.file_id,
            paragraphs=analysis.paragraphs,
            words=analysis.words,
            symbols=analysis.symbols,
            word_cloud_location=analysis.word_cloud_location
        )
        self.db.add(db_analysis)
        self.db.commit()
        self.db.refresh(db_analysis)
        return db_analysis