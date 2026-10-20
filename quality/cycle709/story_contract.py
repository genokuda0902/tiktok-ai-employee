"""Cycle709: reusable 16-scene storyboard, numerical proof and review-only rights gates."""
from dataclasses import dataclass
FPS,DURATION,SCENE_COUNT,WIDTH,HEIGHT=30,36,16,1080,1920
GENRES=tuple(f"genre_{i:02d}" for i in range(1,11))
MONTHLY_SALES=(120000,150000,200000,250000)
SCENE_TITLES=("その作業、まだ手作業？","毎月の集計が大変…","AIを使って整理しよう","売上データを分析して","入力内容を確認","4か月の売上を集計","Excelで使える形に","売上グラフが完成","手作業とAI補助を比較","資料の要約にも応用","営業レポートにも応用","次回はスライド編","AI時短ラボ","作業時間を見直そう","保存して後で試そう","続きは次回の動画で")
SCENE_SUBTITLES=("集計・資料作成をもっとわかりやすく","毎回同じ操作、負担になっていませんか？","まずは架空の売上データから","自然な日本語で指示を作成","送信前に個人情報がないか確認","1月12万・2月15万・3月20万・4月25万","数値と書式を人がチェック","4月が最高：25万円（架空データ）","AIの結果も人による検算が必要","用途に合わせて編集して使う","事実確認を忘れずに","作業の流れを紹介予定","AIでもっと自由な時間を","効果は作業内容で変わります","後で手順を見返せます","フォローして次の実演もチェック")
@dataclass(frozen=True)
class Asset:
    origin:str
    internal_review_allowed:bool
    publication_approved:bool=False
def validate_scenes(titles,subtitles):
    if len(titles)!=SCENE_COUNT or len(subtitles)!=SCENE_COUNT:raise ValueError("16 scenes required")
    for line in list(titles)+list(subtitles):
        if not line or len(line)>48:raise ValueError("Caption empty or too long")
        if any(bad in line for bad in ("必ず成功","100%削減","一瞬で完成")):raise ValueError("Unverified performance claim")
    return True
def validate_asset(asset,*,for_publication=False):
    if asset.origin not in {"user_provided","self_generated","licensed","public_domain"}:raise ValueError("Unknown provenance")
    if not asset.internal_review_allowed:raise ValueError("Internal usage not cleared")
    if for_publication and not asset.publication_approved:raise ValueError("Publication rights not cleared")
    return True
def can_publish(*,asset_approved,employee_approved,narration_verified,captions_synced,privacy_checked,phone_playback_verified):
    return all((asset_approved,employee_approved,narration_verified,captions_synced,privacy_checked,phone_playback_verified))
def sales_proof():
    return {"total":sum(MONTHLY_SALES),"peak_month":"4月","peak_yen":max(MONTHLY_SALES)}
