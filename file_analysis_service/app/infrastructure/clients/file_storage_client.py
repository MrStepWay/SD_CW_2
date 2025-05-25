import uuid
from typing import Optional
import httpx

class FileStorageClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_file_content(self, file_id: uuid.UUID) -> Optional[bytes]:
        """Получает содержимое файла из сервиса хранения."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/api/v1/files/{file_id}")
                response.raise_for_status() # Вызовет исключение для 4xx/5xx
                return response.content
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise