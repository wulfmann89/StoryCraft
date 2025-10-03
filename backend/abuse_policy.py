import datetime
import json
import os

ABUSE_LOG_PATH = "Logs/abuse_log.json"

# Log an abuse incident with timestamp and details
def log_incident(user_id: str, incident_type: str, details: str):
    incident = {
        "user_id": user_id,
        "incident_type": incident_type,
        "details": details,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    os.makedirs(os.path.dirname(ABUSE_LOG_PATH), exist_ok=True)
    if os.path.exists(ABUSE_LOG_PATH, "r"):
        with open(ABUSE_LOG_PATH, "r") as f:
            log = json.load(f)
    else:
        log = []
    log.append(incident)
    with open(ABUSE_LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

# Revoke user access (placeholder logic)
def revoke_access(user_id: str):
    # This could disable session, flag account or notify admin
    print(f"Access revoked for user: {user_id}")
    log_incident(user_id, "access_revoked", "User access revoked due to abuse")

# Check if user has prior incidents
def get_user_incidents(user_id: str) -> list:
    if not os.path.exists(ABUSE_LOG_PATH):
        return[]
    with open(ABUSE_LOG_PATH, "r") as f:
        log= json.load(f)
        if user_id == "*":
            return log
        return[entry for entry in log if entry[user_id] == user_id]