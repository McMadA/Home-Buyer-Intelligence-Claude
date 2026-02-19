import uuid
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import DbSession, DocRepo, Storage, AI, get_db_session
from src.application.services.document_analysis import DocumentAnalysisService
from src.application.services.market_intelligence import MarketIntelligenceService
from src.application.services.risk_scoring import RiskScoringService
from src.application.services.bidding_strategy import BiddingStrategyService
from src.application.dto.analysis_dto import (
    AnalysisResponse,
    AnalysisStatusResponse,
    RiskScoreDTO,
    RiskFindingDTO,
    BiddingAdviceDTO,
    PropertyDTO,
)
from src.infrastructure.database.models import SessionModel, AnalysisResultModel
from src.domain.enums import AnalysisStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions", tags=["analysis"])


@router.post("/{session_id}/analyze", status_code=202)
async def trigger_analysis(
    session_id: str,
    background_tasks: BackgroundTasks,
    db: DbSession,
    doc_repo: DocRepo,
    storage: Storage,
    ai: AI,
):
    """Trigger full analysis pipeline (runs in background)."""
    # Verify session exists
    result = await db.execute(
        select(SessionModel).where(SessionModel.id == session_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Session not found")

    # Check if analysis already exists
    result = await db.execute(
        select(AnalysisResultModel).where(
            AnalysisResultModel.session_id == session_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing and existing.status == AnalysisStatus.COMPLETE:
        raise HTTPException(
            status_code=409,
            detail="Analysis already complete. Delete session to re-analyze.",
        )

    # Create pending analysis record
    analysis_id = str(uuid.uuid4())
    if not existing:
        analysis_model = AnalysisResultModel(
            id=analysis_id, session_id=session_id, status=AnalysisStatus.PENDING
        )
        db.add(analysis_model)
        await db.commit()
    else:
        analysis_id = existing.id
        await db.execute(
            update(AnalysisResultModel)
            .where(AnalysisResultModel.id == analysis_id)
            .values(status=AnalysisStatus.PENDING, error_message=None)
        )
        await db.commit()

    # Run analysis in background
    background_tasks.add_task(_run_analysis_task, session_id, analysis_id)

    return {
        "session_id": session_id,
        "analysis_id": analysis_id,
        "status": "pending",
    }


async def _run_analysis_task(session_id: str, analysis_id: str):
    """Background task to run the full analysis pipeline."""
    from src.infrastructure.database.engine import async_session_factory
    from src.infrastructure.database.repositories.document_repo import (
        SQLDocumentRepository,
    )
    from src.infrastructure.storage.local_storage import LocalDocumentStorage
    from src.infrastructure.ai.claude_gateway import ClaudeGateway
    from src.infrastructure.external.bag_client import PDOKBAGClient
    from src.infrastructure.external.ep_online_client import EPOnlineClient
    from src.infrastructure.external.cbs_client import CBSStatLineClient
    from src.domain.enums import BiddingStrategyType
    from dataclasses import asdict

    async with async_session_factory() as db:
        try:
            doc_repo = SQLDocumentRepository(db)
            storage = LocalDocumentStorage()
            ai = ClaudeGateway()

            service = DocumentAnalysisService(ai, doc_repo, storage)

            # Update status
            await db.execute(
                update(AnalysisResultModel)
                .where(AnalysisResultModel.id == analysis_id)
                .values(status=AnalysisStatus.EXTRACTING)
            )
            await db.commit()

            # Run analysis
            result = await service.run_analysis(uuid.UUID(session_id))

            # Enrich with market data
            market_data = None
            if result.property_data and result.status == AnalysisStatus.COMPLETE:
                await db.execute(
                    update(AnalysisResultModel)
                    .where(AnalysisResultModel.id == analysis_id)
                    .values(status=AnalysisStatus.ENRICHING)
                )
                await db.commit()

                bag = PDOKBAGClient()
                energy = EPOnlineClient()
                cbs = CBSStatLineClient()
                market_service = MarketIntelligenceService(bag, energy, cbs)
                market_data = await market_service.enrich(result.property_data)

                # Re-score with market data
                risk_service = RiskScoringService()
                result.risk_score = risk_service.compute_score(
                    result.risk_score.findings if result.risk_score else [],
                    market_data,
                )

                # Re-generate bidding with market context
                asking_price = result.property_data.get("asking_price")
                if (
                    asking_price
                    and isinstance(asking_price, (int, float))
                    and asking_price > 0
                ):
                    bidding_service = BiddingStrategyService()
                    result.bidding_advice = bidding_service.generate_advice(
                        asking_price, result.risk_score, market_data
                    )

            # Serialize risk score
            risk_score_dict = None
            if result.risk_score:
                risk_score_dict = {
                    "overall_score": result.risk_score.overall_score,
                    "risk_level": result.risk_score.risk_level.value,
                    "category_scores": {
                        k.value: v
                        for k, v in result.risk_score.category_scores.items()
                    },
                    "findings": [
                        {
                            "category": f.category.value,
                            "severity": f.severity.value,
                            "title": f.title,
                            "description": f.description,
                            "source": f.source,
                        }
                        for f in result.risk_score.findings
                    ],
                }

            # Serialize bidding advice
            bidding_dict = None
            if result.bidding_advice:
                bidding_dict = {
                    k.value: {
                        "strategy": v.strategy.value,
                        "min_price": v.min_price,
                        "max_price": v.max_price,
                        "recommended_price": v.recommended_price,
                        "explanation": v.explanation,
                    }
                    for k, v in result.bidding_advice.items()
                }

            # Save results
            await db.execute(
                update(AnalysisResultModel)
                .where(AnalysisResultModel.id == analysis_id)
                .values(
                    status=result.status.value,
                    property_data=result.property_data,
                    strengths=result.strengths,
                    weaknesses=result.weaknesses,
                    risk_score=risk_score_dict,
                    market_position=market_data,
                    bidding_advice=bidding_dict,
                    completed_at=result.completed_at,
                    error_message=result.error_message,
                )
            )
            await db.commit()

        except Exception as e:
            logger.error(f"Analysis task failed: {e}")
            await db.execute(
                update(AnalysisResultModel)
                .where(AnalysisResultModel.id == analysis_id)
                .values(status=AnalysisStatus.FAILED, error_message=str(e))
            )
            await db.commit()


@router.get("/{session_id}/analysis/status", response_model=AnalysisStatusResponse)
async def get_analysis_status(session_id: str, db: DbSession):
    """Poll analysis progress."""
    result = await db.execute(
        select(AnalysisResultModel).where(
            AnalysisResultModel.session_id == session_id
        )
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(
            status_code=404, detail="No analysis found for this session"
        )

    progress_messages = {
        "pending": "Waiting to start...",
        "extracting": "Extracting text from documents...",
        "analyzing": "AI is analyzing your documents...",
        "enriching": "Enriching with market data...",
        "scoring": "Computing risk scores...",
        "complete": "Analysis complete!",
        "failed": f"Analysis failed: {analysis.error_message or 'Unknown error'}",
    }

    return AnalysisStatusResponse(
        session_id=uuid.UUID(session_id),
        status=analysis.status,
        progress_message=progress_messages.get(analysis.status, "Processing..."),
    )


@router.get("/{session_id}/analysis", response_model=AnalysisResponse)
async def get_analysis(session_id: str, db: DbSession):
    """Get complete analysis results."""
    result = await db.execute(
        select(AnalysisResultModel).where(
            AnalysisResultModel.session_id == session_id
        )
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(
            status_code=404, detail="No analysis found for this session"
        )

    # Parse risk score from JSON
    risk_score_dto = None
    if analysis.risk_score:
        rs = analysis.risk_score
        risk_score_dto = RiskScoreDTO(
            overall_score=rs.get("overall_score", 0),
            risk_level=rs.get("risk_level", "low"),
            category_scores=rs.get("category_scores", {}),
            findings=[RiskFindingDTO(**f) for f in rs.get("findings", [])],
        )

    # Parse bidding advice
    bidding_dto = None
    if analysis.bidding_advice:
        bidding_dto = {
            k: BiddingAdviceDTO(**v) for k, v in analysis.bidding_advice.items()
        }

    # Parse property data
    property_dto = None
    if analysis.property_data:
        property_dto = PropertyDTO(
            **{
                k: v
                for k, v in analysis.property_data.items()
                if k in PropertyDTO.model_fields
            }
        )

    return AnalysisResponse(
        id=uuid.UUID(analysis.id),
        session_id=uuid.UUID(analysis.session_id),
        status=analysis.status,
        property_data=property_dto,
        strengths=analysis.strengths or [],
        weaknesses=analysis.weaknesses or [],
        risk_score=risk_score_dto,
        market_position=analysis.market_position,
        bidding_advice=bidding_dto,
        created_at=analysis.created_at,
        completed_at=analysis.completed_at,
        error_message=analysis.error_message,
    )
