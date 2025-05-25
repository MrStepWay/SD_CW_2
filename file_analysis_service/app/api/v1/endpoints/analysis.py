import uuid
import os
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import FileResponse

from app.services.analysis_service import AnalysisService
from app.api.dependencies import get_analysis_service
from ..schemas import AnalysisResultResponse

router = APIRouter()

@router.post("/", response_model=AnalysisResultResponse, status_code=201)
async def start_analysis(
    file_id: uuid.UUID = Body(..., embed=True, description="The unique ID of the file to analyze"),
    service: AnalysisService = Depends(get_analysis_service)
):
    """Запускает анализ файла по его ID."""
    try:
        result = await service.analyze_file(file_id)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.get("/{file_id}", response_model=AnalysisResultResponse)
async def get_analysis_result(
    file_id: uuid.UUID,
    service: AnalysisService = Depends(get_analysis_service)
):
    """Получает результаты анализа по ID файла."""
    result = service.get_analysis_by_file_id(file_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Analysis for this file has not been performed or is not found.")
    return result

@router.get("/wordcloud/{file_id}", response_class=FileResponse)
async def get_word_cloud_image(
    file_id: uuid.UUID,
    service: AnalysisService = Depends(get_analysis_service)
):
    """
    Получает сгенерированную картинку облака слов для файла.
    Возвращает изображение в формате PNG.
    """
    analysis_result = service.get_analysis_by_file_id(file_id)

    if not analysis_result or not analysis_result.word_cloud_location:
        raise HTTPException(
            status_code=404,
            detail="Word cloud image not found for this file. Either analysis was not performed or word cloud generation failed."
        )

    image_path = analysis_result.word_cloud_location

    if not os.path.exists(image_path):
        raise HTTPException(status_code=500, detail="Internal server error: image file is missing on disk.")

    return FileResponse(path=image_path, media_type="image/png")