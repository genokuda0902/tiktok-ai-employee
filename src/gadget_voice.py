#!/usr/bin/env python3
"""Generate a new Raspberry Pi 5 narration using the existing AivisSpeech engine."""
import json, os, time, urllib.parse, urllib.request, wave
from pathlib import Path

base = os.environ.get('AIVIS_URL', 'http://127.0.0.1:10101')
out = Path('output/raspberry_pi5_narration.wav')
out.parent.mkdir(parents=True, exist_ok=True)
lines = [
    ('これ、ただの基板じゃない。', 'これ、ただの基板じゃない。'),
    ('ラズベリーパイ・ファイブ。', 'ラズベリーパイ・ファイブ。'),
    ('小さなパソコンとして、プログラミングや電子工作に使える。', '小さなパソコンとして、プログラミングや電子工作に使える。'),
    ('自分だけの仕組みを作りたい人は、保存してチェック。', '自分だけの仕組みを作りたい人は、保存してチェック。'),
]
def request(path, data=None):
    r = urllib.request.Request(base + path, data=data, headers={'Content-Type': 'application/json'} if data else {}, method='POST' if data is not None else 'GET')
    with urllib.request.urlopen(r, timeout=180) as response:
        return response.read()
speakers = None
for _ in range(60):
    try:
        speakers = json.loads(request('/speakers'))
        break
    except Exception:
        time.sleep(2)
if not speakers:
    raise RuntimeError('AivisSpeech engine not available or no speakers installed')
preferred = os.environ.get('AIVIS_SPEAKER_NAME', 'Flow').lower()
style_name = os.environ.get('AIVIS_STYLE_NAME', '04_FUN').lower()
speaker = next((s for s in speakers if preferred in s['name'].lower() and s.get('styles')), None)
if speaker is None:
    raise RuntimeError(f'Preferred speaker {preferred!r} is not installed; refusing silent voice substitution')
style = next((s for s in speaker['styles'] if style_name in s['name'].lower()), None)
if style is None:
    raise RuntimeError(f'Preferred style {style_name!r} is not installed')
style_id = int(style['id'])
params = None
frames = []
timings = []
cursor = 0.0
for display, spoken in lines:
    query = json.loads(request('/audio_query?' + urllib.parse.urlencode({'text': spoken, 'speaker': style_id}), b''))
    query['speedScale'] = float(os.environ.get('AIVIS_SPEED', '1.13'))
    query['intonationScale'] = float(os.environ.get('AIVIS_INTONATION', '1.12'))
    wav = request('/synthesis?' + urllib.parse.urlencode({'speaker': style_id}), json.dumps(query, ensure_ascii=False).encode())
    temp = out.parent / '_gadget_chunk.wav'
    temp.write_bytes(wav)
    with wave.open(str(temp), 'rb') as audio:
        current = (audio.getnchannels(), audio.getsampwidth(), audio.getframerate())
        if params is not None and current != params:
            raise RuntimeError('Aivis audio parameters changed between chunks')
        params = current
        duration = audio.getnframes() / audio.getframerate()
        frames.append(audio.readframes(audio.getnframes()))
    timings.append({'text': display, 'start': round(cursor, 3), 'end': round(cursor + duration, 3)})
    cursor += duration
    pause = 0.10
    frames.append(b'\0' * int(params[2] * pause) * params[0] * params[1])
    cursor += pause
    temp.unlink(missing_ok=True)
with wave.open(str(out), 'wb') as audio:
    audio.setnchannels(params[0]); audio.setsampwidth(params[1]); audio.setframerate(params[2]); audio.writeframes(b''.join(frames))
(out.parent / 'raspberry_pi5_timing.json').write_text(json.dumps(timings, ensure_ascii=False, indent=2), encoding='utf-8')
assert out.stat().st_size > 1000
print(f'Created {out}, {cursor:.2f}s, speaker={speaker["name"]}, style={style["name"]}')
