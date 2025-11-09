import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

# Our application's core logic
from core.config import Settings, get_settings
from core.parser import ParsedQuery, parse_query
from core.engine import CorrelationEngine, get_correlation_engine

# --- Pydantic Models for API Request/Response ---

class AnalyzeRequest(BaseModel):
    query: str

class AnalyzeResponse(BaseModel):
    original_query: str
    context_package: str
    status: str
    errors: list[str] = []

# --- FastAPI App ---

app = FastAPI(
    title="MCP 'Code Red' DevOps Assistant",
    description="Analyzes a query to find the cause of a production failure."
)

# --- API Endpoint ---

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_failure(
    request: AnalyzeRequest,
    settings: Settings = Depends(get_settings), # Injected config
    engine: CorrelationEngine = Depends(get_correlation_engine) # Injected "brain"
):
    """
    Receives a user query, parses it, correlates events, 
    and returns a formatted context package.
    """
    try:
        # 1. Parse the user's query
        parsed_query: ParsedQuery = parse_query(request.query)

        # 2. Call the Correlation Engine based on intent
        if parsed_query.intent == "find_failure_cause":
            context_package = await engine.find_failure_cause(
                service_name=parsed_query.service
            )
        else:
            context_package = "CONTEXT: I can't understand that request. Try 'Why is [service] failing?'"

        # 3. Return the successful response
        return AnalyzeResponse(
            original_query=request.query,
            context_package=context_package,
            status="success"
        )
        
    except Exception as e:
        # Handle any errors gracefully
        return AnalyzeResponse(
            original_query=request.query,
            context_package="",
            status="error",
            errors=[f"An internal error occurred: {e}"]
        )

# --- Run the server ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)