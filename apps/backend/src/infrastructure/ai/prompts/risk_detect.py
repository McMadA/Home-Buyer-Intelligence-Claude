DETECT_RISKS_TOOL = {
    "name": "detect_risks",
    "description": "Detect risks and issues in a Dutch real estate document",
    "input_schema": {
        "type": "object",
        "properties": {
            "risks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": ["structural", "legal", "financial", "market"],
                            "description": "Risk category"
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"],
                            "description": "Severity level"
                        },
                        "title": {"type": "string", "description": "Short risk title"},
                        "description": {"type": "string", "description": "Detailed explanation of the risk and its potential impact"}
                    },
                    "required": ["category", "severity", "title", "description"]
                }
            }
        },
        "required": ["risks"]
    }
}

DETECT_RISKS_PROMPT = """You are an expert Dutch real estate risk assessor. Analyze the following {doc_type} document and identify ALL potential risks for a home buyer.

Consider these risk categories:

STRUCTURAL risks (building condition):
- Foundation issues (funderingsproblemen), especially in pre-1970 buildings
- Roof condition, moisture/water damage
- Asbestos presence (common in Dutch buildings 1950-1993)
- Concrete rot (betonrot)
- Wood rot, insect damage
- Outdated electrical/plumbing systems
- Poor insulation

LEGAL risks (ownership and restrictions):
- Erfpacht (ground lease) conditions and costs
- VvE (HOA) issues: underfunded reserves, pending assessments, disputes
- Zoning restrictions (bestemmingsplan)
- Right of way (erfdienstbaarheid)
- Monument status (monumentenstatus)
- Pending permits or violations
- Unusual clauses in purchase agreement

FINANCIAL risks (costs and value):
- Price significantly above market average
- High HOA fees relative to property value
- Energy label indicating high energy costs
- Required renovations and estimated costs
- Hidden costs (overdrachtsbelasting, notaris, etc.)
- Upcoming special assessments (VvE)

MARKET risks (market conditions):
- Area decline indicators
- Time on market (long time = potential issues)
- Price trend in the area

Be thorough but fair. Not everything is a risk - only flag genuine concerns.

Document text:
{text}"""
