# cycle816 — Before/After priority reveal (2026-10-24 JST)

## What changed from cycle815
- cycle815 animated the KPI target-gap card at 6–9 s. Scene 4 at 9–12 s was a mostly static checklist.
- cycle816 changes **only frames 270–359** (9–12 s) to a 3-stage **BEFORE → focus → AFTER** comparison: three fictional tasks without priority → a single selected task. No claimed real-world improvement, private employee data or external media.
- The module uses the same ten genre keys as cycle815, keeps captions outside the overlay, and uses an opaque panel to avoid old-text ghosting.
- Inherited Japanese AAC audio is copied bit-for-bit, **not transcribed or independently matched to subtitles**.

## Reproduce locally
```bash
python -m pip install pillow
PYTHONPATH=quality/cycle816 python -m unittest discover -s quality/cycle816 -p 'test_*.py' -v
python quality/cycle816/priority_reveal.py --source /private/cycle815_KPI_GAP_ANIM_REVIEW_ONLY.mp4 --output /private/cycle816_PRIORITY_REVEAL_REVIEW_ONLY.mp4 --genre sales_business --fictional-data
ffmpeg -v error -xerror -i /private/cycle816_PRIORITY_REVEAL_REVIEW_ONLY.mp4 -f null -
```
The source video, Japanese voice and generated review MP4 are NOT committed or uploaded to public GitHub because their full rights have not been verified. GitHub CI instead creates synthetic color+tone, which is NOT Japanese narration.

## Verified local QA
- Input cycle815 SHA256 `c90c94e40af64aeb2932ab70c9b5acf57cae09d9baff8bb157da80a674f91402`.
- Output cycle816 SHA256 `a516461bee7e77c134955fc9d8c46e3a1167fd1028228a391e7d20260e24baaf`.
- 1080×1920, 30fps, 718 frames, 23.933333s, H.264/AAC 48kHz, full A/V decode PASS, inherited AAC ADTS bitstream identical, 12 local tests PASS.
- Mean RGB frame difference vs cycle815: changed scene 10.5s **8.4491**, unchanged 4.5s **1.1570** and 16.5s **1.1451** (re-encode effects).
- Review-only. Rights, independent Japanese ASR and caption semantic alignment, smartphone playback, employee approval and original v33 direct comparison are NOT verified.

## Research and reference
- Previously confirmed summaries of `TikTok市場分析` / `TikTok動画研究`: hook, short scenes, concrete demonstration, Before/After, subtitles safe zone, retention learning and human approval. Full task/chat transcripts inaccessible.
- User's `ChatGPT×Excel時短術16コマ絵コンテ.png` directly inspected. Original reference v33 MP4 unavailable; this is not equivalent to its cinematic robot/office imagery or full 16-scene structure.
- Main verified at `18e084c38db0dc55db7dfc0532b9451b1167f2aa`; stacked on unmerged PR #123. No merge, billing, or automated posting.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
