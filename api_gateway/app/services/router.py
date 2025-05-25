import uuid
from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException
from fastapi.responses import Response 
import httpx

from ..core.config import settings
from .http_client import get_http_client

router = APIRouter()

@router.post("/files/")
async def upload_and_analyze_file(
    file: UploadFile = File(...),
    client: httpx.AsyncClient = Depends(get_http_client)
):
    """
    Организует загрузку файла и запуск его анализа.
    Это основной endpoint для пользователей, предназначенный для отправки новых файлов.
    """

    if not file.filename or not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed and filename is required.")
    content = await file.read()
    storage_url = f"{settings.FILE_STORAGE_SERVICE_URL}/api/v1/files/"
    files_payload = {'file': (file.filename, content, file.content_type)}
    try:
        resp_storage = await client.post(storage_url, files=files_payload, timeout=30.0)
        resp_storage.raise_for_status()
        storage_data = resp_storage.json()
        file_id = storage_data['id']
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception:
        raise HTTPException(status_code=503, detail="File Storage Service is unavailable.")
    
    analysis_url = f"{settings.FILE_ANALYSIS_SERVICE_URL}/api/v1/analysis/"
    analysis_payload = {"file_id": file_id}
    try:
        resp_analysis = await client.post(analysis_url, json=analysis_payload, timeout=60.0)
        resp_analysis.raise_for_status()
        return resp_analysis.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception:
        raise HTTPException(status_code=503, detail="File Analysis Service is unavailable.")


@router.get("/files/{file_id}")
async def get_file_content(
    file_id: uuid.UUID,
    client: httpx.AsyncClient = Depends(get_http_client)
):
    """Перенаправляет запрос для получения содержимого файла из сервиса хранения."""
    url = f"{settings.FILE_STORAGE_SERVICE_URL}/api/v1/files/{file_id}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception:
        raise HTTPException(status_code=503, detail="File Storage Service is unavailable.")


@router.get("/analysis/{file_id}")
async def get_analysis(
    file_id: uuid.UUID,
    client: httpx.AsyncClient = Depends(get_http_client)
):
    """Перенаправляет запрос для получения результатов анализа."""
    url = f"{settings.FILE_ANALYSIS_SERVICE_URL}/api/v1/analysis/{file_id}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception:
        raise HTTPException(status_code=503, detail="File Analysis Service is unavailable.")


@router.get("/analysis/wordcloud/{file_id}")
async def get_wordcloud_image(
    file_id: uuid.UUID,
    client: httpx.AsyncClient = Depends(get_http_client)
):
    """Перенаправляет запрос для получения изображения облака слов."""
    url = f"{settings.FILE_ANALYSIS_SERVICE_URL}/api/v1/analysis/wordcloud/{file_id}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception:
        raise HTTPException(status_code=503, detail="File Analysis Service is unavailable.")