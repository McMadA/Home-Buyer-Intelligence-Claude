import json
import logging
from google import genai
from google.genai import types
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


def _claude_tool_to_gemini_declaration(tool: dict) -> types.FunctionDeclaration:
    """Convert a Claude-style tool dict to a Gemini FunctionDeclaration."""
    schema = tool["input_schema"]
    return types.FunctionDeclaration(
        name=tool["name"],
        description=tool["description"],
        parameters=schema,
    )


class GeminiGateway(AIGateway):
    def __init__(self):
        self._client = genai.Client(api_key=settings.google_api_key)
        self._model = settings.gemini_model
        self._preprocessor = PIIPreprocessor()

    async def classify_document(self, text: str) -> DocumentType:
        redacted = self._preprocessor.redact(text[:3000])
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=CLASSIFY_DOCUMENT_PROMPT.format(text=redacted),
            config=types.GenerateContentConfig(
                max_output_tokens=50,
            ),
        )
        result = response.text.strip().lower()
        try:
            return DocumentType(result)
        except ValueError:
            return DocumentType.OTHER

    async def extract_property_data(self, text: str, doc_type: DocumentType) -> dict:
        redacted = self._preprocessor.redact(text[:8000])
        func_decl = _claude_tool_to_gemini_declaration(EXTRACT_PROPERTY_DATA_TOOL)
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=EXTRACT_PROPERTY_DATA_PROMPT.format(
                doc_type=doc_type.value, text=redacted
            ),
            config=types.GenerateContentConfig(
                max_output_tokens=2000,
                tools=[types.Tool(function_declarations=[func_decl])],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode="ANY",
                        allowed_function_names=["extract_property_data"],
                    )
                ),
            ),
        )
        return self._extract_function_call_args(response)

    async def detect_risks(self, text: str, doc_type: DocumentType) -> list[dict]:
        redacted = self._preprocessor.redact(text[:8000])
        func_decl = _claude_tool_to_gemini_declaration(DETECT_RISKS_TOOL)
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=DETECT_RISKS_PROMPT.format(
                doc_type=doc_type.value, text=redacted
            ),
            config=types.GenerateContentConfig(
                max_output_tokens=3000,
                tools=[types.Tool(function_declarations=[func_decl])],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode="ANY",
                        allowed_function_names=["detect_risks"],
                    )
                ),
            ),
        )
        result = self._extract_function_call_args(response)
        return result.get("risks", [])

    async def identify_strengths_weaknesses(self, text: str, property_data: dict) -> dict:
        redacted = self._preprocessor.redact(text[:6000])
        func_decl = _claude_tool_to_gemini_declaration(STRENGTHS_WEAKNESSES_TOOL)
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=STRENGTHS_WEAKNESSES_PROMPT.format(
                property_data=json.dumps(property_data, indent=2),
                text=redacted,
            ),
            config=types.GenerateContentConfig(
                max_output_tokens=2000,
                tools=[types.Tool(function_declarations=[func_decl])],
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode="ANY",
                        allowed_function_names=["identify_strengths_weaknesses"],
                    )
                ),
            ),
        )
        result = self._extract_function_call_args(response)
        if not result:
            return {"strengths": [], "weaknesses": []}
        return result

    @staticmethod
    def _extract_function_call_args(response) -> dict:
        """Extract arguments from the first function call in the response."""
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    # function_call.args is a dict-like object
                    return dict(part.function_call.args)
        return {}
