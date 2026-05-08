import aiosqlite
import json
import uuid
from datetime import datetime, timedelta

class RiskScorer:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def score_all_entities(self):
        print("🧠 [AI Engine] Analyzing real event logs for threats...")
        
        async with aiosqlite.connect(self.db_path, timeout=15.0) as db:
            now = datetime.now()
            cutoff = (now - timedelta(minutes=15)).isoformat()

            await db.execute("DELETE FROM active_alerts")

            cursor = await db.execute("SELECT event_id, user_id, zone, device_id, action FROM events WHERE timestamp > ?", (cutoff,))
            recent_events = await cursor.fetchall()

            user_denials = {}
            zone_breaches = {}
            device_failures = {}

            for row in recent_events:
                eid, uid, zone, did, action = row
                
                if uid and uid not in ["SYSTEM", "UNKNOWN", "—"]:
                    if "DENIED" in action or "INVALID" in action:
                        if uid not in user_denials: user_denials[uid] = []
                        user_denials[uid].append(eid)
                        
                if zone:
                    if action in ["DOOR_FORCED_ALARM", "TAILGATING_DETECTED"]:
                        if zone not in zone_breaches: zone_breaches[zone] = []
                        zone_breaches[zone].append(eid)
                        
                if did:
                    if action in ["DEVICE_OFFLINE", "TAMPER_DETECTED"]:
                        if did not in device_failures: device_failures[did] = []
                        device_failures[did].append(eid)

            for uid, eids in user_denials.items():
                if len(eids) >= 1:  # Threshold is 1 so threats populate instantly
                    alert_id = f"ALERT-USR-{uid}"
                    await db.execute('''
                        INSERT INTO active_alerts (alert_id, target_id, target_type, alert_title, severity, health_impact, evidence_ids, timestamp) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (alert_id, uid, "USER", "Velocity Anomaly: Access Denied", "HIGH", 45.0, json.dumps(eids), now.isoformat()))

            for zone, eids in zone_breaches.items():
                if len(eids) > 0:
                    alert_id = f"ALERT-ZNE-{zone}"
                    await db.execute('''
                        INSERT INTO active_alerts (alert_id, target_id, target_type, alert_title, severity, health_impact, evidence_ids, timestamp) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (alert_id, zone, "ZONE", "Perimeter Breach: Forced Entry/Tailgating", "CRITICAL", 60.0, json.dumps(eids), now.isoformat()))

            for did, eids in device_failures.items():
                if len(eids) > 0:
                    alert_id = f"ALERT-DEV-{did}"
                    await db.execute('''
                        INSERT INTO active_alerts (alert_id, target_id, target_type, alert_title, severity, health_impact, evidence_ids, timestamp) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (alert_id, did, "DEVICE", "Hardware Compromise: Offline/Tamper", "HIGH", 50.0, json.dumps(eids), now.isoformat()))

            await db.commit()