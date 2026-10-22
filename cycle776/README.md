# Cycle776 — speech-aligned Japanese captions (HUMAN_REVIEW)

Changes from cycle775: detect eight voice-activity blocks in the existing Japanese narration and retime the 16 caption cues to measured speech onsets/offsets. The image slides and inherited audio remain unchanged. The full FFmpeg/Pillow renderer, input MP4, output MP4, timing manifest, QA report, and rights notes are distributed in the cycle776 reproducible ZIP from ChatGPT.

On the actual MP4, measured mean start deviation improved 97.3 ms → 45.0 ms; measured mean end deviation improved 112.6 ms → 45.0 ms. These are **voice activity** measurements, not Japanese phoneme or word-level alignment. 1080×1920, 429 frames, 14.314 s, AAC 48 kHz, 16 captions, 10 genre presets; audio PCM unchanged. Local unit tests 10/10 and full A/V decode verified. GitHub CI only checks synthetic alignment-core unit tests, not MP4 quality or rights.

No auto-post, no paid services, no merge. Source asset rights and human review remain outstanding.
