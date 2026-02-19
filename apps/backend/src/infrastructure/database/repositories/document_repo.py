from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.document import Document
from src.domain.enums import DocumentType
from src.domain.interfaces.document_repository import DocumentRepository
from src.infrastructure.database.models import DocumentModel

class SQLDocumentRepository(DocumentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, document: Document) -> Document:
        result = await self._session.execute(
            select(DocumentModel).where(DocumentModel.id == str(document.id))
        )
        model = result.scalar_one_or_none()

        if not model:
            model = DocumentModel(id=str(document.id))
            self._session.add(model)

        model.session_id = str(document.session_id)
        model.filename = document.filename
        model.document_type = document.document_type.value
        model.file_path = document.file_path
        model.file_size_bytes = document.file_size_bytes
        model.extracted_text = document.extracted_text
        model.parsed_data = document.parsed_data
        model.created_at = document.created_at

        await self._session.commit()
        return document

    async def get_by_id(self, doc_id: UUID) -> Document | None:
        result = await self._session.execute(
            select(DocumentModel).where(DocumentModel.id == str(doc_id))
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._to_domain(model)

    async def get_by_session(self, session_id: UUID) -> list[Document]:
        result = await self._session.execute(
            select(DocumentModel).where(DocumentModel.session_id == str(session_id))
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def delete(self, doc_id: UUID) -> bool:
        result = await self._session.execute(
            delete(DocumentModel).where(DocumentModel.id == str(doc_id))
        )
        await self._session.commit()
        return result.rowcount > 0

    async def delete_by_session(self, session_id: UUID) -> int:
        result = await self._session.execute(
            delete(DocumentModel).where(DocumentModel.session_id == str(session_id))
        )
        await self._session.commit()
        return result.rowcount

    @staticmethod
    def _to_domain(model: DocumentModel) -> Document:
        return Document(
            id=UUID(model.id),
            session_id=UUID(model.session_id),
            filename=model.filename,
            document_type=DocumentType(model.document_type),
            file_path=model.file_path,
            file_size_bytes=model.file_size_bytes,
            extracted_text=model.extracted_text,
            parsed_data=model.parsed_data,
            created_at=model.created_at,
        )
