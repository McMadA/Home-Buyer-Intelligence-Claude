import uuid
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.infrastructure.database.engine import async_session_factory
from src.infrastructure.database.models import AuditLogModel

logger = logging.getLogger(__name__)


class AuditMiddleware(BaseHTTPMiddleware):
    """Log data access for GDPR compliance."""

    AUDITABLE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
    AUDIT_PATHS = {"/api/v1/sessions"}

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if request.method in self.AUDITABLE_METHODS:
            path = request.url.path
            if any(path.startswith(p) for p in self.AUDIT_PATHS):
                await self._log_access(request, response.status_code)

        return response

    async def _log_access(self, request: Request, status_code: int):
        try:
            parts = request.url.path.split("/")
            session_id = None
            for i, part in enumerate(parts):
                if part == "sessions" and i + 1 < len(parts):
                    session_id = parts[i + 1]
                    break

            async with async_session_factory() as session:
                log = AuditLogModel(
                    id=str(uuid.uuid4()),
                    session_id=session_id,
                    action=f"{request.method} {request.url.path}",
                    resource_type="session",
                    resource_id=session_id,
                    details={"status_code": status_code},
                    ip_address=request.client.host if request.client else None,
                )
                session.add(log)
                await session.commit()
        except Exception as e:
            logger.warning(f"Failed to write audit log: {e}")
