import os
import shutil
from pathlib import Path
from uuid import UUID
from src.config import settings
from src.domain.interfaces.document_storage import DocumentStorage

class LocalDocumentStorage(DocumentStorage):
    def __init__(self):
        self._base_path = settings.upload_path

    async def store(self, session_id: UUID, filename: str, content: bytes) -> str:
        session_dir = self._base_path / str(session_id)
        session_dir.mkdir(parents=True, exist_ok=True)
        file_path = session_dir / filename
        # Avoid overwrites by appending counter
        counter = 1
        while file_path.exists():
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            file_path = session_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        file_path.write_bytes(content)
        return str(file_path.relative_to(self._base_path))

    async def retrieve(self, file_path: str) -> bytes:
        full_path = self._base_path / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return full_path.read_bytes()

    async def delete(self, file_path: str) -> bool:
        full_path = self._base_path / file_path
        if full_path.exists():
            full_path.unlink()
            return True
        return False

    async def delete_session(self, session_id: UUID) -> int:
        session_dir = self._base_path / str(session_id)
        if not session_dir.exists():
            return 0
        count = sum(1 for _ in session_dir.iterdir() if _.is_file())
        shutil.rmtree(session_dir)
        return count

    async def get_session_size(self, session_id: UUID) -> int:
        session_dir = self._base_path / str(session_id)
        if not session_dir.exists():
            return 0
        return sum(f.stat().st_size for f in session_dir.iterdir() if f.is_file())
