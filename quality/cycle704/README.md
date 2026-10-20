# cycle704: verified first-second result hook (review only)

2026-10-20 JST. Based on cycle703's 20-second synthetic SUMIF demo.

## Change
- First 0.0–2.0 seconds: immediately show **verified** `6,000円` with
  `2,500 + 3,500` and an original procedural robot accent, instead of
  the previous question-only opening. Remaining 2–20 seconds retain
  the existing eight-scene teaching flow.
- Add a reusable ten-genre hook contract with false-result rejection,
  safe caption region, BGM-not-Japanese-speech detection and fail-closed
  human publication gate.

## Local evidence
- Local renderer `render_cycle704.py` and full reproducible QA bundle
  are attached to the ChatGPT cycle704 run, **not committed here**.
- Local tests: 29 passed (previous 19 + new 10).
- MP4: H.264/AAC, 1080x1920 output, 30 fps, 600 frames, 20.0s;
  original drawing canvas 540x960 upscaled to 1080x1920.
- Full video decode: PASS.
- SHA256: `84f42f09065eec7c40005ed13f17ac99b462467b3a34c45e8eaf408adb2ddfca`.
- Mean absolute pixel difference at 0.4s vs cycle703: 50.763;
  at unchanged 5.0s: 0.064.
- Japanese narration: NOT GENERATED (BGM ONLY). No speech-caption sync.
- Original v33 MP4 not available for direct comparison; no equivalence claim.
- User reference storyboard images not reused in MP4. Fictional amounts only.

## CI and release
Attempt to add `.github/workflows/cycle704-hook-qa.yml` was blocked
by connector safety checks. **No GitHub Actions run** for this cycle.
This PR is a DRAFT. No merge, automatic posting, payment or publication.
Next: recover free Japanese narration and speech-aligned captions,
restore CI registration, persist the exact local renderer, phone QA.
