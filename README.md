# 大阪・京都・神戶 7 天 6 夜 旅のしおり

單一 HTML 檔的行程懶人包：每日 SVG 路線地圖（捲動時畫線動畫）、時刻表、景點卡片（照片輪播＋介紹＋YouTube 內嵌）、車票費用表與訂票時程。
放上 GitHub Pages 就能分享，照片內嵌後離線也能看。

> 目前是**草稿**：日期（2027/3/27–4/2）為示意，航班與三段飯店都標「待訂」，訂位後再回填。

## 行程骨架

| 天 | 內容 | 住 |
|---|---|---|
| Day 1 | 桃園 → 關西機場 → 南海 Rapi:t → 難波；心齋橋、道頓堀 | 難波 |
| Day 2 | 大阪城、黑門市場、新世界・通天閣、梅田藍天大廈夜景（選項：奈良半日） | 難波 |
| Day 3 | JR 新快速到京都；伏見稻荷、清水寺、二三年坂、八坂神社、祇園、先斗町 | 京都站前 |
| Day 4 | 嵯峨野觀光小火車、竹林、天龍寺、渡月橋、金閣寺、錦市場 | 京都站前 |
| Day 5 | JR 新快速到三宮；北野異人館、南京町、舊居留地、メリケンパーク、臨海樂園、神戶牛 | 三宮 |
| Day 6 | 有馬溫泉泡湯 → 六甲有馬纜車 → 六甲ガーデンテラス → 天覧台夜景 → 六甲ケーブル | 三宮 |
| Day 7 | Port Liner → 神戶機場 → Bay Shuttle 高速船 30 分 → 關西機場 → 桃園 | — |

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
