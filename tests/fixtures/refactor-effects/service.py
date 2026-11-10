def transfer(store, events, amount):
    store.begin()
    try:
        store.debit(amount)
        store.credit(amount)
        store.commit()
    except Exception:
        store.rollback()
        raise
    events.publish({"amount": amount})
