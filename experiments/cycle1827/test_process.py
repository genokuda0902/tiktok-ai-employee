import json
import subprocess
import sys


def test_output(path):
    streams = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', path]))['streams']
    assert streams[0]['codec_name'] == 'h264'
    assert (streams[0]['width'], streams[0]['height']) == (1080, 1920)
    assert streams[1]['codec_name'] == 'aac'


if __name__ == '__main__':
    test_output(sys.argv[1])
