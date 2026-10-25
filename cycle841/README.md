# cycle841: editorial slides and single-beat Japanese captions

Review-only proof of concept. The completed local MP4 was generated with Pillow,
FFmpeg and existing AI-generated fictional images. This PR saves the **shared**
10-genre palette, cut-aware subtitle timing engine and tests. The full local
Pillow/FFmpeg renderer, MP4 and source images are in the review ZIP delivered
in ChatGPT; no source photos or audio are committed to this repository.

Change versus cycle840: 3-line captions become one active spoken phrase,
preserving 24 caption states; all eight slides are re-composed with restrained
photo-first layout. AAC stream is bit-identical to cycle840.

Known limitation: the previous 7 photo dissolves were not retained. FFmpeg
xfade failed to establish a valid constant frame rate for looped PNG inputs;
the local renderer uses frame-exact per-scene clips + concat + ASS + audio copy.

QA: 1080x1920, H264/30fps, 691 decoded frames, 23.033s, AAC 48kHz,
24/24 visible subtitle beats, 8 distinct scenes, 12/12 local QA,
8/8 local tests. CI here tests code only, **not** the MP4.

No paid API, merge, publishing, automatic posting or rights approval.
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Employee review then manual posting only.
