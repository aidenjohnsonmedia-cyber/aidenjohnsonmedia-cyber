"""Phone-first README panels: 600px wide, bigger type, fewer panels.  Run: python build/build_mobile.py"""
from build import *  # noqa: reuses helpers, sprites, font

W = 600


def title():
    H = 420
    gy = H - 40
    s = head(W, H, "Aiden Johnson. Press start.", SKY)
    s += f'<g>{px(CLOUD, 4, 40, 60)}{px(CLOUD, 4, 380, 40)}{px(CLOUD, 4, 640, 60)}{px(CLOUD, 4, 980, 40)}<animateTransform attributeName="transform" type="translate" from="0 0" to="-600 0" dur="30s" repeatCount="indefinite"/></g>'
    s += hill(120, gy, 110) + hill(480, gy, 150, "#2f8a3a")
    s += t(24, 36, "AIDEN", 12, "#fff") + t(24, 56, "HAYWIRE", 12, GOLD)
    s += px(COIN, 3, 300, 28) + t(330, 42, "x750", 12, "#fff")
    s += t(W - 24, 42, "WORLD 1-1", 12, "#fff", "end")
    s += shadow_text(W / 2, 150, "AIDEN", 44, "#fff", "#1a1a2e", 4, "middle")
    s += shadow_text(W / 2, 200, "JOHNSON", 44, "#fff", "#1a1a2e", 4, "middle")
    s += t(W / 2, 232, "FOUNDER / BUILDER / HOOPER", 12, GOLD, "middle")
    # press start button
    s += f'<rect x="180" y="262" width="300" height="52" fill="#1a1a2e"/><rect x="180" y="258" width="300" height="48" fill="#d64545"/><rect x="180" y="258" width="300" height="4" fill="#fff" opacity=".5"/>'
    s += t(330, 290, "▶ PRESS START", 14, "#fff", "middle", 'class="blink"')
    s += t(330, 330, "tap to play the level", 9, "#eaf6ff", "middle")
    s += px(BLOCK, 4, 24, gy - 152) + px(BLOCK, 4, 88, gy - 152)
    s += f'<g>{px(COIN, 4, 32, gy - 178)}<animateTransform attributeName="transform" type="translate" values="0 0;0 -40;0 0" keyTimes="0;.5;1" dur="1.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;1;0" keyTimes="0;.6;1" dur="1.4s" repeatCount="indefinite"/></g>'
    s += pipe(500, gy - 64, 64) + px(HAY_BALE, 4, 380, gy - 48)
    s += px(PLAYER_A, 4, 60, gy - 96, 'class="fa"') + px(PLAYER_B, 4, 60, gy - 96, 'class="fb"')
    s += ground_strip(W, gy, 4, anim=True)
    write("m-title.svg", s)


def card(name, world, title_, sub, lines, status, status_col, scene, border=GOLD, strip=None):
    sh = 200
    H = 20 + sh + 20 + 44 + 24 + 20 * len(lines) + 20 + (50 if strip else 0) + 20
    s = head(W, H, title_)
    s += frame(W, H, border=border)
    s += '<clipPath id="sc"><rect x="20" y="20" width="560" height="200"/></clipPath>'
    s += '<g clip-path="url(#sc)">' + scene(20, 20, 560, sh) + "</g>"
    s += '<rect x="20" y="20" width="560" height="200" fill="none" stroke="#2b2b4d" stroke-width="2"/>'
    y = 20 + sh + 20
    x = 32
    s += t(x, y + 10, world, 10, "#ff5a5a" if border != GOLD else GOLD)
    s += t(x, y + 40, title_, 22, "#fff")
    s += t(x, y + 62, sub, 10, "#86e3ff")
    yy = y + 92
    for i, ln in enumerate(lines):
        s += t(x, yy + i * 20, ln, 11, "#d8d8e8")
    yy += 20 * len(lines) + 6
    s += px(FLAG[:5], 2, x, yy - 10) + t(x + 22, yy + 2, status, 10, status_col)
    if strip:
        sy = yy + 22
        s += f'<rect x="20" y="{sy}" width="560" height="46" fill="#0f0f22" stroke="#2b2b4d" stroke-width="2"/>'
        gap = 560 / len(strip)
        for i, (v, k) in enumerate(strip):
            cxx = 20 + gap * i + gap / 2
            s += t(cxx, sy + 20, v, 12, GOLD, "middle") + t(cxx, sy + 36, k, 8, "#9fa8c8", "middle")
            if i:
                s += f'<rect x="{int(20 + gap * i)}" y="{sy + 8}" width="2" height="30" fill="#2b2b4d"/>'
    write(name, s)


