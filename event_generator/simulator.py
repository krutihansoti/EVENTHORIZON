import random
import time
from datetime import datetime
from event_generator.devices import DEVICES, USERS

class EventSimulator:
    def __init__(self):
        self.event_counter = 0
        self.event_queue = []

    def _next_id(self):
        self.event_counter += 1
        return f"EVT-{int(time.time())}-{self.event_counter:04d}"

    def _create_event(self, device_id, action, user_id="—", severity="INFO", description="", risk=None):
        if risk is None: risk = {}
        dev = DEVICES[device_id]
        return {
            "event_id": self._next_id(),
            "timestamp": datetime.now().isoformat(),
            "site": dev["site"],
            "zone": dev["zone"],
            "device_id": dev["name"],
            "device_type": dev["type"],
            "user_id": user_id,
            "action": action,
            "severity": severity,
            "description": description,
            "risk_contribution": risk
        }

    def generate_random_event(self):
        if not self.event_queue:
            self._generate_scenario()
        return self.event_queue.pop(0)

    def _generate_scenario(self):
        scenario = random.choices(
            ["NORMAL_FLOW", "TAILGATING", "HELD_OPEN", "IMPOSSIBLE_TRAVEL", "HARDWARE_BREACH", "ANTI_PASSBACK", "DEVICE_OFFLINE"],
            weights=[0.40, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10]
        )[0]

        u_id, u_name = random.choice(list(USERS.items()))
        user_display = f"{u_name} ({u_id})"
        
        site = random.choice(["Site-1", "Site-2"])
        reader_in_id = random.choice([k for k, v in DEVICES.items() if v["type"] == "reader" and v["site"] == site and "IN" in k])
        door_id = DEVICES[reader_in_id]["door_id"]
        cam_door_id = [k for k, v in DEVICES.items() if v["type"] == "camera" and v.get("door_id") == door_id][0]

        if scenario == "NORMAL_FLOW":
            self.event_queue.append(self._create_event(reader_in_id, "ENTRY_PUNCH_ALLOWED", user_display, "INFO", "Valid badge read"))
            self.event_queue.append(self._create_event(door_id, "DOOR_OPEN", "—", "INFO", "Door opened"))
            self.event_queue.append(self._create_event(door_id, "DOOR_CLOSED", "—", "INFO", "Door closed"))

        elif scenario == "TAILGATING":
            self.event_queue.append(self._create_event(reader_in_id, "ENTRY_PUNCH_ALLOWED", user_display, "INFO", "Group lead"))
            self.event_queue.append(self._create_event(door_id, "DOOR_OPEN", "—", "INFO", "Door opened"))
            self.event_queue.append(self._create_event(cam_door_id, "TAILGATING_DETECTED", user_display, "CRITICAL", "Headcount mismatch", {"user_risk_impact": 30, "zone_risk_impact": 50}))
            self.event_queue.append(self._create_event(door_id, "DOOR_CLOSED", "—", "INFO", "Door closed"))

        elif scenario == "HELD_OPEN":
            self.event_queue.append(self._create_event(reader_in_id, "ENTRY_PUNCH_ALLOWED", user_display, "INFO", "Valid badge read"))
            self.event_queue.append(self._create_event(door_id, "DOOR_OPEN", "—", "INFO", "Door opened"))
            self.event_queue.append(self._create_event(door_id, "DOOR_HELD_OPEN", "—", "HIGH", "Door open > 30s", {"zone_risk_impact": 25}))

        elif scenario == "IMPOSSIBLE_TRAVEL":
            other_site = "Site-2" if site == "Site-1" else "Site-1"
            other_reader_id = random.choice([k for k, v in DEVICES.items() if v["type"] == "reader" and v["site"] == other_site and "IN" in k])
            self.event_queue.append(self._create_event(reader_in_id, "ENTRY_PUNCH_ALLOWED", user_display, "INFO", "Valid badge read"))
            self.event_queue.append(self._create_event(other_reader_id, "IMPOSSIBLE_TRAVEL_DETECTED", user_display, "CRITICAL", "Velocity anomaly", {"user_risk_impact": 90}))

        elif scenario == "HARDWARE_BREACH":
            self.event_queue.append(self._create_event(door_id, "DOOR_FORCED_OPEN", "UNKNOWN", "CRITICAL", "Breach without badge", {"device_risk_impact": 50, "zone_risk_impact": 80}))

        elif scenario == "ANTI_PASSBACK":
            self.event_queue.append(self._create_event(reader_in_id, "ENTRY_PUNCH_DENIED", user_display, "HIGH", "Anti-Passback: No Exit", {"user_risk_impact": 20}))
            
        elif scenario == "DEVICE_OFFLINE":
            random_device_id = random.choice(list(DEVICES.keys()))
            self.event_queue.append(self._create_event(random_device_id, "DEVICE_OFFLINE", "SYSTEM", "HIGH", "Heartbeat lost", {"device_risk_impact": 80, "zone_risk_impact": 40}))
            self.event_queue.append(self._create_event(random_device_id, "DEVICE_ONLINE", "SYSTEM", "INFO", "Restored"))