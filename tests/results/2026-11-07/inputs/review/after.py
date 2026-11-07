def cancel(order, actor_id):
    """Cancel an order before shipping."""
    if order["status"] == "shipped":
        raise ValueError("already shipped")
    return {**order, "status": "cancelled"}
