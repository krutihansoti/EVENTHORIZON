import aiosqlite
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. SECURELY INITIALIZE GEMINI
load_dotenv() # This reads your hidden .env file
gemini_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_key)

class ThreatIntelAgent:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def process_query(self, query: str) -> str:
        print(f"🧠 [Gemini AI] Processing NLQ: {query}")
        
        # Initialize context_data up here so the fallback can access it even if Gemini fails
        context_data = {"risky_users": [], "compromised_zones": [], "failing_devices": []}
        
        try:
            # 2. GATHER LIVE CONTEXT FROM SQLITE
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                # Fetch Users
                c = await db.execute("SELECT target_id, alert_title FROM active_alerts WHERE target_type='USER'")
                context_data["risky_users"] = [dict(r) for r in await c.fetchall()]
                
                # Fetch Zones
                c = await db.execute("SELECT target_id, alert_title FROM active_alerts WHERE target_type='ZONE'")
                context_data["compromised_zones"] = [dict(r) for r in await c.fetchall()]
                
                # Fetch Devices
                c = await db.execute("SELECT target_id, alert_title FROM active_alerts WHERE target_type='DEVICE'")
                context_data["failing_devices"] = [dict(r) for r in await c.fetchall()]

            # 3. BUILD THE PROMPT FOR GEMINI
            prompt = f"""
            You are the EventHorizon AI, an elite Tier-1 SOC physical security assistant.
            You are responding directly to a human security operator's query on a dashboard.
            
            Here is the LIVE JSON state of our facility right now pulled from the database:
            {json.dumps(context_data, indent=2)}
            
            Operator's Query: "{query}"
            
            STRICT INSTRUCTIONS:
            1. Answer the operator's query accurately using ONLY the live JSON data provided above.
            2. If the data shows empty lists ([]), it means the facility is 100% secure in that category.
            3. Keep the response concise, professional, and urgent.
            4. FORMATTING: You must format your response using ONLY basic HTML tags (<b>, <i>, <br>, <ul>, <li>). 
            5. Use HTML inline styles for colors (e.g., <b style='color:#ef4444;'> for critical things, <b style='color:#eab308;'> for warnings, <b style='color:#22c55e;'> for secure statuses).
            6. DO NOT wrap your response in ```html markdown blocks. Just return the raw HTML text.
            """
            
            # 4. ASK GEMINI
            response = await self.model.generate_content_async(prompt)
            return response.text
            
        except Exception as e:
            print(f"⚠️ Gemini Error/Offline: {e}")
            
            # 5. THE HARDCODED FALLBACK LOGIC
            num_users = len(context_data["risky_users"])
            num_zones = len(context_data["compromised_zones"])
            num_devs = len(context_data["failing_devices"])
            
            total_alerts = num_users + num_zones + num_devs
            color = "#ef4444" if total_alerts > 0 else "#22c55e"
            
            fallback_html = f"""
            <strong style="color:#eab308;">⚠️ Tactical Fallback Mode</strong><br>
            <i style="color:#94a3b8; font-size:11px;">(Generative AI connection unavailable. Displaying raw telemetry.)</i><br><br>
            
            <b>Current Threat Overview:</b><br>
            • Risky Personnel: <b style="color:{'#ef4444' if num_users > 0 else '#22c55e'}">{num_users}</b><br>
            • Compromised Zones: <b style="color:{'#ef4444' if num_zones > 0 else '#22c55e'}">{num_zones}</b><br>
            • Failing Hardware: <b style="color:{'#ef4444' if num_devs > 0 else '#22c55e'}">{num_devs}</b><br><br>
            
            Total Active Alerts: <b style="color:{color}">{total_alerts}</b><br>
            <i style="color:#94a3b8; font-size:11px;">Please refer to the dashboard lists below for exact Entity IDs.</i>
            """
            return fallback_html