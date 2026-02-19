from abc import ABC, abstractmethod


class BAGClient(ABC):
    @abstractmethod
    async def lookup_building(self, address: str, postal_code: str) -> dict | None: ...


class EnergyLabelClient(ABC):
    @abstractmethod
    async def lookup_label(self, postal_code: str, house_number: str) -> dict | None: ...


class CBSClient(ABC):
    @abstractmethod
    async def get_area_statistics(self, municipality: str) -> dict | None: ...
