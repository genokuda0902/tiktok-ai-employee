# cycle1030 — Calc correction focus (review only)

This cycle is a **reimplementation**, not original v33 code. At 14.18–16.76 seconds, it adds two transparent focus rings to the existing video: first the incorrect draft **45**, then the Calc verification of **46** (12+16+18). The original spreadsheet visual remains visible; only focus outlines and small labels are added. This is a fictional example, not real business data or a live ChatGPT recording.

Ten genre identifiers and review gates are supported, but only `ai_work` has a full MP4 verified. The inherited source audio and burned Japanese captions are retained. The code verifies stream identity and decodability; **it does not independently transcribe Japanese speech or prove caption semantic alignment**.

Local invocation:

```sh
python cycle1030/source/correction_proof.py --source /private/review-input.mp4 --output /private/review-output.mp4 --report /private/qa.json --expected-source-sha <actual_sha256> --genre ai_work --review-only
```

Requires FFmpeg, Pillow, Noto CJK. Fail closed for missing review flag, wrong SHA, wrong A/V format, missing input, or existing output. CI generates only synthetic 2-second H.264/AAC media and executes unit tests; it does not access or publish user media. The full 23.033-second review MP4 is delivered only in the private ChatGPT conversation.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Original v33 MP4 unavailable, inherited rights unverified, independent Japanese ASR and phone playback unverified. Do not merge, auto-post, pay for services, or publicly upload the inherited video.
