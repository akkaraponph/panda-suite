def cancel(order, actor_id):
    if order["owner_id"] != actor_id:
        raise PermissionError("owner required")
    if order["status"] == "shipped":
        raise ValueError("already shipped")
    return {**order, "status": "cancelled"}