def clear():
    H = 420
    gy = H - 40
    s = head(W, H, "Course clear", SKY)
    s += hill(100, gy, 100) + hill(520, gy, 120, "#2f8a3a")
    s += shadow_text(W / 2, 60, "COURSE CLEAR!", 24, "#fff", "#1a1a2e", 4, "middle")
    px0, py0, pw, ph = 100, 86, 400, 196
    s += f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="#1a1a2e" stroke="{GOLD}" stroke-width="4"/>'
    s += t(W / 2, py0 + 26, "HAYWIRE  ·  FINAL TALLY", 10, GOLD, "middle")
    s += f'<rect x="{px0 + 16}" y="{py0 + 38}" width="{pw - 32}" height="2" fill="#2b2b4d"/>'
    rows = [("SUBSCRIBERS", "750+"), ("REGIONS", "134+"), ("PRICE RECORDS", "125K+"), ("STATES", "25"), ("WEEKLY", "SINCE FEB 26")]
    for i, (k, v) in enumerate(rows):
        y = py0 + 66 + i * 26
        d = .4 + i * .5
        s += f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".05s" begin="{d}s" fill="freeze"/>' + t(px0 + 20, y, k, 10, "#fff") + t(px0 + pw - 20, y, v, 11, GOLD, "end") + "</g>"
    s += f'<rect x="50" y="{gy - 130}" width="6" height="130" fill="#8f8f8f"/><circle cx="53" cy="{gy - 134}" r="8" fill="#7be37a"/>'
    s += f'<g>{px(FLAG[:5], 4, 56, gy - 120)}<animateTransform attributeName="transform" type="translate" values="0 0;0 80" keyTimes="0;1" dur="2.5s" fill="freeze"/></g>'
    s += px(BRICK, 4, 34, gy - 32) + px(PLAYER_STAND, 4, 110, gy - 96) + px(CASTLE, 4, 500, gy - 48)
    s += ground_strip(W, gy, 4)
    write("m-clear.svg", s)


if __name__ == "__main__":
    title()
    card("m-haywire.svg", "WORLD 1-1  ·  FLAGSHIP  ·  EST. FEB 2026", "HAYWIRE", "market intelligence for the hay trade",
         ["Hay has no exchange, no futures market, and",
          "almost no price reporting. Most of it trades",
          "on handshakes.",
          "",
          "HayWire reads every USDA auction report,",
          "normalizes the grades across states, adds a",
          "producer field network, and ships one weekly",
          "price index."],
         "BOSS CLEARED  ·  PRICE OPACITY", "#7be37a", scene_hay,
         strip=[("134+", "REGIONS"), ("125K+", "PRICE RECORDS"), ("750+", "SUBSCRIBERS"), ("WEEKLY", "SINCE FEB 26")])
    card("m-oddlots.svg", "BONUS STAGE  ·  BLOOMBERG  ·  JUNE 12, 2026", "ODD LOTS", "with Joe Weisenthal and Tracy Alloway",
         ['"How a Vibecoded Newsletter Is Making the',
          'Hay Market More Transparent." A 20-year-old',
          "college student explains why nobody knows",
          "what hay costs, and what he built about it."],
         "STAGE CLEARED  ·  ON AIR", "#7be37a", scene_studio, border="#ff5a5a")
    card("m-wireintel.svg", "WORLD 1-2  ·  SYSTEMS", "WIRE INTEL", "the capture-intelligence level",
         ["AI-powered defense capture intelligence.",
          "Finds opportunities, researches them, and",
          "briefs the team before the competition",
          "hears about it."],
         "IN PROGRESS  ·  PRIVATE", "#ffd23f", scene_night)
    card("m-hooper.svg", "WORLD 1-3  ·  THE OTHER FULL-TIME JOB", "D3 HOOPER", "the basketball level",
         ["Guard for the UW-Stout Blue Devils. Two",
          "years of D2 at Jamestown before that. Runs",
          "a company between practices. Teammates",
          "with his brother."],
         "IN SEASON  ·  NO DAYS OFF", "#ffd23f", scene_gym)
    clear()
