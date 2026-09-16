import { chromium } from 'playwright';
import fs from 'fs';
import { execFileSync } from 'child_process';
fs.mkdirSync('output/v19',{recursive:true});
fs.mkdirSync('output/v19_scenes',{recursive:true});
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1080,height:1920}});
await page.setContent(`<!doctype html><meta charset="utf-8"><style>*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 70% 10%,#123f7a,#020817 55%);color:white;font-family:'Noto Sans JP','Noto Sans CJK JP',sans-serif;overflow:hidden}.brand{position:absolute;top:75px;left:70px;font-weight:900;font-size:38px;color:#63ecff}.app{position:absolute;left:65px;top:230px;width:950px;height:1420px;background:#f7f9fc;color:#101727;border-radius:42px;box-shadow:0 45px 120px #000b;overflow:hidden}.bar{height:105px;background:#fff;border-bottom:1px solid #dbe1e8;padding:30px 45px;font-weight:800;font-size:32px}.chat{padding:60px}.bubble{background:#e8edf4;border-radius:28px;padding:35px;font-size:34px;line-height:1.55}.answer{margin-top:45px;opacity:0;transform:translateY(45px);transition:.55s}.answer.show{opacity:1;transform:none}.table{width:100%;border-collapse:collapse;background:white;font-size:27px;box-shadow:0 15px 45px #1232}.table th{background:#10a37f;color:white}.table td,.table th{padding:24px;border:1px solid #d8dee7}.cursor{position:absolute;width:46px;height:46px;left:810px;top:1260px;filter:drop-shadow(0 4px 5px #0005);transition:1s}.caption{position:absolute;bottom:90px;left:70px;width:940px;padding:30px;border-radius:28px;background:#020817e8;color:white;text-align:center;font-size:48px;font-weight:900}.accent{color:#5beaff}</style><div class="brand">AI時短ラボ</div><div class="app"><div class="bar">AI Assistant</div><div class="chat"><div class="bubble">以下の顧客情報から<br><b>氏名・電話番号・メール・希望日時</b>を抽出して、表で出力してください。</div><div class="answer" id="a"><table class="table"><tr><th>氏名</th><th>電話番号</th><th>希望日時</th></tr><tr><td>山田 太郎</td><td>090-1234-5678</td><td>9/18 14:00</td></tr><tr><td>佐藤 花子</td><td>080-9876-5432</td><td>9/19 11:00</td></tr></table></div></div></div><svg class="cursor" viewBox="0 0 32 32"><path fill="white" stroke="#111" stroke-width="2" d="M3 2l21 17-10 2 6 8-5 3-6-9-6 7z"/></svg><div class="caption">長文 → <span class="accent">表が完成</span></div>`);
const cast=page.screencast;
await cast.start({path:'output/v19/browser_proof.webm',size:{width:1080,height:1920},quality:92});
await page.waitForTimeout(900);
await cast.showChapter('長文をそのまま貼る',{description:'必要な項目だけAIが整理',duration:1100});
await page.waitForTimeout(1200);
await page.locator('#a').evaluate(el=>el.classList.add('show'));
await page.waitForTimeout(1600);
await page.locator('.cursor').evaluate(el=>{el.style.left='340px';el.style.top='920px'});
await page.waitForTimeout(1400);
await cast.showOverlay('<div style="font:900 44px sans-serif;background:#10a37f;color:white;padding:22px 38px;border-radius:24px">このままExcelへ</div>',{duration:1300});
await page.waitForTimeout(1500);
await cast.stop(); await browser.close();
// Use real moving browser proof in the final timeline instead of static screenshots.
for (const [scene,start] of [['04','0'],['05','2'],['06','4']]) {
  execFileSync('ffmpeg',['-y','-ss',start,'-i','output/v19/browser_proof.webm','-t','2','-vf','fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920','-an','-c:v','libx264','-crf','16','-preset','medium',`output/v19_scenes/scene_${scene}.mp4`],{stdio:'inherit'});
}
