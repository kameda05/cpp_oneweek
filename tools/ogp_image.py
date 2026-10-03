# -*- coding: utf-8 -*-
"""SNSで共有したときに表示される画像（img/ogp.png、1200x630）を作る。

使い方: python tools/ogp_image.py [出力先フォルダ（省略時は ../img）]
Windows の Noto Sans JP（C:\\Windows\\Fonts\\NotoSansJP-VF.ttf）を使う。
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img')
FONT = r'C:\Windows\Fonts\NotoSansJP-VF.ttf'

W, H = 1200, 630
PRIMARY = (0x00, 0x59, 0x9c)
PRIMARY_DARK = (0x00, 0x44, 0x82)
ACCENT = (0xe8, 0xa0, 0x20)


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f


img = Image.new('RGB', (W, H))
d = ImageDraw.Draw(img)
# サイトのヒーローと同じ、左上から右下へのグラデーション
for y in range(H):
    for x in range(0, W, 4):
        t = (x / W + y / H) / 2
        c = tuple(round(a + (b - a) * t) for a, b in zip(PRIMARY, PRIMARY_DARK))
        d.rectangle([x, y, x + 3, y], fill=c)


def center(text, y, f, fill):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


# バッジ
badge = font(34, 700)
label = 'C++言語 入門'
bw = d.textlength(label, font=badge) + 56
d.rounded_rectangle([(W - bw) / 2, 150, (W + bw) / 2, 210], radius=30, fill=ACCENT)
center(label, 155, badge, (255, 255, 255))

center('一週間で身につく', 250, font(64, 700), (255, 255, 255))
center('C++言語の基本', 335, font(88, 700), (255, 255, 255))
center('クラス・継承・テンプレート・STL を、基本編・応用編・練習問題で学ぶ', 480, font(30, 500), (220, 232, 245))

os.makedirs(OUT, exist_ok=True)
img.save(os.path.join(OUT, 'ogp.png'), optimize=True)
print('ogp.png')
