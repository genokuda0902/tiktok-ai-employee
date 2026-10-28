# cycle945 — Spectral voice badge (review only)

Different from cycle944's voice-active subtitle fade restoration: the existing eight animated teal bars in the top VOICE badge now react to **eight actual frequency bands** of the mixed Japanese audio track, instead of responding mostly to overall loudness. No audio or subtitle text is regenerated.

Source: cycle944 SHA256 `1ce2fe9e1a0c65230b50dcc69c3bc6bf2fd3962ca3210ef95d47db99c4c3ebae`.
Output: cycle945 SHA256 `da1f21c64f7a00e7f8d612a83a18692f60c649d04205946a5fe70fbea6596d10`.

Local verified: 1080x1920 H.264, 30 fps, 691 frames, 23.033s, AAC mono 48kHz; full A/V decode passed; audio AAC bitstream identical. On actual decoded MP4, mean corresponding-band amplitude correlation increased from **0.413 to 0.728** (technical synchronization metric, not a human quality score). 11/11 unit tests passed. Nine samples outside the edited top header had MAE 1.3–1.8 due to re-encoding. Ten genre presets tested, but only one AI-productivity MP4 rendered.

Research context: previous TikTok market/video study summaries support 0–1.5s hook, 15–25s, short scenes, operation demo, before/after, mobile-safe Japanese captions, human approval and manual posting. The user's 16-panel reference storyboard was available as prior summary, not the v33 original MP4; no direct quality comparison was possible.

The audio meter analyzes **mixed audio**, not isolated voice. It does not recognize Japanese words. Independent ASR, narration-caption semantic alignment, subjective smartphone playback, commercial rights of inherited assets, employee approval and actual GitHub Actions billing remain unverified. The complete private MP4 is shared as a ChatGPT attachment only; GitHub CI tests code with synthetic signals and does not upload private media.

Local: `python -m unittest discover -s cycle945/tests -v`.
Render: `python cycle945/src/spectral_voice_meter.py --source SOURCE.mp4 --output OUT.mp4 --report render.json`.

No paid services, automatic posting, public media upload, unauthorized merge, or publication. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Employee approval is required before manual posting.
