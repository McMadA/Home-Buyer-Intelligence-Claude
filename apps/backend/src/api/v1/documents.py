import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from sqlalchemy import select

from src.api.dependencies import DbSession, DocRepo, Storage
from src.config import settings
from src.domain.models.document import Document
from src.application.dto.document_dto import DocumentUploadResponse, DocumentListResponse
from src.infrastructure.database.models import SessionModel

router = APIRouter(prefix="/sessions", tags=["documents"])


@router.post("", status_code=201)
async def create_session(db: DbSession):
    """Create a new analysis session."""
    session = SessionModel(id=str(uuid.uuid4()))
    db.add(session)
    await db.commit()
    return {"session_id": session.id, "created_at": session.created_at}


@router.post(
    "/{session_id}/documents",
    response_model=DocumentUploadResponse,
    status_code=201,
)
async def upload_document(
    session_id: str,
    db: DbSession,
    doc_repo: DocRepo,
    storage: Storage,
    file: UploadFile = File(...),
):
    """Upload a document to a session."""
    result = await db.execute(
        select(SessionModel).where(SessionModel.id == session_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Session not found")

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    content = await file.read()

    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds {settings.max_file_size_mb}MB limit",
        )

    session_size = await storage.get_session_size(uuid.UUID(session_id))
    max_session = settings.max_session_size_mb * 1024 * 1024
    if session_size + len(content) > max_session:
        raise HTTPException(
            status_code=400,
            detail=f"Session storage exceeds {settings.max_session_size_mb}MB limit",
        )

    file_path = await storage.store(uuid.UUID(session_id), file.filename, content)

    doc = Document(
        session_id=uuid.UUID(session_id),
        filename=file.filename,
        file_path=file_path,
        file_size_bytes=len(content),
    )
    saved = await doc_repo.save(doc)

    return DocumentUploadResponse(
        id=saved.id,
        session_id=saved.session_id,
        filename=saved.filename,
        document_type=saved.document_type.value,
        file_size_bytes=saved.file_size_bytes,
        created_at=saved.created_at,
    )


@router.get("/{session_id}/documents", response_model=DocumentListResponse)
async def list_documents(session_id: str, doc_repo: DocRepo):
    """List all documents in a session."""
    docs = await doc_repo.get_by_session(uuid.UUID(session_id))
    return DocumentListResponse(
        documents=[
            DocumentUploadResponse(
                id=d.id,
                session_id=d.session_id,
                filename=d.filename,
                document_type=d.document_type.value,
                file_size_bytes=d.file_size_bytes,
                created_at=d.created_at,
            )
            for d in docs
        ]
    )


@router.get("/{session_id}/documents/{doc_id}")
async def get_document_content(
    session_id: str, doc_id: str, doc_repo: DocRepo, storage: Storage
):
    """Retrieve the raw PDF content for a document."""
    doc = await doc_repo.get_by_id(uuid.UUID(doc_id))
    if not doc or str(doc.session_id) != session_id:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        content = await storage.retrieve(doc.file_path)
        return Response(content=content, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found on storage: {e}")


@router.delete("/{session_id}/documents/{doc_id}", status_code=204)
async def delete_document(
    session_id: str, doc_id: str, doc_repo: DocRepo, storage: Storage
):
    """Delete a specific document."""
    doc = await doc_repo.get_by_id(uuid.UUID(doc_id))
    if not doc or str(doc.session_id) != session_id:
        raise HTTPException(status_code=404, detail="Document not found")
    await storage.delete(doc.file_path)
    await doc_repo.delete(uuid.UUID(doc_id))
