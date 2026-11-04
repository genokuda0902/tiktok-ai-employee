# cycle1211 — structural caption/audio gate

Prior cycle1210 added caption safe-area geometry but failed to render because local runtime returned redis.exceptions.ResponseError. This cycle adds separate **timing/audio-presence** validation, not another overlay.

Usage: import review_gate; call review_gate(mp4_path, captions_json_path). Caption JSON is a list of objects with start/end seconds and text. This is structural only: cannot confirm Japanese speech, pronunciation, visual subtitle placement, or semantic synchronization. A failed check blocks release; a passed check does not approve publication.

GitHub code saved; local ffmpeg and tests unavailable because container returned redis.exceptions.ResponseError. No MP4 generated and no artifact verified. Reference v33 and original market-study chat/video not accessible. No confidential assets committed.

Next: restore runtime; generate new approved-asset MP4 with Japanese narration and timed subtitles; ffprobe + full decode + independent listening/visual QA; run tests and CI. No auto-post or merge.
