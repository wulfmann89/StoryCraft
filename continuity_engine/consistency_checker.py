def check_consistency(entity_profiles, timeline_events):
    issues = []
    for entity_id, profile in entity_profiles.items():
        if "age" in profile and entity_id in timeline_events:
            expected_age = timeline_events[entity_id].get("age")
            if expected_age and profile["age"] != expected_age:
                issues.append(f"{profile['name']} has age mismatch: {profile['age']} vs {expected_age}")
        # Add more checks: traits, relationships, roles, etc.

    return issues