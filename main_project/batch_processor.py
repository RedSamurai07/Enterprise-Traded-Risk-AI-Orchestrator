import asyncio
import pandas as pd
from langgraph_agent import app

async def process_log_async(log: str):
    # Simulate async delay for API/Graph execution
    await asyncio.sleep(0.5)
    result = app.invoke({"incident_report": log})
    return {
        "original_log": log,
        "masked": result.get("masked_report"),
        "escalated": result.get("requires_human")
    }

async def main():
    logs = [
        "John Doe breached Delta limit on ACCT111.",
        "System latency caused 2ms delay.",
        "Jane Smith overrode VaR model for ACCT222."
    ]
    
    tasks = [process_log_async(log) for log in logs]
    results = await asyncio.gather(*tasks)
    
    # Process results with Pandas
    df = pd.DataFrame(results)
    print("--- EOD Batch Report ---")
    print(df.groupby('escalated').count())
    df.to_csv("eod_risk_report.csv", index=False)

if __name__ == "__main__":
    asyncio.run(main())
