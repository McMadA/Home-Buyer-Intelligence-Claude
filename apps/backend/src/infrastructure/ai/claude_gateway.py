import json
import logging
from anthropic import AsyncAnthropic
from src.config import settings
from src.domain.enums import DocumentType
from src.domain.interfaces.ai_gateway import AIGateway
from src.infrastructure.ai.prompts.document_parse import (
    CLASSIFY_DOCUMENT_PROMPT,
    EXTRACT_PROPERTY_DATA_PROMPT,
    EXTRACT_PROPERTY_DATA_TOOL,
)
from src.infrastructure.ai.prompts.risk_detect import DETECT_RISKS_PROMPT, DETECT_RISKS_TOOL
from src.infrastructure.ai.prompts.weakness_detect import (
    STRENGTHS_WEAKNESSES_PROMPT,
    STRENGTHS_WEAKNESSES_TOOL,
)
from src.infrastructure.pdf.preprocessor import PIIPreprocessor

logger = logging.getLogger(__name__)

class ClaudeGateway(AIGateway):
    def __init__(self):
        self._client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._model = settings.claude_model
        self._preprocessor = PIIPreprocessor()

    async def classify_document(self, text: str) -> DocumentType:
        redacted = self._preprocessor.redact(text[:3000])
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": CLASSIFY_DOCUMENT_PROMPT.format(text=redacted),
            }],
        )
        result = response.content[0].text.strip().lower()
        try:
            return DocumentType(result)
        except ValueError:
            return DocumentType.OTHER

    async def extract_property_data(self, text: str, doc_type: DocumentType) -> dict:
        redacted = self._preprocessor.redact(text[:8000])
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=2000,
            tools=[EXTRACT_PROPERTY_DATA_TOOL],
            tool_choice={"type": "tool", "name": "extract_property_data"},
            messages=[{
                "role": "user",
                "content": EXTRACT_PROPERTY_DATA_PROMPT.format(
                    doc_type=doc_type.value, text=redacted
                ),
            }],
        )
        for block in response.content:
            if block.type == "tool_use":
                return block.input
        return {}

    async def detect_risks(self, text: str, doc_type: DocumentType) -> list[dict]:
        redacted = self._preprocessor.redact(text[:8000])
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=3000,
            tools=[DETECT_RISKS_TOOL],
            tool_choice={"type": "tool", "name": "detect_risks"},
            messages=[{
                "role": "user",
                "content": DETECT_RISKS_PROMPT.format(
                    doc_type=doc_type.value, text=redacted
                ),
            }],
        )
        for block in response.content:
            if block.type == "tool_use":
                return block.input.get("risks", [])
        return []

    async def identify_strengths_weaknesses(self, text: str, property_data: dict) -> dict:
        redacted = self._preprocessor.redact(text[:6000])
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=2000,
            tools=[STRENGTHS_WEAKNESSES_TOOL],
            tool_choice={"type": "tool", "name": "identify_strengths_weaknesses"},
            messages=[{
                "role": "user",
                "content": STRENGTHS_WEAKNESSES_PROMPT.format(
                    property_data=json.dumps(property_data, indent=2),
                    text=redacted,
                ),
            }],
        )
        for block in response.content:
            if block.type == "tool_use":
                return block.input
        return {"strengths": [], "weaknesses": []}
