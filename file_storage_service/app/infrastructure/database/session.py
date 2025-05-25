from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Зависимость для FastAPI. Предоставляет сессию БД для одного запроса.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()