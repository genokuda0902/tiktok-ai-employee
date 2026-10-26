# cycle881 — source-grounded proof and fail-closed Japanese caption review

Change from cycle880: the prior cycle animated the final CTA. This cycle instead
replaces the **upper 1450 px** of scene 05 (frames 336–421, 11.200–14.067s)
with three visible stages: source rows → purported AI result → arithmetic check.
The source and computed totals share the same fictional data. The renderer
rejects a mismatched claim instead of displaying it.

Ten genre-neutral Proof configurations are validated; only AI-work has a full
local review MP4. This is an **offline synthetic UI**, not real ChatGPT/Excel
screen recording or recovered v33 source. No real client data.

Local render, using private source video (Pillow, Noto CJK, FFmpeg required):

```bash
python cycle881/proof_audit_scene.py --source PRIVATE_CYCLE880.mp4 --output PRIVATE_CYCLE881.mp4 --manifest PRIVATE_MANIFEST.json --report PRIVATE_REPORT.json
```

Manifest must equal:
`{"review_only":true,"publication_approved":false,"external_upload":false,"automatic_posting":false,"source_rights_reviewed":false,"source_sha256":"<SHA256 OF INPUT>"}`.

Never upload the source, rendered private media, extracted audio or private
manifest to GitHub. Public CI uses only a one-second synthetic A/V clip.

**Japanese caption verification:** An inherited script is not an independent
transcript. `review_caption_alignment` fails closed without independently
checked spoken text and explicit human approval. A literal match does not
prove pronunciation. This run has no independent offline ASR model and cannot
claim speech-content or semantic timing verification.

Original v33 reference MP4 unavailable; no quality parity claim.
Source rights, smartphone playback, employee approval, retention metrics,
and actual Actions billing are unverified. No merge, posting, or paid services.
**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
