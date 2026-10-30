# cycle998 — ghost-free flash-guard (private review only)

Distinct from cycle996: replaces a 5-frame **cross-dissolve** that can visibly double human faces and UI text with a 6-frame **single-source luminance compensation** on each side of qualifying scene cuts. No old/new scene images are ever blended. A feathered ROI (x24–1056, y255–1110) protects captions/footer and outer artwork. Applies to ten named genres; **no automatic publication permission**.

## Reproduction with locally authorized review media

Prerequisites: Python 3.11, NumPy 2.x, OpenCV headless 4.x, FFmpeg/FFprobe. Do not upload private input footage to public GitHub. Run:

\`\`\`bash
python cycle998/ghost_free_guard.py \
  --input /private/cycle994_SHADOW_LIFT_JP_REVIEW_ONLY.mp4 \
  --output /private/cycle998_GHOST_FREE_FLASH_GUARD_JP_REVIEW_ONLY.mp4 \
  --report /private/cycle998_report.json \
  --genre ai_work --cuts 174,348,522 --review-only
python -m unittest discover -s cycle998 -p 'test_*.py' -v
python cycle998/ci_synthetic.py
\`\`\`

CI generates **synthetic-only** video and a synthetic 440Hz tone, NOT the user's Japanese narration or real final review MP4. Real 23s MP4 is generated and verified locally and shared as a conversation attachment, not committed to the public repository. Original reference v33 MP4 and full research transcripts inaccessible; storyboard and research summaries accessible. No merge, no posting, no payment. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
