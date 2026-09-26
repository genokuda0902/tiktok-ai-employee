import pytest

from video_engine.high_fidelity_encode import encode_contract, ffmpeg_args


def test_contract_is_zero_cost_manual_and_audio_copy():
    c = encode_contract()
    assert c["crf"] == 16
    assert c["preset"] == "slow"
    assert c["audio_codec"] == "copy"
    assert c["zero_cost"] is True
    assert c["human_approval_required"] is True
    assert c["auto_post"] is False


def test_contract_fails_closed_on_non_delivery_geometry():
    with pytest.raises(ValueError):
        encode_contract(720, 1280, 30)
    with pytest.raises(ValueError):
        encode_contract(1080, 1920, 24)


def test_ffmpeg_args_preserve_expected_delivery_settings():
    args = ffmpeg_args()
    assert args[args.index("-crf") + 1] == "16"
    assert args[args.index("-pix_fmt") + 1] == "yuv420p"
    assert args[args.index("-c:a") + 1] == "copy"
