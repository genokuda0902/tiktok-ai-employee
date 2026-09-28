# Cycle 174 — progressive reveal image-slide route

Status: experimental / review-only. No automatic TikTok posting. Human employee approval required.

## Difference from cycle 173
- cycle 173: three-beat visual hook (problem -> solution -> payoff)
- cycle 174: four-beat progressive reveal with a shorter 1.6 s hook, explicit AI instruction/processing beat, result beat, and longer payoff.
- Purpose: increase information progression without returning to high-density 9-cut pacing.

## Reusable 10-genre timing manifest
```json
{"beats":[
 {"role":"hook_problem","duration_s":1.6},
 {"role":"solution_action","duration_s":2.7},
 {"role":"proof_result","duration_s":3.2},
 {"role":"payoff_cta","duration_s":4.5}
],"total_s":12.0,"canvas":"1080x1920","fps":30}
```

## Local technical evidence
Generated review MP4: `tiktok_image_slide_cycle174_progressive_reveal.mp4`
SHA-256: `7fff64922f238675ba72eac2a7b94ce77d55c91f9fce4b649f72cce765d273bf`
ffprobe: H.264 1080x1920 30fps + AAC 48kHz stereo; duration 12.000 s.
Full ffmpeg decode: exit 0, no decode errors.

Audio is inherited from the previous review master; this cycle does NOT claim improved Japanese TTS naturalness.
Generated visual asset is review-only and must pass rights/quality/human approval before manual posting.
