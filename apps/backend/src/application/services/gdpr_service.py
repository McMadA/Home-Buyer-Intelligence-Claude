import logging
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interfaces.document_repository import DocumentRepository
from src.domain.interfaces.document_storage import DocumentStorage
from src.infrastructure.database.models import (
    SessionModel,
    AnalysisResultModel,
    PropertyModel,
    AuditLogModel,
)

logger = logging.getLogger(__name__)


class GDPRService:
    def __init__(
        self,
        db_session: AsyncSession,
        doc_repo: DocumentRepository,
        storage: DocumentStorage,
    ):
        self._db = db_session
        self._doc_repo = doc_repo
        self._storage = storage

    async def export_session_data(self, session_id: UUID) -> dict:
        """Export all data for a session as JSON (GDPR data portability)."""
        sid = str(session_id)

        result = await self._db.execute(
            select(SessionModel).where(SessionModel.id == sid)
        )
        session = result.scalar_one_or_none()

        documents = await self._doc_repo.get_by_session(session_id)

        result = await self._db.execute(
            select(AnalysisResultModel).where(AnalysisResultModel.session_id == sid)
        )
        analyses = result.scalars().all()

        result = await self._db.execute(
            select(PropertyModel).where(PropertyModel.session_id == sid)
        )
        properties = result.scalars().all()

        result = await self._db.execute(
            select(AuditLogModel).where(AuditLogModel.session_id == sid)
        )
        audit_logs = result.scalars().all()

        return {
            "session": {
                "id": sid,
                "created_at": session.created_at.isoformat() if session else None,
            },
            "documents": [
                {
                    "id": str(doc.id),
                    "filename": doc.filename,
                    "document_type": (
                        doc.document_type.value
                        if hasattr(doc.document_type, "value")
                        else doc.document_type
                    ),
                    "file_size_bytes": doc.file_size_bytes,
                    "created_at": (
                        doc.created_at.isoformat() if doc.created_at else None
                    ),
                }
                for doc in documents
            ],
            "analyses": [
                {
                    "id": a.id,
                    "status": a.status,
                    "property_data": a.property_data,
                    "strengths": a.strengths,
                    "weaknesses": a.weaknesses,
                    "risk_score": a.risk_score,
                    "bidding_advice": a.bidding_advice,
                    "created_at": (
                        a.created_at.isoformat() if a.created_at else None
                    ),
                }
                for a in analyses
            ],
            "properties": [
                {
                    "id": p.id,
                    "address": p.address,
                    "postal_code": p.postal_code,
                    "city": p.city,
                }
                for p in properties
            ],
            "audit_logs": [
                {
                    "action": log.action,
                    "resource_type": log.resource_type,
                    "created_at": (
                        log.created_at.isoformat() if log.created_at else None
                    ),
                }
                for log in audit_logs
            ],
            "exported_at": datetime.utcnow().isoformat(),
        }

    async def delete_session_data(self, session_id: UUID) -> dict:
        """Delete all data for a session (GDPR right to erasure)."""
        sid = str(session_id)
        deleted = {
            "files": 0,
            "documents": 0,
            "analyses": 0,
            "properties": 0,
            "audit_logs": 0,
        }

        deleted["files"] = await self._storage.delete_session(session_id)
        deleted["documents"] = await self._doc_repo.delete_by_session(session_id)

        result = await self._db.execute(
            delete(AnalysisResultModel).where(AnalysisResultModel.session_id == sid)
        )
        deleted["analyses"] = result.rowcount

        result = await self._db.execute(
            delete(PropertyModel).where(PropertyModel.session_id == sid)
        )
        deleted["properties"] = result.rowcount

        result = await self._db.execute(
            delete(AuditLogModel).where(AuditLogModel.session_id == sid)
        )
        deleted["audit_logs"] = result.rowcount

        await self._db.execute(delete(SessionModel).where(SessionModel.id == sid))
        await self._db.commit()

        logger.info(f"Deleted all data for session {session_id}: {deleted}")
        return deleted
