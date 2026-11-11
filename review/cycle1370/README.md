# cycle1370 review only
Input: cycle1369_REVIEW_ONLY.mp4 (local previous cycle, not committed).
Output: 10s 1080x1920 H.264 AAC plus Japanese mov_text selectable subtitle stream.
Local pytest: 2 passed. ffmpeg full decode: PASS. SHA256: a817c854af98724de0bff9fed61d41c730ce45a53615b823dcc3459ab0cb2afa.
No Japanese speech. Timed subtitles are NOT speech-synchronized. PUBLICATION_NOT_APPROVED.
To reproduce, place the previous cycle MP4 at ../cycle1369/cycle1369_REVIEW_ONLY.mp4 then run python render.py.
Previous cycle lacked selectable subtitle stream. No user reference original available for direct comparison.
