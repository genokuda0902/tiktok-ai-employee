"""Capture 26 screenshots of an actually interactive, offline Chromium demo.

No network access, no third-party login, no real spreadsheet/AI claims.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML='''<!doctype html><html lang="ja"><meta charset="utf-8"><style>
*{box-sizing:border-box}body{margin:0;background:#0a1e2e;color:#eefaff;font-family:"Noto Sans CJK JP",sans-serif}
#app{width:900px;height:560px;padding:27px 31px;background:linear-gradient(125deg,#0d3144,#091f30)}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.title{font-size:29px;font-weight:800}.badge{font-size:18px;border:1px solid #55d7ef;border-radius:18px;padding:7px 16px;color:#b0effa}
.info{font-size:21px;color:#b2d7e5;margin-bottom:12px}
textarea{width:100%;height:230px;border:2px solid #4abed5;border-radius:16px;padding:21px 24px;background:#f7fdff;color:#102d3a;font:700 27px/1.55 "Noto Sans CJK JP",sans-serif;resize:none}
.footer{display:flex;justify-content:space-between;align-items:center;margin-top:17px}
button{border:0;background:#06a9ca;color:white;font-size:25px;font-weight:800;border-radius:14px;padding:13px 30px;cursor:pointer}
#status{font-size:23px;font-weight:800;color:#8de6dc}
.pills{display:flex;gap:14px;margin-top:17px}.pills span{background:#15475a;border:1px solid #2f90a5;border-radius:13px;padding:6px 18px;font-size:19px}
</style><main id="app"><div class="top"><div class="title">指示テンプレートを保存する</div><div class="badge">架空データ / LOCAL</div></div>
<div class="info">繰り返す作業の「目的・条件・確認」を1つに</div>
<textarea id="prompt" placeholder="ここに指示を入力" spellcheck="false"></textarea>
<div class="footer"><div id="status">未保存</div><button id="save">テンプレートを保存</button></div>
<div class="pills"><span>目的：売上整理</span><span>条件：要点3つ</span><span>確認：元データ</span></div>
</main><script>document.querySelector('#save').onclick=()=>{const v=document.querySelector('#prompt').value;if(v.trim()){window.saveTemplate(v).then(()=>{document.querySelector('#status').textContent='✓ 保存しました';});}};</script></html>'''
TEXT='この売上データを整理し、\n要点を3つ示して。\n数字は必ず元データと照合。'

def capture(outdir):
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu','--disable-background-networking'])
  context=browser.new_context(viewport={'width':900,'height':560},device_scale_factor=1)
  page=context.new_page();page.expose_function('saveTemplate',lambda v: (out/'saved_template.txt').write_text(v,encoding='utf-8'));page.set_content(HTML)
  field=page.locator('#prompt')
  for i in range(26):
   if 2<=i<=20:
    field.fill(TEXT[:round((i-1)/19*len(TEXT))])
   elif i>20: field.fill(TEXT)
   if i==21:
    page.locator('#save').click()
    page.locator('#status').wait_for(state='visible')
    page.wait_for_function("document.querySelector('#status').textContent.includes('保存しました')")
   page.locator('#app').screenshot(path=str(out/f'{i:02d}.png'))
  assert page.locator('#status').inner_text()=='✓ 保存しました'
  assert (out/'saved_template.txt').read_text(encoding='utf-8')==TEXT
  context.close();browser.close()
 return len(list(out.glob('*.png')))

if __name__=='__main__':
 import sys
 print('captured',capture(sys.argv[1]))
