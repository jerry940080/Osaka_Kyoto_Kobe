# 大阪・京都・神戶 8 天 7 夜 旅のしおり（叔叔阿姨版）

單一 HTML 檔的行程懶人包：每日 SVG 路線地圖（捲動時畫線動畫）、時刻表、景點卡片（照片輪播＋介紹＋YouTube 內嵌）、車票費用表與訂票時程。
放上 GitHub Pages 就能分享，照片內嵌後離線也能看。

> 依 2023 年 10/4–10/11 學生時期實走行程改編：兩人成行、可自駕、預算較寬裕。日期以週四出發為例，航班與三段候選飯店標「待訂」；唯一直接推薦的飯店是神戶 The Royal Park Canvas 神戶三宮。

## 行程骨架

| 天 | 內容 | 住 |
|---|---|---|
| Day 1（四） | 桃園 → 關西機場 → 南海 Rapi:t → 難波；心齋橋、道頓堀晚餐 | 難波（候選：Swissôtel 南海大阪） |
| Day 2（五） | 黑門市場、大阪城、阿倍野 HARUKAS 300（選項四天王寺）、新世界串炸・通天閣、道頓堀夜景 | 難波 |
| Day 3（六） | JR 新快速到京都；清水寺、二三年坂、高台寺、八坂神社、祇園，晚餐十二段家 | 京都三條・河原町（候選） |
| Day 4（日） | 京阪到宇治：宇治上神社、平等院、中村藤吉本店；JR 回程伏見稻荷千本鳥居；晚餐焼肉弘 | 京都三條・河原町 |
| Day 5（一） | JR 到三宮；神戶牛午餐（彩DINING／モーリヤ本店）；租車 → 有馬溫泉 太閤の湯 → 六甲ガーデンテラス夜景 | The Royal Park Canvas 神戶三宮 ★ |
| Day 6（二） | 自駕：姬路城、好古園 → 舞子公園・明石海峽大橋 → 還車；元町商店街、南京町（選項港塔夜景） | The Royal Park Canvas 神戶三宮 ★ |
| Day 7（三） | JR 到大阪；中之島中央公會堂・薔薇園、梅田百貨、空中庭園夕陽、北新地晚餐 | 大阪站上（候選：Hotel Granvia） |
| Day 8（四） | 特急 HARUKA 大阪站 → 關西機場 → 桃園（建議下午班） | — |

## 檔案

```
index.html           成品（所有資料都在這一個檔）
template.html        原始模板（熱海・伊豆範例），不要改，留給下一趟行程重生
TEMPLATE_GUIDE.md    模板通用說明：資料格式、引擎行為、風格慣例
CLAUDE.md            這個專案的修改指南（給 Claude Code 與人看）
tools/embed_images.py  照片轉 base64 塞進 index.html（pip install pillow）
tools/make_land.py     重生海岸線資料（目的地換區域時才需要）
tools/check_keys.js    檢查資料區 key 是否互相對得上
```

## 本機預覽

```bash
python3 -m http.server 8000
# 開 http://localhost:8000
```
不要直接用 `file://` 開：YouTube 內嵌需要 referrer，本機檔案會顯示錯誤 153，上了網址就正常。

## 修改資料

所有內容都在 `index.html` 第二段 `<script>` 的資料區，由上而下：
`P`（座標）→ `RAILS`（背景鐵路）→ `NAMES`（顯示名／類型）→ `CARDS`（景點卡）→ `IMG`（照片）→ `DAYS`（每日行程）。
首頁總覽圖在 `/* RENDER */` 裡的 `const cfg={pts:...}`。詳細格式見 `TEMPLATE_GUIDE.md`，這個專案的慣例見 `CLAUDE.md`。

改完跑一次：
```bash
node tools/check_keys.js
```

## 加照片

```bash
python3 tools/embed_images.py index.html inari=1.jpg,2.jpg   # 覆蓋，第一張＝卡片封面
python3 tools/embed_images.py index.html +inari=3.jpg        # 追加
```
key 就是 `CARDS` 裡的 key（例如 `inari`、`kiyomizu`、`arima`）。工具會自動縮到 1200 寬、轉 JPEG q82；截圖請先裁掉浮水印。每張約 100–250 KB，20–30 張成品約 3–7 MB。

## 部署到 GitHub Pages

1. 把這個分支合併到 `main`。
2. GitHub → Settings → Pages → Source 選 **Deploy from a branch** → `main` / `/ (root)` → Save。
3. 幾分鐘後網址是 `https://jerry940080.github.io/Osaka_Kyoto_Kobe/`。

## 海岸線資料

第一段 `<script>` 的 `const LAND` 已用 `tools/make_land.py` 重生為關西版：

```bash
# 核心六府縣，高精度
python3 tools/make_land.py --lat0 34.0 --lat1 35.5 --lng0 134.5 --lng1 136.5 \
  --prefs 大阪府 京都府 兵庫県 奈良県 滋賀県 和歌山県 --eps 0.0007 > core.js
# 外圍六縣，低精度，只為了首頁總覽圖邊緣不露出海
python3 tools/make_land.py --lat0 33.9 --lat1 35.6 --lng0 134.0 --lng1 137.5 \
  --prefs 三重県 徳島県 香川県 岡山県 愛知県 岐阜県 --eps 0.003 > outer.js
# 兩段陣列串接後取代第一段 <script> 的內容
```
資料來源：國土数値情報（dataofjapan/land）。
