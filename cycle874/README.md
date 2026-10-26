# cycle874 — source-visible animated chart (HUMAN_REVIEW / PUBLICATION_NOT_APPROVED)

Stacked on unmerged PR #229; parallel PR #230 is untouched. This is a reimplementation, not recovered v33 source.

## Concrete improvement over cycle873
In the *intermediate animation* at 6.9s, the June bars appeared shorter than May and June's numeric labels were not yet shown, which could be mistaken for a data mismatch. **Important correction:** the prior chart at 7.8s already displayed June as tallest with the correct final values; the old completed chart was NOT mathematically wrong. The new scene03 displays all three months' fictional source values immediately while bars animate and derives completed bar heights and labels from the same source tuples (A 12/16/18, B 8/9/12). This makes the progressive animation more interpretable, not a correction of final source arithmetic. Only frames 170–250 (5.667–8.367s) change. The Japanese narration, burned-in captions, other scenes and private source remain unchanged.

## Local reproduction (PRIVATE MP4 only)
The ChatGPT review ZIP includes private source, manifest, output and full QA. These are not in GitHub.
```bash
PYTHONPATH=cycle874 python -m unittest discover -s cycle874 -p 'test_*.py' -v
python cycle874/chart_truth.py --source /PRIVATE/cycle873_input.mp4 --output /PRIVATE/cycle874_review.mp4 --manifest /PRIVATE/manifest.json --report /PRIVATE/render.json
```
The manifest must equal POLICY plus source_sha256. Requires Python/Pillow, Noto CJK and FFmpeg. CI checks 16 portable tests and synthetic one-second A/V, NOT the private Japanese MP4.

## Research and safety
Accessible TikTok市場分析 / TikTok動画研究 summaries: first 1.5s hook, purposeful cuts, UI proof, Before/After, legible Japanese captions and employee review. Full chats unavailable. User 16-panel storyboard directly inspected; original v33 MP4 inaccessible. Natural actors, genuine ChatGPT/Excel interaction and rich reference cinematography remain unmatched. Independent Japanese pronunciation/meaning, semantic subtitle timing, media/voice publication rights, phone playback, employee approval and actual Actions billing are unverified. No merge, paid service, public private-media upload or auto-post.
