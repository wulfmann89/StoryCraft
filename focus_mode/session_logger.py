import json
import os
from datetime import datetime

LOG_PATH = "logs/focus_sessions.json"

def log_session(start_time, end_time, interrupted=False):
    session = {
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "duration_minutes": round((end_time - start_time).total_seconds() / 60, 2),
        "interrupted": interrupted
    }
    sessions = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            try:
                sessions = json.load(f)
            except json.JSONDecodeError:
                sessions = []
    sessions.insert(0, session)
    with open(LOG_PATH, "w") as f:
        json.dump(sessions, f, indent=2)