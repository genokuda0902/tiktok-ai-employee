"""Reusable ten-genre geometry and Japanese speech-cue contract (cycle730)."""
GENRES = {
 'AI・仕事効率化':'#5DD9FF','美容・身だしなみ':'#FFB2D3','恋愛・心理':'#DCA9FF',
 'お金・節約':'#81E4B2','営業・ビジネス':'#FFCC74','転職・キャリア':'#ADC6FF',
 '健康・生活改善':'#7DDFCA','雑学・科学':'#56E6D4','旅行・グルメ':'#FFAD8C',
 '商品比較・暮らし':'#D7E6A3'
}
FRAME_SIZE=(1080,1920)
FPS=30
FRAME_RANGE=(392,461)
CAPTION_BOUNDS=(61,1355,890,1530)
RIGHT_SAFE_LIMIT=900
BOTTOM_SAFE_LIMIT=1600
CUES=((13.2333,14.1333,'入力、処理、'),(14.1333,14.6667,'出力。'))

def caption_at(t):
 for start,end,phrase in CUES:
  if start <= t < end:return phrase
 return ''

def validate():
 assert len(GENRES)==len(set(GENRES.values()))==10
 assert FRAME_SIZE==(1080,1920) and FPS==30
 assert FRAME_RANGE[1]-FRAME_RANGE[0]==69
 assert CAPTION_BOUNDS[2]<RIGHT_SAFE_LIMIT
 assert CAPTION_BOUNDS[3]<BOTTOM_SAFE_LIMIT
 assert caption_at(13.8)=='入力、処理、'
 assert caption_at(14.4)=='出力。'
 assert caption_at(15.0)==''
 return True
