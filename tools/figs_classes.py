# -*- coding: utf-8 -*-
"""サイトの図（img/fig*.svg）を生成するスクリプト その1。

共通部品（Svg クラス、ファイル・UML の描画など）と、クラス名を含む図 10 枚を定義する。
使い方は tools/README.md を参照。
"""
import os
import sys
from xml.sax.saxutils import escape

# 出力先。引数がなければ、このスクリプトから見た ../img に書き出す
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'img')

INK = '#333'
RED = '#d93025'
BLUE = '#3b5bdb'
FONT = "'Noto Sans JP','Hiragino Sans','Meiryo',sans-serif"
MONO = "'Source Code Pro','Consolas','Menlo',monospace"


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.items = w, h, []

    def add(self, s):
        self.items.append(s)

    def text(self, x, y, s, size=13, anchor='start', color=INK, weight='normal', mono=False):
        fam = MONO if mono else FONT
        self.add(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{color}" '
                 f'text-anchor="{anchor}" font-weight="{weight}" xml:space="preserve">{escape(s)}</text>')

    def rect(self, x, y, w, h, stroke=INK, fill='#fff', dash=None, sw=1.2, rx=0):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, color=INK, arrow=None, dash=None, sw=1.2):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        m = f' marker-end="url(#{arrow})"' if arrow else ''
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}{m}/>')

    def path(self, d, color=INK, arrow=None, dash=None, sw=1.2, fill='none'):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        m = f' marker-end="url(#{arrow})"' if arrow else ''
        self.add(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{da}{m}/>')

    def circle(self, cx, cy, r, dash=None, stroke='#888', fill='none'):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"{d}/>')

    def ellipse(self, cx, cy, rx, ry, stroke='#888'):
        self.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{stroke}" stroke-width="1.2"/>')

    def callout(self, x, y, w, h, lines, tip, size=12):
        """角丸の吹き出し。tip は (x, y) の指し先。"""
        tx, ty = tip
        cx = x + w / 2
        # 吹き出しの根元は、指し先に近い辺の中央付近に置く
        if ty > y + h:
            base = f'{cx - 10},{y + h} {cx + 10},{y + h}'
        elif ty < y:
            base = f'{cx - 10},{y} {cx + 10},{y}'
        elif tx < x:
            base = f'{x},{y + h / 2 - 8} {x},{y + h / 2 + 8}'
        else:
            base = f'{x + w},{y + h / 2 - 8} {x + w},{y + h / 2 + 8}'
        self.add(f'<polygon points="{base} {tx},{ty}" fill="#fff" stroke="#777" stroke-width="1"/>')
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="#777" stroke-width="1"/>')
        # 根元の線を隠す
        b = base.split()
        (x1, y1), (x2, y2) = [tuple(map(float, p.split(','))) for p in b]
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-width="2"/>')
        n = len(lines)
        for i, s in enumerate(lines):
            self.text(cx, y + h / 2 + (i - (n - 1) / 2) * (size + 3) + size * 0.35, s, size, 'middle')

    def save(self, name):
        defs = (
            '<defs>'
            f'<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
            f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>'
            f'<marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
            '<marker id="tri" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="13" markerHeight="13" orient="auto-start-reverse"><path d="M0,0 L12,6 L0,12 z" fill="#fff" stroke="#333" stroke-width="1"/></marker>'
            '</defs>')
        body = '\n'.join(self.items)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">\n'
               f'{defs}\n<rect width="100%" height="100%" fill="#fff"/>\n{body}\n</svg>\n')
        open(os.path.join(OUT, name + '.svg'), 'w', encoding='utf-8', newline='\n').write(svg)


def doc(s, x, y, w, h, label):
    """右下が折れた「ファイル」の形。"""
    f = 12
    s.path(f'M{x},{y} H{x + w} V{y + h - f} L{x + w - f},{y + h} H{x} Z', fill='#fff')
    s.path(f'M{x + w},{y + h - f} H{x + w - f} V{y + h}')
    s.text(x + 8, y + 24, label, 14, mono=True)


