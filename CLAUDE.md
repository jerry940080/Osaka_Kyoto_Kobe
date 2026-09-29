# CLAUDE.md — 大阪・京都・神戶 旅行懶人包

單一 HTML 檔的行程懶人包（`index.html`），由 `template.html` 模板產生。
原則只有一條：**改資料、不動引擎。**

## 檔案

| 檔案 | 用途 |
|---|---|
| `index.html` | 成品。放上 GitHub Pages 就是網站本體，所有資料都在這個檔裡 |
| `template.html` | 原始模板（熱海・伊豆範例），**不要改**，留著給下一趟行程重生用 |
| `TEMPLATE_GUIDE.md` | 模板通用說明：資料格式、引擎行為、風格慣例 |
| `tools/embed_images.py` | 把照片轉 base64 塞進 `index.html` 的 `IMG`（需 `pip install pillow`） |
| `tools/make_land.py` | 從 dataofjapan/land 重生海岸線 `const LAND` |
| `tools/check_keys.js` | 檢查資料區的 key 是否互相對得上（`node tools/check_keys.js`） |

## index.html 的結構

1. `<head>`：`<title>`、CSS（不動）
2. `<header class="hero">`：標題、日期、路線、航班文字
3. `#pre`：行前一頁看懂（住宿表）
4. `#days`：空的，由 JS 依 `DAYS` 產生
5. `#tickets`、`#food`：車票費用、訂票時程、美食、行李（純 HTML 表格與清單）
6. 第一段 `<script>`：`const LAND`（海岸線，已是關西版，一整行約 146 KB，不要手改）
7. 第二段 `<script>`：
   - `/* DATA */` 到 `/* MAP ENGINE */` 之間是**資料區**：`P` → `RAILS` → `MODE` → `KIND` → `NAMES` → `CARDS` → `IMG` → `DAYS`
   - `/* MAP ENGINE */` 與 `/* RENDER */` 之後是引擎，不動；唯一例外是 `/* RENDER */` 裡的 `const cfg={pts:...}`（首頁總覽圖）

## 常見修改怎麼做

- **新增一個景點**：`P` 加座標（`key:[緯度,經度]`，key 英文小寫）→ `NAMES` 加 `[顯示名, 類型]` → `CARDS` 加卡片 → 在某天的 `DAYS[n].map.pts/legs`、`labels`、`cards`、`tl` 加進去 → `node tools/check_keys.js`。
- **改日期**：hero 的 kicker、`<title>`、住宿表、訂票時程、每個 `DAYS[n].date/wd`、頁尾。換星期時注意休市日（木津市場週日・假日與不定期週三、黑門市場部分店週日、十二段家週四與第二週三、金の湯第 2・4 週二、國立國際美術館週一）。
- **填航班**：hero 的 `.flights` 三行、Day 1 與 Day 7 時刻表第一列／最後一列（目前寫「待訂」）。
- **填飯店**：`NAMES` 的 `nambahotel / kyotohotel / umedahotel` 顯示名、對應 `CARDS`、住宿表、每天的 `stay`；座標可改成真正的飯店位置。`kobehotel` 已是 The Royal Park Canvas 神戶三宮（下山手通 2-3-1），不用改。
- **加照片**：`python3 tools/embed_images.py index.html inari=a.jpg,b.jpg`（覆蓋，第一張是封面）、`+inari=c.jpg`（追加）。照片先裁掉浮水印。
- **加影片**：`CARDS[key].video=[{u:'https://youtu.be/xxxx',l:'標籤'}]`，網址帶 `t=53s` 會從該秒開始播。目前所有卡片都沒放影片，要放請用真的看過的連結。
- **地圖標籤重疊**：改 `labels` 方位（`t/b/l/r`）、加大 `minSpan`，或把太近的點從 `pts` 拿掉只留卡片。來回同一段路，回程 leg 加 `curve:.2`（負值彎另一邊）。
- **海岸線**：目前 `LAND` 涵蓋 北緯 33.9–35.6、東經 134.0–137.5，核心六府縣（大阪・京都・兵庫・奈良・滋賀・和歌山）精度 0.0007 度，外圍六縣（三重・徳島・香川・岡山・愛知・岐阜）精度 0.003 度，只為了首頁總覽圖邊緣不要露出海。行程範圍沒變就不用重生。

## 驗證

```bash
node tools/check_keys.js            # key 對不對得上
python3 -m http.server 8000         # 開 http://localhost:8000 看，別用 file:// （YouTube 內嵌會報錯 153）
```
瀏覽器 console 不該有 JS 錯誤；每張地圖的標籤不能疊在一起（桌機與手機各看一次）。

## 風格慣例

- 繁體中文文案，專名保留日文原文；估算時間一律寫「約」；時刻表 `tl` 只放標題，長描述放卡片 `text`。
- 顏色：JR 藍 `#2b4c7e`、私鐵綠 `#3c9a72`、地鐵與纜車紫 `#6f5aa0`、公車黃 `#d9a21b`、住宿與租車朱紅 `#c8452e`、小火車棕 `#8b5a2b`、高速船藍綠 `#1f7a8c`。
- 景點類型 `kind`：景點／午餐／晚餐／夜景／交通／住宿／購物／體驗／選項／雨備。選項與雨備一律放在該天卡片的最後。
- 車資與開放時間會變，寫進去的數字都是「約」，並在頁尾聲明以官方公告為準。

## 目前狀態

- 行程本體：8 天 7 夜（難波 2 晚・京都 2 晚・三宮 2 晚・梅田 1 晚），依 2023 年 10/4–10/11 學生時期實走版改編給叔叔阿姨（兩人、可自駕、預算較寬裕）。旅行時間 5 月底–6 月初（頁面以 2027/5/27–6/3 週四出發為例），航班與三段候選飯店標「待訂」；神戶 The Royal Park Canvas 神戶三宮 是唯一住過、直接推薦的飯店。
- 神戶兩天（Day 5–6）以租車為主軸：三宮 → 有馬 → 六甲山 → 三宮、三宮 → 姬路 → 舞子 → 三宮；每天的 `rain` 欄有公共運輸備案。
- 京都 Day 4 是洛北（叡山電車→貴船川床→一乗寺→下鴨神社），宇治已拿掉；伏見稻荷改成 Day 3 早上的選項。大阪 Day 2 早餐主推木津市場，黑門市場只逛。
- 出發前要確認的店：貴船川床（ひろ文／仲よし／ふじや，雨天停業）、彩DINING（網路有 2023 年底歇業留言，備案 モーリヤ本店）、十二段家（週四休）、焼肉弘（建議改訂正規店）。
- 季節相關數字（日落約 19:05、春薔薇、青楓徐行 4 月中–5 月底、梅雨平年 6/6）都是依 5 月底寫的，換季節要一起改。
- 照片：`IMG={}`，尚未嵌入；卡片先用 Wikipedia 縮圖當備援（連網才會顯示）。
- 影片：全部未放。
