from src.infrastructure.pdf.preprocessor import PIIPreprocessor


def test_bsn_redaction():
    p = PIIPreprocessor()
    assert "[BSN_REDACTED]" in p.redact("BSN: 123456789")
    assert "[BSN_REDACTED]" in p.redact("BSN: 123.456.789")


def test_email_redaction():
    p = PIIPreprocessor()
    assert "[EMAIL_REDACTED]" in p.redact("Contact: test@example.com")


def test_iban_redaction():
    p = PIIPreprocessor()
    assert "[IBAN_REDACTED]" in p.redact("IBAN: NL91 ABNA 0417 1643 00")


def test_preserves_normal_text():
    p = PIIPreprocessor()
    text = "De woning is gelegen aan de Keizersgracht."
    assert p.redact(text) == text
