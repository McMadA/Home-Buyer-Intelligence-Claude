import logging
import httpx
from src.domain.interfaces.external_data import BAGClient

logger = logging.getLogger(__name__)

BAG_BASE_URL = "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2"
PDOK_LOCATIESERVER = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/free"

class PDOKBAGClient(BAGClient):
    """Client for BAG data via PDOK APIs (no API key needed)."""

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=10.0)

    async def lookup_building(self, address: str, postal_code: str) -> dict | None:
        try:
            query = f"{address} {postal_code}"
            response = await self._client.get(
                PDOK_LOCATIESERVER,
                params={"q": query, "fq": "type:adres", "rows": 1},
            )
            response.raise_for_status()
            data = response.json()
            docs = data.get("response", {}).get("docs", [])
            if not docs:
                return None
            doc = docs[0]
            lat, lon = None, None
            if doc.get("centroide_ll"):
                try:
                    coords = doc["centroide_ll"].replace("POINT(", "").replace(")", "").split(" ")
                    if len(coords) >= 2:
                        lon = coords[0]
                        lat = coords[1]
                except Exception:
                    pass

            return {
                "bag_nummeraanduiding_id": doc.get("nummeraanduiding_id"),
                "address": doc.get("weergavenaam"),
                "municipality": doc.get("gemeentenaam"),
                "province": doc.get("provincienaam"),
                "lat": lat,
                "lon": lon,
                "year_built": doc.get("bouwjaar"),
                "usage_purpose": doc.get("gebruiksdoel"),
                "floor_area": doc.get("oppervlakte"),
            }
        except Exception as e:
            logger.warning(f"BAG lookup failed: {e}")
            return None

    async def close(self):
        await self._client.aclose()
