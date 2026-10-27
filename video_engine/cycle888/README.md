# cycle888 — contextual editorial focus guides (HUMAN REVIEW ONLY)

## Distinct change from cycle887
cycle887 animated seven narration-frequency bands in the header. cycle888 adds **eight timed focus-corner highlights** on the existing mock-UI demonstration: purpose, conditions, output, human verification, vague instruction, specific instruction, save name, and saved content. Each uses four short corner brackets, fade-in/out and explicit geometry checks. The existing Japanese narration, 24 burned caption intervals, header waveform, and scene artwork remain inherited.

## How to render locally
python render.py /private/review_input.mp4 /private/review_output.mp4

Requires FFmpeg with libass, 1080x1920 30fps H.264 input and AAC 48kHz audio. The source is **not** committed. This program never posts, uploads media, purchases services or merges a branch.

## Quality evidence
The separately shared, actual local review MP4 is 1080x1920, H264 30fps, 691 frames / 23.033s, AAC 48kHz, full decode passed, audio elementary stream unchanged, 8 focus windows visually detected, local QA 18/18 and unit tests 14/14. GitHub CI uses **synthetic two-second video and sound only**, not this inherited user MP4.

The input UI is a local fictional demo, not a recording of an external AI service. Focus timing is manually assigned from visible frames and captions; it does not establish word-level speech alignment or independently verified Japanese pronunciation. The generic ten-genre geometry code has not been tested as ten complete genre videos.

## Release gate
**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Original v33 video side-by-side, independent ASR/semantic synchronization, inherited audio/image commercial rights, real phone playback, employee approval and actual GitHub Actions billing are unverified. Employee-approved manual posting only; no auto-post, merge, paid contracts or public upload of private media.
