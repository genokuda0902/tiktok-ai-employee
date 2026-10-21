"""Map phrase timestamps from source timeline to silence-trimmed TikTok video.
No ASR claim: these are manually curated/VAD-estimated phrase boundaries.
Works for any of the 10 genres with the same edit decision list.
"""
FPS = 30

def map_frame(old_frame: int, kept_ranges: list[tuple[int,int]]) -> int:
    offset = 0
    for start, end in kept_ranges:
        if start <= old_frame < end:
            return offset + old_frame - start
        offset += end - start
    if old_frame == kept_ranges[-1][1]:
        return offset
    raise ValueError(f"frame {old_frame} removed by silence edit")

def remap_phrase_cues(cues: list[dict], kept_ranges: list[tuple[int,int]]) -> list[dict]:
    out = []
    for cue in cues:
        frames = [map_frame(round(cue[k] * FPS), kept_ranges)
                  for k in ("start_s", "boundary_s", "end_s")]
        if not (frames[0] < frames[1] < frames[2]):
            raise ValueError(f"invalid phrase times: {cue}")
        out.append({"scene": cue["scene"], "phrases": cue["phrases"],
                    "frames": frames,
                    "seconds": [round(f / FPS, 4) for f in frames],
                    "method": "VAD phrase estimate; not word-level forced alignment"})
    return out

def safe_caption_box(x: int, y: int, width: int, height: int) -> bool:
    return x >= 35 and x + width <= 945 and y >= 0 and y + height <= 1690

def srt_timestamp(frame: int) -> str:
    ms = round(frame * 1000 / FPS)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def make_srt(cues: list[dict]) -> str:
    lines = []
    index = 0
    for cue in cues:
        a, b, c = cue["frames"]
        for start, end, text in [(a, b, cue["phrases"][0]),
                                 (b, c, cue["phrases"][1])]:
            index += 1
            lines += [str(index), f"{srt_timestamp(start)} --> {srt_timestamp(end)}",
                      text, ""]
    return "\n".join(lines)
