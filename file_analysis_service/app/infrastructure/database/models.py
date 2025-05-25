import uuid
from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.session import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True)
    paragraphs: Mapped[int] = mapped_column(Integer)
    words: Mapped[int] = mapped_column(Integer)
    symbols: Mapped[int] = mapped_column(Integer)
    word_cloud_location: Mapped[str] = mapped_column(String, nullable=True)