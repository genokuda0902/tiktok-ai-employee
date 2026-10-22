"""CI fixture: verify 1080x1920 slide -> H.264/AAC MP4 full decode.
Synthetic audio only. Not a Japanese narration quality check.
"""
import json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
GENRES=['AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし']
def run(*cmd):
    return subprocess.run(cmd,check=True,capture_output=True,text=True).stdout
def main():
    assert len(set(GENRES))==10
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp);png=p/'scene.png';mp4=p/'smoke.mp4'
        im=Image.new('RGB',(1080,1920),(3,14,30));d=ImageDraw.Draw(im)
        font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',64)
        d.rounded_rectangle((65,400,1015,1080),radius=30,fill=(6,48,63),outline=(77,236,201),width=4)
        d.text((110,560),'たった一行。',font=font,fill=(245,251,255));im.save(png)
        run('ffmpeg','-y','-v','error','-loop','1','-framerate','30','-i',str(png),'-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1','-t','1','-c:v','libx264','-pix_fmt','yuv420p','-r','30','-c:a','aac','-ar','48000','-movflags','+faststart',str(mp4))
        info=json.loads(run('ffprobe','-v','error','-show_streams','-of','json',str(mp4)))
        v=next(s for s in info['streams'] if s['codec_type']=='video')
        a=next(s for s in info['streams'] if s['codec_type']=='audio')
        assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'])==(1080,1920,'h264','30/1')
        assert a['codec_name']=='aac' and a['sample_rate']=='48000'
        run('ffmpeg','-v','error','-xerror','-i',str(mp4),'-f','null','-')
        print('PASS: 10 genres, Japanese slide, 1080x1920, H264/AAC, decode')
if __name__=='__main__':main()
