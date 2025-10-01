def tag_entity(entity_id, scope="local"):
    if scope not in ["local", "universal"]:
        raise ValueError("Scope must be 'local' or 'universal'")
    return {
        "entity_id": entity_id,
        "scope": scope
    }