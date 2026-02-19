import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.api.dependencies import DbSession, DocRepo, Storage
from src.application.services.gdpr_service import GDPRService
from src.infrastructure.database.models import SessionModel

router = APIRouter(prefix="/sessions", tags=["gdpr"])


@router.delete("/{session_id}", status_code=200)
async def delete_session(
    session_id: str, db: DbSession, doc_repo: DocRepo, storage: Storage
):
    """Delete all session data (GDPR right to erasure)."""
    result = await db.execute(
        select(SessionModel).where(SessionModel.id == session_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Session not found")

    service = GDPRService(db, doc_repo, storage)
    deleted = await service.delete_session_data(uuid.UUID(session_id))
    return {"message": "Session data deleted", "details": deleted}


@router.get("/{session_id}/export")
async def export_session(
    session_id: str, db: DbSession, doc_repo: DocRepo, storage: Storage
):
    """Export all session data as JSON (GDPR data portability)."""
    result = await db.execute(
        select(SessionModel).where(SessionModel.id == session_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Session not found")

    service = GDPRService(db, doc_repo, storage)
    return await service.export_session_data(uuid.UUID(session_id))
