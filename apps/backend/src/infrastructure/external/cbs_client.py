import logging
import httpx
from src.domain.interfaces.external_data import CBSClient

logger = logging.getLogger(__name__)

CBS_ODATA_BASE = "https://odata4.cbs.nl/CBS"

class CBSStatLineClient(CBSClient):
    """Client for CBS StatLine OData API for housing statistics."""

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=15.0)

    async def get_area_statistics(self, municipality: str) -> dict | None:
        try:
            # Escape single quotes for OData (e.g. 's-Hertogenbosch)
            safe_municipality = municipality.replace("'", "''")

            # Existing housing prices dataset
            response = await self._client.get(
                f"{CBS_ODATA_BASE}/83913NED/Observations",
                params={
                    "$filter": f"contains(RegioS, '{safe_municipality}')",
                    "$top": 5,
                    "$orderby": "Perioden desc",
                },
            )
            response.raise_for_status()
            data = response.json()
            observations = data.get("value", [])
            if not observations:
                return None
            latest = observations[0]
            return {
                "municipality": municipality,
                "avg_purchase_price": latest.get("GemiddeldeVerkoopprijs_1"),
                "num_transactions": latest.get("AantalVerkopen_2"),
                "price_index": latest.get("PrijsindexBestaandeKoopwoningen_3"),
                "period": latest.get("Perioden"),
            }
        except Exception as e:
            logger.warning(f"CBS StatLine lookup failed: {e}")
            return None

    async def close(self):
        await self._client.aclose()
