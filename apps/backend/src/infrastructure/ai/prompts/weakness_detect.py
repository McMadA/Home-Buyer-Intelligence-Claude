STRENGTHS_WEAKNESSES_TOOL = {
    "name": "identify_strengths_weaknesses",
    "description": "Identify property strengths and weaknesses for a Dutch home buyer",
    "input_schema": {
        "type": "object",
        "properties": {
            "strengths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of property strengths and positive aspects"
            },
            "weaknesses": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of property weaknesses and concerns"
            }
        },
        "required": ["strengths", "weaknesses"]
    }
}

STRENGTHS_WEAKNESSES_PROMPT = """You are an expert Dutch real estate advisor. Based on the following document text and extracted property data, identify the key strengths and weaknesses of this property for a potential buyer.

Property data:
{property_data}

Consider factors like:
- Location and neighborhood quality
- Building condition and age
- Energy efficiency
- Price relative to market
- HOA situation (if apartment)
- Garden, parking, storage
- Room layout and living space
- Future value potential
- Required maintenance/renovations

Provide clear, actionable insights in Dutch real estate context. Each strength/weakness should be a concise but informative sentence.

Document text:
{text}"""
