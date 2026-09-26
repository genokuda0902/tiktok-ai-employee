from dataclasses import dataclass

@dataclass(frozen=True)
class HookLatencyPlan:
    lead_silence: float
    max_lead_silence: float = 0.12
    target_duration: float = 0.0

    def validate(self):
        if self.lead_silence < 0 or self.lead_silence > self.max_lead_silence:
            raise ValueError("lead silence outside bounded hook-latency correction")
        if self.target_duration <= 0:
            raise ValueError("target duration must be positive")
        return self

    def ffmpeg_audio_filter(self) -> str:
        self.validate()
        d = self.target_duration
        s = self.lead_silence
        return (
            f"atrim=start={s:.3f},asetpts=PTS-STARTPTS,"
            f"apad=pad_dur={s:.3f},atrim=duration={d:.3f}"
        )

def release_contract():
    return {
        "zero_cost": True,
        "preserve_video": True,
        "preserve_burned_captions": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "max_lead_silence_s": 0.12,
    }
