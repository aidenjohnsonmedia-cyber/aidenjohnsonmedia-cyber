"""Builds every SVG panel for the README into ../assets.  Run: python build/build.py"""
import base64
import re
import pathlib
from sprites import *  # noqa

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

FONT_B64 = base64.b64encode(
    (ROOT / "fonts" / "press-start-2p-latin-400-normal.woff2").read_bytes()
).decode()

SKY = "#6fb7ff"
NIGHT = "#0f1433"
FRAME_BG = "#14142b"
GOLD = "#e7c45a"


def head(w, h, label, bg=None):
    bgrect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" shape-rendering="crispEdges">
<defs><style>
@font-face{{font-family:'PS2P';src:url(data:font/woff2;base64,{FONT_B64}) format('woff2');}}
.px{{font-family:'PS2P','Press Start 2P',monospace;}}
.blink{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}
.fa{{animation:fa .36s steps(1) infinite}}@keyframes fa{{50%{{opacity:0}}}}
.fb{{animation:fb .36s steps(1) infinite}}@keyframes fb{{0%{{opacity:0}}50%{{opacity:1}}}}
.bob{{animation:bob 1.2s ease-in-out infinite}}@keyframes bob{{50%{{transform:translateY(-6px)}}}}
.twk{{animation:tw 2s ease-in-out infinite}}@keyframes tw{{50%{{opacity:.15}}}}
</style></defs>{bgrect}'''


def t(x, y, s, size=8, fill="#fff", anchor="start", extra=""):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    cls = "px"
    m = re.search(r'class="([^"]+)"', extra)
    if m:
        cls += " " + m.group(1)
        extra = extra.replace(m.group(0), "")
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'


def shadow_text(x, y, s, size, fill="#fff", shadow="#1a1a2e", off=3, anchor="start"):
    return t(x + off, y + off, s, size, shadow, anchor) + t(x, y, s, size, fill, anchor)


def ground_strip(w, y, scale=4, anim=False):
    tw = 16 * scale
    n = w // tw + 2
    tiles = "".join(px(GROUND, scale, i * tw, 0) for i in range(n))
    a = f'<animateTransform attributeName="transform" type="translate" from="0 {y}" to="-{tw} {y}" dur=".5s" repeatCount="indefinite"/>' if anim else ""
    tr = "" if anim else f'transform="translate(0,{y})"'
    return f'<g {tr}>{tiles}{a}</g>'


def pipe(x, y, h, scale=4):
    """Green warp pipe with its top at (x, y) and total height h."""
    w = 14 * scale
    lip = 4 * scale
    return (
        f'<rect x="{x - scale}" y="{y}" width="{w + 2 * scale}" height="{lip}" fill="#2fa84f"/>'
        f'<rect x="{x - scale}" y="{y}" width="{scale}" height="{lip}" fill="#7be37a"/>'
        f'<rect x="{x + w - scale}" y="{y}" width="{2 * scale}" height="{lip}" fill="#1b6b2f"/>'
        f'<rect x="{x}" y="{y + lip}" width="{w}" height="{h - lip}" fill="#2fa84f"/>'
        f'<rect x="{x}" y="{y + lip}" width="{scale}" height="{h - lip}" fill="#7be37a"/>'
        f'<rect x="{x + w - 2 * scale}" y="{y + lip}" width="{2 * scale}" height="{h - lip}" fill="#1b6b2f"/>'
    )


def hill(cx, base, r, fill="#3f9b47"):
    return f'<path d="M{cx - r} {base} A{r} {r} 0 0 1 {cx + r} {base} Z" fill="{fill}"/>'


def frame(w, h, inner=12, border=GOLD):
    return (
        f'<rect width="{w}" height="{h}" fill="{FRAME_BG}"/>'
        f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" fill="none" stroke="{border}" stroke-width="4"/>'
        f'<rect x="{inner}" y="{inner}" width="{w - 2 * inner}" height="{h - 2 * inner}" fill="none" stroke="#2b2b4d" stroke-width="2"/>'
    )


def write(name, svg):
    (OUT / name).write_text(svg + "</svg>\n", encoding="utf-8")
    print("wrote", name)


# ---------------------------------------------------------------- header
def header():
    W, H = 900, 340
    gy = H - 32
    s = head(W, H, "Aiden Johnson, founder, builder, hooper", SKY)
    # clouds (scrolling)
    cl = "".join(px(CLOUD, 4, x, y) for x, y in [(60, 60), (320, 40), (600, 70), (800, 110), (200, 150)])
    cl2 = cl.replace('translate(', 'translate(900+')  # placeholder, replaced below
    cl_all = cl + "".join(px(CLOUD, 4, x + 900, y) for x, y in [(60, 60), (320, 40), (600, 70), (800, 110), (200, 150)])
    s += f'<g>{cl_all}<animateTransform attributeName="transform" type="translate" from="0 0" to="-900 0" dur="40s" repeatCount="indefinite"/></g>'
    # hills + bushes
    s += hill(150, gy, 90) + hill(700, gy, 140, "#2f8a3a") + hill(420, gy, 60)
    s += px(BUSH, 4, 500, gy - 24) + px(BUSH, 4, 780, gy - 24)
    # title
    s += shadow_text(300, 120, "AIDEN JOHNSON", 34, "#fff", "#1a1a2e", 4)
    s += t(300, 150, "FOUNDER / BUILDER / HOOPER", 11, GOLD)
    s += t(300, 172, "HAYWIRE AG  ·  UW-STOUT  ·  MINNESOTA", 8, "#eaf6ff")
    # HUD
    s += t(28, 34, "AIDEN", 10, "#fff") + t(28, 52, "HAYWIRE", 10, GOLD)
    s += px(COIN, 2, 300, 24) + t(322, 38, "x270", 10, "#fff")
    s += t(520, 34, "WORLD", 10, "#fff") + t(520, 52, " 1-1", 10, "#fff")
    s += t(760, 34, "TIME", 10, "#fff") + t(760, 52, " 999", 10, "#fff")
    # blocks over the player
    s += px(BLOCK, 4, 150, 196) + px(BRICK, 4, 214, 196) + px(BRICK, 4, 214, 228) + px(BLOCK, 4, 278, 196)
    # coin popping out of the first block
    s += f'<g>{px(COIN, 4, 158, 170)}<animateTransform attributeName="transform" type="translate" values="0 0;0 -44;0 0" keyTimes="0;.5;1" dur="1.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;1;0" keyTimes="0;.6;1" dur="1.4s" repeatCount="indefinite"/></g>'
    # pipe and bale on the right
    s += pipe(820, gy - 72, 72) + px(HAY_BALE, 4, 640, gy - 48)
    # crow flying
    s += f'<g>{px(CROW, 3, 0, 0)}<animateTransform attributeName="transform" type="translate" from="960 60" to="-60 90" dur="16s" repeatCount="indefinite"/></g>'
    # player running in place
    s += px(PLAYER_A, 4, 120, gy - 64, 'class="fa"') + px(PLAYER_B, 4, 120, gy - 64, 'class="fb"')
    # ground
    s += ground_strip(W, gy, 4, anim=True)
    s += t(872, gy - 12, "PRESS START", 9, "#fff", "end", 'class="blink"')
    write("header.svg", s)


# ---------------------------------------------------------------- divider
def divider():
    W, H = 900, 72
    gy = H - 24
    s = head(W, H, "")
    s += pipe(80, gy - 40, 40, 3) + pipe(760, gy - 48, 48, 3)
    s += px(BUSH, 3, 300, gy - 18) + px(HAY_BALE, 3, 480, gy - 36) + px(SQUARE_BALE, 3, 600, gy - 24)
    s += f'<g class="bob">{px(COIN, 3, 420, gy - 56)}</g>'
    s += ground_strip(W, gy, 3)
    write("divider.svg", s)


# ---------------------------------------------------------------- banners
def banner(name, label, icon=None):
    W, H = 900, 48
    s = head(W, H, label)
    s += f'<rect width="{W}" height="{H}" fill="#1a1a2e"/><rect x="3" y="3" width="{W - 6}" height="{H - 6}" fill="none" stroke="#fff" stroke-width="2"/><rect x="9" y="9" width="{W - 18}" height="{H - 18}" fill="none" stroke="{GOLD}" stroke-width="2"/>'
    s += t(28, 31, "▶", 12, GOLD, extra='class="blink"') + t(52, 31, label, 13, "#fff")
    if icon:
        s += px(icon, 2, W - 60, 12)
    write(name, s)


# ---------------------------------------------------------------- level cards
def scene_hay(x, y, w, h):
    gy = y + h - 24
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{SKY}"/>'
    s += f'<circle cx="{x + w - 40}" cy="{y + 40}" r="18" fill="#ffe66d"/>'
    s += px(CLOUD, 3, x + 20, y + 20)
    s += hill(x + 90, gy, 70) + hill(x + 230, gy, 90, "#2f8a3a")
    s += px(HAY_BALE, 3, x + 30, gy - 36) + px(HAY_BALE, 3, x + 80, gy - 36)
    s += px(SQUARE_BALE, 3, x + 170, gy - 24) + px(SQUARE_BALE, 3, x + 170, gy - 48) + px(SQUARE_BALE, 3, x + 194, gy - 24)
    s += f'<g class="bob">{px(COIN, 3, x + 130, gy - 70)}</g>'
    s += f'<g transform="translate({x},{gy})">' + "".join(px(GROUND, 3, i * 48, 0) for i in range(w // 48 + 1)) + "</g>"
    return s


def scene_night(x, y, w, h):
    gy = y + h - 24
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{NIGHT}"/>'
    for i, (sx, sy) in enumerate([(30, 30), (90, 60), (150, 25), (210, 70), (260, 40), (120, 110), (240, 120)]):
        s += f'<rect x="{x + sx}" y="{y + sy}" width="3" height="3" fill="#fff" class="twk" style="animation-delay:{i * .3}s"/>'
    s += f'<circle cx="{x + w - 50}" cy="{y + 45}" r="16" fill="#f4f1d0"/><circle cx="{x + w - 58}" cy="{y + 40}" r="14" fill="{NIGHT}"/>'
    # radar blips
    for i in range(3):
        s += f'<circle cx="{x + 150}" cy="{y + 36}" r="10" fill="none" stroke="#86e3ff" stroke-width="2" opacity="0"><animate attributeName="r" from="10" to="90" dur="3s" begin="{i}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="3s" begin="{i}s" repeatCount="indefinite"/></circle>'
    # tower with rotating dish
    tower = RADAR[5:]
    dish = RADAR[:5]
    s += px(tower, 4, x + 118, gy - 44)
    s += f'<g>{px(dish, 4, x + 118, gy - 64)}<animateTransform attributeName="transform" type="rotate" values="-25 {x + 150} {y + 40};25 {x + 150} {y + 40};-25 {x + 150} {y + 40}" dur="4s" repeatCount="indefinite"/></g>'
    s += f'<rect x="{x}" y="{gy}" width="{w}" height="24" fill="#1f2a3a"/><rect x="{x}" y="{gy}" width="{w}" height="4" fill="#2f4a5a"/>'
    return s


def scene_gym(x, y, w, h):
    gy = y + h - 24
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#3a2b5a"/>'
    s += f'<rect x="{x}" y="{gy}" width="{w}" height="24" fill="#d9a066"/>'
    for i in range(0, w, 24):
        s += f'<rect x="{x + i}" y="{gy}" width="2" height="24" fill="#b5804a"/>'
    s += f'<rect x="{x}" y="{gy + 10}" width="{w}" height="2" fill="#c4904f"/>'
    s += f'<rect x="{x + 60}" y="{y + 20}" width="120" height="40" fill="#2a1f45"/>' + t(x + 120, y + 46, "HOME 20", 9, "#ff5a5a", "middle")
    s += px(HOOP, 3, x + w - 80, gy - 110)
    s += f'<rect x="{x + w - 30}" y="{gy - 70}" width="6" height="70" fill="#8f8f8f"/>'
    s += px(PLAYER_STAND, 3, x + 40, gy - 48)
    ball = ["..OO..", ".OOOO.", "OOoOOO", "OOOoOO", ".OOOO.", "..OO.."]
    s += f'<g>{px(ball, 3, x + 88, gy - 18)}<animateTransform attributeName="transform" type="translate" values="0 0;0 -70;0 0" keyTimes="0;.5;1" calcMode="spline" keySplines=".2 .8 .4 1;.6 0 .8 .2" dur="1s" repeatCount="indefinite"/></g>'
    return s


def level(name, world, title, sub, lines, status, status_col, link, scene):
    W, H = 900, 230
    s = head(W, H, title)
    s += frame(W, H)
    s += f'<clipPath id="sc"><rect x="20" y="20" width="300" height="190"/></clipPath>'
    s += '<g clip-path="url(#sc)">' + scene(20, 20, 300, 190) + "</g>"
    s += f'<rect x="20" y="20" width="300" height="190" fill="none" stroke="#2b2b4d" stroke-width="2"/>'
    x = 352
    s += t(x, 52, world, 9, GOLD) + t(W - 28, 52, "1UP", 9, "#7be37a", "end")
    s += t(x, 86, title, 20, "#fff")
    s += t(x, 108, sub, 9, "#86e3ff")
    for i, ln in enumerate(lines):
        s += t(x, 140 + i * 16, ln, 8, "#d8d8e8")
    s += px(FLAG[:5], 2, x, 186) + t(x + 22, 198, status, 9, status_col)
    if link:
        s += t(W - 28, 198, link + " ▶", 9, "#ffd23f", "end", 'class="blink"')
    write(name, s)


# ---------------------------------------------------------------- power-ups
def powerups():
    W, H = 900, 180
    s = head(W, H, "Stack")
    s += frame(W, H)
    items = ["PYTHON", "SUPABASE", "NETLIFY", "ACTIONS", "BEEHIIV", "CLAUDE"]
    n = len(items)
    gap = (W - 80) / n
    for i, name in enumerate(items):
        bx = int(40 + gap * i + gap / 2 - 32)
        d = i * .35
        s += (
            f'<g>{px(COIN, 4, bx + 16, 60)}'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -36;0 0" keyTimes="0;.5;1" dur="1.6s" begin="{d}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.6;1" dur="1.6s" begin="{d}s" repeatCount="indefinite"/></g>'
        )
        s += (
            f'<g>{px(BLOCK, 4, bx, 68)}'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" keyTimes="0;.2;.5" dur="1.6s" begin="{d}s" repeatCount="indefinite"/></g>'
        )
        s += t(bx + 32, 158, name, 8, "#fff", "middle")
    s += t(W - 28, 40, "HIT A BLOCK", 8, "#8f8f8f", "end")
    write("powerups.svg", s)


# ---------------------------------------------------------------- world map
def worldmap():
    W, H = 900, 220
    s = head(W, H, "World map")
    s += frame(W, H)
    s += f'<rect x="20" y="20" width="{W - 40}" height="{H - 40}" fill="#3f8f3f"/>'
    for i in range(0, W, 40):
        s += f'<rect x="{20 + i}" y="20" width="2" height="{H - 40}" fill="#378237"/>'
    for j in range(0, H, 40):
        s += f'<rect x="20" y="{20 + j}" width="{W - 40}" height="2" fill="#378237"/>'
    nodes = [
        (120, "CANNON FALLS, MN", "START", "cleared"),
        (380, "JAMESTOWN, ND", "D2 · 2 YRS", "cleared"),
        (640, "MENOMONIE, WI", "UW-STOUT · D3", "here"),
        (840, "? ? ?", "LOCKED", "locked"),
    ]
    yy = 120
    s += f'<path d="M120 {yy} L380 {yy} L640 {yy} L840 {yy}" fill="none" stroke="#ffe08a" stroke-width="6" stroke-dasharray="12 10"><animate attributeName="stroke-dashoffset" from="0" to="-44" dur="1.2s" repeatCount="indefinite"/></path>'
    for x, name, sub, st in nodes:
        col = {"cleared": "#ffd23f", "here": "#fff", "locked": "#2e6b2e"}[st]
        s += f'<rect x="{x - 14}" y="{yy - 14}" width="28" height="28" fill="{col}" stroke="#1a1a2e" stroke-width="4"/>'
        s += t(x, yy + 44, name, 8, "#fff" if st != "locked" else "#9fd49f", "middle")
        s += t(x, yy + 60, sub, 7, "#ffe08a" if st != "locked" else "#9fd49f", "middle")
        if st == "cleared":
            s += px(FLAG, 2, x - 6, yy - 56)
        if st == "here":
            s += px(PLAYER_STAND, 3, x - 18, yy - 70)
            s += f'<g class="bob">{t(x, yy - 80, "YOU ARE HERE", 8, "#fff", "middle")}</g>'
    write("worldmap.svg", s)


# ---------------------------------------------------------------- course clear
def complete():
    W, H = 900, 300
    gy = H - 32
    s = head(W, H, "Course clear", SKY)
    s += hill(160, gy, 100) + hill(760, gy, 120, "#2f8a3a")
    s += shadow_text(450, 70, "COURSE CLEAR!", 22, "#fff", "#1a1a2e", 4, "middle")
    rows = [("SUBSCRIBERS", "270+"), ("MARKETS", "134+"), ("STATES", "25"), ("TIME BONUS", "999")]
    for i, (k, v) in enumerate(rows):
        y = 110 + i * 20
        s += t(330, y, k, 9, "#fff") + t(570, y, v, 9, GOLD, "end")
    # flagpole with flag sliding down
    s += f'<rect x="150" y="{gy - 180}" width="6" height="180" fill="#8f8f8f"/><circle cx="153" cy="{gy - 184}" r="8" fill="#7be37a"/>'
    s += f'<g>{px(FLAG[:5], 4, 156, gy - 170)}<animateTransform attributeName="transform" type="translate" values="0 0;0 120;0 120;0 0" keyTimes="0;.4;.9;1" dur="6s" repeatCount="indefinite"/></g>'
    s += px(BRICK, 4, 134, gy - 32)
    s += px(CASTLE, 5, 660, gy - 60)
    s += px(PLAYER_STAND, 4, 220, gy - 64)
    s += px(COIN, 3, 600, 100)
    s += ground_strip(W, gy, 4)
    write("complete.svg", s)


# ---------------------------------------------------------------- buttons + dialog
def button(name, label, col, dark):
    W, H = 260, 60
    s = head(W, H, label)
    s += f'<rect x="4" y="8" width="{W - 8}" height="{H - 8}" fill="{dark}"/><rect x="4" y="4" width="{W - 8}" height="{H - 16}" fill="{col}"/>'
    s += f'<rect x="4" y="4" width="{W - 8}" height="4" fill="#fff" opacity=".5"/>'
    s += t(W / 2, 36, label, 11, "#fff", "middle")
    write(name, s)


def dialog():
    W, H = 900, 110
    s = head(W, H, "Dialog")
    s += f'<rect x="2" y="2" width="{W - 4}" height="{H - 4}" fill="#fff" stroke="#1a1a2e" stroke-width="4"/><rect x="12" y="12" width="{W - 24}" height="{H - 24}" fill="none" stroke="#1a1a2e" stroke-width="2"/>'
    s += t(36, 50, "AIDEN wants to connect.", 12, "#1a1a2e") + t(36, 80, "What will you do?", 12, "#1a1a2e")
    s += f'<rect x="640" y="24" width="224" height="62" fill="none" stroke="#1a1a2e" stroke-width="3"/>'
    s += t(664, 50, "▶", 10, "#d64545", extra='class="blink"') + t(690, 50, "EMAIL", 11, "#1a1a2e") + t(690, 76, "VISIT SITE", 11, "#1a1a2e")
    write("dialog.svg", s)


if __name__ == "__main__":
    header()
    divider()
    banner("banner-worlds.svg", "SELECT WORLD", HAY_BALE)
    banner("banner-powerups.svg", "POWER-UPS", COIN)
    banner("banner-map.svg", "WORLD MAP", FLAG[:5])
    banner("banner-clear.svg", "COURSE CLEAR", CASTLE)
    level("level-1.svg", "WORLD 1-1  ·  FLAGSHIP", "HAYWIRE", "the hay-price level",
          ["Weekly hay market intelligence for a market with",
           "no exchange and no futures. USDA auction data from",
           "134+ markets, delivered to 270+ subscribers."],
          "CLEARED  ·  LIVE", "#7be37a", "haywireag.com", scene_hay)
    level("level-2.svg", "WORLD 1-2  ·  SYSTEMS", "WIRE INTEL", "the capture-intelligence level",
          ["AI-powered defense capture intelligence. Finds",
           "opportunities, researches them, and briefs the",
           "team before the competition hears about it."],
          "IN PROGRESS  ·  PRIVATE", "#ffd23f", "", scene_night)
    level("level-3.svg", "WORLD 1-3  ·  SIDE QUEST", "SKILLS ACADEMY", "the basketball level",
          ["D3 hooper at UW-Stout, D2 before that at",
           "Jamestown. Johnson Skills Academy trains the",
           "next class of players. Nobody misses leg day."],
          "CLEARED  ·  ACTIVE", "#7be37a", "", scene_gym)
    powerups()
    worldmap()
    complete()
    button("btn-email.svg", "EMAIL", "#d64545", "#8c1d1d")
    button("btn-site.svg", "HAYWIREAG.COM", "#2f6fd6", "#1b3f8a")
    button("btn-x.svg", "X / @aidenjohnsonn_", "#1a1a2e", "#000")
    dialog()
