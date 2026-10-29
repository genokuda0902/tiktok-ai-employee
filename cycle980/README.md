# cycle980 — emotional Before/After hook (review-only)

## Change vs cycle978 and parallel cycle979
Replace only first 45 frames (0–1.5s) in upper artwork y<1440 with a split-screen contrast: an inherited illustrative human/robot scene vs an inherited fictional Calc result. Both source stills are extracted from the *same private local MP4* (frames 105 and 195); they are NOT committed. No fabricated productivity claims. The original burned Japanese subtitles and AAC are inherited. This differs from cycle978's 17.4s transition ghost fix and cycle979's all-scene edge clarity pass.

## Local commands
```bash
python cycle980/hook_before_after.py --source /private/cycle978_CLEAN_TRANSITION_JP_REVIEW_ONLY.mp4 --output /private/cycle980_BEFORE_AFTER_HOOK_JP_REVIEW_ONLY.mp4 --work /private/cycle980_work
PYTHONPATH=cycle980 python -m unittest discover -s cycle980 -p 'test_*.py' -v
python cycle980/qa_hook.py --source /private/cycle978_CLEAN_TRANSITION_JP_REVIEW_ONLY.mp4 --output /private/cycle980_BEFORE_AFTER_HOOK_JP_REVIEW_ONLY.mp4 --report /private/qa980.json
```

CI uses generated synthetic footage only, never private images/audio. Ten genre names exist; only ai_work real layout is reviewed, others fail closed. Current video 8 scenes/23.033s remains below user's 16-panel/36s reference in visual diversity. Original v33 MP4, full TikTok市場分析/TikTok動画研究 transcripts, independent Japanese ASR/caption semantic alignment, rights, smartphone playback, employee signoff and Actions billing remain UNVERIFIED. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, auto-post, paid service or release.
