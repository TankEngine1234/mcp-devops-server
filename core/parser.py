import re
from pydantic import BaseModel
from typing import Optional

class ParsedQuery(BaseModel):
    intent: str
    service: Optional[str] = None
    raw: str

def parse_query(query: str) -> ParsedQuery:
    """
    A simple keyword-based parser.
    """
    query_lower = query.lower()
    
    # --- Intent 1: Find Failure Cause ---
    # UPDATED REGEX:
    # This now matches "why is 'auth-service' failing" OR "why is auth-service failing"
    failure_match = re.search(
        r"why is ['\"]?(\S+)['\"]? (failing|down|broken)", # <--- THIS LINE IS UPDATED
        query_lower
    )
    if failure_match:
        # group(1) is the (S+) part, which is our service name
        service_name = failure_match.group(1) 
        return ParsedQuery(
            intent="find_failure_cause",
            service=service_name,
            raw=query
        )

    # --- Default/Fallback Intent ---
    return ParsedQuery(
        intent="unknown",
        raw=query
    )