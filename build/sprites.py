"""ASCII pixel-art sprites and a renderer that turns them into SVG rects.

All art here is original. Each sprite is a list of rows; characters map to
palette colors, '.' is transparent. Horizontal runs are merged into one rect.
"""

PAL = {
    # player
    "H": "#f3d26b",  # hair
    "S": "#ffcfa3",  # skin
    "E": "#1a1a1a",  # eye
    "B": "#1f4ea3",  # hoodie
    "L": "#3b6fd1",  # hoodie highlight
    "J": "#2d3f78",  # jeans
    "W": "#f4f4f4",  # shoes
    "O": "#e07a2a",  # ball
    "o": "#8a3f10",  # ball seam
    # hay
    "G": "#8a6a1e",
    "Y": "#e7c45a",
    "D": "#c9a13e",
    # blocks
    "k": "#5a3a0a",
    "g": "#f2b134",
    "l": "#ffe08a",
    "q": "#5a3a0a",
    # coin
    "c": "#ffd23f",
    "C": "#c88f00",
    # misc
    "w": "#fcfcfc",
    "a": "#a4e4fc",
    "r": "#d64545",
    "R": "#8c1d1d",
    "m": "#8f8f8f",
    "M": "#4a4a4a",
    "n": "#1a1a1a",
    "p": "#2fa84f",
    "P": "#7be37a",
    "d": "#1b6b2f",
    "t": "#d9a066",
    "T": "#8a4b2a",
    "u": "#5a2f18",
    "x": "#ff5a5a",
    "z": "#86e3ff",
}

PLAYER_A = [
    "..HHHHHH....",
    ".HHHHHHHH...",
    ".HHSSSSHH...",
    "..SSESSE....",
    "..SSSSSS....",
    "...SSSS.....",
    "..BBLBBB.O..",
    ".BBBLBBBBOO.",
    ".B.BBBB.BoO.",
    ".B.BBBB..O..",
    "...BBBB.....",
    "...JJJJ.....",
    "...JJJJ.....",
    "..JJ..JJ....",
    "..WW..WW....",
    ".WWW..WWW...",
]

PLAYER_B = [
    "..HHHHHH....",
    ".HHHHHHHH...",
    ".HHSSSSHH...",
    "..SSESSE....",
    "..SSSSSS....",
    "...SSSS.....",
    "..BBLBBB.O..",
    ".BBBLBBBBOO.",
    ".B.BBBB.BoO.",
    ".B.BBBB..O..",
    "...BBBB.....",
    "...JJJJ.....",
    "..JJJJJJ....",
    ".JJ....JJ...",
    "WW......WW..",
    "WWW.....WWW.",
]

PLAYER_STAND = [
    "..HHHHHH....",
    ".HHHHHHHH...",
    ".HHSSSSHH...",
    "..SSESSE....",
    "..SSSSSS....",
    "...SSSS.....",
    "..BBLBBB....",
    ".BBBLBBBB...",
    ".B.BBBB.B...",
    ".B.BBBB.B...",
    "...BBBB.....",
    "...JJJJ.....",
    "...JJJJ.....",
    "...JJJJ.....",
    "...WWWW.....",
    "..WWWWWW....",
]

HAY_BALE = [
    "...GGGGGGGG...",
    "..GYYYYYYYYG..",
    ".GYYYYDDYYYYG.",
    "GYYYDDYYDDYYYG",
    "GYYDYYYYYYDYYG",
    "GYDYYYDDYYYDYG",
    "GYDYYYDDYYYDYG",
    "GYYDYYYYYYDYYG",
    "GYYYDDYYDDYYYG",
    ".GYYYYDDYYYYG.",
    "..GYYYYYYYYG..",
    "...GGGGGGGG...",
]

SQUARE_BALE = [
    "GGGGGGGGGGGGGGGG",
    "GYYYYYYYYYYYYYYG",
    "GYDDDDDDDDDDDDYG",
    "GYYYYYYYYYYYYYYG",
    "GYYYYYYYYYYYYYYG",
    "GYDDDDDDDDDDDDYG",
    "GYYYYYYYYYYYYYYG",
    "GGGGGGGGGGGGGGGG",
]

BLOCK = [
    "kkkkkkkkkkkkkkkk",
    "klggggggggggggkk",
    "kggggggggggggggk",
    "kggggggkkgggggk",
    "kgggggkkkkggggk",
    "kgggggkkkkggggk",
    "kgggggkkkkggggk",
    "kgggggkkkkggggk",
    "kggggggkkgggggk",
    "kggggggkkgggggk",
    "kggggggggggggggk",
    "kggggggkkgggggk",
    "kggggggkkgggggk",
    "kggggggggggggggk",
    "kkggggggggggggkk",
    "kkkkkkkkkkkkkkkk",
]
# pad rows to 16
BLOCK = [r.ljust(16, "k") for r in BLOCK]

USED_BLOCK = [
    "kkkkkkkkkkkkkkkk",
    "kTTTTTTTTTTTTTTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTttttttttttttTk",
    "kTTTTTTTTTTTTTTk",
    "kkkkkkkkkkkkkkkk",
]

BRICK = [
    "TTTTTTTTuTTTTTTT",
    "TttttttTuTtttttT",
    "TttttttTuTtttttT",
    "uuuuuuuuuuuuuuuu",
    "TTTuTTTTTTTTuTTT",
    "TttuTtttttttuttT",
    "TttuTtttttttuttT",
    "uuuuuuuuuuuuuuuu",
]

