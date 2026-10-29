# Cycle 981 — review-only, hard-cut-aware scene wipes
Base: cycle979 local-clarity PR #379; parallel cycle980 PR #381 inspected but its private video is not available here.
Distinct improvement: smooth only the two largest true artwork cuts (frames 175 and 261) using a seven-frame, left-to-right feathered wipe. No additional effects at existing animated transitions. Protect y>=1180 from intentional edits, retain original AAC elementary stream.
Private local review MP4 (NOT committed or uploaded): 1080x1920, 30fps, 691 frames, 23.033333s. SHA256 c3cbec8278acde8e362f80153ef82006ec3e2050592cd440a965c5acb09f2319.
Full A/V decode PASS; source/output AAC ADTS identical; caption ROI y>=1230 all 691 frames quarter sampled maximum MAE 1.627/255; artwork cut-frame jump MAE mean 99.578 -> 16.946/255 (82.98% technical reduction, NOT perceived-quality score). 10 local tests PASS.
Only ai_work real-video layout checked; nine other genre IDs fail closed pending review. CI uses synthetic footage only. No independent Japanese ASR or semantic subtitle synchronization, original v33 comparison, commercial rights verification, smartphone playback, employee approval or actual Actions billing verification.
**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No automatic posting, merge, external source upload, purchase, or public release.
