# 旅行懶人包模板 使用說明

一套「單一 HTML 檔」的行程懶人包模板。改資料、不動引擎，就能做出新行程：
每日 SVG 路線地圖（捲動時畫線動畫）、時刻表、景點卡片（照片輪播＋介紹＋YouTube 內嵌）、
車票費用表與訂票時程。放上 GitHub Pages／Netlify 即可分享，照片內嵌離線也能看。

## 檔案

| 檔案 | 用途 |
|---|---|
| `template.html` | 模板本體（內含熱海・伊豆・靜岡 8 天行程當作完整範例，照片已清空約 150 KB） |
| `tools/embed_images.py` | 把照片轉 base64 塞進 HTML（`pip install pillow`） |
| `tools/make_land.py` | 目的地不在關東–靜岡時，重生海岸線資料 |
| `CLAUDE.md`（原專案） | 若用 Claude Code 協作，把改寫過的版本放 repo 根目錄 |

## 製作新行程的順序

1. **複製 `template.html` 改名 `index.html`**，先改 `<title>` 與 hero 區的標題、日期、路線、航班文字。
2. **海岸線（第一段 script 的 `const LAND`）**：範例涵蓋約 北緯 34.4–36.0、東經 138.2–140.6
   （關東＋靜岡＋伊豆）。目的地超出範圍就跑：
   ```bash
   python3 tools/make_land.py --lat0 34.0 --lat1 35.5 --lng0 135.0 --lng1 136.5 \
     --prefs 大阪府 京都府 兵庫県 奈良県 --eps 0.0007 > land.js
   ```
   把輸出整段取代第一段 script 內容。純城市行程不想要地形，也可以 `const LAND=[];`（地圖變純色底）。
3. **第二段 script 的資料區，由上而下改**：
   - `P`：所有會用到的地點 `{key:[緯度,經度]}`。key 用英文小寫。
   - `RAILS`：背景鐵路虛線（裝飾用），沿線車站串起來即可，不需要可設 `const RAILS=[];`
   - `NAMES`：`{key:['顯示名','類型']}`，類型 `hotel`（紅點＋🛏）/`spot`（粉點）/`station`（白圈）/`air`（黑菱形）。
   - `MODE`：交通方式的線色線型，通常不用改；要新增交通工具照格式加一行。
   - `IMG`：留 `{}`，照片之後用工具塞（見下）。
   - `CARDS`：景點卡。格式：
     ```js
     key:{name:'中文名',jp:'日文/原文名',kind:'景點',short:'卡片上的一句話',
          wiki:['維基百科條目名'],            // 沒自備照片時的備援圖（連網才會載）
          video:[{u:'https://youtu.be/xxxx',l:'標籤可空'}],  // 可省略；網址帶 t=53s 會從該秒播
          text:'展開後的完整介紹（2–4 句）',
          chips:['開放時間','費用','交通']},
     ```
   - `DAYS`：每天一個物件：
     ```js
     {n:1,date:'2/10',wd:'三',title:'A → B',sub:'副標一句',stay:'今晚飯店',
      map:{pts:['要顯示的點'],legs:[{a:'起',b:'訖',mode:'rail',via:['中途點'],curve:.2}],
           labels:{key:'t|b|l|r'},minSpan:.1},   // minSpan=地圖最小緯度跨幅，市區日 .02、跨縣日 .2–.3
      tl:[{t:'09:00',i:'🚄',h:'標題（只放標題，不放長描述）',move:1}],  // move:1 淡藍底=移動列
      cards:['cardKey'],
      rain:'<b>雨備</b>　...'}                    // 可省略
     ```
   - 首頁總覽圖：搜 `const cfg={pts:` 那段，放整趟的大路線。
4. **HTML 區塊**：行前一頁看懂（住宿表）、車票與費用、訂票時程、美食與行李，直接改表格文字。
5. **照片**：
   ```bash
   python3 tools/embed_images.py index.html kinomiya=1.jpg,2.jpg   # 覆蓋，第一張=封面
   python3 tools/embed_images.py index.html +kinomiya=3.jpg        # 追加
   ```
   截圖先裁掉浮水印／Google 鏡頭圖示（常在底部 8–9%）。工具會自動縮 1200 寬、轉 JPEG q82。
6. **部署**：GitHub repo 放 `index.html` → Settings → Pages → main 分支。
   注意：YouTube 內嵌需要 referrer，**本機 file:// 開啟影片會顯示錯誤 153**，上了網址就正常。

## 引擎行為備忘

- 地圖 bbox 由 `pts` 自動計算，`labels` 控制標籤在點的上/下/左/右，重疊就換方位或加大 `minSpan`。
- 同一段路來回會疊線，回程 leg 加 `curve:0.2`（負值彎另一邊）。
- 卡片點開＝彈窗：上照片輪播（←→、圓點、手機滑動）、中文字、分隔線下影片。
- 每日地圖捲入視窗會播路線動畫，`重播路線` 鈕可重看；尊重系統「減少動態」設定。
- 桌機把滑鼠移到首頁大地圖會展開完整比例。
- 檔案大小：引擎＋海岸線約 150 KB，每張照片約 100–250 KB，20–30 張照片的成品約 3–7 MB。

## 風格慣例（想維持同一系列感的話）

和紙底 `#f8f5ee`、藍 `#2b4c7e`、櫻粉 `#e28aa5`、朱紅 `#c8452e`（住宿/租車）；
標題 Noto Serif TC。時刻表只放標題；估算時間寫「約」；文案繁體中文、專名保留原文。
