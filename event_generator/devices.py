USERS = {f"USR-{i:03d}": f"Employee {i}" for i in range(1, 20)}

DEVICES = {
    # ================= SITE 1: HEADQUARTERS =================
    # S1 - ZONE 1 (LOBBY)
    "R-S1-Z1-IN":  {"type": "reader", "site": "Site-1", "zone": "Z1-Lobby", "name": "Site-1 Zone-1 Door-1 Entry", "door_id": "D-S1-Z1"},
    "R-S1-Z1-OUT": {"type": "reader", "site": "Site-1", "zone": "Z1-Lobby", "name": "Site-1 Zone-1 Door-1 Exit", "door_id": "D-S1-Z1"},
    "D-S1-Z1":     {"type": "door",   "site": "Site-1", "zone": "Z1-Lobby", "name": "S1 Main Glass Door"},
    "C-S1-Z1-D":   {"type": "camera", "site": "Site-1", "zone": "Z1-Lobby", "name": "Cam-S1-Z1-Gateway", "loc": "gateway", "door_id": "D-S1-Z1"},
    "C-S1-Z1-I":   {"type": "camera", "site": "Site-1", "zone": "Z1-Lobby", "name": "Cam-S1-Z1-Internal", "loc": "inside"},

    # S1 - ZONE 2 (DATA CENTER)
    "R-S1-Z2-IN":  {"type": "reader", "site": "Site-1", "zone": "Z2-DataCenter", "name": "Site-1 Zone-2 Door-1 Entry", "door_id": "D-S1-Z2"},
    "R-S1-Z2-OUT": {"type": "reader", "site": "Site-1", "zone": "Z2-DataCenter", "name": "Site-1 Zone-2 Door-1 Exit", "door_id": "D-S1-Z2"},
    "D-S1-Z2":     {"type": "door",   "site": "Site-1", "zone": "Z2-DataCenter", "name": "S1 Vault Door"},
    "C-S1-Z2-D":   {"type": "camera", "site": "Site-1", "zone": "Z2-DataCenter", "name": "Cam-S1-Z2-Gateway", "loc": "gateway", "door_id": "D-S1-Z2"},

    # ================= SITE 2: BRANCH OFFICE =================
    # S2 - ZONE 1 (OFFICE)
    "R-S2-Z1-IN":  {"type": "reader", "site": "Site-2", "zone": "Z1-Office", "name": "Site-2 Zone-1 Door-1 Entry", "door_id": "D-S2-Z1"},
    "R-S2-Z1-OUT": {"type": "reader", "site": "Site-2", "zone": "Z1-Office", "name": "Site-2 Zone-1 Door-1 Exit", "door_id": "D-S2-Z1"},
    "D-S2-Z1":     {"type": "door",   "site": "Site-2", "zone": "Z1-Office", "name": "S2 Office Main Door"},
    "C-S2-Z1-D":   {"type": "camera", "site": "Site-2", "zone": "Z1-Office", "name": "Cam-S2-Z1-Gateway", "loc": "gateway", "door_id": "D-S2-Z1"},
}