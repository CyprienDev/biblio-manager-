def is_available(copy) -> bool:
    return copy.status in {"available", "repair"}
