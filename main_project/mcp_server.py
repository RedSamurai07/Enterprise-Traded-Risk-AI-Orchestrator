from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="HSBC Risk MCP Server")

class PortfolioRequest(BaseModel):
    portfolio_id: str
    metric: str # 'VaR' or 'Greeks'

@app.post("/mcp/risk-calc")
async def calculate_risk(req: PortfolioRequest):
    
    if req.portfolio_id.startswith("ACCT"):
        raise HTTPException(status_code=400, detail="PII detected. Rejecting.")
    # Mocking a legacy quantitative risk system
    if req.metric == 'VaR':
        return {"portfolio": req.portfolio_id, "VaR_99": random.uniform(1000000, 5000000)}
    elif req.metric == 'Greeks':
        return {"Delta": 0.45, "Gamma": 0.02, "Vega": 0.15}
    return {"error": "Unknown metric"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
