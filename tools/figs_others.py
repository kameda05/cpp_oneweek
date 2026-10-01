# -*- coding: utf-8 -*-
"""サイトの図（img/fig*.svg）を生成するスクリプト その2。

figs_classes.py 以外の図 28 枚を定義する。共通部品は figs_classes.py のものを使う。
使い方は tools/README.md を参照。
"""
import math
from xml.sax.saxutils import escape

from figs_classes import Svg, doc, uml, INK, RED, BLUE, FONT, MONO

CYAN = '#4dd0e1'
GOLD = '#f5c400'
GRAY = '#999'


# ---------------------------------------------------------------- 共通のイラスト
def car(s, x, y, w=150, body='#f5c400', stripe=None, roof_color=None):
    """横から見た乗用車。(x, y) は左上。"""
    k = w / 150
    def P(px, py):
        return f'{x + px * k:.1f},{y + py * k:.1f}'
    s.path(f'M{P(8, 52)} L{P(10, 36)} Q{P(12, 30)} {P(22, 29)} L{P(40, 27)} L{P(58, 8)} Q{P(62, 5)} {P(70, 5)} '
           f'L{P(104, 5)} Q{P(112, 5)} {P(117, 11)} L{P(132, 27)} L{P(140, 29)} Q{P(147, 31)} {P(146, 40)} '
           f'L{P(144, 52)} Z', color='#555', fill=body, sw=1.2)
    s.path(f'M{P(46, 27)} L{P(62, 11)} L{P(84, 11)} L{P(84, 27)} Z', color='#555', fill='#cfe8f7', sw=1)
    s.path(f'M{P(90, 27)} L{P(90, 11)} L{P(108, 11)} L{P(122, 27)} Z', color='#555', fill='#cfe8f7', sw=1)
    if roof_color:
        s.rect(x + 74 * k, y + 1 * k, 14 * k, 5 * k, stroke='#555', fill=roof_color, sw=1)
    if stripe:
        s.rect(x + 10 * k, y + 37 * k, 134 * k, 5 * k, stroke='none', fill=stripe, sw=0)
    for cx in (36, 116):
        s.circle(x + cx * k, y + 52 * k, 12 * k, stroke='#333', fill='#333')
        s.circle(x + cx * k, y + 52 * k, 5 * k, stroke='#bbb', fill='#ccc')


def van(s, x, y, w=150, body='#fff', stripe=RED):
    """救急車（箱型の車）。"""
    k = w / 150
    s.path(f'M{x + 6 * k},{y + 52 * k} V{y + 6 * k} H{x + 104 * k} L{x + 128 * k},{y + 26 * k} '
           f'L{x + 144 * k},{y + 32 * k} V{y + 52 * k} Z', color='#555', fill=body)
    s.path(f'M{x + 106 * k},{y + 10 * k} L{x + 124 * k},{y + 27 * k} H{x + 106 * k} Z', color='#555', fill='#cfe8f7')
    s.rect(x + 6 * k, y + 32 * k, 138 * k, 6 * k, stroke='none', fill=stripe, sw=0)
    s.rect(x + 46 * k, y + 12 * k, 6 * k, 16 * k, stroke='none', fill=RED, sw=0)
    s.rect(x + 41 * k, y + 17 * k, 16 * k, 6 * k, stroke='none', fill=RED, sw=0)
    s.rect(x + 60 * k, y + 1 * k, 12 * k, 5 * k, stroke='#555', fill=RED, sw=1)
    for cx in (34, 118):
        s.circle(x + cx * k, y + 52 * k, 12 * k, stroke='#333', fill='#333')
        s.circle(x + cx * k, y + 52 * k, 5 * k, stroke='#bbb', fill='#ccc')


def truck(s, x, y, w=150):
    k = w / 150
    s.rect(x + 4 * k, y, 98 * k, 48 * k, stroke='#555', fill='#2f6fdb')
    s.path(f'M{x + 104 * k},{y + 48 * k} V{y + 14 * k} H{x + 128 * k} L{x + 144 * k},{y + 30 * k} V{y + 48 * k} Z',
           color='#555', fill='#f39c12')
    s.path(f'M{x + 110 * k},{y + 18 * k} H{x + 126 * k} L{x + 138 * k},{y + 30 * k} H{x + 110 * k} Z', color='#555', fill='#cfe8f7')
    for cx in (26, 82, 124):
        s.circle(x + cx * k, y + 52 * k, 11 * k, stroke='#333', fill='#333')
        s.circle(x + cx * k, y + 52 * k, 4.5 * k, stroke='#bbb', fill='#ccc')


