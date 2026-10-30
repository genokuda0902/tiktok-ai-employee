# Cycle1017: scene-safe image slide motion (review only)

Date: 2026-10-30 (JST). Base: draft PR #415, cycle1015.
Source: cycle1015 local 22.5s, 1080x1920/30fps H.264 + Japanese-tagged AAC 48kHz + 8 chapters.
Research consulted: prior TikTok market/video-study summaries: proof before feature lists, readable captions, real UI/Before-After, hook within 1–1.5s. User's 16-panel storyboard was available as an earlier description, not as original v33 video.

## Distinct improvement
Previous cycle1015 sharpened the screenshot ROI (static image quality). This cycle adds an eased 2.6% center push-in to the screenshot ROI for each of eight chapter intervals, with a feathered mask. Scene starts/ends return to original scale. The subtitle-safe area (y>=1400), header, and footer are not deliberately modified; original audio stream and chapter metadata are copied. Ten genre identifiers reuse the same motion logic; only ai_work has a rendered full video.

## Local full-video QA (not CI)
- Local artifact: cycle1017_SCENE_SAFE_PUSHIN_JP_HUMAN_REVIEW.mp4
- SHA256: 3b2810240fecd18cbaf1aed697816f4f1b8139be6624a7b7308e61e7856bbe25
- Size: 9,879,616 bytes; 22.5s, 675 frames, 1080x1920, 30fps, 8 chapters.
- FFmpeg full video+audio decode PASS; AAC compressed bitstream hash identical to cycle1015.
- Screenshot ROI mid-scene changed in all eight scenes (MAE 12.463–25.319 /255).
- Caption/footer sampled mid-scene MAE <=0.361 /255.
- Unit tests 16/16 PASS. CI workflow uses **synthetic 2s only**.
- No human visual-quality score; no independent Japanese ASR, voice/caption semantic alignment, v33 direct comparison, phone playback, or commercial rights verification.
- Zero new paid purchases/services; GitHub Actions actual billing not independently verified.

## Safety
Draft PR only. No merge, publication, automatic upload/post, or approval. Human review and explicit employee approval required before manual TikTok posting.
