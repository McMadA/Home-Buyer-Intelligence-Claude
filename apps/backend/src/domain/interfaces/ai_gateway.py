from abc import ABC, abstractmethod
from ..enums import DocumentType


class AIGateway(ABC):
    @abstractmethod
    async def classify_document(self, text: str) -> DocumentType: ...

    @abstractmethod
    async def extract_property_data(self, text: str, doc_type: DocumentType) -> dict: ...

    @abstractmethod
    async def detect_risks(self, text: str, doc_type: DocumentType) -> list[dict]: ...

    @abstractmethod
    async def identify_strengths_weaknesses(self, text: str, property_data: dict) -> dict: ...