def block_arrow(s, x1, y1, x2, y2, width=22, head=16, both=False, fill='#fff'):
    """太い（白抜きの）矢印。"""
    ang = math.atan2(y2 - y1, x2 - x1)
    L = math.hypot(x2 - x1, y2 - y1)
    w = width / 2
    hw = width
    pts = []
    if both:
        pts = [(0, 0), (head, -hw), (head, -w), (L - head, -w), (L - head, -hw), (L, 0),
               (L - head, hw), (L - head, w), (head, w), (head, hw)]
    else:
        pts = [(0, -w), (L - head, -w), (L - head, -hw), (L, 0), (L - head, hw), (L - head, w), (0, w)]
    ca, sa = math.cos(ang), math.sin(ang)
    p = ' '.join(f'{x1 + px * ca - py * sa:.1f},{y1 + px * sa + py * ca:.1f}' for px, py in pts)
    s.add(f'<polygon points="{p}" fill="{fill}" stroke="#555" stroke-width="1.2"/>')


def rich(s, x, y, parts, size=13, mono=False, anchor='start'):
    """色や太さの違う文字列を 1 行に並べる。parts は (文字列, 色, 太字) の列。"""
    fam = MONO if mono else FONT
    spans = ''.join(f'<tspan fill="{c}" font-weight="{"bold" if b else "normal"}">{escape(t)}</tspan>'
                    for t, c, b in parts)
    s.add(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" text-anchor="{anchor}" '
          f'xml:space="preserve">{spans}</text>')


# ---------------------------------------------------------------- 0日目
def fig0_1():
    s = Svg(600, 270)
    s.text(110, 26, '操作（メソッド）', 15, 'middle', weight='bold')
    s.text(470, 26, '属性', 15, 'middle', weight='bold')
    s.callout(20, 42, 175, 160, [], (230, 150))
    for i, t in enumerate(['走行する', '停車する', '曲がる']):
        s.text(50, 100 + i * 24, '・' + t, 15)
    s.callout(405, 42, 175, 160, [], (375, 150))
    for i, t in enumerate(['スピード', '走行距離', '排気量']):
        s.text(430, 100 + i * 24, '・' + t, 15)
    car(s, 220, 100, 160)
    s.text(300, 250, 'オブジェクト（自動車）', 14, 'middle', weight='bold')
    s.save('fig0-1')


def blueprint(s, x, y):
    s.rect(x, y, 110, 90, stroke='#888', fill='#eef4fb')
    for i in range(1, 6):
        s.line(x, y + i * 15, x + 110, y + i * 15, color='#c7d8ec', sw=0.8)
        s.line(x + i * 18, y, x + i * 18, y + 90, color='#c7d8ec', sw=0.8)
    s.path(f'M{x + 60},{y + 12} L{x + 60},{y + 70} L{x + 100},{y + 70} Z', color='#556', fill='none', sw=1.5)
    s.rect(x + 10, y + 74, 70, 8, stroke='#a0703a', fill='#e2b56a', sw=1)
    s.circle(x + 30, y + 40, 16, stroke='#556')


def fig0_2():
    s = Svg(600, 400)
    s.add(f'<ellipse cx="420" cy="200" rx="165" ry="155" fill="none" stroke="#888" stroke-width="1.2" stroke-dasharray="8 6"/>')
    s.text(420, 24, 'オブジェクト（自動車）', 14, 'middle', weight='bold')
    blueprint(s, 20, 140)
    s.text(75, 252, 'クラス', 13, 'middle', weight='bold')
    s.text(75, 270, '（設計図に相当）', 12, 'middle')
    for (cx, cy) in [(340, 60), (420, 165), (330, 260)]:
        car(s, cx, cy, 130)
    s.line(140, 170, 330, 95, color=RED, arrow='ar', sw=2)
    s.line(140, 185, 410, 195, color=RED, arrow='ar', sw=2)
    s.line(140, 200, 320, 285, color=RED, arrow='ar', sw=2)
    s.text(300, 385, 'クラスがあれば、いくらでもオブジェクトを生成することが可能。', 13, 'middle', weight='bold')
    s.save('fig0-2')


# ---------------------------------------------------------------- 1日目
def fig1_1():
    s = Svg(480, 300)
    for cx, label in [(130, '名前空間A'), (340, '名前空間B')]:
        s.add(f'<ellipse cx="{cx}" cy="110" rx="95" ry="70" fill="none" stroke="#888" stroke-width="1.2" stroke-dasharray="8 6"/>')
        s.text(cx, 26, label, 13, 'middle', weight='bold')
        s.text(cx, 115, 'power', 14, 'middle', weight='bold', mono=True)
    s.line(225, 230, 140, 125, arrow='a')
    s.line(225, 230, 325, 125, arrow='a')
    s.circle(60, 270, 6, stroke=RED)
    s.text(76, 275, '名前空間が異なれば、同じ名前を用いてもよい。', 13)
    s.save('fig1-1')


def fig1_2():
    s = Svg(480, 260)
    s.add('<ellipse cx="130" cy="130" rx="95" ry="90" fill="none" stroke="#888" stroke-width="1.2" stroke-dasharray="8 6"/>')
    s.text(130, 26, '名前空間C', 13, 'middle', weight='bold')
    s.text(120, 105, 'power', 14, 'middle', weight='bold', mono=True)
    s.text(120, 160, 'power', 14, 'middle', weight='bold', mono=True)
    s.line(270, 130, 172, 100, arrow='a')
    s.line(270, 130, 172, 155, arrow='a')
    s.add(f'<path d="M282,122 l14,14 M296,122 l-14,14" stroke="{RED}" stroke-width="2.5"/>')
    s.text(306, 126, '同一名前空間では、', 13)
    s.text(306, 146, '同じ名前は使えない。', 13)
    s.save('fig1-2')


