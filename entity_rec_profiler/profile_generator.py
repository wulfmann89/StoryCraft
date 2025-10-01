from datetime import datetime

def generate_profile(entity):
    label = entity["label"]
    name = entity["text"]

    profile = {
        "name": name,
        "type": label,
        "traits": [],
        "roles": [],
        "relationships": [{"entity": None, "type": "Unknown", "strength": 0}],
        "perception": {"others": {}, "self": "Neutral"},
        "timeline": [],
        "emotional_tone": None,
        "metadata": {
            "source_text": name,
            "created_at": datetime.now().isoformat(),
            "confidence": 1.0
        }
    }

    # Basic defaults based on entity type

    if label == "PERSON":
        profile["traits"] = ["Unknown"]
        profile["roles"] = ["Character"]
        profile["emotional_tone"] = "Neutral"
    elif label == "GPE":
        profile["roles"] = ["Location"]
        profile["traits"] = ["Geopolitical Entity"]
    elif label == "ORG":
        profile["roles"] = ["Faction", "Group"]
        profile["traits"] = ["Organizational"]

    return profile