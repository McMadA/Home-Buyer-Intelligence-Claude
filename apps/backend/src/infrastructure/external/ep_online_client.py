import logging
import httpx
from src.config import settings
from src.domain.interfaces.external_data import EnergyLabelClient

logger = logging.getLogger(__name__)

EP_ONLINE_BASE = "https://public.ep-online.nl/api/v3"

class EPOnlineClient(EnergyLabelClient):
    """Client for EP-Online energy label API."""

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=10.0)
        self._api_key = settings.ep_online_api_key

    async def lookup_label(self, postal_code: str, house_number: str) -> dict | None:
        if not self._api_key:
            logger.info("EP-Online API key not configured, skipping energy label lookup")
            return None
        try:
            response = await self._client.get(
                f"{EP_ONLINE_BASE}/PandEnergielabel/Adres",
                params={
                    "postcode": postal_code.replace(" ", ""),
                    "huisnummer": house_number,
                },
                headers={"Authorization": f"Bearer {self._api_key}"},
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                return None
            label = data[0] if isinstance(data, list) else data
            return {
                "energy_label": label.get("labelLetter"),
                "energy_index": label.get("energieIndex"),
                "registration_date": label.get("opnamedatum"),
                "valid_until": label.get("geldigTot"),
            }
        except Exception as e:
            logger.warning(f"EP-Online lookup failed: {e}")
            return None

    async def close(self):
        await self._client.aclose()
