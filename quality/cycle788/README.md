# cycle788 — image-first opening comparison (REVIEW ONLY)

**Problem addressed:** cycle787's 0–1.5s hook stayed mostly on one static robot/title shot. User storyboard panel 9 explicitly shows a BEFORE/AFTER contrast; the quality brief calls for a visual change in the first 1.5s.

**Change:** configurable 45-frame, 1.5s cinematic BEFORE/AFTER split-card hook with two existing local review-video frame crops, Japanese title, demo disclaimer, eased card movement and fade back into the original scene. Only the opening is changed; source audio is copied without re-encoding. No third-party images, external APIs, billing, merging or posting.

**Local verified MP4:** 1080×1920 H.264/AAC 30fps, 23.843s, 714 frames. Local 10/10 tests PASS; full decode PASS; PCM and AAC packet hashes match cycle787. Mean absolute pixel difference at 0.9s ~41.7, outside hook at 8s ~1.1 (re-encoding only). MP4 is delivered in the chat sandbox, **not committed** because source media rights and employee approval are not verified.

**Exact local command** (requires local review-only cycle787 MP4 and two screenshots):
```sh
python quality/cycle788/first_second_comparison.py --input cycle787.mp4 --before before.png --after after.png --config quality/cycle788/config.json --output cycle788.mp4 --report cycle788.json
```

**CI:** `.github/workflows/cycle788-review.yml` runs unit tests and creates a **separate, reproducible four-second synthetic fixture** with Japanese Open JTalk narration and burned Japanese title. This fixture is NOT the full 23.843-second user review video; the latter still requires local unapproved source assets. CI artifact is review-only.

**Research:** TikTok市場分析/動画研究 full chat logs not accessible. Earlier summarized design: hook in 0–1.5s, image-first scenes, real Before/After, concise Japanese captions, manual approval. User 16-panel storyboard inspected; original v33 MP4 not accessible in this run. No direct v33 comparison or equality claim.

**Unverified:** narration meaning / captions semantic sync; source voice/image rights; mobile-device playback; 10-genre end-to-end render; employee quality acceptance. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Do not merge or post without explicit review.

**Dependency:** stacked on unmerged cycle787 PR #69. This PR should target its branch, not main, until reviewed.