def uml(s, x, y, w, name, attrs, ops, row=17, size=12):
    """UML のクラス図。各区画の下端の y 座標を返す。"""
    s.rect(x, y, w, 24)
    s.text(x + w / 2, y + 17, name, 13, 'middle', weight='bold')
    y1 = y + 24
    h1 = max(1, len(attrs)) * row + 8
    s.rect(x, y1, w, h1)
    for i, a in enumerate(attrs):
        s.text(x + 8, y1 + 4 + (i + 1) * row - 4, a, size, mono=True)
    y2 = y1 + h1
    h2 = max(1, len(ops)) * row + 8
    s.rect(x, y2, w, h2)
    for i, o in enumerate(ops):
        s.text(x + 8, y2 + 4 + (i + 1) * row - 4, o, size, mono=True)
    return y2 + h2


# ---------------------------------------------------------------- 図2-1
def fig2_1():
    s = Svg(620, 330)
    doc(s, 40, 40, 110, 80, 'main.cpp')
    doc(s, 260, 40, 110, 80, 'sample.h')
    doc(s, 260, 200, 110, 80, 'sample.cpp')
    s.line(150, 80, 258, 80, arrow='a')
    s.line(315, 200, 315, 122, arrow='a')
    s.callout(420, 52, 170, 44, ['クラスSampleの定義'], (372, 80), 13)
    s.callout(420, 216, 170, 44, ['クラスSampleの実装'], (372, 240), 13)
    s.callout(30, 180, 150, 40, ['クラスSampleの利用'], (95, 122), 12)
    s.save('fig2-1')


# ---------------------------------------------------------------- 図5-1・5-2
def rat_step(s, top, title, count, ids, dashed_first=False, verb='生成'):
    """静的メンバの領域と、インスタンスの円を描く。ids は左から並べる m_id。"""
    s.text(20, top + 14, title, 14, weight='bold')
    bx, by = 20, top + 26
    s.rect(bx, by, 120, 92)
    # m_count の行と、インスタンスの m_id の行を同じ高さにそろえる（点線を水平にするため）
    s.text(bx + 8, by + 40, f'm_count = {count};', 13, color=RED, mono=True, weight='bold')
    s.text(bx + 8, by + 64, 'showNum();', 13, mono=True)
    s.text(bx + 60, by + 112, 'Rat', 13, 'middle', weight='bold', mono=True)
    s.line(160, by + 70, 230, by + 70, arrow='a')
    s.text(195, by + 60, verb, 12, 'middle')
    for i, (rid, label) in enumerate(ids):
        cx = 290 + i * 92
        cy = by + 46
        s.circle(cx, cy, 40, dash='4 3' if (dashed_first and i == 0) else None)
        s.text(cx, by - 4, label, 13, 'middle', mono=True)
        s.text(cx, cy - 6, f'm_id = {rid};', 12, 'middle', mono=True)
        s.text(cx, cy + 18, 'squeak();', 12, 'middle', mono=True)
        if i == 0:
            ly = by + 36                      # m_id・m_count の文字の中央の高さ
            lx = cx - (40 ** 2 - (cy - ly) ** 2) ** 0.5   # 円周上の点
            s.add(f'<circle cx="{lx:.1f}" cy="{ly}" r="3.5" fill="{INK}"/>')
            s.line(round(lx, 1), ly, bx + 122, ly, dash='2 3', arrow='a')


def fig5_1():
    s = Svg(560, 470)
    rat_step(s, 10, '① r1 = new Rat();', 1, [(0, 'r1')])
    rat_step(s, 165, '② r2 = new Rat();', 2, [(1, 'r2'), (0, 'r1')])
    rat_step(s, 320, '③ r3 = new Rat();', 3, [(2, 'r3'), (1, 'r2'), (0, 'r1')])
    s.save('fig5-1')


