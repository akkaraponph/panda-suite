def normalize_labels(values):
    return list(dict.fromkeys(
        value.strip().lower() for value in values if value.strip()
    ))
