def sync_and_refresh(version_id, invalidate, refresh):
    invalidate(version_id)
    refresh(version_id)
