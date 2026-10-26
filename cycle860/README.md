# cycle860 — BEFORE→AFTER prompt micro-demo

**Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**

Compared with cycle859, scene 4 replaces a static instruction card with a timed
BEFORE ("いい感じに書いて") → AFTER ("社内向け・丁寧・150字") example,
and scene 5 adds a human fact-check reminder (numbers, names, dates).
The 23.033s Japanese voice, 24 subtitle states, 8 scenes and progress bar
are inherited. The source contains 6 AI-generated photos + 2 vector graphics;
**8 newly generated independent photos are not claimed.**

This branch includes the reusable 10-genre core and 10 unit tests.
The full Pillow/FFmpeg renderer, original source MP4, completed MP4 and actual
MP4 QA report are in the accompanying ChatGPT review ZIP, not GitHub Actions.
CI only validates core rules; it does not render the completed Japanese MP4.

Local QA: 13/13 checks PASS, 29/29 local unit tests PASS. Video:
H.264 1080x1920 30fps 691 frames / 23.033s, Japanese AAC 48kHz
elementary stream identical to cycle859, all frames decoded, subtitle ROI
preserved. Full human evaluation of voice quality, semantic subtitle sync,
source rights, reference-video parity, smartphone playback and retention
gain is **pending**. No merge, publishing, auto-posting or paid service.
Only manually post after employee approval.
