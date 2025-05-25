from typing import AsyncGenerator
import httpx
from fastapi import Request

async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """
    Зависимость для получения httpx.AsyncClient.
    Гарантирует корректное закрытие клиента после выполнения запроса.
    """
    async with httpx.AsyncClient() as client:
        yield client