def fig1_3():
    s = Svg(520, 320)
    s.circle(55, 95, 38, stroke=GRAY)
    s.text(55, 101, 'cout', 16, 'middle', weight='bold', mono=True)
    s.circle(55, 195, 38, stroke=GRAY)
    s.text(55, 201, 'cin', 16, 'middle', weight='bold', mono=True)
    s.rect(180, 85, 120, 120, stroke='#666', fill='#bdbdbd', rx=16)
    s.text(240, 150, 'ストリーム', 14, 'middle', weight='bold')
    block_arrow(s, 93, 100, 182, 100)
    block_arrow(s, 182, 190, 93, 190)
    s.ellipse(430, 55, 75, 40)
    s.text(430, 60, 'ファイル', 14, 'middle')
    s.ellipse(430, 245, 75, 40)
    s.text(430, 250, 'コンソール', 14, 'middle')
    block_arrow(s, 300, 110, 362, 75, both=True)
    block_arrow(s, 300, 180, 362, 225, both=True)
    s.line(240, 285, 240, 210, arrow='a')
    s.text(240, 306, '必要に応じて、入出力対象を切り替える', 13, 'middle')
    s.save('fig1-3')


# ---------------------------------------------------------------- 2日目
def fig2_2():
    s = Svg(520, 300)
    s.text(230, 26, 'オブジェクト：obj', 15, 'middle', weight='bold')
    s.circle(250, 165, 115, stroke=GRAY)
    s.text(250, 105, 'm_num', 15, 'middle', mono=True)
    s.text(250, 205, 'void set(int num)', 14, 'middle', mono=True)
    s.text(250, 245, 'int get()', 14, 'middle', mono=True)
    s.line(470, 200, 340, 200, arrow='a', sw=3)
    s.text(400, 190, '① 値の設定', 14, weight='bold')
    s.line(470, 240, 300, 240, arrow='a', sw=3)
    s.text(400, 230, '③ 値の取得', 14, weight='bold')
    s.path('M178,200 C150,175 160,120 200,102', arrow='a', sw=3)
    s.text(196, 160, '② m_numに代入', 14, weight='bold')
    s.path('M195,245 C10,250 20,60 215,84', arrow='a', sw=3)
    s.text(20, 66, '④ m_num読み出し', 14, weight='bold')
    s.save('fig2-2')


def fig2_3():
    s = Svg(520, 300)
    for cx, name in [(140, 'obj1'), (380, 'obj2')]:
        s.text(cx, 28, f'インスタンス：{name}', 14, 'middle', weight='bold')
        s.circle(cx, 130, 85, stroke=GRAY)
        s.text(cx, 90, 'm_num', 14, 'middle', mono=True)
        s.text(cx, 150, 'void set(int num)', 13, 'middle', mono=True)
        s.text(cx, 174, 'int get()', 13, 'middle', mono=True)
        s.line(cx + 50, 255, cx + 30, 185, arrow='a')
    s.text(260, 285, 'インスタンスが異なると、メンバ変数、メンバ関数は異なる。', 13, 'middle')
    s.save('fig2-3')


# ---------------------------------------------------------------- 3日目
def fig3_1():
    s = Svg(560, 260)
    s.ellipse(370, 130, 140, 105)
    s.text(370, 18, 'Sampleクラス', 13, 'middle')
    s.text(300, 60, 'publicメンバ', 13, weight='bold')
    s.rect(300, 66, 100, 46)
    s.text(308, 85, 'a', 13, mono=True)
    s.text(308, 104, 'func1()', 13, mono=True)
    s.text(300, 140, 'privateメンバ', 13, weight='bold')
    s.rect(300, 146, 100, 46)
    s.text(308, 165, 'b', 13, mono=True)
    s.text(308, 184, 'func2()', 13, mono=True)
    s.line(130, 89, 298, 89, arrow='a')
    s.text(20, 94, 'アクセス可能', 13)
    s.line(130, 169, 298, 169, arrow='a')
    s.text(20, 174, 'アクセス不可能', 13)
    s.add(f'<path d="M206,161 l16,16 M222,161 l-16,16" stroke="{RED}" stroke-width="2.5"/>')
    s.line(490, 89, 402, 89, arrow='a')
    s.text(448, 80, 'アクセス可能', 11, 'middle')
    s.line(490, 169, 402, 169, arrow='a')
    s.text(448, 160, 'アクセス可能', 11, 'middle')
    s.text(60, 222, 'クラス外', 14, color=RED, weight='bold')
    s.text(370, 222, 'クラス内', 14, 'middle', color=RED, weight='bold')
    s.save('fig3-1')


