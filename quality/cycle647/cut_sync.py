"""Reusable audio-energy-guided scene boundaries; NOT speech recognition or transcript alignment."""
from dataclasses import dataclass
import numpy as np

GENRES = (
    'AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約',
    '営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学',
    '旅行・グルメ','商品比較・暮らし',
)

@dataclass(frozen=True)
class Safety:
    publication: str = 'NOT_APPROVED'
    human_review: bool = True
    auto_post: bool = False

def assert_safe(safety=Safety()):
    if (safety.publication, safety.human_review, safety.auto_post) != ('NOT_APPROVED', True, False):
        raise ValueError('publication must remain blocked until human approval')

def rms_envelope(pcm, sample_rate, fps=30):
    """Compute a per-video-frame RMS envelope from mono float PCM."""
    if sample_rate <= 0 or fps <= 0:
        raise ValueError('invalid sample rate/fps')
    pcm=np.asarray(pcm, dtype=np.float32)
    if pcm.ndim!=1 or not len(pcm):
        raise ValueError('mono nonempty PCM required')
    frame_count=int(np.ceil(len(pcm)*fps/sample_rate))
    energy=np.zeros(frame_count, dtype=np.float32)
    for frame in range(frame_count):
        a=round(frame*sample_rate/fps)
        b=max(a+1,round((frame+1)*sample_rate/fps))
        block=pcm[a:min(len(pcm),b)]
        energy[frame]=float(np.sqrt(np.mean(block*block))) if len(block) else 0
    return energy

def optimize_boundaries(original, energy, max_shift=12, min_frames=35):
    """Choose local energy minima near cuts; NOT a sentence-boundary guarantee."""
    if not original or original[0]!=0 or original[-1]>len(energy):
        raise ValueError('invalid boundaries')
    if any(b<=a for a,b in zip(original,original[1:])):
        raise ValueError('unordered boundaries')
    if max_shift<0 or min_frames<=0:
        raise ValueError('invalid constraints')
    cuts=[original[0]]
    for i, old in enumerate(original[1:-1],1):
        lower=max(old-max_shift,cuts[-1]+min_frames)
        upper=min(old+max_shift,original[i+1]-min_frames)
        if lower>upper:
            raise ValueError('no feasible boundary')
        options=[]
        for k in range(lower,upper+1):
            window=energy[max(0,k-1):min(len(energy),k+2)]
            options.append((float(np.mean(window))+0.00025*abs(k-old),abs(k-old),k))
        cuts.append(min(options)[2])
    cuts.append(original[-1])
    if any(b-a<min_frames for a,b in zip(cuts,cuts[1:])):
        raise ValueError('scene too short')
    return cuts
