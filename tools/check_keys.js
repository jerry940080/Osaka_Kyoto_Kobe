#!/usr/bin/env node
// 檢查 index.html 資料區的 key 是否互相對得上：
//   DAYS / RAILS / hero cfg 用到的地點都在 P 裡、有畫成標記的點都在 NAMES 裡、cards 都在 CARDS 裡、mode 都在 MODE 裡。
// 用法：node tools/check_keys.js [index.html]
const fs = require('fs');
const file = process.argv[2] || 'index.html';
const s = fs.readFileSync(file, 'utf8');
const data = s.match(/\/\* ================= DATA ================= \*\/([\s\S]*?)\/\* ================= MAP ENGINE/);
const hero = s.match(/const cfg=\{pts:[\s\S]*?bbox:\{[^}]*\}\};/);
if (!data || !hero) { console.error('找不到資料區或 hero cfg'); process.exit(1); }
eval(data[1].replace(/\bconst /g, 'var ')); eval(hero[0].replace(/\bconst /g, 'var '));

const problems = [];
const need = new Set(), markers = new Set();
RAILS.forEach(r => r.pts.forEach(k => need.add(k)));
function check(cfg, tag) {
  cfg.pts.forEach(k => { need.add(k); markers.add(k); });
  cfg.legs.forEach(l => {
    [l.a, l.b].forEach(k => { need.add(k); markers.add(k); });
    (l.via || []).forEach(k => need.add(k));
    if (!MODE[l.mode]) problems.push(`${tag}: 未定義的 mode「${l.mode}」`);
  });
  Object.keys(cfg.labels || {}).forEach(k => {
    if (!markers.has(k)) problems.push(`${tag}: labels 有「${k}」但地圖上沒有這個點`);
  });
}
DAYS.forEach(d => {
  check(d.map, `Day ${d.n}`);
  d.cards.forEach(c => { if (!CARDS[c]) problems.push(`Day ${d.n}: cards 有「${c}」但 CARDS 沒有`); });
});
check(cfg, 'hero');
need.forEach(k => { if (!P[k]) problems.push(`P 缺少座標「${k}」`); });
markers.forEach(k => { if (!NAMES[k]) problems.push(`NAMES 缺少「${k}」`); });
Object.keys(IMG).forEach(k => { if (!CARDS[k]) problems.push(`IMG 有「${k}」但 CARDS 沒有這張卡`); });

const unusedCards = Object.keys(CARDS).filter(c => !DAYS.some(d => d.cards.includes(c)));
console.log(`地點 ${Object.keys(P).length}、景點卡 ${Object.keys(CARDS).length}、天數 ${DAYS.length}、照片 ${Object.keys(IMG).length} 組`);
if (unusedCards.length) console.log('提醒：沒被任何一天用到的卡片：', unusedCards.join(', '));
if (problems.length) { console.log('\n有問題：'); problems.forEach(p => console.log(' -', p)); process.exit(1); }
console.log('OK，所有 key 都對得上。');
