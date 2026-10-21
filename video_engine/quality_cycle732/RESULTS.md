# cycle732 verified local result

- 2026-10-21 JST, zero incremental spend.
- Baseline cycle731 SHA256: `40570798d65c64eb025516496f17ace19fa0dece7643ef9c72e97d1b5adf31d7`.
- New review-only MP4 SHA256: `f5c396bafda7347c41ae27b5e60518d64b48b202b7c472a658c2320f9b9ddbdc`.
- 1080x1920, H.264 30fps, 819 frames, 27.343s, AAC Japanese narration. Full decode PASS; decoded PCM hash matches baseline. Eight scene-level Japanese captions; pronunciation and word-level sync not verified.
- Redrawn frames 384–603 (12.8–20.133s): highlight months 1–2 then months 3–4, subtle camera zoom. Mean absolute pixel differences: frame420=34.920; frame540=34.624; unchanged frame240=0.222 and frame660=0.531.
- Ten local tests PASS; GitHub CI not executed. No PR created. Exact renderer and tests retained in the conversation ZIP, but GitHub code upload was blocked. This branch is NOT reproducible from GitHub alone.
- Research task full texts and reference v33 MP4 inaccessible; 16-panel storyboard inspected. No equivalence or publication approval. No merge or posting.
