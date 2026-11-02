# cycle1136 — content-only spatial scene wipes (REVIEW ONLY)

**Independent cycle after cycle1134 proportional proof bars.** The prior cut transitions were abrupt. This cycle adds seven 8-frame (0.267-second) left-to-right spatial wipes at the existing eight scene boundaries. Only the audited main visual ROI (x60..1019, y190..1089) is altered; top header, bottom chapter rail and Japanese burned-in caption area are not overlaid. Wipe uses a 32px moving feather rather than image-wide dissolve to avoid doubled Japanese UI text. The H264 video is re-encoded, so protected regions can have subpixel compression differences. AAC jpn 48kHz is stream-copied, with elementary ADTS SHA256 verified identical.

## Free, local, repeatable command

Install FFmpeg/FFprobe and `Pillow>=10,<12` (no paid API). Use an authorized private review-only source:

```sh
python quality/cycle1136/scene_wipe.py --source /private/previous.mp4 --output /private/new.mp4 --manifest /private/manifest.private.json --report /private/qa.json
python -m unittest discover -s quality/cycle1136 -p 'test_*.py' -v
```

Private manifest fields: `policy=HUMAN_REVIEW/PUBLICATION_NOT_APPROVED`, `asset_approval=private_review_only`, exact `source_sha256`, `genre` (ai/business/money/learning/health/food/travel/beauty/career/life), `roi` (x,y,width,height), `cut_frames` and `transition_frames` (5–10). Cuts must be manually audited and have verified visual change; the renderer rejects unknown source hash, unapproved media, invalid cuts, subtitles-overlapping ROI and unsupported geometry. **Ten genre configurations are validated, only one AI/Excel genre MP4 has been rendered.** A new layout requires audited ROI and cuts.

## Evidence and limits

The local, private 23.033-second review MP4 was rendered and fully decoded: H264 1080×1920 30fps, 691 frames, AAC 48kHz jpn; original AAC ADTS bit-identical; seven wipes verified by sampled frame differences; caption ROI sampled max MAE 0.749/255 (30 frames). Nine local tests PASS; synthetic video is tested in CI, not the actual review MP4. Source, actual MP4 and private manifest must **never be committed or uploaded to GitHub**.

Research summaries from `TikTok市場分析`/`TikTok動画研究` support purposeful cuts, hook, proof, Before/After and manual review; full transcripts unavailable. User 16-panel storyboard was viewed via Library, with more cinematic human/robot footage and 16 scenes/36 seconds vs 8 scenes/23 seconds here. Original v33 MP4 inaccessible. Independent Japanese ASR, semantic subtitle synchronization, source rights, phone playback, user/employee approval, real billing and reference quality remain **UNVERIFIED**. No merge, paid services, auto-posting or publication.
