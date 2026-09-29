#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重生模板用的海岸線資料（LAND）。

用法：
  python3 make_land.py --lat0 34.4 --lat1 36.0 --lng0 138.2 --lng1 140.6 \
      --prefs 静岡県 神奈川県 東京都 千葉県 山梨県 埼玉県 > land.js
  然後把輸出的 `const LAND=[...];` 整段取代 template.html 第一段 <script> 的內容。

資料來源：dataofjapan/land（國土数値情報，都道府縣邊界 GeoJSON）。
日本以外的行程，改用 Natural Earth 10m coastline 自行替換 fetch 網址與屬性欄位。
"""
import json, math, sys, argparse, urllib.request

URL = "https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson"

def dp(pts, eps):  # Douglas-Peucker 簡化
    if len(pts) < 3: return pts
    def d(p, a, b):
        (x, y), (x1, y1), (x2, y2) = p, a, b
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0: return math.hypot(x - x1, y - y1)
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))
    a, b = pts[0], pts[-1]; imax = 0; dmax = 0
    for i in range(1, len(pts) - 1):
        dd = d(pts[i], a, b)
        if dd > dmax: dmax, imax = dd, i
    if dmax > eps:
        return dp(pts[:imax + 1], eps)[:-1] + dp(pts[imax:], eps)
    return [a, b]

def rings(geom):
    if geom["type"] == "Polygon":
        yield from geom["coordinates"]
    else:
        for p in geom["coordinates"]:
            yield from p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat0", type=float, required=True)
    ap.add_argument("--lat1", type=float, required=True)
    ap.add_argument("--lng0", type=float, required=True)
    ap.add_argument("--lng1", type=float, required=True)
    ap.add_argument("--prefs", nargs="+", required=True, help="都道府縣名（日文），例：静岡県")
    ap.add_argument("--eps", type=float, default=0.0007, help="簡化容差(度)，越大檔越小")
    a = ap.parse_args()
    g = json.load(urllib.request.urlopen(URL))
    out = []
    for name in a.prefs:
        fs = [f for f in g["features"] if f["properties"]["nam_ja"] == name]
        if not fs:
            print(f"!! 找不到 {name}", file=sys.stderr); continue
        for r in rings(fs[0]["geometry"]):
            if not any(a.lat0 <= y <= a.lat1 and a.lng0 <= x <= a.lng1 for x, y in r):
                continue
            sr = dp(r, a.eps)
            if len(sr) < 5: continue
            out.append([[round(x, 4), round(y, 4)] for x, y in sr])
    sys.stdout.write("const LAND=" + json.dumps(out, separators=(",", ":")) + ";\n")
    print(f"rings={len(out)} points={sum(len(o) for o in out)}", file=sys.stderr)

if __name__ == "__main__":
    main()
