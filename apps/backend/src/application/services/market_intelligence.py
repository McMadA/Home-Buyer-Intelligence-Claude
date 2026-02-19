import logging
import re

from src.domain.interfaces.external_data import BAGClient, EnergyLabelClient, CBSClient

logger = logging.getLogger(__name__)


class MarketIntelligenceService:
    def __init__(
        self,
        bag_client: BAGClient,
        energy_client: EnergyLabelClient,
        cbs_client: CBSClient,
    ):
        self._bag = bag_client
        self._energy = energy_client
        self._cbs = cbs_client

    async def enrich(self, property_data: dict) -> dict:
        """Enrich property data with external API data."""
        result = {
            "bag_data": None,
            "energy_label_data": None,
            "area_statistics": None,
        }

        address = property_data.get("address", "")
        postal_code = property_data.get("postal_code", "")

        if address and postal_code:
            result["bag_data"] = await self._bag.lookup_building(address, postal_code)

        if postal_code:
            house_number = re.search(r"\d+", address or "")
            if house_number:
                result["energy_label_data"] = await self._energy.lookup_label(
                    postal_code, house_number.group()
                )

        municipality = None
        if result["bag_data"]:
            municipality = result["bag_data"].get("municipality")
        if municipality:
            result["area_statistics"] = await self._cbs.get_area_statistics(
                municipality
            )

        return result
