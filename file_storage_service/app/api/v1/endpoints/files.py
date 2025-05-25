import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import Response

from app.api.v1.schemas import FileUploadResponse
from app.services.file_service import FileService
from app.api.dependencies import get_file_service

router = APIRouter()

@router.post("/", response_model=FileUploadResponse, status_code=201)
async def upload_file_endpoint(
    file: UploadFile = File(...),
    service: FileService = Depends(get_file_service)
):
    """
    Эндпоинт для загрузки файла.
    Принимает .txt файл, возвращает его уникальный ID.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
        
    content = await file.read()
    metadata = service.upload_file(filename=file.filename, content=content)
    
    return FileUploadResponse(id=metadata.id)


@router.get("/{file_id}", response_class=Response)
async def get_file_endpoint(
    file_id: uuid.UUID,
    service: FileService = Depends(get_file_service)
):
    """
    Эндпоинт для получения содержимого файла по его ID.
    """
    result = service.get_file_content(file_id)
    if result is None:
        raise HTTPException(status_code=404, detail="File not found")
        
    metadata, content = result
    
    return Response(
        content=content, 
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={metadata.name}"}
    )