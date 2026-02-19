import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.infrastructure.database.engine import init_db
from src.api.middleware.errors import ErrorHandlerMiddleware
from src.api.middleware.audit import AuditMiddleware
from src.api.v1 import documents, analysis, market, gdpr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Home Buyer Intelligence Engine",
    description="AI-powered Dutch home buyer document analysis and bidding advice",
    version="0.1.0",
    lifespan=lifespan,
)

# Store settings on app state for middleware access
app.state.settings = settings

# Middleware (order matters - last added = first executed)
app.add_middleware(AuditMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(documents.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
app.include_router(market.router, prefix="/api/v1")
app.include_router(gdpr.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "healthy", "environment": settings.environment}
