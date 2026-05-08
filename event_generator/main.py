from pydantic import BaseModel
from db.ai_agent import ThreatIntelAgent

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
import aiosqlite

from event_generator.simulator import EventSimulator
from db.database import init_db, save_event
from db.risk_scorer import RiskScorer

app = FastAPI()

# 1. DEFINE THIS FIRST
DB_PATH = "./eventhorizon.db"

class NLQRequest(BaseModel):
    query: str

# 2. NOW PYTHON KNOWS WHAT DB_PATH IS
ai_agent = ThreatIntelAgent(DB_PATH)
simulator = EventSimulator()
scorer = RiskScorer(DB_PATH)

latest_event = None

async def simulation_loop():
    global latest_event
    print("🚀 [Simulator] Engine started in background...")
    while True:
        try:
            event = simulator.generate_random_event()
            await save_event(event) # Crash-proofed with await
            latest_event = event
        except Exception as e:
            print(f"⚠️ Simulator Error: {e} - Retrying...")
        await asyncio.sleep(1.0) 

async def scoring_loop():
    while True:
        await asyncio.sleep(5)
        try:
            await scorer.score_all_entities()
        except Exception as e:
            print(f"⚠️ AI Engine Error: {e}")

@app.on_event("startup")
async def startup_event():
    init_db()
    asyncio.create_task(scoring_loop())
    asyncio.create_task(simulation_loop())

@app.get("/")
async def serve_dashboard():
    return FileResponse("event_generator/static/index.html")

@app.get("/live_logs")
async def serve_live_logs():
    return FileResponse("event_generator/static/live_logs.html")

@app.get("/stream")
async def stream_events(request: Request):
    async def event_generator():
        last_id = None
        while True:
            if await request.is_disconnected():
                break
            if latest_event and latest_event.get("event_id") != last_id:
                last_id = latest_event.get("event_id")
                yield {"event": "message", "data": json.dumps(latest_event)}
            await asyncio.sleep(0.5)
    return EventSourceResponse(event_generator())

@app.get("/api/scores/users")
async def get_user_scores():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM active_alerts WHERE target_type = 'USER' ORDER BY health_impact DESC LIMIT 5")
        rows = await cursor.fetchall()
        return [{"user_id": r["target_id"], "combined_score": r["health_impact"], "rule_score": r["health_impact"], "anomaly_score": 0, "alert_id": r["alert_id"]} for r in rows]

@app.get("/api/scores/zones")
async def get_zone_scores():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM active_alerts WHERE target_type = 'ZONE' ORDER BY health_impact DESC LIMIT 5")
        rows = await cursor.fetchall()
        return [{"zone": r["target_id"], "vulnerability_percent": r["health_impact"], "alert_id": r["alert_id"]} for r in rows]
        
@app.get("/api/scores/devices")
async def get_device_scores():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM active_alerts WHERE target_type = 'DEVICE' ORDER BY health_impact DESC LIMIT 5")
        rows = await cursor.fetchall()
        return [{"device_id": r["target_id"], "combined_score": r["health_impact"], "health_score": 1, "alert_id": r["alert_id"]} for r in rows]

@app.get("/api/evidence/{alert_id}")
async def get_evidence(alert_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT evidence_ids FROM active_alerts WHERE alert_id = ?", (alert_id,))
        row = await cursor.fetchone()
        if not row: return []
        
        event_ids = json.loads(row["evidence_ids"])
        if not event_ids: return []
        
        placeholders = ','.join('?' for _ in event_ids)
        query = f"SELECT * FROM events WHERE event_id IN ({placeholders}) ORDER BY timestamp DESC"
        cursor = await db.execute(query, event_ids)
        events = await cursor.fetchall()
        return [dict(e) for e in events]

@app.get("/api/ai/insiders")
async def get_insider_threats(): return []
@app.get("/api/ai/predictions")
async def get_predictions(): return []

@app.post("/api/ask_ai")
async def ask_ai(req: NLQRequest):
    response_text = await ai_agent.process_query(req.query)
    return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9091)