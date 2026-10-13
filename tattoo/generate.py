"""Generates the refined fine-line tattoo design as SVG."""
import base64, math, random, sys

random.seed(7)
W, H = 500, 1420
CX = 250
INK = "#141414"
out = []
defs = []


def add(s):
    out.append(s)


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def inside(poly, x, y):
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def stipple(poly, n, rmin=0.45, rmax=0.85, bias=None):
    """Dotwork shading inside polygon; bias(x,y)->0..1 keep-probability."""
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    placed = 0
    tries = 0
    dots = []
    while placed < n and tries < n * 40:
        tries += 1
        x = random.uniform(min(xs), max(xs))
        y = random.uniform(min(ys), max(ys))
        if not inside(poly, x, y):
            continue
        if bias and random.random() > bias(x, y):
            continue
        r = random.uniform(rmin, rmax)
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
        placed += 1
    add(f'<g fill="{INK}">' + "".join(dots) + "</g>")


def line(p, w=1.0, extra="", col=INK):
    add(f'<polyline points="{pts(p)}" fill="none" stroke="{col}" stroke-width="{w}" '
        f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def path(d, w=1.0, fill="none", extra=""):
    add(f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{w}" '
        f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def poly(p, w=1.0, fill="#fff", extra=""):
    add(f'<polygon points="{pts(p)}" fill="{fill}" stroke="{INK}" stroke-width="{w}" '
        f'stroke-linejoin="round" {extra}/>')


def dot(x, y, r=1.6):
    add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>')


def diamond(x, y, s=4):
    add(f'<polygon points="{x},{y-s*1.6} {x+s*0.7},{y} {x},{y+s*1.6} {x-s*0.7},{y}" fill="{INK}"/>')


def spine(y1, y2):
    add(f'<line x1="{CX}" y1="{y1}" x2="{CX}" y2="{y2}" stroke="{INK}" stroke-width="0.8"/>')


# ---------------------------------------------------------------- compass
def compass(cx, cy):
    add(f'<text x="{cx}" y="{cy-92}" text-anchor="middle" font-family="Georgia,serif" '
        f'font-size="15" fill="{INK}" letter-spacing="1">N</text>')
    dot(cx, cy - 78, 1.5)
    for k in range(8):
        a = math.radians(k * 45 - 90)
        L = 66 if k % 2 == 0 else 34
        wdt = 9 if k % 2 == 0 else 6
        tip = (cx + L * math.cos(a), cy + L * math.sin(a))
        l = (cx + wdt * math.cos(a - math.pi / 2), cy + wdt * math.sin(a - math.pi / 2))
        r = (cx + wdt * math.cos(a + math.pi / 2), cy + wdt * math.sin(a + math.pi / 2))
        c = (cx, cy)
        # half solid, half open: classic engraved compass rose
        if k % 2 == 1:
            poly([c, l, tip], 0.9, "#fff")
            poly([c, tip, r], 0.9, INK)
    for k in range(0, 8, 2):
        a = math.radians(k * 45 - 90)
        L, wdt = 66, 9
        tip = (cx + L * math.cos(a), cy + L * math.sin(a))
        l = (cx + wdt * math.cos(a - math.pi / 2), cy + wdt * math.sin(a - math.pi / 2))
        r = (cx + wdt * math.cos(a + math.pi / 2), cy + wdt * math.sin(a + math.pi / 2))
        poly([(cx, cy), l, tip], 1.0, "#fff")
        poly([(cx, cy), tip, r], 1.0, INK)
    add(f'<circle cx="{cx}" cy="{cy}" r="24" fill="none" stroke="{INK}" stroke-dasharray="0.1 3.2" stroke-linecap="round" stroke-width="1.2"/>')
    add(f'<circle cx="{cx}" cy="{cy}" r="2.2" fill="#fff" stroke="{INK}" stroke-width="0.9"/>')


compass(CX, 150)
spine(222, 236)
diamond(CX, 246, 3)
spine(256, 276)

# ---------------------------------------------------------------- sky
add(f'<circle cx="300" cy="318" r="23" fill="none" stroke="{INK}" stroke-width="1"/>')
for bx, by, s in [(330, 268, 5), (342, 262, 4), (352, 272, 3.2), (316, 276, 3)]:
    path(f"M{bx-s},{by} q{s/2},{-s*0.6} {s},0 q{s/2},{-s*0.6} {s},0", 0.9)
# a few soft cloud strokes
path("M352,300 q8,-6 16,-2 q6,-5 13,0 q4,1 6,4", 0.8)
path("M118,322 q7,-5 14,-1 q6,-4 12,1", 0.8)

# ---------------------------------------------------------------- mountains
sky = [(92, 418), (108, 402), (122, 392), (134, 376), (148, 356), (156, 364), (166, 372),
       (176, 350), (188, 328), (197, 312), (205, 300), (214, 312), (224, 322), (236, 330),
       (248, 344), (262, 354), (276, 344), (288, 334), (298, 346), (310, 356), (322, 368),
       (336, 382), (352, 398)]
poly(sky + [(352, 446), (92, 446)], 0, "#fff")
line(sky, 1.1)
faces = [
    ([(148, 356), (156, 364), (166, 372), (162, 394), (152, 420), (146, 402), (152, 380)], 110),
    ([(205, 300), (214, 312), (224, 322), (236, 330), (248, 344), (262, 354), (256, 386),
      (240, 420), (212, 432), (214, 398), (204, 362), (210, 332)], 330),
    ([(288, 334), (298, 346), (310, 356), (322, 368), (336, 382), (352, 398), (346, 422),
      (300, 432), (296, 396), (286, 366), (292, 350)], 210),
]
for f, n in faces:
    top = min(p[1] for p in f)
    stipple(f, n, bias=lambda x, y, t=top: max(0.25, 1 - (y - t) / 140))
line([(148, 356), (152, 380), (146, 402), (152, 420)], 0.8)
line([(205, 300), (210, 332), (204, 362), (214, 398), (212, 432)], 0.9)
line([(288, 334), (292, 350), (286, 366), (296, 396), (300, 432)], 0.8)
# gullies / snow lines on lit faces
for d in ["M196,318 l-6,14", "M190,336 l-8,16", "M180,356 l-5,14", "M136,384 l-6,12",
          "M276,352 l-5,12", "M228,338 l4,10", "M120,400 l-7,8"]:
    path(d, 0.7)
# foothill plain dots
stipple([(92, 418), (352, 400), (352, 446), (92, 446)], 70, 0.35, 0.6,
         bias=lambda x, y: 0.5)

# ---------------------------------------------------------------- moroccan town
# hill under the town
path("M252,506 C270,492 330,486 410,500", 0.9, "#fff")
houses = [(258, 18, 22), (276, 20, 34), (318, 22, 44), (340, 18, 30), (356, 16, 22),
          (266, 16, 14), (288, 14, 18), (330, 18, 16), (348, 14, 12)]
for i, (x, w, h) in enumerate(houses):
    base = 500 if i < 5 else 506
    poly([(x, base), (x, base - h), (x + w, base - h), (x + w, base)], 0.9, "#fff")
    # shaded right wall strip
    add(f'<rect x="{x+w-4:.1f}" y="{base-h+1:.1f}" width="3.4" height="{h-1.5:.1f}" fill="{INK}" opacity="0.85"/>')
    # small arched windows
    for wy in range(int(base - h + 6), int(base - 5), 10):
        for wx in range(int(x + 4), int(x + w - 7), 7):
            path(f"M{wx},{wy+5} v-3 a1.6,1.6 0 0 1 3.2,0 v3 z", 0.6, INK)
# minaret (Koutoubia style)
mx, mw = 300, 14
poly([(mx, 504), (mx, 410), (mx + mw, 410), (mx + mw, 504)], 1.0, "#fff")
add(f'<rect x="{mx+mw-4}" y="411" width="3.4" height="92" fill="{INK}" opacity="0.85"/>')
for my in (424, 448, 472):
    path(f"M{mx+4},{my+8} v-5 a2.5,2.5 0 0 1 5,0 v5 z", 0.7, INK)
    line([(mx, my + 13), (mx + mw, my + 13)], 0.5)
for k in range(4):  # merlons
    add(f'<rect x="{mx + k*3.8:.1f}" y="406" width="2.4" height="4" fill="{INK}"/>')
poly([(mx + 4, 406), (mx + 4, 395), (mx + 10, 395), (mx + 10, 406)], 0.9, "#fff")
path(f"M{mx+4},395 a3,3 0 0 1 6,0", 0.9)
line([(mx + 7, 392), (mx + 7, 382)], 0.8)
for by in (388, 385):
    dot(mx + 7, by, 1.1)


# palms
def palm(bx, by, tx, ty, s=1.0):
    path(f"M{bx-2},{by} Q{bx+ (tx-bx)*0.2 - 2},{(by+ty)/2} {tx-1.2},{ty}", 0.9)
    path(f"M{bx+2},{by} Q{bx+ (tx-bx)*0.2 + 2},{(by+ty)/2} {tx+1.2},{ty}", 0.9)
    for k in range(1, 12):
        t = k / 12
        x = (1 - t) ** 2 * bx + 2 * (1 - t) * t * (bx + (tx - bx) * 0.2) + t * t * tx
        y = by + (ty - by) * t
        line([(x - 1.8, y), (x + 1.8, y - 1)], 0.6)
    for ang, ln, droop in [(-170, 30, 14), (-140, 26, 10), (-105, 18, 2), (-70, 22, 6),
                           (-35, 28, 12), (0, 30, 16), (150, 20, 10), (30, 18, 12)]:
        a = math.radians(ang)
        ex, ey = tx + ln * s * math.cos(a), ty + ln * s * math.sin(a) + droop * s
        mx_, my_ = tx + ln * 0.55 * s * math.cos(a), ty + ln * 0.55 * s * math.sin(a) - 4 * s
        path(f"M{tx},{ty} Q{mx_:.1f},{my_:.1f} {ex:.1f},{ey:.1f}", 0.9)
        for k in range(2, 9):
            t = k / 9
            px = (1 - t) ** 2 * tx + 2 * (1 - t) * t * mx_ + t * t * ex
            py = (1 - t) ** 2 * ty + 2 * (1 - t) * t * my_ + t * t * ey
            leaf = (1 - t) * 7 * s + 2
            line([(px, py), (px + leaf * 0.35, py + leaf)], 0.6)
            line([(px, py), (px - leaf * 0.35, py + leaf)], 0.6)


palm(376, 500, 384, 410, 1.0)
palm(398, 504, 402, 432, 0.8)

# ---------------------------------------------------------------- shore & sea
path("M410,506 C360,512 300,512 268,522 C236,532 246,548 214,556 C196,560 188,566 196,572", 1.0)
path("M404,516 C350,522 312,522 284,530 C258,538 262,556 236,566", 0.7, extra='stroke-dasharray="6 5"')
stipple([(270, 520), (410, 508), (410, 516), (284, 530), (250, 552), (222, 560)], 80, 0.35, 0.6)
random.seed(11)
for i, y in enumerate([564, 569, 575, 582, 590, 599]):
    x = 214 + i * 3
    while x < 405:
        L = random.uniform(10, 26) + i * 3
        if x + L > 405:
            L = 405 - x
        if L > 4:
            line([(x, y), (x + L, y)], 0.7)
        x += L + random.uniform(5, 12)
# boats
for bx, by in [(262, 560), (292, 557)]:
    line([(bx, by), (bx + 7, by)], 0.8)
    poly([(bx + 3, by - 1), (bx + 3, by - 8), (bx + 7, by - 2)], 0.6, INK)

# ---------------------------------------------------------------- wave + surfer
add('<g transform="translate(0 -14)">')
path("M226,706 C262,694 294,660 318,630 C334,610 362,600 382,608 "
     "C398,615 402,634 392,645 C384,653 371,651 369,642 C368,635 375,632 380,636", 1.4, "#fff")
path("M382,608 C398,612 408,630 414,652 C416,668 412,690 410,706", 1.1)
# barrel shadow
path("M392,645 C384,653 371,651 369,642 C366,654 356,662 346,664 C370,668 392,660 398,640 Z", 0.8, INK)
# face lines following the curl
for k, (sx, ex, ey) in enumerate([(250, 360, 640), (270, 362, 652), (292, 366, 664),
                                  (316, 372, 676), (342, 382, 688)]):
    path(f"M{sx},{706} C{sx+30},{690-k*2} {ex-30},{ey+6} {ex},{ey}", 0.75)
# lip spray
for _ in range(26):
    a = random.uniform(-0.6, 1.4)
    r = random.uniform(4, 16)
    add(f'<circle cx="{392+r*math.cos(a):.1f}" cy="{612-r*math.sin(a):.1f}" r="{random.uniform(0.4,0.9):.2f}" fill="{INK}"/>')
# foam at the base
foam = ""
x = 228
while x < 412:
    s = random.uniform(4, 8)
    foam += f"M{x:.1f},{706} a{s/2:.1f},{s/2.6:.1f} 0 0 1 {s:.1f},0 "
    x += s + random.uniform(0, 2)
path(foam, 0.8)
stipple([(230, 704), (412, 696), (412, 716), (230, 716)], 90, 0.35, 0.7)
# surfer
add(f'<g transform="rotate(-18 336 686)">'
    f'<ellipse cx="336" cy="690" rx="20" ry="2.6" fill="{INK}"/></g>')
for seg in [[(325, 690), (323, 680), (333, 672)], [(345, 684), (347, 675), (336, 671)],
            [(335, 672), (340, 660)], [(340, 661), (330, 660), (323, 665)],
            [(340, 661), (349, 662), (356, 657)]]:
    line(seg, 3.6 if len(seg) == 3 and seg[0][1] > 680 else 3.0)
dot(343, 654, 3.4)
poly([(336, 658), (345, 661), (341, 674), (331, 671)], 0.6, INK)

add('</g>')
# ---------------------------------------------------------------- cliff + traveler
cliff = [(100, 644), (118, 639), (140, 642), (162, 638), (184, 641), (196, 647), (201, 662),
         (195, 674), (205, 692), (199, 708), (211, 728), (205, 748), (217, 772), (211, 796),
         (224, 820), (214, 838), (180, 846), (140, 842), (118, 826), (110, 806), (114, 780),
         (102, 752), (108, 726), (98, 702), (104, 680), (96, 662)]
poly(cliff, 1.2, "#fff")
stipple([(184, 641), (196, 647), (201, 662), (195, 674), (205, 692), (199, 708), (211, 728),
         (205, 748), (217, 772), (211, 796), (224, 820), (214, 838), (190, 840), (192, 800),
         (186, 760), (182, 720), (178, 680), (176, 650)], 260,
        bias=lambda x, y: 0.35 + 0.65 * max(0, (x - 176) / 40))
stipple([(118, 826), (140, 842), (180, 846), (214, 838), (200, 822), (150, 826)], 60)
for d in ["M120,660 l18,6 l14,-3", "M110,690 l20,8", "M150,676 l14,10 l8,-2", "M118,724 l16,4 l10,10",
          "M140,700 l10,14", "M160,740 l12,6", "M124,760 l18,10", "M150,790 l16,4 l8,8",
          "M168,712 l6,12", "M130,808 l14,6"]:
    path(d, 0.75)
# traveler, seen from behind, looking out to the sea
J = "#1f1f1f"
line([(146, 604), (145, 621), (144, 637)], 6.4)
line([(156, 604), (157, 621), (158, 637)], 6.4)
add(f'<path d="M139,640 q0,-4 5,-4 h4 q2,0 2,4 z" fill="{INK}"/>')
add(f'<path d="M154,640 q0,-4 4,-4 h4 q4,0 4,4 z" fill="{INK}"/>')
add(f'<path d="M140,606 C138,594 137,584 139,576 C143,571 157,571 162,576 C164,584 163,594 161,606 Z" fill="{J}"/>')
line([(139, 578), (135, 592), (137, 605)], 4.6)
line([(162, 578), (166, 592), (165, 605)], 4.6)
add(f'<rect x="141" y="575" width="19" height="25" rx="5" fill="{INK}" stroke="#fff" stroke-width="0.8"/>')
add(f'<path d="M144,588 h13 M145,594 h11" stroke="#fff" stroke-width="0.6"/>')
add(f'<rect x="147" y="567" width="7" height="6" fill="{INK}"/>')
add(f'<circle cx="150.5" cy="562" r="6.2" fill="{INK}"/>')
for hx, hy in [(146, 557), (150, 555), (154, 556.5), (156.5, 560), (144.5, 561)]:
    add(f'<circle cx="{hx}" cy="{hy}" r="2.3" fill="{INK}"/>')

# ---------------------------------------------------------------- airplane
add(f'<g transform="translate(372 750) rotate(-16) scale(0.9)" fill="{INK}">'
    f'<path d="M-16,0 C-10,-2.4 10,-2.4 16,-0.6 C18,0 18,1 16,1.4 C10,2.6 -10,2.6 -16,1.6 Z"/>'
    f'<path d="M-2,0 L-10,-10 L-6,-10 L6,0 Z"/><path d="M-2,1 L-8,9 L-4,9 L6,1 Z"/>'
    f'<path d="M-14,0 L-18,-6 L-15,-6 L-10,0 Z"/></g>')
path("M300,778 q24,-6 50,-18", 0.6, extra='stroke-dasharray="1 4"')

# ---------------------------------------------------------------- dubai skyline
BASE = 880
towers = [(132, 10, 48, "h"), (144, 14, 70, "v"), (160, 10, 58, "s"), (172, 15, 96, "spire"),
          (190, 12, 82, "h"), (204, 17, 118, "v"), (224, 11, 74, "s"),
          (272, 15, 112, "v"), (289, 11, 86, "h"), (302, 18, 132, "slant"), (323, 12, 98, "v"),
          (337, 15, 70, "s"), (354, 11, 56, "h"), (367, 9, 40, "v")]
for x, w, h, kind in towers:
    top = BASE - h
    if kind == "slant":
        poly([(x, BASE), (x, top + 10), (x + w, top), (x + w, BASE)], 1.0, "#fff")
        line([(x + w / 2, top + 5), (x + w / 2, top - 14)], 0.8)
    else:
        poly([(x, BASE), (x, top), (x + w, top), (x + w, BASE)], 1.0, "#fff")
    if kind == "spire":
        line([(x + w / 2, top), (x + w / 2, top - 26)], 0.9)
        poly([(x + 3, top), (x + w / 2, top - 8), (x + w - 3, top)], 0.8, "#fff")
    if kind == "s":
        add(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{INK}"/>')
        for yy in range(int(top + 6), BASE - 3, 7):
            line([(x + 2.5, yy), (x + w - 2.5, yy)], 0.6, col="#fff")
    elif kind == "v":
        for xx in range(int(x + 4), int(x + w - 2), 4):
            line([(xx, top + 4), (xx, BASE - 2)], 0.5)
        add(f'<rect x="{x+w-3.5}" y="{top+0.5 if kind!="slant" else top+5}" width="3" height="{h-1}" fill="{INK}"/>')
    elif kind == "h":
        for yy in range(int(top + 5), BASE - 2, 6):
            line([(x + 2, yy), (x + w - 2, yy)], 0.5)
    else:
        for xx in range(int(x + 4), int(x + w - 2), 4):
            line([(xx, top + 12), (xx, BASE - 2)], 0.5)

# Burj Khalifa — stepped setbacks spiralling to the spire
bk = [(238, BASE), (238, 836), (241, 836), (241, 800), (244, 800), (244, 768), (246.5, 768),
      (246.5, 744), (248.2, 744), (248.2, 724), (249.4, 724), (249.4, 712),
      (250.6, 712), (250.6, 724), (251.8, 724), (251.8, 752), (253.5, 752), (253.5, 784),
      (256, 784), (256, 818), (259, 818), (259, 850), (262, 850), (262, BASE)]
poly(bk, 1.0, "#fff")
line([(250, 712), (250, 698)], 1.0)
poly([(250, 724), (250, BASE), (262, BASE), (262, 850), (259, 850), (259, 818), (256, 818),
      (256, 784), (253.5, 784), (253.5, 752), (251.8, 752), (251.8, 724)], 0, INK)
for yy in range(840, BASE, 8):
    line([(240, yy), (248, yy)], 0.4)
# Burj Al Arab — the sail on its own island
path(f"M384,{BASE} L384,806 C400,818 408,848 406,{BASE}", 1.0, "#fff")
line([(384, 806), (384, 794)], 0.9)
line([(381, 816), (381, BASE)], 1.4)
for k, yy in enumerate((828, 846, 864)):
    path(f"M384,{yy} Q{392+k},{yy-4} {401+k*1.3},{yy-10+k*2}", 0.55)
line([(380, BASE), (408, BASE)], 1.0)
# water line + reflections
line([(122, BASE + 0.5), (412, BASE + 0.5)], 1.1)
random.seed(3)
allt = [(x, w, h) for x, w, h, _ in towers] + [(238, 24, 168), (384, 20, 72)]
for i, y in enumerate(range(BASE + 5, BASE + 56, 5)):
    fade = 1 - i / 11
    for x, w, h in allt:
        if h * 0.45 < (y - BASE):
            continue
        if random.random() > fade:
            continue
        jitter = random.uniform(-1.5, 1.5)
        line([(x + 1 + jitter, y), (x + w - 1 + jitter, y)], 0.7 if i < 4 else 0.55)
for y in (BASE + 12, BASE + 26, BASE + 42):
    line([(126 + random.uniform(0, 10), y), (150, y)], 0.5)
    line([(392, y), (412 - random.uniform(0, 10), y)], 0.5)

# ---------------------------------------------------------------- lower spine
spine(942, 958)
dot(CX, 950, 1.4)
# laptop
add(f'<rect x="211" y="964" width="78" height="50" rx="3" fill="{INK}"/>')
add(f'<rect x="215" y="968" width="70" height="42" rx="1" fill="none" stroke="#fff" stroke-width="0.6"/>')
add(f'<text x="250" y="996" text-anchor="middle" font-family="DejaVu Sans Mono,monospace" '
    f'font-size="15" font-weight="bold" fill="#fff">&lt;/&gt;</text>')
path("M198,1016 L302,1016 L309,1025 Q309,1028 305,1028 L195,1028 Q191,1028 191,1025 Z", 1.0, "#fff")
line([(240, 1016.5), (240, 1019), (260, 1019), (260, 1016.5)], 0.6)
for yy in (1021, 1024):
    line([(202, yy), (298, yy)], 0.4, 'stroke-dasharray="3 1.6"')
spine(1034, 1050)

# olive branch (peace, roots, Morocco)
path("M214,1178 C210,1146 198,1110 186,1060", 1.1)
leaves = [(212, 1162, 30, 22), (210, 1150, 150, 20), (205, 1134, 25, 24), (203, 1122, 155, 22),
          (198, 1106, 20, 22), (195, 1094, 160, 21), (191, 1078, 30, 18), (189, 1068, 150, 17),
          (186, 1058, 100, 14)]
for i, (x, y, ang, L) in enumerate(leaves):
    a = math.radians(ang + 180 if ang > 90 else ang) if False else math.radians(-ang if ang < 90 else -ang)
    ex, ey = x + L * math.cos(a), y + L * math.sin(a)
    nx, ny = -math.sin(a) * L * 0.2, math.cos(a) * L * 0.2
    m1 = (x + (ex - x) * 0.5 + nx, y + (ey - y) * 0.5 + ny)
    m2 = (x + (ex - x) * 0.5 - nx, y + (ey - y) * 0.5 - ny)
    path(f"M{x},{y} Q{m1[0]:.1f},{m1[1]:.1f} {ex:.1f},{ey:.1f} Q{m2[0]:.1f},{m2[1]:.1f} {x},{y} Z", 0.9, "#fff")
    path(f"M{x},{y} L{x+(ex-x)*0.85:.1f},{y+(ey-y)*0.85:.1f}", 0.5)
    # dotwork on one half of each leaf
    half = [(x, y), (x + (ex - x) * 0.25 + nx * 0.8, y + (ey - y) * 0.25 + ny * 0.8), m1,
            (x + (ex - x) * 0.8 + nx * 0.4, y + (ey - y) * 0.8 + ny * 0.4), (ex, ey)]
    stipple(half, 14, 0.3, 0.55)
for ox, oy in [(196, 1116), (201, 1142)]:
    add(f'<ellipse cx="{ox}" cy="{oy}" rx="3.2" ry="4.2" fill="{INK}"/>')
    add(f'<circle cx="{ox-1}" cy="{oy-1.6}" r="0.9" fill="#fff"/>')

# script lettering
add(f'<text font-family="TattooScript" font-size="17" fill="{INK}">'
    f'<tspan x="244" y="1098">Same boy,</tspan>'
    f'<tspan x="252" y="1132">bigger dreams</tspan></text>')

# hourglass (time)
spine(1186, 1196)
hx, hy = CX, 1226
add(f'<rect x="{hx-14}" y="{hy-30}" width="28" height="3.4" rx="1" fill="{INK}"/>')
add(f'<rect x="{hx-14}" y="{hy+26.6}" width="28" height="3.4" rx="1" fill="{INK}"/>')
line([(hx - 11, hy - 26.6), (hx - 11, hy + 26.6)], 0.9)
line([(hx + 11, hy - 26.6), (hx + 11, hy + 26.6)], 0.9)
path(f"M{hx-8},{hy-26.6} C{hx-8},{hy-10} {hx-1.5},{hy-4} {hx-1.5},{hy} C{hx-1.5},{hy+4} {hx-8},{hy+10} {hx-8},{hy+26.6}", 0.9)
path(f"M{hx+8},{hy-26.6} C{hx+8},{hy-10} {hx+1.5},{hy-4} {hx+1.5},{hy} C{hx+1.5},{hy+4} {hx+8},{hy+10} {hx+8},{hy+26.6}", 0.9)
path(f"M{hx-5.2},{hy-12} Q{hx},{hy-14} {hx+5.2},{hy-12} C{hx+3},{hy-6} {hx+1},{hy-3} {hx},{hy-1} C{hx-1},{hy-3} {hx-3},{hy-6} {hx-5.2},{hy-12} Z", 0, INK)
line([(hx, hy), (hx, hy + 18)], 0.5)
path(f"M{hx-7.6},{hy+26} Q{hx},{hy+12} {hx+7.6},{hy+26} Z", 0, INK)
spine(1260, 1270)

# Moroccan star (interlaced pentagram, as on the flag)
sx, sy, R = CX, 1298, 24
star = []
for k in range(5):
    a = math.radians(-90 + k * 144)
    star.append((sx + R * math.cos(a), sy + R * math.sin(a)))
add(f'<polygon points="{pts(star)}" fill="none" stroke="{INK}" stroke-width="4.6" stroke-linejoin="miter"/>')
add(f'<polygon points="{pts(star)}" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="miter"/>')

spine(1330, 1342)
dot(CX, 1350, 1.4)
diamond(CX, 1366, 2.6)
dot(CX, 1382, 1.1)

font = base64.b64encode(open(sys.argv[1], "rb").read()).decode()
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W*2}" height="{H*2}">'
       f'<defs><style>@font-face{{font-family:"TattooScript";src:url(data:font/woff2;base64,{font}) format("woff2");}}</style></defs>'
       f'<rect width="{W}" height="{H}" fill="#fff"/>' + "".join(out) + "</svg>")
open(sys.argv[2], "w").write(svg)
print("ok", len(svg))
