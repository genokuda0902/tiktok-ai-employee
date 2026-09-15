import { chromium } from 'playwright';
import fs from 'fs';

const plan=JSON.parse(fs.readFileSync('output/v19_plan.json','utf8'));
fs.mkdirSync('output/v19_scenes',{recursive:true});
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1080,height:1920}});

const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
for(const s of plan.scenes){
  const isRobot=s.type==='character'||s.type==='cta';
  const isHuman=s.type==='human'||s.type==='before_after';
  const isProof=s.type.includes('proof');
  const html=`<!doctype html><html><head><meta charset="utf-8"><style>
  *{box-sizing:border-box}body{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:'Noto Sans CJK JP',sans-serif;background:radial-gradient(circle at 50% 25%,#143b72 0,#06152c 45%,#020713 100%);color:white}
  .glow{position:absolute;width:900px;height:900px;border-radius:50%;left:90px;top:220px;background:radial-gradient(circle,#16c8ff55,transparent 65%);filter:blur(30px);animation:pulse 1.2s ease-in-out infinite alternate}
  .tag{position:absolute;top:92px;left:72px;font-size:34px;font-weight:800;color:#65ddff}.title{position:absolute;left:72px;right:72px;bottom:250px;font-size:82px;font-weight:900;line-height:1.15;text-shadow:0 8px 30px #000}
  .sub{position:absolute;left:74px;bottom:150px;font-size:34px;color:#bfefff}.card{position:absolute;left:85px;right:85px;top:420px;height:720px;border-radius:48px;background:#ffffff12;border:2px solid #58d9ff55;backdrop-filter:blur(18px);box-shadow:0 40px 100px #0008;transform:perspective(900px) rotateX(2deg);animation:float 1.4s ease-in-out infinite alternate}
  .robot{font-size:310px;text-align:center;padding-top:120px;filter:drop-shadow(0 20px 40px #00bfff88)}.human{font-size:260px;text-align:center;padding-top:135px}.ui{margin:70px;background:#f8fbff;color:#14233b;border-radius:30px;padding:45px;font-size:36px;box-shadow:0 25px 70px #0008}.bar{height:22px;background:#e7edf6;border-radius:20px;margin:24px 0;overflow:hidden}.bar:after{content:'';display:block;height:100%;width:78%;background:linear-gradient(90deg,#18c8ff,#176cff);animation:load 1.6s ease-in-out infinite alternate}.cursor{position:absolute;font-size:70px;right:150px;top:850px;animation:cursor 1.1s ease-in-out infinite alternate}
  @keyframes pulse{to{transform:scale(1.12);opacity:.7}}@keyframes float{to{transform:perspective(900px) rotateX(-2deg) translateY(-22px) scale(1.02)}}@keyframes load{from{width:15%}to{width:92%}}@keyframes cursor{to{transform:translate(-170px,-120px) scale(.85)}}
  </style></head><body><div class="glow"></div><div class="tag">AI時短ラボ · SCENE ${s.id}</div><div class="card">${isRobot?'<div class="robot">🤖</div>':isHuman?'<div class="human">👨🏻‍💼</div>':isProof?'<div class="ui"><b>AI WORKFLOW</b><div class="bar"></div><p>データを読み込み中…</p><p>✓ 表に整理</p><p>✓ 要点を抽出</p><p>✓ 次の操作へ</p></div><div class="cursor">➤</div>':'<div class="ui"><b>SMART WORK</b><div class="bar"></div><p>時短　→　効率化　→　成果</p></div>'}</div><div class="title">${esc(s.message)}</div><div class="sub">${esc(s.role)} · ${s.duration.toFixed(1)} sec</div></body></html>`;
  await page.setContent(html,{waitUntil:'load'});
  await page.screenshot({path:`output/v19_scenes/scene_${String(s.id).padStart(2,'0')}.png`,fullPage:false});
}
await browser.close();
console.log(`rendered ${plan.scenes.length} independent 1080x1920 scene masters`);
