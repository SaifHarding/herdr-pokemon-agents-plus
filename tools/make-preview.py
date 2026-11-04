#!/usr/bin/env python3
"""Draws preview.png for the pokemon-agents Herdr mod: a mock window, no real data."""
import re, subprocess, sys
from pathlib import Path

OUT = Path(sys.argv[1])
DL = Path(sys.argv[2])          # downloads (untrusted data) live here
ICONS = Path(sys.argv[3])       # the mod's cached 2x menu icons
DL.mkdir(parents=True, exist_ok=True)
PMD = "https://raw.githubusercontent.com/PMDCollab/SpriteCollab/master/sprite"

SANS = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
SANS_MED = "/usr/share/fonts/noto/NotoSans-Medium.ttf"
SANS_BOLD = "/usr/share/fonts/noto/NotoSans-Bold.ttf"
MONO = str(Path.home() / ".local/share/fonts/JetBrainsMonoNerdFont-Regular.ttf")

C = dict(page="#0e0f11", win="#16171a", edge="#2a2c31", chrome="#1b1c20", text="#e6e6e6",
         muted="#9aa0aa", dim="#5f6570", accent="#8bd5a0", working="#e0af68",
         blocked="#f7768e", done="#9ece6a", idle="#6b7089", card="#202126", hover="#2a2c33")


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"failed: {' '.join(map(str, args[:6]))}...\n{r.stderr}")
    return r.stdout.strip()


def anims(pid):
    xml = DL / f"{pid:04d}.xml"
    if not xml.exists():
        run(["curl", "-sfL", "-o", xml, f"{PMD}/{pid:04d}/AnimData.xml"])
    out = {}
    for body in re.findall(r"<Anim>([\s\S]*?)</Anim>", xml.read_text()):
        g = lambda t: (re.search(f"<{t}>([^<]*)</{t}>", body) or [None, None])[1]
        out[g("Name")] = dict(copy=g("CopyOf"), fw=int(g("FrameWidth") or 0), fh=int(g("FrameHeight") or 0))
    return out


