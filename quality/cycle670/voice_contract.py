GENRES = ("AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約", "営業・ビジネス", "転職・キャリア", "健康・生活改善", "雑学・科学", "旅行・グルメ", "商品比較・暮らし")
BEATS = ((0,2,"集計、まだ手作業？"),(2,4,"毎月、同じ作業。"),(4,6,"AIに式を聞く。"),(6,8,"実画面で確かめる。"),(8,10,"数字を確認。"),(10,14,"サム関数で、合計は六百五十。"),(14,16,"グラフも一致。"),(16,18,"式と結果を比較。"),(18,20,"保存して試そう。"))
def validate(genre, beats=BEATS, actual_voice_durations=None):
    if genre not in GENRES or not beats: raise ValueError("Invalid genre")
    cursor=0
    if actual_voice_durations is not None and len(actual_voice_durations)!=len(beats): raise ValueError("Count mismatch")
    for i,(a,b,caption) in enumerate(beats):
        if a!=cursor or b<=a or not caption: raise ValueError("Invalid timeline")
        if actual_voice_durations is not None and not 0<actual_voice_durations[i]<=b-a-.12: raise ValueError("Audio overflow")
        cursor=b
    if cursor!=20: raise ValueError("Duration mismatch")
    return True
def srt(beats=BEATS):
    def ts(s): return f"00:{int(s//60):02d}:{int(s%60):02d},000"
    return "\n\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{c}" for i,(a,b,c) in enumerate(beats,1))+"\n"
def review_gate(narration_present=False, voice_sync_human_checked=False):
    return {"quality":"HUMAN_REVIEW","publication":"NOT_APPROVED","manual_post_only":True,"japanese_narration":"PRESENT_UNREVIEWED" if narration_present else "ABSENT","voice_caption_sync_verified":bool(narration_present and voice_sync_human_checked)}
