# cycle1086 — real Calc UI evidence bridge (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Reimplementation, not recovered v33 code.

## Distinct improvement
cycle1084 made a truthful but diagram-only 46 + 29 = 75 proof in scene06. This cycle uses a cropped frame from the actual scripted LibreOffice Calc recording already in cycle1078, then adds progressive source-value highlights and a separately calculated sum. This improves continuity between scene03 real UI and scene06 proof. It is a genuine recorded Calc UI but not a ChatGPT live operation; all numbers are fictional. No productivity/accuracy claim.

## Reproduce with locally authorized private sources
PYTHONPATH=. python3 -m unittest quality.cycle1086.test_calc_proof_bridge -v

PYTHONPATH=. python3 -m quality.cycle1086.calc_proof_bridge --source /private/cycle1084.mp4 --source-sha VERIFIED_SHA256 --ui-video /private/cycle1078.mp4 --ui-sha VERIFIED_UI_SHA256 --data-json quality/cycle1082/sample_data.json --out /private/cycle1086.mp4 --genre ai_work

PYTHONPATH=. python3 -m quality.cycle1086.calc_proof_bridge --smoke

SHA-256 pins both private MP4s; fail closed. Ten genre palette presets are unit-tested, but only ai_work is rendered with locally reviewed inputs. The private MP4s, frames and audio are not committed or uploaded to GitHub. CI uses an 18-second synthetic H264/AAC file, not the real 23-second video.

## Reference and remaining gates
Prior research summaries for TikTok市場分析/TikTok動画研究 emphasize fast hook, real UI, Before/After, readable subtitles and manual human review. User's 16-panel storyboard has cinematic human/robot/ChatGPT/Calc/CTA variety; original v33 MP4 and full chat transcripts unavailable in this run. Japanese independent ASR and semantic caption alignment, mobile playback, media publication rights and employee approval remain unverified. No merge, no auto-post, no paid services.
