def normalize_labels(values):
    result = []
    for value in values:
        normalized = value.strip().lower()
        if normalized:
            result.append(normalized)
    return result
