from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from ..enums import DocumentType


@dataclass
class Document:
    session_id: UUID
    filename: str
    document_type: DocumentType = DocumentType.OTHER
    id: UUID = field(default_factory=uuid4)
    file_path: str = ""
    file_size_bytes: int = 0
    extracted_text: str | None = None
    parsed_data: dict | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