def frame(pid, anim, row, scale=3):
    """First frame of one facing, trimmed and pixel-scaled. Returns (path, w, h)."""
    a = anims(pid)
    name = anim
    while a[name]["copy"]:
        name = a[name]["copy"]
    fw, fh = a[name]["fw"], a[name]["fh"]
    sheet = DL / f"{pid:04d}-{name}.png"
    if not sheet.exists():
        run(["curl", "-sfL", "-o", sheet, f"{PMD}/{pid:04d}/{name}-Anim.png"])
    h = int(run(["magick", "identify", "-format", "%h", sheet]))
    row = min(row, h // fh - 1)
    out = DL / f"f-{pid}-{anim}-{row}.png"
    run(["magick", sheet, "-crop", f"{fw}x{fh}+0+{row * fh}", "+repage", "-trim", "+repage",
         "-scale", f"{scale * 100}%", out])
    w, hh = map(int, run(["magick", "identify", "-format", "%w %h", out]).split())
    return out, w, hh


W, H = 1600, 960
cmd = ["magick", "-size", f"{W}x{H}", f"xc:{C['page']}"]


def text(x, y, s, size=14, color=C["text"], font=SANS, gravity=None):
    cmd.extend(["-font", font, "-pointsize", str(size), "-fill", color])
    if gravity:
        cmd.extend(["-gravity", gravity])
    cmd.extend(["-annotate", f"+{x}+{y}", s])
    if gravity:
        cmd.extend(["-gravity", "NorthWest"])


def draw(spec, fill="none", stroke="none", sw=1):
    cmd.extend(["-fill", fill, "-stroke", stroke, "-strokewidth", str(sw), "-draw", spec, "-stroke", "none"])


def place(path, x, y):
    cmd.extend(["(", str(path), ")", "-geometry", f"+{int(x)}+{int(y)}", "-composite"])


def text_w(s, size, font=SANS):
    return int(run(["magick", "-font", font, "-pointsize", str(size), f"label:{s}", "-format", "%w", "info:"]))


# ---- heading
text(56, 58, "pokemon-agents", 26, C["text"], SANS_BOLD)
text(56, 86, "A Herdr mod: every agent is a pixel-art Pokémon roaming the bottom of the window.", 15, C["muted"])

# ---- window
X0, Y0, X1, Y1 = 48, 112, 1552, 912
draw(f"roundrectangle {X0},{Y0} {X1},{Y1} 14,14", C["win"], C["edge"], 2)
# tab bar
draw(f"line {X0},{Y0 + 46} {X1},{Y0 + 46}", stroke=C["edge"])
tx = X0 + 18
for i, (name, st) in enumerate([("fix login", "working"), ("refactor api", "working"), ("write tests", "idle"),
                                 ("nightly build", "idle"), ("review PR", "blocked"), ("update docs", "done")]):
    w = text_w(name, 13) + 34
    if i == 0:
        draw(f"roundrectangle {tx},{Y0 + 10} {tx + w},{Y0 + 36} 8,8", C["hover"])
    draw(f"circle {tx + 14},{Y0 + 23} {tx + 18},{Y0 + 23}", C[st])
    text(tx + 26, Y0 + 28, name, 13, C["text"] if i == 0 else C["muted"])
    tx += w + 8

# terminal: a made-up agent session
lines = [("› ", C["accent"], "fix the session timeout on login"),
         ("", C["dim"], ""),
         ("● ", C["working"], "Reading src/auth/session.ts"),
         ("● ", C["working"], "Editing src/auth/session.ts  (+12 −4)"),
         ("● ", C["done"], "Ran tests: 48 passed"),
         ("", C["dim"], ""),
         ("● ", C["working"], "Thinking… (esc to interrupt)")]
ly = Y0 + 92
for mark, col, s in lines:
    if mark:
        text(X0 + 32, ly, mark, 15, col, MONO)
    text(X0 + 56, ly, s, 15, C["muted"] if mark != "› " else C["text"], MONO)
    ly += 30

# ---- the strip
SY = 712
draw(f"rectangle {X0 + 1},{SY} {X1 - 1},{Y1 - 14}", C["chrome"])
draw(f"roundrectangle {X0 + 1},{Y1 - 30} {X1 - 1},{Y1 - 1} 13,13", C["chrome"])
draw(f"line {X0},{SY} {X1},{SY}", stroke=C["edge"])
GROUND = 858
draw(f"line {X0 + 1},{GROUND + 6} {X1 - 1},{GROUND + 6}", stroke=C["edge"])

mons = [  # (dex, anim, row, x, tag, status, extra)
    (25, "Walk", 2, 230, "fix login", "working", "dust-left"),
    (4, "Walk", 6, 470, "refactor api", "working", "dust-right"),
    (1, "Idle", 1, 700, "write tests", "idle", None),
    (143, "Sleep", 0, 930, "nightly build", "idle", "zzz"),
    (7, "Idle", 7, 1160, "Squirtle · review PR", "blocked", "!"),
    (133, "Idle", 1, 1380, "update docs", "done", "✓"),
]
for pid, anim, row, x, tag, st, extra in mons:
    scale = 3
    path, w, h = frame(pid, anim, row, scale)
    draw(f"ellipse {x},{GROUND} {max(10, int(w * 0.36))},5 0,360", "#00000066")
    place(path, x - w // 2, GROUND + 2 - h)
    top = GROUND - h
    if extra == "zzz":
        text(x + w // 2 - 6, top + 14, "z", 13, C["muted"], SANS_MED)
        text(x + w // 2 + 4, top + 2, "Z", 16, C["muted"], SANS_MED)
        text(x + w // 2 + 18, top - 12, "z", 19, C["muted"], SANS_MED)
    elif extra in ("!", "✓"):
        col = C["blocked"] if extra == "!" else C["done"]
        draw(f"roundrectangle {x - 13},{top - 34} {x + 13},{top - 8} 9,9", col)
        font = SANS_BOLD if extra == "!" else "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
        text(x - text_w(extra, 16, font) // 2, top - 14, extra, 16, "#ffffff", font)
    elif extra and extra.startswith("dust"):
        sgn = -1 if extra == "dust-left" else 1
        for i, (dx, r) in enumerate([(w // 2 + 8, 4), (w // 2 + 20, 3), (w // 2 + 30, 2)]):
            cx = x + sgn * dx
            draw(f"circle {cx},{GROUND - 4 - i * 3} {cx + r},{GROUND - 4 - i * 3}", "#3a3d45")
    tw = text_w(tag, 13)
    draw(f"circle {x - tw // 2 - 8},{GROUND + 25} {x - tw // 2 - 4},{GROUND + 25}", C[st])
    text(x - tw // 2 + 2, GROUND + 30, tag, 13, C["text"] if st in ("blocked", "done") else C["muted"])


# ---- the picker
PX0, PY0, PX1, PY1 = 980, 150, 1516, 640
draw(f"roundrectangle {PX0 + 4},{PY0 + 8} {PX1 + 4},{PY1 + 10} 14,14", "#00000070")
draw(f"roundrectangle {PX0},{PY0} {PX1},{PY1} 14,14", C["card"], C["edge"], 2)
text(PX0 + 24, PY0 + 40, "Choose a Pokémon", 19, C["text"], SANS_MED)
text(PX0 + 24, PY0 + 64, "for review PR · now Squirtle", 13, C["muted"])
text(PX1 - 46, PY0 + 40, "Esc", 12, C["dim"])
draw(f"roundrectangle {PX0 + 24},{PY0 + 82} {PX1 - 24},{PY0 + 120} 9,9", C["win"], C["accent"], 2)
text(PX0 + 38, PY0 + 107, "Search by name or number…", 14, C["dim"])
grid = list(range(1, 13))
names = dict(enumerate(["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard",
                        "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree"], 1))
cw, ch = 122, 112
gx0, gy0 = PX0 + 24, PY0 + 138
for i, pid in enumerate(grid):
    cx, cy = gx0 + (i % 4) * cw, gy0 + (i // 4) * ch
    if pid == 7:
        draw(f"roundrectangle {cx + 2},{cy} {cx + cw - 6},{cy + ch - 6} 9,9", "#26332c", C["accent"], 2)
    place(ICONS / f"{pid}.png", cx + (cw - 4) // 2 - 40, cy + 6)
    num = f"#{pid:03d}"
    text(cx + (cw - 4) // 2 - text_w(num, 11) // 2, cy + 78, num, 11, C["dim"])
    text(cx + (cw - 4) // 2 - text_w(names[pid], 13) // 2, cy + 97, names[pid], 13, C["text"])

cmd.append(str(OUT))
run(cmd)
print(OUT)
