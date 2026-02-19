from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    id: UUID
    session_id: UUID
    filename: str
    document_type: str
    file_size_bytes: int
    created_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentUploadResponse]
