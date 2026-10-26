# cycle855 PHOTO route — review only

Compared with cycle854 photo route: **fix a real TikTok UI collision**. Previous Japanese subtitles were centered around y=1532 on a 1080×1920 frame, below the conservative In-Feed bottom UI exclusion start y=1260. This route relocates all 24 Japanese subtitle states to center (445,1160) and all critical slide information to x=130..760, y=284..1244, avoiding the right action-button column x>=780 at y>=840.

## What is verified

- Local final MP4: 1080×1920 H.264 30fps, 691 frames, 23.033s; inherited Japanese AAC 48kHz, unchanged decoded PCM from cycle854.
- 8 native 1080×1920 **slide layouts**, 24 burned-in subtitle states, 15/15 local video QA checks, 12/12 local layout/compositor tests.
- This GitHub PR CI tests **only the 10-genre shared geometry core**. It does **not** generate the final MP4 or certify Japanese pronunciation, human quality, TikTok device UI, or media rights.
- Full offline compositor, reused low-resolution AI photos, inherited audio, generated slides, final MP4 and QA report are distributed in a separate local review ZIP.
- External free photo download was attempted but unavailable in this execution environment. Do not claim 8 new high-resolution photographs.
- Safe-zone measurements are conservative and derived from TikTok **ad** In-Feed template, not a guaranteed organic-post safe zone; app UI and caption length may change.

## Safety

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No automatic posting, no merge, no paid service, no purchase. Human approval and source/voice rights review required before manual posting.
