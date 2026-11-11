# cycle1371 — review only
Improvement over cycle1370: burn existing timed Japanese subtitles into visible frames rather than relying on player support for selectable mov_text subtitles.
Input: prior local cycle1370_REVIEW_ONLY.mp4 and extracted captions.srt; these are NOT committed. Video is NOT independently reproducible from this repository.
Command: python experiments/cycle1371/render.py input.mp4 captions.srt review.mp4
Local tests: 2/2 PASS. FFmpeg decode: PASS. Output H.264 1080x1920 10.0s AAC test tone, NO Japanese narration and NO speech synchronization.
SHA256 local MP4: 29563f5bca6d5831462597707c5fd8794601df7990ebc9605f22408a436bef29.
No publication approval. Do not merge or post. Reference v33 video and research source unavailable for direct comparison.
