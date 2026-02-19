CLASSIFY_DOCUMENT_PROMPT = """You are a Dutch real estate document classifier. Analyze the following text extracted from a PDF and classify it into one of these document types:

- purchase_agreement: Koopovereenkomst / koopakte - the purchase contract
- energy_label: Energielabel - energy performance certificate
- inspection_report: Bouwkundig rapport / bouwtechnische keuring - building inspection report
- hoa_documents: VvE stukken - homeowners association documents (splitsingsakte, huishoudelijk reglement, jaarrekening, MJOP)
- property_listing: Brochure / funda listing - property marketing materials
- other: Any other document type

Return ONLY the document type string, nothing else.

Document text:
{text}"""

EXTRACT_PROPERTY_DATA_TOOL = {
    "name": "extract_property_data",
    "description": "Extract structured property data from a Dutch real estate document",
    "input_schema": {
        "type": "object",
        "properties": {
            "address": {"type": "string", "description": "Full street address (straat + huisnummer)"},
            "postal_code": {"type": "string", "description": "Dutch postal code (e.g., 1234 AB)"},
            "city": {"type": "string", "description": "City/municipality name"},
            "square_meters": {"type": "number", "description": "Living area in square meters (woonoppervlakte)"},
            "year_built": {"type": "integer", "description": "Year the building was constructed (bouwjaar)"},
            "energy_label": {"type": "string", "description": "Energy label (A++++ to G)"},
            "property_type": {"type": "string", "description": "Type: appartement, tussenwoning, hoekwoning, vrijstaand, twee-onder-een-kap, etc."},
            "asking_price": {"type": "number", "description": "Asking price in euros (vraagprijs)"},
            "hoa_monthly_cost": {"type": "number", "description": "Monthly HOA fee (VvE bijdrage) in euros"},
            "num_rooms": {"type": "integer", "description": "Number of rooms (kamers)"},
            "has_garden": {"type": "boolean", "description": "Whether property has a garden (tuin)"},
            "has_parking": {"type": "boolean", "description": "Whether property has parking (parkeerplaats/garage)"},
            "conditions": {"type": "array", "items": {"type": "string"}, "description": "Special conditions or clauses (ontbindende voorwaarden, bijzondere bepalingen)"},
            "transfer_date": {"type": "string", "description": "Planned transfer date (leveringsdatum)"},
            "confidence_notes": {"type": "object", "description": "For each field, note 'confirmed', 'inferred', or 'unknown'"}
        },
        "required": ["confidence_notes"]
    }
}

EXTRACT_PROPERTY_DATA_PROMPT = """You are an expert Dutch real estate document analyzer. Extract all structured property data from the following {doc_type} document.

IMPORTANT RULES:
- Only extract data that is explicitly stated in the document
- For fields you cannot find, omit them entirely
- Use the confidence_notes field to indicate for each extracted field whether it was:
  - "confirmed": explicitly stated in the document
  - "inferred": reasonably inferred from context
  - "unknown": could not be determined
- All prices should be in euros (numbers only, no currency symbols)
- Postal codes should be in format "1234 AB"
- Square meters should be the woonoppervlakte (living area), not total plot

Document text:
{text}"""
