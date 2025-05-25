from typing import Optional
import httpx

class WordCloudClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    async def generate_word_cloud(self, text: str) -> Optional[bytes]:
        payload = {"text": text, "format": "png"}
        async with httpx.AsyncClient() as client:
            try:
                # Увеличиваем таймаут, так как генерация может быть долгой
                response = await client.post(self.api_url, json=payload, timeout=30.0)
                response.raise_for_status()
                return response.content
            except httpx.RequestError:
                # Если сервис недоступен, просто возвращаем None
                return None