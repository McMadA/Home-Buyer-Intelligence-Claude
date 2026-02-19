from abc import ABC, abstractmethod
from uuid import UUID
from ..models.document import Document


class DocumentRepository(ABC):
    @abstractmethod
    async def save(self, document: Document) -> Document: ...

    @abstractmethod
    async def get_by_id(self, doc_id: UUID) -> Document | None: ...

    @abstractmethod
    async def get_by_session(self, session_id: UUID) -> list[Document]: ...

    @abstractmethod
    async def delete(self, doc_id: UUID) -> bool: ...

    @abstractmethod
    async def delete_by_session(self, session_id: UUID) -> int: ...
