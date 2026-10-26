# cycle874 — chart data integrity (HUMAN_REVIEW / PUBLICATION_NOT_APPROVED)

Stacked on unmerged PR #229, separate from parallel PR #230. Original v33 generator remains unrecovered; this is a reimplementation.

## Concrete defect fixed
The prior scene03 bar chart showed June lower than May even though the source table says sales A: 12,16,18 and B: 8,9,12 (April, May, June). The new scene03 uses a **single tuple source** for visible labels and bar heights; June is now correctly tallest for both series. Staged bars, readable Japanese, shared 10-genre fictional sample presets. No real sales or actual AI-generated spreadsheet result is claimed.

## Reproduce the PRIVATE MP4
Use the private review package supplied in the ChatGPT conversation, not GitHub. Never commit or upload inherited video, voices, source stills, or user storyboard.
```bash
PYTHONPATH=cycle874 python -m unittest discover -s cycle874 -p 'test_*.py' -v
python cycle874/chart_truth.py --source /PRIVATE/cycle873_input.mp4 --output /PRIVATE/cycle874_review.mp4 --manifest /PRIVATE/manifest.json --report /PRIVATE/render.json
```
Manifest requires all keys from POLICY plus exact source_sha256; no public-use approval is implied. Requires Python/Pillow, Noto CJK, FFmpeg. CI checks 16 tests and synthetic one-second A/V only, NOT private Japanese MP4.

## References / limitations
Accessible summaries of TikTok市場分析 and TikTok動画研究: first 1.5s hook, purposeful short shots, UI proof, Before/After, readable Japanese captions and human approval. Full research chats unavailable. User's 16-panel storyboard directly inspected; original v33 MP4 inaccessible this run. Reference cinematic actors, real ChatGPT/Excel operation, image diversity remain unmatched. Japanese narration bitstream and subtitle pixel area preserved, but pronunciation, meaning, semantic timing, rights, phone playback and employee signoff unverified. No merge, paid services or automatic TikTok posting.