def fig3_2():
    s = Svg(560, 310)
    s.text(270, 28, 'メンバ変数', 15, 'middle')
    s.text(270, 50, 'privateなので、外部からアクセスできない。', 15, 'middle')
    s.circle(330, 205, 92, stroke=GRAY)
    s.add('<ellipse cx="330" cy="150" rx="48" ry="22" fill="none" stroke="#888" stroke-width="1.2" stroke-dasharray="8 6"/>')
    s.text(330, 156, 'm_num', 16, 'middle', mono=True)
    s.path('M300,60 C300,90 320,100 322,124', arrow='a', sw=2)
    s.text(330, 210, 'void setNum()', 15, 'middle', mono=True)
    s.text(330, 250, 'int getNum()', 15, 'middle', mono=True)
    s.text(20, 210, 'セッター：値の設定', 15)
    s.line(185, 205, 252, 205, arrow='a', sw=2)
    s.text(20, 250, 'ゲッター：値の取得', 15)
    s.line(258, 245, 185, 245, arrow='a', sw=2)
    s.path('M412,205 H445 V160 H382', arrow='a', sw=2)
    s.path('M378,140 H460 V245 H412', arrow='a', sw=2)
    s.save('fig3-2')


# ---------------------------------------------------------------- 4日目
def fig4_1():
    s = Svg(560, 330)
    s.rect(20, 50, 130, 220, fill='#fafafa')
    s.line(85, 90, 85, 230, dash='10 8', arrow='a')
    s.text(85, 295, 'プログラム', 13, 'middle', weight='bold')
    s.text(170, 40, 'クラス名：Car', 13, weight='bold')
    s.circle(300, 170, 115, stroke=GRAY)
    s.text(300, 108, 'Car()', 13, 'middle', mono=True, weight='bold')
    s.rect(235, 116, 130, 30)
    s.text(300, 137, 'コンストラクタ', 15, 'middle')
    s.text(300, 206, '~Car()', 13, 'middle', mono=True, weight='bold')
    s.rect(235, 214, 130, 30)
    s.text(300, 235, 'デストラクタ', 15, 'middle')
    s.line(150, 131, 233, 131, arrow='a')
    s.text(175, 122, '生成', 13, weight='bold')
    s.line(150, 229, 233, 229, arrow='a')
    s.text(175, 220, '消去', 13, weight='bold')
    s.text(300, 310, 'インスタンス', 13, 'middle', weight='bold')
    s.callout(410, 50, 130, 46, ['生成時に', '一度だけ呼ばれる'], (367, 120), 12)
    s.callout(410, 150, 130, 46, ['消去時に', '一度だけ呼ばれる'], (367, 220), 12)
    s.save('fig4-1')


def fig4_2():
    s = Svg(520, 330)
    s.callout(40, 15, 440, 44, ['newとdeleteを使えば、生成と消去のタイミングを好きにできる。'], (140, 90), 13)
    s.rect(40, 90, 140, 200, fill='#fafafa')
    s.text(110, 125, 'new', 14, 'middle', weight='bold', mono=True)
    s.line(110, 140, 110, 245, dash='10 8', arrow='a')
    s.text(110, 270, 'delete', 14, 'middle', weight='bold', mono=True)
    s.text(110, 314, 'プログラム', 13, 'middle', weight='bold')
    s.line(140, 120, 340, 120, arrow='a')
    s.text(240, 110, '生成', 13, 'middle', weight='bold')
    s.circle(380, 120, 36, stroke=GRAY)
    s.text(380, 176, 'インスタンス', 13, 'middle')
    s.line(160, 265, 340, 265, arrow='a')
    s.text(240, 255, '消去', 13, 'middle', weight='bold')
    s.circle(380, 265, 36, dash='3 3', stroke=GRAY)
    s.text(380, 320, 'インスタンス', 13, 'middle')
    s.save('fig4-2')


# ---------------------------------------------------------------- 6日目
def fig6_1():
    s = Svg(600, 330)
    car(s, 225, 20, 150)
    s.text(395, 50, '自動車', 13, weight='bold')
    s.text(205, 40, '親クラス（スーパークラス）', 13, 'end', color=BLUE, weight='bold')
    for x2, lbl in [(105, '継承'), (300, '継承'), (495, '継承')]:
        s.line(300, 92, x2, 160, color=RED, arrow='ar', sw=2)
        s.text((300 + x2) / 2 + (8 if x2 > 300 else (-8 if x2 < 300 else 8)), 122, lbl, 12, 'start' if x2 >= 300 else 'end')
    car(s, 35, 175, 140, body='#fff', stripe='#222', roof_color=RED)
    s.text(105, 262, 'パトカー', 13, 'middle', weight='bold')
    van(s, 230, 170, 140)
    s.text(300, 262, '救急車', 13, 'middle', weight='bold')
    truck(s, 425, 172, 140)
    s.text(495, 262, 'トラック', 13, 'middle', weight='bold')
    for x in (105, 300, 495):
        s.text(x, 292, '子クラス', 13, 'middle', color=BLUE, weight='bold')
        s.text(x, 310, '（サブクラス）', 12, 'middle', color=BLUE)
    s.save('fig6-1')


