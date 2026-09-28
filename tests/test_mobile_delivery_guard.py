import pytest
from video_engine.mobile_delivery_guard import DeliveryMeta, validate_mobile_delivery

def good():
    return DeliveryMeta(1080,1920,30.0,"h264","aac",48000,2,True,1.0)

def test_accepts_tiktok_delivery_contract():
    validate_mobile_delivery(good())

@pytest.mark.parametrize("field,value",[
    ("width",720),("fps",29.0),("video_codec","hevc"),("audio_rate",44100),
    ("audio_channels",1),("moov_before_mdat",False),("max_keyframe_gap_s",2.0),
])
def test_rejects_invalid_delivery_metadata(field,value):
    d=good().__dict__.copy(); d[field]=value
    with pytest.raises(ValueError):
        validate_mobile_delivery(DeliveryMeta(**d))
