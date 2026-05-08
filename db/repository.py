import aiosqlite
import json
from typing import List, Dict
from datetime import datetime

class EventRepository:
    """Handle event storage and retrieval."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def insert_event(self, event: Dict) -> bool:
        """Store a single event into the database."""
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("""
                    INSERT INTO events_unified 
                    (event_id, timestamp, source, user_id, device_id, device_type, zone, 
                     action, event_type, severity, result, confidence, metadata, risk_contribution)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.get("event_id"),
                    event.get("timestamp"),
                    event.get("source"),
                    event.get("user_id"),
                    event.get("device_id"),
                    event.get("device_type"),
                    event.get("zone"),
                    event.get("action"),
                    event.get("event_type"),
                    event.get("severity"),
                    event.get("result"),
                    event.get("confidence"),
                    json.dumps(event.get("metadata", {})),
                    json.dumps(event.get("risk_contribution", {}))
                ))
                await db.commit()
                return True
            except Exception as e:
                print(f"❌ Error inserting event: {e}")
                return False
    
    async def get_recent_events(self, limit: int = 100) -> List[Dict]:
        """Get the last N events to show on the dashboard timeline."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT * FROM events_unified 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def count_events(self) -> int:
        """Count how many total events are in the database."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM events_unified")
            result = await cursor.fetchone()
            return result[0] if result else 0