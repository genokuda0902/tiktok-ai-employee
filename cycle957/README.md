# cycle957 — Three-step actionable closing scene (private review only)

Distinct from cycle955 (prompt-template reuse scene07) and parallel PR #354 (container metadata packaging): replaces the final 2.733 seconds of scene08 with a readable, staged **試す → 元データと照合 → 明日も続ける** sequence. The previous final card only highlighted step 02, making the closing call-to-action less actionable. Keeps the existing burned-in Japanese subtitle and audio. Displays a persistent **未承認｜社員確認後に手動投稿** warning. This is reimplementation, **not the original v33 renderer**.

Source is private cycle955 MP4, SHA256 `24af228e2842a53e124cdd8f0b329c10fd3399dba36f0734c500d3597f35e223`. Output is **not uploaded to public GitHub**. Reproduction requires OpenCV, numpy, Pillow, ffmpeg, Noto Sans CJK font:

```sh
python -m pytest -q cycle957/test_closing_actions.py
python cycle957/closing_actions.py --source /private/cycle955.mp4 --output /private/cycle957.mp4 --qa /private/render_qa957.json
```

Ten genre action triplets are configured. **Only ai_work has private visual review**; other genre layouts fail closed. Synthetic tests run in CI. No private video, voice, image or audio is committed.

Local render: 1080x1920, H.264 30fps 691 frames, 23.033333s, AAC 48kHz stereo. Last 82 frames changed, bottom subtitle band y>=1490 preserved before compression. Source and output AAC elementary streams are identical (SHA256 `37df7a17744c68dc6952f0778e57ef4ad94c977057a470cd12ea951e8bcb1e27`). Local tests 17 passed. Output SHA256 `f270177b38a04a357fea3f86e6d70c1f8ef3da028004e1845b5f0310dca37e73`.

References: accessible summaries of TikTok市場分析/TikTok動画研究, user-provided 16-panel ChatGPT×Excel storyboard described in prior QA. Original v33 MP4 and full source chat not accessible in this run; no visual parity claim. Original v33 source unlocated. Independent Japanese ASR/speech-caption meaning and timing, rights, smartphone playback, employee approval and Actions actual billing **unverified**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No auto-post, merge or paid contract.
