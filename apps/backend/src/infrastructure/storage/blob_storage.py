"""Azure Blob Storage implementation - placeholder for production migration."""
from uuid import UUID
from src.domain.interfaces.document_storage import DocumentStorage

class BlobDocumentStorage(DocumentStorage):
    """Placeholder for Azure Blob Storage. Implement when migrating to Azure."""

    async def store(self, session_id: UUID, filename: str, content: bytes) -> str:
        raise NotImplementedError("Azure Blob Storage not yet implemented")

    async def retrieve(self, file_path: str) -> bytes:
        raise NotImplementedError("Azure Blob Storage not yet implemented")

    async def delete(self, file_path: str) -> bool:
        raise NotImplementedError("Azure Blob Storage not yet implemented")

    async def delete_session(self, session_id: UUID) -> int:
        raise NotImplementedError("Azure Blob Storage not yet implemented")

    async def get_session_size(self, session_id: UUID) -> int:
        raise NotImplementedError("Azure Blob Storage not yet implemented")
