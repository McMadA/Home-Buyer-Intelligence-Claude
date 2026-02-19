import io
import pdfplumber
import fitz  # PyMuPDF
import anyio

class PDFExtractor:
    """Extract text and tables from PDF files using pdfplumber (primary) and PyMuPDF (fallback)."""

    async def extract_text(self, content: bytes) -> str:
        text = await anyio.to_thread.run_sync(self._extract_with_pdfplumber, content)
        if not text or len(text.strip()) < 50:
            text = await anyio.to_thread.run_sync(self._extract_with_pymupdf, content)
        return text

    async def extract_tables(self, content: bytes) -> list[list[list[str]]]:
        return await anyio.to_thread.run_sync(self._extract_tables_pdfplumber, content)

    def _extract_with_pdfplumber(self, content: bytes) -> str:
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                pages = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages.append(text)
                return "\n\n".join(pages)
        except Exception:
            return ""

    def _extract_with_pymupdf(self, content: bytes) -> str:
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            pages = []
            for page in doc:
                pages.append(page.get_text())
            doc.close()
            return "\n\n".join(pages)
        except Exception:
            return ""

    def _extract_tables_pdfplumber(self, content: bytes) -> list[list[list[str]]]:
        tables = []
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
        except Exception:
            pass
        return tables
