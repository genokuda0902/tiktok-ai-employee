"""Ten-genre, review-only Japanese caption timing contract."""
GENRES=("ai_productivity","trivia","cooking","beauty","finance","wellness","travel","product_demo","story","business")
SPEECH_WINDOWS=((.27,2.34),(3.51,5.64),(6.90,9.03),(10.29,12.09),(13.35,15.78),(17.04,19.53),(20.82,23.73),(25.02,26.79))
CAPTIONS=("Excelの集計、まだ手作業？","まずは売上データを準備","AIに分析の指示を入力","4か月の売上をグラフ化","表とグラフで変化を確認","手計算と表計算で検算","合計65万円を両方で確認","手順を保存してあとで試そう")
def validate(genre, windows=SPEECH_WINDOWS, captions=CAPTIONS, approved=False):
    if genre not in GENRES or approved or len(windows)!=len(captions):
        raise ValueError("unsupported genre or unapproved publication")
    prev=0
    for (start,end),caption in zip(windows,captions):
        if start<prev or end<=start or end>27.343 or len(caption)>22 or len(caption)<6:
            raise ValueError("invalid caption or speech window")
        prev=end
    return True
