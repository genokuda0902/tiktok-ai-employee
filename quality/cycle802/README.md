# cycle802 — original artwork + new Japanese TTS recovery (DRAFT)

Local deliverable: 1080×1920 / 30fps, 8 scenes, 16 caption cues, original Pillow vector illustrations, new 16-beat cue-level visual accent. It uses the inherited Japanese audio from cycle801 strictly for **internal review**, since source rights remain unverified.

This PR includes an independently reproducible **free Japanese narration test** with Open JTalk, the original Japanese script, eight self-generated slides, tests and a GitHub Actions workflow. The CI sample is NOT the local full renderer or a publication-approved video. It is meant to remove the repeated failure to obtain new Japanese narration from network-dependent TTS services.

**Differences vs cycle801:** no inherited photographic assets, 16 cue-driven attention markers (vs static scenes), local vector-only imagery, and a new offline-capable Japanese TTS recovery route in CI. The full local renderer and the completed 16-cue review MP4 are provided in the cycle802 ZIP separately; the local renderer is **not** committed here.

All assets remain HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No paid API, auto-posting, automatic merging, or unauthorized use of personal information.

## New Japanese voice result (verified after initial PR)
- Open JTalk CI **succeeded**: run 40037488690, artifact 12537553015.
- The artifact was downloaded and inspected: H.264 1080×1920, AAC 48kHz, Japanese voice generated from eight Japanese sentences.
- The new voice was integrated into the local **original vector + 16 caption cue** video: 648 frames / 21.600s, H.264 30fps, AAC 48kHz.
- PCM audio MD5 exactly matches the downloaded CI sample: `58c74ddee1477665a8e20cfd3ff98d39`.
- Scene boundaries follow the 8 TTS segment lengths. Sixteen subtitle phrase splits are **estimated** by character counts, not forced-aligned to phonemes.
- Local QA: 16/16 technical checks; 13/13 unit tests. The local renderer and final video remain in the separately delivered ZIP and sandbox files, **not synced to GitHub**.
- Nitech voice model licensing/attribution, pronunciation, smartphone playback, comparison to user reference videos, and employee approval remain pending. Do not publish.
