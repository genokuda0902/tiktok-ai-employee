# Cycle 1660 — delivery integrity

Baseline cycle1659: 15s, 1080x1920, AAC sound effects only; Japanese speech absent.

This change addresses issue #22: distinguish source-side resolution from recipient-side downloaded bytes. Recipient must run:

`python -m tools.delivery_integrity received.mp4 --expected-sha256 <sender-sha>`

A passing checksum/resolution check is **not** quality approval. Japanese narration, captions, license and human approval remain unverified. Local review render is not committed, and must not be published.

Prior research chat originals and reference MP4 were unavailable in this run. This is not v33 reproduction.
