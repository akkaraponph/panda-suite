"""Intentionally broken transfer implementation for investigation practice."""

import sqlite3


def transfer(db_path, from_id, to_id, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")

    connection = sqlite3.connect(db_path)
    try:
        connection.execute("BEGIN")
        sent = connection.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_id),
        )
        if sent.rowcount != 1:
            raise ValueError("source account not found")

        received = connection.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_id),
        )
        if received.rowcount != 1:
            raise ValueError("destination account not found")
        return None
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
