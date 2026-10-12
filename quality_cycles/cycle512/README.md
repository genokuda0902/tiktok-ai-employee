# cycle512 | zero-cost Japanese voice recovery

- Topic: 会議メモを次の行動が分かる3項目に整理
- Compared to cycle511: first 1.3 seconds explicitly compare BEFORE/AFTER; high-contrast beat-aware captions; original light editorial design.
- Local MP4: 1080x1920, 20.375 sec, H.264/AAC, 16 original slides; **SFX only, NOT APPROVED**. Full source and MP4 supplied separately as conversation artifacts.
- New path: `kokoro_voice.py` generates eight **native Japanese** WAV files, records actual speech durations and SHA-256, and refuses silent segments.
- Workflow on PR generates a downloadable WAV artifact for the next cycle to retime the slides and subtitles against *actual* speech.
- Do NOT label generated speech natural or synchronized before human listening and video alignment.
- Original vector art, fictional meeting examples, no PII. No posting, merging, paid API or automatic publication.