def fig6_3():
    s = Svg(520, 170)
    s.rect(20, 20, 260, 40)
    s.text(150, 47, 'クラス名', 18, 'middle', weight='bold')
    s.rect(20, 60, 260, 42)
    s.text(32, 87, 'メンバ変数', 16)
    s.rect(20, 102, 260, 42)
    s.text(32, 129, 'メンバ関数', 16)
    for i, (m, t) in enumerate([('+', 'publicメンバ'), ('#', 'protectedメンバ'), ('-', 'privateメンバ')]):
        s.text(320, 56 + i * 28, f'{m} : {t}', 16)
    s.save('fig6-3')


def fig6_6():
    s = Svg(520, 190)
    s.text(100, 24, '単一継承', 14, 'middle', weight='bold')
    s.text(350, 24, '多重継承', 14, 'middle', weight='bold')
    def box(x, y, t):
        s.rect(x, y, 120, 32)
        s.text(x + 60, y + 21, t, 14, 'middle')
    box(40, 40, 'スーパークラス')
    box(40, 140, 'サブクラス')
    s.line(100, 140, 100, 74, arrow='tri')
    box(225, 40, 'スーパークラス')
    box(355, 40, 'スーパークラス')
    box(290, 140, 'サブクラス')
    s.path('M350,140 V110 H285 V74', arrow='tri')
    s.path('M350,110 H415 V74', arrow='tri')
    s.save('fig6-6')


# ---------------------------------------------------------------- 7日目
def fig7_1():
    s = Svg(580, 140)
    s.text(30, 52, 'add(3, 4)', 20, mono=True)
    s.line(150, 46, 300, 46, arrow='a', sw=1.5)
    s.text(315, 52, 'int add(int a, int b)', 18, mono=True)
    s.text(30, 108, 'add()', 20, mono=True)
    s.line(150, 102, 300, 102, arrow='a', sw=1.5)
    s.text(315, 108, 'int add()', 18, mono=True)
    s.save('fig7_1'.replace('_', '-'))


def fig7_2():
    s = Svg(560, 270)
    # sp1->func(); の行（3行目）と、Sup1 の func() の行が同じ高さ（中心 y=87）になるように置く
    cx = 60                      # コードの左端
    for i, t in enumerate(['sp1 = new Sup1();', 'sp2 = new Sub1();', 'sp1->func();', 'sp2->func();']):
        s.text(cx, 45 + i * 24, t, 16, mono=True)
    uml(s, 310, 20, 210, 'Sup1', [], ['+ func() : void'], row=20, size=14)   # func() の行の中心 y=87
    uml(s, 310, 160, 210, 'Sub1', [], ['+ func() : void'], row=20, size=14)  # func() の行の中心 y=227
    s.line(415, 160, 415, 102, arrow='tri')
    start = cx + 12 * 8.8 + 8    # 「sp1->func();」（12文字）の右端のすぐ横
    s.line(start, 87, 308, 87, arrow='a')
    s.path(f'M{start},111 H230 V227 H308', arrow='a')
    s.save('fig7-2')


# ---------------------------------------------------------------- 応用編1日目
def figex1_1():
    s = Svg(440, 330)
    code = [(30, '…'), (55, 'int n = 5;'), (80, 'print(n);'), (105, '//  参照渡し'), (130, 'ref(n);'),
            (155, 'print(n);'), (180, '…')]
    for y, t in code:
        s.text(130, y, t, 18, mono=True)
    s.rect(124, 113, 88, 25, stroke=RED, sw=2, fill='none')
    s.text(30, 70, 'n = 5;', 18, color=BLUE, mono=True)
    s.line(105, 45, 105, 95, color=BLUE, arrow='ab', sw=2)
    s.text(30, 165, 'n = 1;', 18, color=BLUE, mono=True)
    s.line(105, 140, 105, 190, color=BLUE, arrow='ab', sw=2)
    s.text(100, 240, 'void ref(int& n){', 18, mono=True)
    s.rect(225, 222, 26, 25, stroke=RED, sw=2, fill='none')
    s.text(130, 270, 'n = 1;', 18, mono=True)
    s.rect(124, 252, 76, 25, stroke=RED, sw=2, fill='none')
    s.text(100, 300, '}', 18, mono=True)
    s.path('M212,126 H260 V220', color=RED, arrow='ar', sw=2)
    s.text(280, 132, '①アドレス', 18, color=RED)
    s.path('M124,265 H60 V200', color=RED, arrow='ar', sw=2)
    s.text(240, 300, '②値の変更', 18, color=RED)
    s.save('figex1-1')


# ---------------------------------------------------------------- 応用編2日目
def code_doc(s, x, y, w, h, label, lines, colors=None, label_top=False):
    f = 12
    s.path(f'M{x},{y} H{x + w} V{y + h - f} L{x + w - f},{y + h} H{x} Z', fill='#fff')
    s.path(f'M{x + w},{y + h - f} H{x + w - f} V{y + h}')
    for i, t in enumerate(lines):
        c = (colors or {}).get(i, INK)
        s.text(x + 8, y + 24 + i * 20, t, 14, color=c, mono=True)
    if label_top:
        s.text(x + w / 2, y - 8, label, 14, 'middle', mono=True)
    else:
        s.text(x + w / 2, y + h + 18, label, 14, 'middle', mono=True)


