# cycle957 — protected artwork midtone lift (REVIEW ONLY)

2026-10-29 JST. Distinct from cycle956's lossless metadata packaging. This stage gently lifts midtones of the image artwork (gamma 1.14; gamma_weight 0.82), while protecting header, burned Japanese captions, and progress/footer UI with a 70px cosine-feathered mask. No new people, speech, captions or claims are generated.

## Real private MP4 evidence

- Source: private cycle956 MP4 SHA256 `c9b4680679977fdf20d139d9106e4ca219fad267595f005f3eb6e00e48a3414d`.
- Output: `cycle957_ARTWORK_MIDTONE_JP_HUMAN_REVIEW.mp4`, SHA256 `d57c2224d64c9d589caadbbb0fe487507becc403b2d4e74f1c41d8bef80e632a`.
- 8 scene midtone mean luma gain +5.99 / 255 (range +5.21 to +6.52). Mean abs RGB difference in subtitle protected band <=0.23 / 255 across 8 samples (codec re-encode).
- 691 frames, 1080x1920, 30fps, H.264, 23.033333s, AAC 48kHz mono. Audio ADTS SHA256 unchanged `0045ddfb9eb47f798aa6ae3a465f885409dab58ce27ad0fa1479901becddc57d`. Full video/audio decode PASS. Local tests 16/16 PASS.
- The private MP4 and before/after preview are shared via ChatGPT attachments, not committed to public GitHub. CI tests code and synthetic masks, **not** the real MP4.

## Use and safety

`python quality/cycle957/midtone_lift.py <private-input.mp4> <private-output.mp4> --genre ai_work`

10 genre presets are validated. Only the exact reviewed AI-work test input hash can render; the other nine genres fail closed pending a separate rights/layout review. This source identity gate is NOT proof of commercial usage rights.

Research summaries consulted: 1–1.5s hook, 15–25s duration, short purposeful scenes, real UI, Before/After, readable captions and manual employee approval. The 16-panel ChatGPT×Excel reference storyboard contains cinematic people/robot/UI/graphs, while this 8-scene 23s clip does not match that reference. Full research transcripts and original v33 MP4 were not available.

**Unverified:** original v33 direct comparison, Japanese ASR transcription and caption semantic/timing alignment, source commercial rights, master colorimetry (BT.709 remains provisional), smartphone playback, human approval and actual Actions charges. No paid services, no auto-post, no merge. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
