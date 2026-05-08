import sqlite3
import aiosqlite
import json
import uuid
from datetime import datetime

DB_PATH = "./eventhorizon.db"

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    cursor = conn.cursor()
    
    # 1. THE HISTORIAN
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        event_id TEXT, timestamp TEXT, site TEXT, zone TEXT, 
        device_id TEXT, device_type TEXT, action TEXT, 
        user_id TEXT, severity TEXT, description TEXT, 
        risk_contribution TEXT, raw_data TEXT
    )''')
    
    # 2. ENTITY STATE 
    cursor.execute('''CREATE TABLE IF NOT EXISTS entity_state (
        entity_id TEXT PRIMARY KEY, 
        entity_type TEXT,  
        current_zone TEXT,
        last_seen TEXT,
        current_health_score REAL DEFAULT 100.0
    )''')
    
    # 3. ACTIVE ALERTS 
    cursor.execute('''CREATE TABLE IF NOT EXISTS active_alerts (
        alert_id TEXT PRIMARY KEY,
        target_id TEXT,       
        target_type TEXT,     
        alert_title TEXT,     
        severity TEXT,        
        health_impact REAL,   
        evidence_ids TEXT,    
        timestamp TEXT
    )''')
    
    conn.commit()
    conn.close()

async def save_event(event_data):
    event_id = event_data.get("event_id") or str(uuid.uuid4())
    
    # Async connection prevents the "Database is locked" crash
    async with aiosqlite.connect(DB_PATH, timeout=15.0) as db:
        await db.execute('''
            INSERT INTO events (event_id, timestamp, site, zone, device_id, device_type, action, user_id, severity, description, risk_contribution, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_id, 
            event_data.get("timestamp"), 
            event_data.get("site"), 
            event_data.get("zone"), 
            event_data.get("device_id"), 
            event_data.get("device_type", "reader"), 
            event_data.get("action"), 
            event_data.get("user_id"), 
            event_data.get("severity"), 
            event_data.get("description"), 
            json.dumps(event_data.get("risk_contribution", {})), 
            json.dumps(event_data)
        ))
        await db.commit()