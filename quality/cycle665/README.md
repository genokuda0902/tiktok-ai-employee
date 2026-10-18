# Cycle 665: subtitle repair

Compared with cycle 664, the rendered Japanese subtitles now use the exact `spoken_text` strings rather than editorial summaries in all eight scenes. Original AAC audio is preserved. This verifies the script-to-caption contract only; speech transcription and Japanese voice naturalness remain unverified.

Local checks: 1080x1920, H.264, AAC, 468 frames, 15.6 seconds, full decode, 4 unit tests passing. Ten genre profiles configured, science genre rendered. Publication requires human approval. No posting or merging.

The reproducible local ZIP contains the full renderer, images, audio and tests. No binary video is committed to GitHub.
