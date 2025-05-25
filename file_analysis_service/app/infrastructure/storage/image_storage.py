import uuid
from pathlib import Path

class ImageStorage:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, content: bytes, file_id: uuid.UUID) -> str:
        filename = f"wordcloud_{file_id}.png"
        file_path = self.base_path / filename
        with open(file_path, "wb") as f:
            f.write(content)
        return str(file_path)