# cycle579 — stable proof loop (REVIEW ONLY)

Previous cycle578 reversed the first second at the end. This made intermediate synthetic totals (704, 572, 200) visible during the loop tail even though the caption stated the verified total was 720. The first frame also showed 0 before the count-up.

This cycle fixes the factual inconsistency: frame 27 (0.9s, verified 720) is used as a static hook for 0–1s and a static return for 19–20s. The 1–19s scenes remain intact. Audio uses a 120ms fade at both edges. The same validation contract names 10 genres; only ai_productivity has a tested real MP4.

Reproduce locally with:
python quality/cycle579/proof_loop.py --source cycle578_loop_reentry_REVIEW_ONLY.mp4 --output cycle579_proof_stable_loop_REVIEW_ONLY.mp4

The source file is NOT committed because inherited asset rights are unverified. Exact source SHA256: c0bb03263495f4b3bacbe1cf9e7f65c4187f4dce336aac70cc0713484f3f3cd7

Local: 9 tests PASS; 20s, 1080x1920, 30fps, 600 frames, H.264/AAC, 9 subtitle cues, decode PASS. CI unit tests: 7 PASS; CI does not render the MP4.

Reference: the user-provided 16-panel ChatGPT x Excel storyboard was visually inspected. The original v33/reference MP4 bytes were unavailable due to Library materialization permissions. The actual research-result bodies for TikTok市場分析 and TikTok動画研究 were inaccessible; task settings only were checked.

Quality: HUMAN_REVIEW. No Japanese narration; no verified speech/subtitle sync; inherited rights unapproved. PUBLICATION_NOT_APPROVED. No merge or automatic posting.
