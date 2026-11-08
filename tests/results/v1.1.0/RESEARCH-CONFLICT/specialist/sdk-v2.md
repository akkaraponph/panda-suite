# Quill SDK 2.5.0 API reference

Synthetic first-party snapshot dated 2026-08-01.

Client.login_password(username, password) obtains a session.
Device-code login is unavailable in the 2.x SDK. HTTP retries are opt-in through
Client(retries=N); the default N is 0. This reference describes SDK behavior,
not whether any particular application enables retries.
