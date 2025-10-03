import datetime
import json
import os

APPEAL_LOG_PATH = "logs/appeals.json"

# Submit an appeal for a flagged incident
def submit_appeal(user_id: str, incident_id: str, message: str):
    appeal = {
        "user_id": user_id,
        "incident_id": incident_id,
        "message": message,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "status": "pending"
    }
    os.makedirs(os.path.dirname(APPEAL_LOG_PATH), exist_ok=True)
    if os.path.exists(APPEAL_LOG_PATH):
        with open(APPEAL_LOG_PATH, "r") as f:
            appeals = json.load(f)
    else:
        appeals = []
    appeals.append(appeal)
    with open(APPEAL_LOG_PATH, "w") as f:
        json.dump(appeals, f, indent=2)

# Generate a review report for a specific incident
def generate_review_report(incident_id: str):
    from backend.abuse_policy import get_user_incidents
    report = {
        "incident_id": incident_id,
        "related_entries": []
    }
    # Search abuse log for matching incident
    incidents = get_user_incidents("*")                                                     # WWildcard to get all entries
    for entry in incidents:
        if entry.get("incident_type") == incident_id or entry.get("timestamp") == incident_id:
            report["related_entries"].append(entry)
    return report             

# Update appeal status (e.g., approved, denied)
def update_appeal_status(incident_id: str, new_status: str):
    if not os.path.exists(APPEAL_LOG_PATH):
        return False
    with open(APPEAL_LOG_PATH, "r") as f:
        appeals = json.load(f)
    for appeal in appeals:
        if appeal["incident_id"] == incident_id:
            appeal["status"] = new_status
    with open(APPEAL_LOG_PATH, "w") as f:
        json.dump(appeals, f, indent=2)
    return True