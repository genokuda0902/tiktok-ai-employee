# cycle1152 — simultaneous prompt Before/After (REVIEW ONLY)

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. This is a reimplementation, not recovered original v33 code. Never auto-post, merge without approval, or upload confidential media.

## Change from cycle1150
- Previous: verified fictional result \`46 + 29 = 75\` appears in first 1.5 seconds. Scene 04 then used sequential before/after cards.
- Now: scene 04, 8.75–10.85s, shows **simultaneous** BEFORE "集計して" vs AFTER "目的・条件・形式" for faster comparison. Fade in/out 0.22s. Original scene header, lower chapter progress, Japanese burned-in captions and audio retained.
- First render had duplicate inherited BEFORE panel; corrected by an opaque explanatory footer masking y1070..1218. The overlay is transparent below y1218 and therefore does not deliberately alter captions y>=1280.
- Ten genre color palettes are reusable. Only \`ai\` has a real completed review MP4; no claim of ten finished videos.

## Private review output (not committed to public GitHub)
- Input cycle1150 SHA256: \`7a29934c65dc0768ce97130e17321f3e0cc61204dcf7c63982974e59e66cb4c8\`
- Output cycle1152 SHA256: \`e97b3ca09192cf8d7b80c0c55590b1a51b0b547867e0e8630ab9cedaae480b6c\`
- H264 1080×1920 / 30fps / 691 frames / 23.033333s, AAC 48kHz stereo.
- AAC ADTS input/output SHA256 identical: \`27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65\`.
- Full A/V decode PASS. 62 changed panel frames (264–325), mean panel MAE 30.483/255. Across all 691 frames, sampled caption-region max MAE 0.865/255 (codec re-encode difference). Outside-window sampled max whole-frame MAE 0.982/255.
- 8 chapter audio RMS positive; **this is not ASR** and does not prove spoken Japanese, subtitle meaning or exact timing.
- Local 11 unit tests PASS, synthetic 2-second 60-frame H264/AAC render/decode PASS. GitHub CI tests synthetic media only, not the completed private MP4.

## Reproduction with locally authorized private input
Install free \`ffmpeg\`, \`fonts-noto-cjk\`, \`pillow==11.1.0\`. Make a private manifest:
\`\`\`json
{"policy":"HUMAN_REVIEW/PUBLICATION_NOT_APPROVED","genre":"ai",
 "source_sha256":"<SHA256 of locally approved source>",
 "asset_approval":"review_only_no_publication","manual_post_only":true,
 "window":[8.75,10.85]}
\`\`\`
Then run:
\`\`\`bash
PYTHONPATH=quality/cycle1152 python -m unittest discover -s quality/cycle1152/tests -p 'test_*.py'
PYTHONPATH=quality/cycle1152 python quality/cycle1152/tests/ci_smoke.py
python quality/cycle1152/prompt_contrast.py --source PRIVATE_SOURCE.mp4 --output PRIVATE_REVIEW.mp4 --manifest PRIVATE_MANIFEST.json --workdir PRIVATE_TMP
\`\`\`
Do not commit private manifest, input, overlay, audio, output MP4 or reference images.

## Reference and limitations
Directly inspected user's 16-panel, ~36s \`ChatGPT×Excel時短術16コマ絵コンテ.png\` and accessible past summaries of \`TikTok市場分析\` / \`TikTok動画研究\`: strong opening hook, short purposeful cuts, realistic UI, readable captions, Before/After and manual review. Original full research chats and original v33 MP4 unavailable. Current output remains 8 scenes/23.033s, without reference-grade 3D/people/cinematic diversity. Independent Japanese ASR, subtitle semantic alignment, asset rights, phone playback, employee approval and actual GitHub Actions billing unverified.
