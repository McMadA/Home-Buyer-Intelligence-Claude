from abc import ABC, abstractmethod
from uuid import UUID


class DocumentStorage(ABC):
    @abstractmethod
    async def store(self, session_id: UUID, filename: str, content: bytes) -> str: ...

    @abstractmethod
    async def retrieve(self, file_path: str) -> bytes: ...

    @abstractmethod
    async def delete(self, file_path: str) -> bool: ...

    @abstractmethod
    async def delete_session(self, session_id: UUID) -> int: ...

    @abstractmethod
    async def get_session_size(self, session_id: UUID) -> int: ...
