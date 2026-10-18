"""Original music generator for 10 TikTok genres. Offline; no external assets."""
import numpy as np
from scipy.ndimage import gaussian_filter1d

GENRE_PRESETS = {
    "ai_productivity": (112, "C"), "beauty": (94, "F"),
    "relationships": (92, "G"), "money": (108, "D"),
    "sales": (122, "E"), "career": (105, "C"),
    "health": (88, "F"), "science": (114, "C"),
    "travel": (118, "G"), "shopping": (124, "D"),
}
ROOTS = {"C": 48, "D": 50, "E": 52, "F": 53, "G": 55}
CHORDS = [(0, 3, 7), (-4, 0, 3), (3, 7, 10), (-2, 2, 5)]

def render_music(duration=15.6, sr=44100, genre="science", seed=671):
    if genre not in GENRE_PRESETS:
        raise ValueError("Unsupported genre")
    bpm, key = GENRE_PRESETS[genre]
    rng = np.random.default_rng(seed)
    n = int(round(duration * sr))
    audio = np.zeros(n, np.float64)
    beat = 60 / bpm
    def hz(midi):
        return 440 * 2 ** ((midi - 69) / 12)
    for ci, start in enumerate(np.arange(0, duration, beat * 4)):
        stop = min(duration, start + beat * 4 + 0.16)
        st, en = int(start * sr), int(stop * sr)
        t = np.arange(en - st) / sr
        env = np.maximum(0, np.minimum(np.minimum(1, t / 0.20),
                         np.minimum(1, (stop - start - t) / 0.35)))
        for interval in CHORDS[ci % 4]:
            f = hz(ROOTS[key] + interval)
            audio[st:en] += 0.11 * (np.sin(2 * np.pi * f * t) +
                            0.19 * np.sin(2 * np.pi * 2 * f * t)) * env / 3
    for k, start in enumerate(np.arange(0, duration, beat)):
        if k % 4 == 3:
            continue
        chord = CHORDS[int(start / (beat * 4)) % 4]
        f = hz(ROOTS[key] + chord[(k // 2) % 3] + 12)
        length = min(0.38, duration - start)
        st = int(start * sr)
        en = min(n, st + int(length * sr))
        t = np.arange(en - st) / sr
        audio[st:en] += 0.06 * (np.sin(2 * np.pi * f * t) +
                        0.17 * np.sin(2 * np.pi * 3 * f * t)) * np.exp(-12 * t)
    audio += 0.009 * gaussian_filter1d(rng.normal(0, 1, n), 18)
    fade = np.minimum(1, np.arange(n) / (0.35 * sr)) * np.minimum(
        1, (n - 1 - np.arange(n)) / (0.8 * sr))
    audio *= np.maximum(0, fade)
    peak = np.max(np.abs(audio))
    if peak:
        audio *= min(1, 0.029 / peak)
    return audio.astype("float32")

def duck_music(music, voice, sr=44100, target=0.38):
    if len(music) != len(voice):
        raise ValueError("Audio length mismatch")
    block = max(1, int(0.05 * sr))
    levels = np.array([
        float(np.sqrt(np.mean(voice[i:i + block] ** 2)))
        for i in range(0, len(voice), block)
    ])
    gain = 1 - (1 - target) * np.clip((levels - 0.007) / 0.045, 0, 1)
    gain = gaussian_filter1d(gain, 3)
    env = np.interp(np.arange(len(music)), np.arange(len(gain)) * block, gain)
    return (music * env).astype("float32"), {
        "mean_gain": float(env.mean()), "min_gain": float(env.min()),
        "max_gain": float(env.max())
    }
