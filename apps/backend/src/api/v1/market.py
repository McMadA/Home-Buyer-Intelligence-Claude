import uuid

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select

from src.api.dependencies import DbSession
from src.application.dto.market_dto import MarketDataResponse
from src.infrastructure.database.models import AnalysisResultModel
from src.infrastructure.external.bag_client import PDOKBAGClient
from src.infrastructure.external.ep_online_client import EPOnlineClient
from src.infrastructure.external.cbs_client import CBSStatLineClient
from src.application.services.market_intelligence import MarketIntelligenceService

router = APIRouter(prefix="/sessions", tags=["market"])


@router.get("/{session_id}/market", response_model=MarketDataResponse)
async def get_market_data(session_id: str, db: DbSession):
    """Get market context data for a session."""
    result = await db.execute(
        select(AnalysisResultModel).where(
            AnalysisResultModel.session_id == session_id
        )
    )
    analysis = result.scalar_one_or_none()
    if not analysis or not analysis.market_position:
        raise HTTPException(
            status_code=404,
            detail="No market data available. Run analysis first.",
        )

    mp = analysis.market_position
    area = mp.get("area_statistics") or {}

    return MarketDataResponse(
        municipality=area.get("municipality"),
        avg_purchase_price=area.get("avg_purchase_price"),
        num_transactions=area.get("num_transactions"),
        price_index=area.get("price_index"),
        period=area.get("period"),
        bag_data=mp.get("bag_data"),
        energy_label_data=mp.get("energy_label_data"),
    )