def figex2_1():
    s = Svg(560, 240)
    code_doc(s, 30, 20, 200, 180, 'A.h', ['#include "B.h"', '', 'class A{', '    B* m_pB;', '    …', '}'])
    code_doc(s, 330, 20, 200, 180, 'B.h', ['#include "A.h"', '', 'class B{', '    A* m_pA;', '    …', '}'])
    s.rect(24, 26, 190, 26, stroke=BLUE, sw=1.6, fill='none')
    s.rect(324, 26, 190, 26, stroke=RED, sw=1.6, fill='none')
    s.path('M214,39 L328,80', color=BLUE, arrow='ab', sw=1.6)
    s.path('M324,39 L218,80', color=RED, arrow='ar', sw=1.6)
    s.text(250, 30, '①', 15, 'middle', weight='bold')
    s.text(300, 30, '②', 15, 'middle', weight='bold')
    s.save('figex2-1')


def figex2_2():
    s = Svg(560, 420)
    code_doc(s, 40, 30, 180, 150, 'A.h', ['class B;', '', 'class A{', '    B* m_pB;', '    …', '}'],
             {0: BLUE}, label_top=True)
    code_doc(s, 340, 30, 180, 150, 'B.h', ['class A;', '', 'class B{', '    A* m_pA;', '    …', '}'],
             {0: RED}, label_top=True)
    code_doc(s, 40, 260, 180, 110, 'A.cpp', ['#include "A.h"', '#include "B.h"'])
    code_doc(s, 340, 260, 180, 110, 'B.cpp', ['#include "A.h"', '#include "B.h"'])
    s.line(130, 258, 130, 184, color=RED, arrow='ar', sw=1.6)
    s.line(430, 258, 430, 184, color=RED, arrow='ar', sw=1.6)
    s.path('M222,305 L338,120', color=BLUE, arrow='ab', sw=1.4)
    s.path('M338,280 L222,120', color=BLUE, arrow='ab', sw=1.4)
    s.save('figex2-2')


# ---------------------------------------------------------------- 応用編3日目
def figex3_1():
    s = Svg(540, 170)
    s.text(20, 92, 'add(T x, T y)', 15, mono=True)
    s.line(140, 82, 290, 34, color=RED, arrow='ar', sw=2)
    s.line(140, 92, 290, 140, color=BLUE, arrow='ab', sw=2)
    s.text(170, 46, 'add<int>', 14, color=RED, mono=True, weight='bold')
    s.text(160, 140, 'add<string>', 14, color=BLUE, mono=True, weight='bold')
    rich(s, 300, 38, [('add(', INK, False), ('int', RED, True), (' x, ', INK, False), ('int', RED, True), (' y)', INK, False)], 15, True)
    rich(s, 300, 146, [('add(', INK, False), ('string', BLUE, True), (' x, ', INK, False), ('string', BLUE, True), (' y)', INK, False)], 15, True)
    s.save('figex3-1')


def figex3_3():
    s = Svg(600, 450)
    def column(x, y, n, colored, color):
        for i in range(n):
            s.rect(x, y + i * 22, 24, 22, stroke='#666', fill=color if i in colored else '#fff', sw=1)
    s.text(40, 28, '(1) 外部からの呼び出し', 15, weight='bold')
    column(60, 50, 16, {5, 12}, CYAN)
    s.text(140, 110, '関数部分', 14, weight='bold')
    for i in range(3):
        s.rect(150, 125 + i * 22, 24, 22, stroke='#666', fill=GOLD, sw=1)
    s.circle(72, 171, 4.5, stroke=BLUE, fill=BLUE)
    s.path('M76,171 H124 V136 H146', color=BLUE, arrow='ab', sw=2)
    s.circle(162, 180, 4.5, stroke=BLUE, fill=BLUE)
    s.path('M162,184 V198 H118 V194 H90', color=BLUE, arrow='ab', sw=2)
    s.circle(72, 325, 5, stroke=RED, fill=RED)
    s.path('M77,325 H132 V148 H146', color=RED, arrow='ar', sw=2)
    s.circle(165, 194, 5, stroke=RED, fill=RED)
    s.path('M165,199 V345 H90', color=RED, arrow='ar', sw=2)
    s.callout(190, 280, 120, 60, ['呼び出すたびに', 'プログラムの流れ', 'が変わる'], (175, 240), 12)
    s.text(30, 428, 'プログラムのサイズは小さいが、分岐の', 13, weight='bold')
    s.text(30, 444, 'オーバーヘッドが発生', 13, weight='bold')
    s.text(360, 28, '(2) inline関数', 15, weight='bold')
    column(370, 50, 16, {5, 6, 7, 12, 13, 14}, GOLD)
    s.text(410, 165, '関数部分', 14, weight='bold')
    s.text(410, 320, '関数部分', 14, weight='bold')
    s.text(404, 230, '分岐は発生しないが、', 12, weight='bold')
    s.text(404, 248, 'プログラムのサイズは大きくなる', 12, weight='bold')
    s.callout(440, 360, 120, 46, ['関数部分が', '埋め込まれる'], (420, 340), 12)
    s.save('figex3-3')


