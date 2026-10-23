# cycle802 — original artwork + new Japanese TTS recovery (DRAFT)

Local deliverable: 1080×1920 / 30fps, 8 scenes, 16 caption cues, original Pillow vector illustrations, new 16-beat cue-level visual accent. It uses the inherited Japanese audio from cycle801 strictly for **internal review**, since source rights remain unverified.

This PR includes an independently reproducible **free Japanese narration test** with Open JTalk, the original Japanese script, eight self-generated slides, tests and a GitHub Actions workflow. The CI sample is NOT the local full renderer or a publication-approved video. It is meant to remove the repeated failure to obtain new Japanese narration from network-dependent TTS services.

**Differences vs cycle801:** no inherited photographic assets, 16 cue-driven attention markers (vs static scenes), local vector-only imagery, and a new offline-capable Japanese TTS recovery route in CI. The full local renderer and the completed 16-cue review MP4 are provided in the cycle802 ZIP separately; the local renderer is **not** committed here.

All assets remain HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No paid API, auto-posting, automatic merging, or unauthorized use of personal information.
