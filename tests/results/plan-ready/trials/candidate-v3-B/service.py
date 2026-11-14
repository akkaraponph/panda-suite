"""Small, current approval service. No HTTP server or database is implemented."""


def approve(request, actor):
    if actor["role"] != "manager":
        raise PermissionError("manager required")
    if request["status"] != "pending":
        raise ValueError("request must be pending")
    return {**request, "status": "approved", "reviewer_id": actor["id"]}


def label(request):
    return f'{request["id"]}: {request["status"]}'