def fig5_2():
    s = Svg(560, 470)
    rat_step(s, 10, '④ delete r1;', 2, [(0, 'r1'), (1, 'r2'), (2, 'r3')], True, '消去')
    rat_step(s, 165, '⑤ delete r2;', 1, [(1, 'r2'), (2, 'r3')], True, '消去')
    rat_step(s, 320, '⑥ delete r3;', 0, [(2, 'r3')], True, '消去')
    s.save('fig5-2')


# ---------------------------------------------------------------- 図6-2
def fig6_2():
    s = Svg(560, 400)
    s.rect(20, 20, 110, 320, fill='#fafafa')
    s.line(75, 70, 75, 300, dash='10 8', arrow='a')
    s.text(75, 365, 'プログラム', 13, 'middle', weight='bold')
    s.circle(330, 205, 150)
    s.text(185, 38, 'クラス名：Ambulance', 13, weight='bold')
    s.text(185, 56, 'インスタンス', 13, weight='bold')
    boxes = [(102, 'Car()', 'コンストラクタ（親）'), (150, 'Ambulance()', 'コンストラクタ（子）'),
             (240, '~Ambulance()', 'デストラクタ（子）'), (290, '~Car()', 'デストラクタ（親）')]
    for y, label, body in boxes:
        s.text(330, y - 8, label, 12, 'middle', mono=True, weight='bold')
        s.rect(255, y, 150, 28)
        s.text(330, y + 19, body, 14, 'middle')
    s.path('M405,116 C440,120 440,160 407,164', arrow='a')
    s.path('M405,254 C440,258 440,300 407,304', arrow='a')
    s.line(130, 116, 253, 116, arrow='a')
    s.text(150, 108, '生成', 13, weight='bold')
    s.line(130, 254, 253, 254, arrow='a')
    s.text(150, 246, '消去', 13, weight='bold')
    s.callout(390, 14, 160, 44, ['最初は親クラスの', 'コンストラクタが呼ばれる'], (370, 92), 11)
    s.callout(370, 345, 180, 44, ['消去の場合、親クラスの', 'デストラクタが最後に呼ばれる'], (380, 318), 11)
    s.save('fig6-2')


# ---------------------------------------------------------------- 図6-4
def fig6_4():
    s = Svg(560, 470)
    b1 = uml(s, 40, 20, 200, 'Car', ['- m_fuel : int', '- m_migration : int'],
             ['+ Car()', '+ ~Car()', '+ move() : void', '+ supply() : void'])
    top2 = b1 + 70
    uml(s, 40, top2, 200, 'Ambulance', ['- m_number : int'],
        ['+ Ambulance()', '+ ~Ambulance()', '+ savePeople() : void', '+ supply() : void'])
    s.line(140, top2, 140, b1 + 2, arrow='tri')
    s.callout(320, 30, 200, 40, ['親クラス・スーパークラス'], (242, 50), 13)
    s.callout(320, b1 + 10, 200, 40, ['継承を表す'], (146, b1 + 35), 13)
    s.callout(320, top2 + 10, 200, 40, ['子クラス・サブクラス'], (242, top2 + 30), 13)
    s.save('fig6-4')


