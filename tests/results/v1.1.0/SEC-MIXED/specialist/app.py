"""Synthetic local audit fixture. No server, real secrets, or external services."""
import json
import pickle

# Treat request arguments as untrusted. These functions are the entry points.
def find_user(db, name):
    return db.execute("SELECT id FROM users WHERE name = '" + name + "'").fetchall()


def find_user_safe(db, name):
    return db.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchall()


def import_profile(body):
    return pickle.loads(body)


def parse_settings(body):
    return json.loads(body)


def read_invoice(db, actor, invoice_id):
    return db.execute("SELECT * FROM invoices WHERE id = ? AND owner_id = ?",
                      (invoice_id, actor["id"])).fetchone()


EXAMPLE_TOKEN = "YOUR_API_TOKEN_HERE"  # Placeholder in developer examples.
