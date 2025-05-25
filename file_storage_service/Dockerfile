FROM python:3.10-slim

WORKDIR /app

# Устанавливаем переменные окружения, чтобы питон не буферизировал stdout и stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

COPY alembic.ini .
COPY migrations /app/migrations

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]