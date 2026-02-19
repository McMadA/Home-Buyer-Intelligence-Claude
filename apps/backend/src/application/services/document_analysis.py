import logging
from uuid import UUID
from datetime import datetime

from src.domain.enums import AnalysisStatus, RiskCategory, Severity, BiddingStrategyType
from src.domain.models.risk import RiskFinding, RiskScore
from src.domain.models.analysis import AnalysisResult
from src.domain.models.bidding import BiddingAdvice
from src.domain.interfaces.ai_gateway import AIGateway
from src.domain.interfaces.document_repository import DocumentRepository
from src.domain.interfaces.document_storage import DocumentStorage
from src.infrastructure.pdf.extractor import PDFExtractor

logger = logging.getLogger(__name__)


class DocumentAnalysisService:
    def __init__(
        self,
        ai_gateway: AIGateway,
        doc_repo: DocumentRepository,
        storage: DocumentStorage,
    ):
        self._ai = ai_gateway
        self._doc_repo = doc_repo
        self._storage = storage
        self._extractor = PDFExtractor()

    async def run_analysis(self, session_id: UUID) -> AnalysisResult:
        """Run full analysis pipeline on all documents in a session."""
        analysis = AnalysisResult(
            session_id=session_id, status=AnalysisStatus.EXTRACTING
        )

        documents = await self._doc_repo.get_by_session(session_id)
        if not documents:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = "No documents found for this session"
            return analysis

        all_text = ""

        for doc in documents:
            try:
                if not doc.extracted_text:
                    content = await self._storage.retrieve(doc.file_path)
                    text = await self._extractor.extract_text(content)
                    doc.extracted_text = text
                    await self._doc_repo.save(doc)

                doc_type = await self._ai.classify_document(doc.extracted_text)
                doc.document_type = doc_type
                await self._doc_repo.save(doc)

                all_text += f"\n\n--- {doc.filename} ({doc_type.value}) ---\n{doc.extracted_text}"
            except Exception as e:
                logger.error(f"Failed to process {doc.filename}: {e}")
                continue

        if not all_text.strip():
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = "Could not extract text from any documents"
            return analysis

        analysis.status = AnalysisStatus.ANALYZING
        try:
            property_data = await self._ai.extract_property_data(
                all_text, documents[0].document_type
            )
            analysis.property_data = property_data

            risk_dicts = await self._ai.detect_risks(
                all_text, documents[0].document_type
            )
            findings = []
            for r in risk_dicts:
                try:
                    findings.append(
                        RiskFinding(
                            category=RiskCategory(r.get("category", "structural")),
                            severity=Severity(r.get("severity", "low")),
                            title=r.get("title", "Unknown"),
                            description=r.get("description", ""),
                            source="ai_extraction",
                        )
                    )
                except (ValueError, KeyError):
                    continue

            sw = await self._ai.identify_strengths_weaknesses(all_text, property_data)
            analysis.strengths = sw.get("strengths", [])
            analysis.weaknesses = sw.get("weaknesses", [])

        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = f"AI analysis failed: {str(e)}"
            return analysis

        analysis.status = AnalysisStatus.SCORING
        analysis.risk_score = RiskScore.compute(findings)

        asking_price = property_data.get("asking_price")
        if asking_price and isinstance(asking_price, (int, float)) and asking_price > 0:
            analysis.bidding_advice = {
                BiddingStrategyType.CONSERVATIVE: BiddingAdvice(
                    strategy=BiddingStrategyType.CONSERVATIVE,
                    min_price=round(asking_price * 0.90),
                    max_price=round(asking_price * 0.97),
                    recommended_price=round(asking_price * 0.93),
                    explanation="Conservative strategy: bid below asking price, suitable for properties with significant risks or in a buyer's market.",
                ),
                BiddingStrategyType.COMPETITIVE: BiddingAdvice(
                    strategy=BiddingStrategyType.COMPETITIVE,
                    min_price=round(asking_price * 0.97),
                    max_price=round(asking_price * 1.05),
                    recommended_price=round(asking_price * 1.00),
                    explanation="Competitive strategy: bid around asking price. Balanced approach for average market conditions.",
                ),
                BiddingStrategyType.AGGRESSIVE: BiddingAdvice(
                    strategy=BiddingStrategyType.AGGRESSIVE,
                    min_price=round(asking_price * 1.03),
                    max_price=round(asking_price * 1.15),
                    recommended_price=round(asking_price * 1.08),
                    explanation="Aggressive strategy: bid above asking price. Suitable for high-demand properties or in a strong seller's market.",
                ),
            }

        analysis.status = AnalysisStatus.COMPLETE
        analysis.completed_at = datetime.utcnow()
        return analysis
