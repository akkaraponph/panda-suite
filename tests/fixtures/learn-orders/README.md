# Parcel Orders

A small order service for learning request and worker boundaries. The original
overview says orders are saved synchronously in SQLite and notifications are
delivered exactly once before the request returns. Check the implementation and
tests before relying on that description.

The only checked-in configuration is for local development. No production
deployment record or design decision history is included.

For an interactive demo, the old onboarding notes recommend `python demo.py`.
Inspect what that command does before deciding whether it belongs in your task.