# ---------------------------------------------------------------- 応用編4日目
def cells(s, x, y, values, red=(), size=40, gap=0, index=False):
    for i, v in enumerate(values):
        cx = x + i * (size + gap)
        s.rect(cx, y, size, size, stroke=RED if i in red else '#888', sw=2 if i in red else 1)
        s.text(cx + size / 2, y + size / 2 + 6, str(v), 17, 'middle')
        if index:
            s.text(cx + size / 2, y - 5, str(i), 11, 'middle')


def figex4_1():
    s = Svg(560, 240)
    rows = [([1], 'v1.push_back(1);'), ([1, 2], 'v1.push_back(2);'), ([1, 2, 3], 'v1.push_back(3);')]
    for r, (vals, code) in enumerate(rows):
        y = 30 + r * 70
        s.text(20, y + 26, '①②③'[r], 17)
        s.text(55, y + 26, 'v1', 17, mono=True)
        cells(s, 100, y, vals, red={len(vals) - 1}, index=True)
        s.text(330, y + 26, code, 17, mono=True)
    s.save('figex4-1')


def figex4_2():
    s = Svg(560, 240)
    rows = [([1], {0}, 'li.push_back(1);'), ([1, 2], {1}, 'li.push_back(2);'), ([3, 1, 2], {0}, 'li.push_front(3);')]
    for r, (vals, red, code) in enumerate(rows):
        y = 30 + r * 70
        s.text(20, y + 26, '①②③'[r], 17)
        s.text(55, y + 26, 'li', 17, mono=True)
        cells(s, 100, y, vals, red=red, gap=14)
        for i in range(len(vals) - 1):
            s.line(140 + i * 54, y + 20, 154 + i * 54, y + 20, color='#888')
        s.text(330, y + 26, code, 17, mono=True)
    s.save('figex4-2')


def figex4_3():
    s = Svg(520, 230)
    s.text(150, 30, '(3) li.insert(itr, 4);', 16, mono=True)
    s.text(55, 86, 'li', 17, mono=True)
    cells(s, 100, 60, [3, 4, 1, 2], red={1}, gap=14)
    for i in range(3):
        s.line(140 + i * 54, 80, 154 + i * 54, 80, color='#888')
    s.line(60, 185, 115, 104, color=RED, arrow='ar', sw=2)
    s.text(20, 210, '(1) itr = li.begin();', 16, mono=True)
    s.path('M120,104 C140,150 200,150 220,104', color=RED, arrow='ar', sw=2)
    s.text(150, 168, '(2) itr++;', 16, mono=True)
    s.text(270, 130, '※ insert は、itr が指す要素の前に挿入する', 12, color='#666')
    s.save('figex4-3')


# ---------------------------------------------------------------- 応用編5日目
def figex5_1():
    s = Svg(360, 320)
    s.text(180, 22, 'score', 14, 'middle', mono=True)
    s.circle(180, 160, 130, stroke=GRAY)
    s.rect(85, 70, 90, 190, stroke=RED, dash='2 3', fill='none', rx=10)
    s.rect(190, 70, 90, 190, stroke=RED, dash='2 3', fill='none', rx=10)
    for i, (k, v) in enumerate([('"Tom"', 100), ('"Bob"', 80), ('"Mike"', 120)]):
        y = 85 + i * 60
        s.rect(92, y, 76, 28)
        s.text(130, y + 19, k, 13, 'middle', mono=True)
        s.rect(197, y, 76, 28)
        s.text(235, y + 19, str(v), 13, 'middle', mono=True)
        s.line(168, y + 14, 195, y + 14, arrow='a')
    s.text(130, 285, 'キー', 14, 'middle', weight='bold')
    s.text(235, 285, '値', 14, 'middle', weight='bold')
    s.save('figex5-1')


def figex5_2():
    s = Svg(520, 360)
    s.text(320, 22, 'names', 14, 'middle', mono=True)
    s.circle(330, 165, 130, stroke=GRAY)
    targets = []
    for i, name in enumerate(['"Tom"', '"Bob"', '"Mike"']):
        y = 80 + i * 60
        s.rect(290, y, 84, 28)
        s.text(332, y + 19, name, 13, 'middle', mono=True)
        targets.append(y + 14)
    for i, name in enumerate(['"Tom"', '"Bob"', '"Mike"', '"Mike"']):
        y = 94 + i * 60 if i < 3 else 300
        s.text(40, y + 5, name, 13, mono=True)
        ty = targets[min(i, 2)]
        if i < 3:
            s.path(f'M100,{y} C190,{y} 200,{ty} 288,{ty}', arrow='a')
        else:
            s.path(f'M100,{y} C200,{y} 180,{ty} 288,{ty}', arrow='a')
    s.callout(390, 280, 120, 50, ['同じものは', '一つになる。'], (350, 240), 13)
    s.save('figex5-2')


