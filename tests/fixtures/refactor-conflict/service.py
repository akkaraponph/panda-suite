def normalize_labels(values):
    return list(dict.fromkeys(v.strip().lower() for v in values if v.strip()))