# ---------------------------------------------------------------- 図6-5
def fig6_5():
    s = Svg(560, 340)
    s.ellipse(330, 172, 170, 160)
    s.text(330, 28, 'Position2Dクラス', 13, 'middle')
    s.ellipse(330, 150, 118, 112)
    s.text(330, 56, 'Vector2Dクラス', 13, 'middle')
    s.text(258, 86, 'publicメンバ', 12, weight='bold')
    s.rect(258, 92, 110, 44)
    s.text(266, 110, 'setValue()', 12, mono=True)
    s.text(266, 128, 'getX(), getY()', 12, mono=True)
    s.text(258, 158, 'protectedメンバ', 12, weight='bold')
    s.rect(258, 164, 110, 44)
    s.text(266, 182, 'm_x, m_y', 12, mono=True)
    s.text(266, 200, 'init()', 12, mono=True)
    # クラス外から
    s.line(120, 114, 256, 114, arrow='a')
    s.text(30, 118, 'アクセス可能', 13)
    s.line(120, 186, 256, 186, arrow='a')
    s.text(30, 190, 'アクセス不可能', 13)
    s.text(355, 194, '', 1)
    s.add(f'<path d="M186,178 l16,16 M202,178 l-16,16" stroke="{RED}" stroke-width="2.5"/>')
    s.text(50, 222, 'クラス外', 13, color=RED, weight='bold')
    # クラス内から
    s.line(440, 128, 370, 128, arrow='a')
    s.text(405, 122, 'アクセス可能', 11, 'middle')
    s.line(440, 186, 370, 186, arrow='a')
    s.text(405, 180, 'アクセス可能', 11, 'middle')
    s.text(330, 236, 'クラス内', 13, 'middle', color=RED, weight='bold')
    # サブクラス内から
    s.line(290, 268, 290, 210, arrow='a')
    s.text(290, 286, 'アクセス可能', 12, 'middle')
    s.path('M420,282 H475 V100 H370', arrow='a')
    s.text(410, 286, 'アクセス可能', 12, 'end')
    s.text(330, 318, 'サブクラス内', 13, 'middle', color=RED, weight='bold')
    s.save('fig6-5')


# ---------------------------------------------------------------- 応用編 図3-2
def figex3_2():
    s = Svg(560, 560)
    tmpl = ['class Calc{', 'private:', '    T m_n1;', '    T m_n2;', 'public:',
            '    inline void set(const T n1, const T n2);', '    inline T add() const;', '};']
    def code(y0, lines, typ=None, color=INK):
        for i, l in enumerate(lines):
            yy = y0 + i * 17
            if typ is None:
                s.text(30, yy, l, 12, mono=True)
            else:
                # T の部分を色付きで表示する
                parts = l.replace('T ', '\u0000 ').split('\u0000')
                x = 30
                out = ''
                for j, p in enumerate(parts):
                    out += f'<tspan>{escape(p)}</tspan>'
                    if j < len(parts) - 1:
                        out += f'<tspan fill="{color}" font-weight="bold">{typ}</tspan>'
                s.add(f'<text x="{x}" y="{yy}" font-family="{MONO}" font-size="12" fill="{INK}" xml:space="preserve">{out}</text>')
    code(30, tmpl)
    s.line(120, 175, 120, 238, color=RED, arrow='ar', sw=2)
    s.text(30, 212, 'Calc<int>', 13, color=RED, mono=True, weight='bold')
    code(265, tmpl, 'int', RED)
    s.path('M380,130 H520 V505 H470', color=BLUE, arrow='ab', sw=2)
    s.text(400, 212, 'Calc<string>', 13, color=BLUE, mono=True, weight='bold')
    code(415, tmpl, 'string', BLUE)
    s.save('figex3-2')


# ---------------------------------------------------------------- 応用編 図6-1
def figex6_1():
    s = Svg(460, 280)
    def box(x, y, name):
        s.rect(x, y, 110, 22)
        s.text(x + 55, y + 16, name, 13, 'middle')
        s.rect(x, y + 22, 110, 44)
        s.rect(x + 3, y + 26, 50, 18, stroke=RED, dash='2 2', fill='none')
        s.text(x + 8, y + 40, 'sing()', 12, mono=True)
        s.text(x + 8, y + 58, 'fly()', 12, mono=True)
    box(90, 120, 'Bird')
    box(320, 20, 'Crow')
    box(320, 190, 'Chicken')
    s.line(320, 75, 202, 140, arrow='tri')
    s.line(320, 225, 202, 170, arrow='tri')
    s.line(20, 155, 92, 155, color=RED, arrow='ar', sw=1.6)
    s.line(143, 152, 322, 56, color=RED, arrow='ar', dash='3 3')
    s.line(143, 158, 322, 225, color=RED, arrow='ar', dash='3 3')
    s.callout(60, 20, 100, 40, ['仮想関数'], (110, 145), 13)
    s.save('figex6-1')


