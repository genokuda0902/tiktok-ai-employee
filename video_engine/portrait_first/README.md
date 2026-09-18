# Portrait-first reusable editor — status: prototype, NOT a fully automatic multi-genre generator

## Run
Install Python 3, Pillow, ffmpeg and ffprobe; install a licensed Japanese font at `/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc` (change `FONT` in `build.py` on other systems). Put `build.py`, a JSON config, an **approved 9:16 image**, and an **approved portrait MP4 with matching narration** in one folder. Example config:

```json
{"body_video":"approved_body.mp4","portrait_image":"approved_portrait.png","output":"candidate.mp4","title":"その集計、まだ手作業？","subtitle":"Excel × AI｜実演はこのあと","intro_seconds":2.0}
```

Run `python build.py --config config.json`. Outputs a 720×1280 H.264/AAC MP4 and `opening.jpg`. Body audio and body frames stay aligned; a silent 2-second intro precedes them. The script rejects landscape source videos/images, missing assets, and body videos without audio. This is an **editor for pre-made genre-specific body videos**, not an AI scriptwriter or a body-video generator. The middle two opening lines are currently Excel-specific in code; they must be parameterized before other genres are production-ready.

## September 18 candidate
A 33.43-second first-post candidate was rendered locally using the user's original v33 MP4 as the complete body and a new synthetic portrait poster for the opening. The original v33 body retains its existing man-and-robot closing scene. The newly generated portrait image and original MP4 are NOT committed to GitHub. The poster's source has embedded typography, so inspect the opening for cropped letters. This is a review candidate, not verified publish-ready; user must approve before publishing. No confidential IMG_5805–IMG_5814 assets are used.

## Mandatory release gates
1. Verify all image/video rights and that there are no internal figures, names, personal data, or confidential screens.
2. Confirm original audio matches every scene; avoid unsupported time-saving or sales-growth claims.
3. Review first, middle, and final frames on an actual phone; check safe zones and that no face or embedded text is cropped.
4. Check audio and picture playback in the target iOS app, not just ffprobe.
5. Replace all Excel-specific title, footage and narration with new genre-specific approved assets before using another genre. Do not promise equal quality automatically.

## Persistence
Only source and documentation are in GitHub. Keep approved media in access-controlled durable storage, and preserve its version/checksum and license details separately. This repository alone is not a full media backup.
