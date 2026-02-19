from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.engine import get_session
from src.infrastructure.database.repositories.document_repo import SQLDocumentRepository
from src.infrastructure.database.repositories.property_repo import SQLPropertyRepository
from src.infrastructure.storage.local_storage import LocalDocumentStorage
from src.infrastructure.ai.gemini_gateway import GeminiGateway
from src.domain.interfaces.document_repository import DocumentRepository
from src.domain.interfaces.property_repository import PropertyRepository
from src.domain.interfaces.document_storage import DocumentStorage
from src.domain.interfaces.ai_gateway import AIGateway


async def get_db_session():
    async for session in get_session():
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def get_document_repository(session: DbSession) -> DocumentRepository:
    return SQLDocumentRepository(session)


def get_property_repository(session: DbSession) -> PropertyRepository:
    return SQLPropertyRepository(session)


def get_document_storage() -> DocumentStorage:
    return LocalDocumentStorage()


def get_ai_gateway() -> AIGateway:
    return GeminiGateway()


DocRepo = Annotated[DocumentRepository, Depends(get_document_repository)]
PropRepo = Annotated[PropertyRepository, Depends(get_property_repository)]
Storage = Annotated[DocumentStorage, Depends(get_document_storage)]
AI = Annotated[AIGateway, Depends(get_ai_gateway)]
