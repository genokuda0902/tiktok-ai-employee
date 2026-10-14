# cycle561 — full-frame synchronized loop

Zero-additional-cost offline MP4 improvement, compared with cycle560. In the final 12 frames, replace the inherited mixed scene/subtitle wipe with one diagonal wipe applied to the entire 1080x1920 frame (including captions, scene number and footer). Preserve the original Japanese AAC bitstream. Source and local tests are bundled in the conversation's cycle561 reproducible ZIP.

Validation: 12/12 local tests passed; 375 frames at 30 fps, H.264/AAC, 12.5 seconds, 1080x1920, full decode, audio MD5 unchanged. Remaining: human voice naturalness, word-level subtitle sync, rights audit, real mobile playback, reference-video comparison. Quality: HUMAN_REVIEW; publication: NOT_APPROVED. No posting, no merge, no paid services.
