# cycle1147 — original sound cues, HUMAN_REVIEW only

Distinct from cycle1145's intro title ghost fix: add seven original 160ms soft
transition sounds at existing chapter boundaries, placed into the quietest
speech window within 180ms of the cut. 48kHz mono, deterministic seed 1147,
SFX peak -22dBFS. No downloaded music or samples. Retains the complete video
H264 bitstream and existing Japanese subtitle pixels; re-encodes AAC audio to
mix the SFX, with Japanese narration retained.

Private local completed review MP4 (not committed): 22.5s, 1080x1920, 30fps,
675 frames, H264/AAC 48kHz. Full A/V decode passed; H264 bitstream identical;
seven cue windows increased from roughly -64 to -37dBFS; non-cue voice waveform
correlation 0.9999931; integrated loudness -16.28 LUFS unchanged; true peak
-1.59dBFS unchanged. Output SHA256:
a7084d2bd7d54464e9d0b4fd67446fd024ea07fa46a8b21317e18ddf22b33c78

Run local source only after rights review:
python quality/cycle1147/code/scene_cue_audio.py SOURCE.mp4 OUT.mp4 SFX.wav SOURCE_SHA256

CI uses synthetic 2.5-second H264/AAC material and 2 cues, never private
Japanese narration or the user's reference video. Previous research summaries
emphasize a strong hook, purposeful cuts, readable Japanese captions and
employee manual approval. The 16-panel storyboard is known from prior review,
but v33 original MP4 is unavailable for direct comparison.

Not verified: independent Japanese ASR or speech-caption semantic/timing
alignment, rights to pre-existing audio/images, phone playback, employee
approval, reference-v33 parity, actual Actions billing. No merge, contract,
paid service or auto-post. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