def figex5_3():
    s = Svg(560, 330)
    def stack_col(x, top_fill, bottom_fill):
        for i, v in enumerate([3, 2, 1]):
            fill = top_fill if i == 0 else (bottom_fill if i == 2 else '#fff')
            s.rect(x, 110 + i * 60, 60, 60, stroke=RED if i == 0 else '#666', fill=fill, sw=2 if i == 0 else 1)
            s.text(x + 30, 147 + i * 60, str(v), 18, 'middle')
    s.text(160, 28, 'stack', 15, 'middle', weight='bold', mono=True)
    stack_col(130, CYAN, '#fff')
    s.text(30, 58, 'push()', 13, mono=True)
    s.path('M80,54 C150,50 160,70 160,106', arrow='a')
    s.text(30, 145, 'top()', 13, mono=True)
    s.line(80, 140, 128, 140, arrow='a')
    s.text(225, 145, 'pop()', 13, mono=True)
    s.line(220, 140, 192, 140, dash='2 3', arrow='a')
    s.text(420, 28, 'queue', 15, 'middle', weight='bold', mono=True)
    stack_col(390, '#fff', CYAN)
    s.text(290, 58, 'push()', 13, mono=True)
    s.path('M340,54 C410,50 420,70 420,106', arrow='a')
    s.text(300, 265, 'front()', 13, mono=True)
    s.line(355, 260, 388, 260, arrow='a')
    s.text(485, 265, 'pop()', 13, mono=True)
    s.line(480, 260, 452, 260, dash='2 3', arrow='a')
    s.save('figex5-3')


# ---------------------------------------------------------------- 応用編6日目
def chicken(s, x, y):
    s.path(f'M{x + 30},{y + 80} C{x},{y + 70} {x + 5},{y + 30} {x + 40},{y + 40} C{x + 50},{y + 10} {x + 75},{y + 10} '
           f'{x + 80},{y + 30} L{x + 95},{y + 35} L{x + 80},{y + 40} C{x + 85},{y + 75} {x + 60},{y + 85} {x + 30},{y + 80} Z',
           color='#777', fill='#fff', sw=1.5)
    s.path(f'M{x + 60},{y + 18} q4,-12 8,0 q4,-12 8,0 q4,-10 6,4', color=RED, fill=RED)
    s.path(f'M{x + 78},{y + 40} q4,10 -2,14 q-5,-4 2,-14', color=RED, fill=RED)
    s.circle(x + 70, y + 28, 2.5, stroke=INK, fill=INK)
    s.path(f'M{x + 10},{y + 50} q-15,-25 5,-30 q0,15 10,25', color='#777', fill='#fff')
    s.path(f'M{x + 40},{y + 82} v16 m-6,0 h12 M{x + 55},{y + 82} v16 m-6,0 h12', color='#e09a1e', sw=2.5)


def crow(s, x, y):
    s.path(f'M{x + 5},{y + 60} L{x + 30},{y + 50} C{x + 35},{y + 30} {x + 55},{y + 25} {x + 70},{y + 28} '
           f'C{x + 80},{y + 15} {x + 95},{y + 15} {x + 100},{y + 25} L{x + 118},{y + 30} L{x + 100},{y + 36} '
           f'C{x + 100},{y + 60} {x + 80},{y + 75} {x + 50},{y + 72} Z', color='#111', fill='#222')
    s.path(f'M{x + 100},{y + 25} L{x + 118},{y + 30} L{x + 100},{y + 36} Z', color='#d9a400', fill=GOLD)
    s.circle(x + 92, y + 26, 2.5, stroke='#fff', fill='#fff')
    s.path(f'M{x + 60},{y + 72} v18 m-6,0 h12 M{x + 72},{y + 70} v20 m-6,0 h12', color='#333', sw=2.5)


def figex6_2():
    s = Svg(480, 330)
    s.text(240, 50, '鳥', 26, 'middle', weight='bold')
    s.callout(20, 15, 160, 50, ['"鳥"はあくまでも', '抽象的な概念'], (218, 40), 12)
    s.line(225, 65, 120, 140, arrow='a')
    s.line(255, 65, 360, 140, arrow='a')
    chicken(s, 60, 150)
    crow(s, 300, 160)
    s.text(110, 275, 'ニワトリ', 13, 'middle', weight='bold')
    s.text(360, 275, 'カラス', 13, 'middle', weight='bold')
    s.callout(150, 285, 180, 40, ['ニワトリやカラスは実在する鳥'], (240, 260), 12)
    s.save('figex6-2')


ALL = [fig0_1, fig0_2, fig1_1, fig1_2, fig1_3, fig2_2, fig2_3, fig3_1, fig3_2, fig4_1, fig4_2,
       fig6_1, fig6_3, fig6_6, fig7_1, fig7_2, figex1_1, figex2_1, figex2_2, figex3_1, figex3_3,
       figex4_1, figex4_2, figex4_3, figex5_1, figex5_2, figex5_3, figex6_2]

if __name__ == '__main__':
    for f in ALL:
        f()
    print('ok', len(ALL))