GROUND = [
    "pPpPpPpPpPpPpPpP",
    "pppppppppppppppp",
    "ddddddddddddddd",
    "TTTTTTTTTTTTTTTT",
    "TtTTTTtTTTtTTTTT",
    "TTTTTTTTTTTTTTTT",
    "TTTtTTTTTTTTTtTT",
    "uuuuuuuuuuuuuuuu",
]
GROUND = [r.ljust(16, r[-1]) for r in GROUND]

COIN = [
    "..cccc..",
    ".cccccc.",
    "ccCCCCcc",
    "ccCccCcc",
    "ccCccCcc",
    "ccCCCCcc",
    ".cccccc.",
    "..cccc..",
]

CLOUD = [
    ".....wwww.......",
    "...wwwwwwww.....",
    "..wwwwwwwwww.ww.",
    ".wwwwwwwwwwwwwww",
    "wwwwwwwwwwwwwwww",
    "wwwwwwwwwwwwwwww",
    ".aaaaaaaaaaaaaa.",
]

BUSH = [
    ".....pp.........",
    "...pPPpp..pp....",
    "..pPPPPppPPpp...",
    ".pPPPPPPPPPPpp..",
    "pPPPPPPPPPPPPpp.",
    "ddddddddddddddd.",
]

FLAG = [
    "n.......",
    "nxxxxxx.",
    "nxxxxxxx",
    "nxxxxxx.",
    "nxxxx...",
    "n.......",
    "n.......",
    "n.......",
    "n.......",
    "n.......",
    "n.......",
    "n.......",
    "n.......",
    "n.......",
    "n.......",
    "n.......",
]

CROW = [
    "....nn....",
    "...nnnn...",
    "..nnxnnn..",
    "nnnnnnnng.",
    ".nnnnnnn..",
    "..nnnnn...",
    "...n.n....",
]

HOOP = [
    "wwwwwwwwwwwwwwwwwwww",
    "wrrrrrrrrrrrrrrrrrrw",
    "wrwwwwwwwwwwwwwwwwrw",
    "wrwwwwwwwwwwwwwwwwrw",
    "wrwwwwwwwwwwwwwwwwrw",
    "wrwwwwwrrrrrrwwwwwrw",
    "wrwwwwwrwwwwrwwwwwrw",
    "wrrrrrrrrrrrrrrrrrrw",
    "wwwwwwwwwwwwwwwwwwww",
    "......xxxxxxxx......",
    "......w.w..w.w......",
    ".......w.ww.w.......",
    ".......w.ww.w.......",
    "........w..w........",
]

RADAR = [
    "......mmmm......",
    "....mmzzzzmm....",
    "...mzzzzzzzzm...",
    "...mzzzzzzzzm...",
    "....mmzzzzmm....",
    "......mMMm......",
    ".......MM.......",
    ".......MM.......",
    "......MMMM......",
    ".....MM..MM.....",
    "....MM....MM....",
    "...MMMMMMMMMM...",
    "...MM......MM...",
    "..MM........MM..",
    "..MM........MM..",
    ".MMMMMMMMMMMMMM.",
]

CASTLE = [
    "....n.n.n.n.n....",
    "....nnnnnnnnn....",
    "....nMMMMMMMn....",
    "....nMMMnMMMn....",
    "n.n.nMMMnMMMn.n.n",
    "nnnnnnnnnnnnnnnnn",
    "nMMMMMMMMMMMMMMMn",
    "nMMMMMMnnnMMMMMMn",
    "nMMMMMnnnnnMMMMMn",
    "nMMMMMnnnnnMMMMMn",
    "nMMMMMnnnnnMMMMMn",
    "nnnnnnnnnnnnnnnnn",
]


def px(sprite, scale=4, x=0, y=0, extra_attr=""):
    """Render a sprite to an SVG <g>. Runs of identical pixels merge into one rect."""
    out = [f'<g transform="translate({x},{y})" {extra_attr}>']
    for ry, row in enumerate(sprite):
        cx = 0
        while cx < len(row):
            ch = row[cx]
            if ch == ".":
                cx += 1
                continue
            start = cx
            while cx < len(row) and row[cx] == ch:
                cx += 1
            out.append(
                f'<rect x="{start * scale}" y="{ry * scale}" width="{(cx - start) * scale}" '
                f'height="{scale}" fill="{PAL[ch]}"/>'
            )
    out.append("</g>")
    return "".join(out)


def size(sprite, scale=4):
    return len(sprite[0]) * scale, len(sprite) * scale


ARROW_UP = [
    "...cc...",
    "..cccc..",
    ".cccccc.",
    "cccccccc",
    "..cCCc..",
    "..cCCc..",
    "..cCCc..",
    "..cccc..",
]

DOC = [
    "wwwwww..",
    "wMMMMww.",
    "wwwwwwww",
    "wMMMMMMw",
    "wwwwwwww",
    "wMMMMMMw",
    "wwwwwwww",
    "wwwwwwww",
]

BUBBLE = [
    "zzzzzzzz",
    "zwwwwwwz",
    "zwnwnwnz",
    "zwwwwwwz",
    "zzzzzzzz",
    "..zz....",
    ".zz.....",
    "zz......",
]

CLOCK = [
    "..mmmm..",
    ".mwwwwm.",
    "mwwnwwwm",
    "mwwnwwwm",
    "mwwnnnwm",
    "mwwwwwwm",
    ".mwwwwm.",
    "..mmmm..",
]

MAIL = [
    "wwwwwwww",
    "wnwwwwnw",
    "wwnwwnww",
    "wwwnnwww",
    "wwnwwnww",
    "wnwwwwnw",
    "wwwwwwww",
    "........",
]

MIC = [
    "..rrrr..",
    ".rrrrrr.",
    ".rrrrrr.",
    ".rrrrrr.",
    "..rrrr..",
    "m..mm..m",
    ".mmmmmm.",
    "...mm...",
]
