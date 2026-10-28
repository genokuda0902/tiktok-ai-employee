# cycle936 — guided prompt typing (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Never merge, publish, upload private video, auto-post or use paid services without separate authorization.

## Improvement and provenance
Builds on **unmerged** cycle934 PR #321. Previous cycle934 improved the opening Before/After hook (scene01). This cycle replaces **scene04 (8.7–11.6s, 87 frames)** with original animated fictional prompt input: **purpose → constraints → output format**. It explicitly says this is not a ChatGPT screen recording. It is a reimplementation, not the lost original v33 generator. The scene06 changes in parallel cycle935 PR #322 are not merged.

10 genre presets share the same layout, safety checks and timing; only `ai_work` has a completed local MP4.

## Private local reproduction
Requires Python 3.11+, Pillow, FFmpeg, free Noto CJK fonts and the authorized **private** cycle934 review MP4. No MP4, audio or third-party assets are committed.

```bash
python cycle936/src/prompt_typing_scene04.py \
  --source /private/cycle934_BEFORE_AFTER_HOOK_REVIEW_ONLY.mp4 \
  --output /private/cycle936_GUIDED_PROMPT_TYPING_REVIEW_ONLY.mp4 \
  --workdir /private/cycle936_render \
  --genre ai_work \
  --expected-source-sha 91772ba5d4f9048435aedf0d56dc762dc721208027c879d45e19fbc505816919
python -m unittest discover -s cycle936/tests -p 'test_*.py' -v
```

## Locally verified private MP4
- Input SHA256: `91772ba5d4f9048435aedf0d56dc762dc721208027c879d45e19fbc505816919`.
- Output SHA256: `9ba495276c6d42ffb178a58c80b2d8164bc21a98f330cb44270925413faa77a2`.
- H264 1080×1920, 30fps, 691 frames, 23.033s; AAC48kHz ADTS SHA256 `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9` unchanged.
- Full video/audio decode PASS; scene04 87/87 frames changed, average 1/8-scale MAE 23.693; outside scene max 0.285; subtitle band max 0.159.
- Local 12/12 tests PASS. GitHub CI tests code and synthetic overlays, **not the completed private MP4**.

## Research, quality gaps and policy
Consulted accessible summaries of `TikTok市場分析` and `TikTok動画研究` (first-second hook, purposeful cuts, real demonstrations, readable Japanese captions). Directly inspected the user's 16-panel ChatGPT×Excel storyboard in the Library. Original v33 MP4 and full original task/chat transcripts unavailable this cycle. Reference has cinematic robot/person footage, genuine-looking ChatGPT/Excel demonstrations and 16 scenes; this is an 8-scene, 23s video with an illustrated fictional prompt, not equivalent quality.

Independent Japanese ASR/transcription, pronunciation, speech/caption semantic and word-level timing, inherited source rights, smartphone playback, employee approval, and actual GitHub Actions billing remain **unverified**. Employee must approve before **manual** posting. No automatic posting.
