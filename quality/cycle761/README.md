# cycle761 — review-only clean CTA end card

Base: cycle760 video SHA256 cad62b895a50b69200d665dbd993969dc49c600dd727ff575a7bccd062eda06c. Main SHA 18e084c38db0dc55db7dfc0532b9451b1167f2aa. Branch was forked from cycle760 branch SHA f858dbe8c4dc34fb936c81ae18e57c47c691248f.

Problem: final CTA at 24.3–27.3 seconds overlapped the burned narration caption and disclaimer. This cycle replaces the final 90 frames with a single, readable image-first 3-step CTA. All visuals are locally drawn from synthetic example data; no reference image, customer data, confidential footage or external image asset is embedded.

Local QA: 1080x1920, H.264, 30fps, 819 frames, duration 27.343 s, AAC 24 kHz mono. Video and audio decoded fully; PCM audio SHA identical to cycle760; 10 local unit tests passed. Outside replacement, mean pixel differences at 1/8/15/23 seconds were 0.277/0.443/0.479/0.412; inside at 24.8/25.9/26.7 seconds were 45.389/45.898/46.292. SHA256 of candidate MP4 1278d26f167924d4268666861f5381c1a70b1c9b6d7b5cd76d927d774a87a054.

Reproduction (local source MP4 is deliberately NOT committed): install Pillow, ffmpeg, Japanese Noto CJK fonts; run:
```bash
python quality/cycle761/src/cycle761_endcard.py --source cycle760.mp4 --config quality/cycle761/config/ai_work_endcard.json --output cycle761.mp4 --expected-sha cad62b895a50b69200d665dbd993969dc49c600dd727ff575a7bccd062eda06c --frames tmp_frames
python -m unittest discover -s quality/cycle761/tests -v
```

Reference: user-provided 16-panel AI×Excel storyboard was inspected. Original v33 MP4 and full results of TikTok市場分析 / TikTok動画研究 not available this cycle. Genre-common end-card profiles cover ten genres; only ai_work has been rendered. Does not establish reference equivalence, speech/caption word sync, rights for inherited audio, smartphone UI approval, or posting readiness. Human approval mandatory; manual posting only. No merge, purchase or automatic posting.
