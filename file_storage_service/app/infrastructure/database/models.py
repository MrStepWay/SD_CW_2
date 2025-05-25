import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base

class File(Base):
    """ORM-модель для таблицы 'files'."""
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hash: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    location: Mapped[str] = mapped_column(String, unique=True, nullable=False)