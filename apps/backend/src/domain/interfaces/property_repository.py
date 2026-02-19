from abc import ABC, abstractmethod
from uuid import UUID
from ..models.property import Property


class PropertyRepository(ABC):
    @abstractmethod
    async def save(self, prop: Property) -> Property: ...

    @abstractmethod
    async def get_by_id(self, prop_id: UUID) -> Property | None: ...
