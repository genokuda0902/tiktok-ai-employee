from pathlib import Path
import pytest
from tools.cycle1893_audio_level import normalize

def test_missing_source():
    with pytest.raises(FileNotFoundError):
        normalize(Path("/not-existing.mp4"),Path("/tmp/test.mp4"))
