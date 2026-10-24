# cycle825 — image-led data scene + strict script/caption gate (REVIEW ONLY)

## Delta from cycle824 (no duplicate experiment)
- The local sales_business 23.933s review MP4 uses prior cycle824 output, but replaces only center panel at 6.47–9.45s with a distinct, previously generated photo of a generic laptop/desk. Top Japanese title, lower subtitles, and exact inherited AAC packets retained.
- Image is a conversation-generated original; NOT uploaded to GitHub. Internal review provenance is explicit; public-release rights and employee approval NOT established. Repository holds only reusable source.
- New image_scene825.py works for ten genre identifiers and fails closed on missing, untrusted or private asset manifests. No posting or publishing.
- New audit825.py compares all 8 narration SOURCE texts against all 24 ASS caption states; rejects wrong text, timing boundaries and overlap. This verifies the TTS INPUT script, NOT what a human actually hears. No ASR, naturalness or word-level alignment claim.
- CI generates separate ai_work Japanese Open JTalk narration and procedural artwork, renders a new MP4 and uploads a 7-day review artifact. CI does NOT use the conversation photo or inherited local audio.
- Local source: cycle824 sales_business review MP4; local output SHA256 3cf5dd5a286ce3f896b3df40e62218ba2d90841167123fb9fc6ebf291f361ce5. 1080x1920, H.264/30fps/718 frames, 23.933s, AAC/48kHz; full decode PASS; audio bitstream MD5 unchanged 8d0baabf50866471846346e7159046e2. Eight local unit tests PASS.

## Reproduce (internal review only)
    python -m unittest discover -s quality/cycle825 -p 'test_*.py' -v
    python quality/cycle825/audit825.py --root GENERATED_CI_DIR --report GENERATED_CI_DIR/output/audit825.json
    python quality/cycle825/image_scene825.py --source PREVIOUS_REVIEW.mp4 --image REVIEW_ASSET.png --manifest review_asset.json --output cycle825_REVIEW_ONLY.mp4 --genre sales_business --start 6.47 --duration 2.98

Provenance manifest example (only when true):
    {"origin":"user_conversation_generated","review_allowed":true,"private_data":false,"publication_approved":false}

## Reference and limitations
- Past TikTok市場分析 and TikTok動画研究 research summaries accessed; complete task/chat transcripts unavailable.
- User's 16-panel ChatGPT×Excel storyboard found and inspected. Reference v33 original MP4 unavailable this cycle; no direct visual equivalence test.
- Local video remains mixed procedural/photographic slideshow, not cinematic v33 parity. Still lacks full 16-scene visual variety, genuine PC demonstration and approved assets.
- Local inherited Japanese audio was bitstream-verified but not independently transcribed or checked against captions. CI script/caption parity does not prove spoken-audio parity.
- Smartphone device, licensing/publication, human listening, employee approval: pending.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, payment or TikTok posting.
