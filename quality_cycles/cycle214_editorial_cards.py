# cycle214 editorial-card renderer
# Common 10-genre concept: scene data -> native 9:16 image card -> captions -> MP4.
# Runtime artifact was generated separately and validated at 1080x1920 / SAR 1:1 / DAR 9:16.
SCENES = [
 ("その集計、まだ10分かけてる？","毎日の集計、まだ手作業？"),
 ("AIに入れる","必要なデータをAIに入力"),
 ("集計 → 分析 → 整理","AIがまとめて処理"),
 ("確認するだけ","結果をすぐ確認"),
 ("10分 → 1分","作業時間を短縮"),
]
VIDEO_SPEC={"width":1080,"height":1920,"fps":30,"sar":"1:1","dar":"9:16"}
QUALITY_STATE="HUMAN_REVIEW"
PUBLICATION="NOT_APPROVED"
# New TTS was attempted via free gTTS but network connection failed.
# Therefore cycle214 reuses previously verified Japanese AAC and does NOT claim new TTS success.
