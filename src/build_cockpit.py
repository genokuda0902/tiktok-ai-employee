import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for p in sorted((ROOT/"config/accounts").glob("*.json")):
    a=json.loads(p.read_text(encoding="utf-8"))
    rows.append({"employee":a["name"],"account":a["account"],"niche":a["niche"],
                 "status":"READY","today_target":2,"generated":0,"posted":0,
                 "monthly_follower_gain":0})
out=ROOT/"output"; out.mkdir(exist_ok=True)
(out/"cockpit.json").write_text(json.dumps({"accounts":rows},ensure_ascii=False,indent=2),encoding="utf-8")
html=["<meta charset='utf-8'><title>AI社員 COCKPIT</title>",
"<style>body{font-family:sans-serif;background:#07101f;color:#fff;padding:30px}table{width:100%;border-collapse:collapse}td,th{padding:14px;border-bottom:1px solid #334155}h1{color:#67e8f9}</style>",
"<h1>TikTok AI社員 COCKPIT</h1><table><tr><th>社員</th><th>アカウント</th><th>ジャンル</th><th>状態</th><th>本日目標</th></tr>"]
for r in rows: html.append(f"<tr><td>{r['employee']}</td><td>{r['account']}</td><td>{r['niche']}</td><td>{r['status']}</td><td>2本</td></tr>")
html.append("</table>")
(out/"cockpit.html").write_text("".join(html),encoding="utf-8")
