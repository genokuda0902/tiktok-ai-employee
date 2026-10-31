# cycle1141 — caption-island stabilization (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No automatic posting, merge, paid API or private-media upload.

Distinct from cycle1139: the previous 2.4% chapter-aware push-in enlarged and moved the burned Japanese subtitles. This change locks the lower narration card, audio meter, progress and footer at their original scale while preserving cinematic movement in the upper illustration. It feathers y=1220–1350 to avoid a hard horizontal seam. Ten color-agnostic genre identifiers; one real AI-workflow MP4 produced privately.

Local actual-video QA: 22.5 seconds, 675 frames, H264 1080x1920 30fps, AAC 48kHz, full decode PASS, original/output audio ADTS SHA256 identical. At eight scene-end frames, subtitle ROI MAE vs unzoomed reference improved from 21.74–31.92 to 0.65–0.90/255; upper moving region preserved (MAE 1.77–1.93/255). This measures caption position stability, NOT speech meaning or subjective legibility.

CI tests reusable Python/Pillow/FFmpeg code on **synthetic 2-second** H264/AAC material, not the user's private MP4. Run unit tests with python -m unittest discover -s quality/cycle1141/tests -v, then python quality/cycle1141/code/ci_synthetic.py.

Accessible prior TikTok market/video research summaries stress first 1–1.5s hook, purposeful cuts, actual demonstrations, Before/After, legible captions and human-approved manual posting. User's 16-panel storyboard is available; original v33 MP4 inaccessible, so no parity claim.

Unverified: independent Japanese ASR, subtitle meaning/timing, inherited audio commercial rights, mobile physical-device playback, employee approval, actual GitHub Actions billing. No merge or posting.