# ---------------------------------------------------------------- 応用編 図6-3
def figex6_3():
    s = Svg(520, 340)
    def pair(top, sup, sub, virtual):
        s.rect(80, top, 130, 22)
        s.text(145, top + 16, sup, 13, 'middle', mono=True)
        s.rect(80, top + 22, 130, 44)
        s.text(88, top + 38, f'{sup}()', 12, mono=True)
        if virtual:
            s.add(f'<text x="88" y="{top + 58}" font-family="{MONO}" font-size="12" fill="{INK}"><tspan fill="{BLUE}" font-weight="bold">virtual</tspan> ~{sup}()</text>')
        else:
            s.text(88, top + 58, f'~{sup}()', 12, mono=True)
        s.rect(310, top, 130, 22)
        s.text(375, top + 16, sub, 13, 'middle', mono=True)
        s.rect(310, top + 22, 130, 44)
        s.text(318, top + 38, f'{sub}()', 12, mono=True)
        s.text(318, top + 58, f'~{sub}()', 12, mono=True)
        s.text(20, top - 6, 'new', 12, color=RED, weight='bold', mono=True)
        s.line(30, top, 82, top + 34, color=RED, arrow='ar', sw=1.6)
        s.line(160, top + 34, 312, top + 34, color=RED, arrow='ar', sw=1.6)
        s.text(14, top + 96, 'delete', 12, color=BLUE, weight='bold', mono=True)
        s.line(34, top + 84, 82, top + 56, color=BLUE, arrow='ab', sw=1.6)
        if virtual:
            s.line(208, top + 54, 312, top + 54, color=BLUE, arrow='ab', sw=1.6)
            s.line(312, top + 60, 212, top + 60, arrow='a')
        else:
            s.line(312, top + 54, 212, top + 54, arrow='a')
            s.rect(314, top + 46, 70, 16, stroke=BLUE, dash='2 2', fill='none')
    pair(30, 'Sup1', 'Sub1', False)
    s.callout(300, 118, 190, 34, ['virtualでなければ呼ばれない'], (340, 92), 13)
    pair(210, 'Sup2', 'Sub2', True)
    s.save('figex6-3')


# ---------------------------------------------------------------- 応用編 図6-4
def figex6_4():
    s = Svg(480, 330)
    def box(x, y, name, ops, w=100):
        s.rect(x, y, w, 22)
        s.text(x + w / 2, y + 16, name, 13, 'middle', mono=True)
        s.rect(x, y + 22, w, len(ops) * 17 + 8)
        for i, o in enumerate(ops):
            s.text(x + 8, y + 22 + (i + 1) * 17, o, 12, mono=True)
    box(50, 15, 'IInf1', ['func1()', 'func2()'])
    box(330, 15, 'IInf2', ['func3()', 'func4()'])
    box(180, 165, 'Sample', ['func1()', 'func2()', 'func3()', 'func4()'])
    s.line(230, 165, 112, 74, arrow='tri')
    s.line(230, 165, 368, 74, arrow='tri')
    s.rect(183, 190, 70, 34, stroke=BLUE, dash='2 2', fill='none')
    s.rect(183, 224, 70, 34, stroke=RED, dash='2 2', fill='none')
    s.path('M50,60 C10,120 40,205 181,207', color=BLUE, arrow='ab', dash='3 3')
    s.path('M430,60 C470,140 440,240 255,241', color=RED, arrow='ar', dash='3 3')
    s.callout(20, 250, 140, 48, ['func1()とfunc2()', 'のみアクセス可能'], (80, 200), 12)
    s.callout(320, 260, 140, 48, ['func3()とfunc4()', 'のみアクセス可能'], (380, 230), 12)
    s.save('figex6-4')


if __name__ == '__main__':
    for f in [fig2_1, fig5_1, fig5_2, fig6_2, fig6_4, fig6_5, figex3_2, figex6_1, figex6_3, figex6_4]:
        f()
    print('ok')
