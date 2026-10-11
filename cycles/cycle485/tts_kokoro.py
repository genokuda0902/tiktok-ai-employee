"""Japanese narration synthesis experiment. Human review required."""
import numpy as np
import soundfile as sf
from kokoro import KPipeline
from ci_build import OUT, TEXTS

def main():
    pipeline = KPipeline(lang_code="j")
    segments = []
    for scene in TEXTS:
        audio_parts = [np.asarray(w, dtype=np.float32) for _, _, w in pipeline(scene[2], voice="jf_alpha", speed=1.0)]
        if not audio_parts:
            raise RuntimeError("No narration generated")
        audio = np.concatenate(audio_parts)
        required = 76800
        if len(audio) > required:
            raise RuntimeError("Narration exceeds scene duration; revision required")
        segments.append(np.pad(audio, (0, required-len(audio))))
    sf.write(OUT / "narration_ja.wav", np.concatenate(segments), 24000)

if __name__ == "__main__":
    main()
