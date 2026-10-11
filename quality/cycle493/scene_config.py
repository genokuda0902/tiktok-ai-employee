"""Cycle493 common data contract. Local full renderer is in cycle493_source_tests_qa.zip.
Zero-cost original image slides; Japanese TTS is strictly required before publication.
"""
GENRES = {
 "ai_workflow":"AI・仕事効率化","business":"ビジネス","sales":"営業",
 "beauty":"美容","money":"お金","psychology":"心理",
 "career":"キャリア","science":"科学","travel":"旅行","comparison":"比較",
}
RESOLUTION=(1080,1920)
FPS=30
SCENE_SECONDS=3.2
SAFE_TEXT_BOX=(72,210,875,1570)
SCENES=[
 {"kind":"hook","title":"AIに任せる？ それとも人？","clauses":["AIに任せる仕事、任せない仕事。","境界線を、整理します。"]},
 {"kind":"draft","title":"文章の下書きは AIに任せる","clauses":["文章の下書きは、AIで効率化。","仕上げは、自分の言葉で。"]},
 {"kind":"table","title":"表の整理も AIが手伝う","clauses":["表の整理も、AIが手伝える。","数字の正しさは、確認。"]},
 {"kind":"privacy","title":"個人情報は 入力前に確認","clauses":["個人情報は、むやみに入力しない。","社内ルールを、優先。"]},
 {"kind":"verify","title":"出典のない答え 断定しない","clauses":["出典が不明なら、断定しない。","事実と条件を、照合。"]},
 {"kind":"finish","title":"AIが作る。人が決める。","clauses":["AIが作り、人が決める。","この順番を、忘れずに。"]},
]
def release_gate(qa):
 """Technical playback does not imply publication permission."""
 return (
  qa.get("voice_native_japanese_verified") is True
  and qa.get("full_decode") == "PASS"
  and qa.get("resolution") == [1080,1920]
  and qa.get("human_review") == "APPROVED"
  and qa.get("rights") == "ORIGINAL_PROCEDURAL"
  and qa.get("publication") == "MANUAL_POST_APPROVED"
 )
