import re

class PIIPreprocessor:
    """Redact PII from text before sending to external AI services."""

    # Dutch BSN pattern (9 digits, often with dots or dashes)
    BSN_PATTERN = re.compile(r'\b\d{3}[.\-]?\d{3}[.\-]?\d{3}\b')

    # Dutch phone numbers
    PHONE_PATTERN = re.compile(r'\b(?:0|\+31[\s-]?)(?:[1-9]\d{1,2}[\s-]?\d{6,7}|\d{2}[\s-]?\d{7})\b')

    # Email addresses
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    # IBAN numbers
    IBAN_PATTERN = re.compile(r'\b[A-Z]{2}\d{2}[\s]?[A-Z]{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{2,4}\b')

    def redact(self, text: str) -> str:
        text = self.BSN_PATTERN.sub('[BSN_REDACTED]', text)
        text = self.PHONE_PATTERN.sub('[PHONE_REDACTED]', text)
        text = self.EMAIL_PATTERN.sub('[EMAIL_REDACTED]', text)
        text = self.IBAN_PATTERN.sub('[IBAN_REDACTED]', text)
        return text
