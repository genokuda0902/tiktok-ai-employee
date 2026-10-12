from pathlib import Path
from tts_offline import synthesize

def test_missing_voice():
    try:
        synthesize('こんにちは', Path('/not-found'), Path('/not-found.htsvoice'), Path('out.wav'))
    except RuntimeError:
        return
    raise AssertionError('Missing voice was not rejected')
