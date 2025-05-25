import hashlib
import os
from pathlib import Path

class FileSystemStorage:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, content: bytes, filename: str) -> str:
        """Сохраняет контент в файл и возвращает полный путь."""
        file_path = self.base_path / filename
        with open(file_path, "wb") as f:
            f.write(content)
        return str(file_path)

    def read(self, location: str) -> bytes:
        """Читает контент из файла по указанному пути."""
        with open(location, "rb") as f:
            return f.read()

    @staticmethod
    def get_hash(content: bytes) -> str:
        """Вычисляет SHA-256 хэш контента."""
        return hashlib.sha256(content).hexdigest()