# cycle1112 — two-beat numeric verification cut (REVIEW ONLY)

## Improvement vs cycle1110
Previous cycle1110 changed the prompt Before/After cue at 8.85–10.95s. This cycle adds a new visual insert at **11.70–13.29s** (48 frames) inside scene05: first show fictional April input numbers **営業A 12 + 営業B 8**, then reveal the verified arithmetic **20**. This is a local example of checking AI output, not evidence of measured productivity. It does not add a new full chapter; existing 8-chapter structure and Japanese AAC narration/subtitles are retained.

The renderer uses ten reusable genre palettes, strict source SHA, fail-closed manifest metadata, and rejects incorrect sums. It draws only in y=315–1025, leaving burned subtitles at y>=1280 untouched. No private media is committed.

## Local commands
Requires Python 3.11, Pillow, ffmpeg, ffprobe and Noto CJK fonts.

    python3 -m unittest discover -s quality/cycle1112 -p 'test_*.py' -v
    python3 quality/cycle1112/row_verification_cut.py \
      --source /private/cycle1110_PROMPT_BEFORE_AFTER_JP_REVIEW_ONLY.mp4 \
      --source-sha bcf5b872effca785199589caa45f825f6a38c96f68263388b0fe50b3f3f6aa3b \
      --manifest quality/cycle1112/manifest.json \
      --out /private/cycle1112_ROW_VERIFICATION_CUT_JP_REVIEW_ONLY.mp4 \
      --report /private/render_report1112.json

## Verified private local MP4
Source SHA256 bcf5b872effca785199589caa45f825f6a38c96f68263388b0fe50b3f3f6aa3b.
Output SHA256 aff73f105774cb6fbfad6ccc8b656e3626365d144c0feffc044002767dd31b1c.

H264 1080x1920 30fps, 691 frames/23.033333s; AAC 48kHz. Full A/V decode PASS, AAC ADTS bitstream unchanged. All 691 frames compared at 1/4 scale: max mean caption-region delta 0.2323/255; outside edit max 0.2034/255; edited 48-frame ROI mean 93.6569/255. Local 15 unit tests and synthetic 15s A/V smoke PASS. CI tests only synthetic media, not the private finished video.

## Research and limitations
Directly inspected user's 16-panel ChatGPT×Excel storyboard: cinematic robot/human, rich UI, 16 cuts/~36s. Available TikTok市場分析 and TikTok動画研究 summaries recommend a strong opening hook, purposeful scene changes, real UI, before/after, readable Japanese captions, and manual employee-reviewed posting. Full original chats and original v33 MP4 were not accessible in this run. This 8-scene/23s reimplementation is not equivalent to v33.

Independent Japanese ASR, pronunciation and semantic subtitle timing (especially 20.3s onward), source rights, phone playback, employee approval and actual Actions billing remain unverified. Next priority: permitted offline Japanese ASR or employee transcription, then eight subtitle semantic/timing checks.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, auto-post, public media upload or paid services.
