#!/usr/bin/env python3
"""
Generates the animated SVGs for the KazamaNoob profile README.

Edit the CONFIG block, run:  python3 build_svgs.py
then commit the assets/ folder. No third-party services, no workflows.
"""
import html
import math
import os
import random

# ----------------------------- CONFIG ---------------------------------
SUBTITLE = "> security tooling · automation · bug bounty (learning)"

SCAN_ROWS = [
    ("SUBJECT", "Parikshit"),
    ("HANDLE", "@KazamaNoob"),
    ("ROLE", "CSE @ IIT Delhi"),
    ("STATUS", "Bug bounty hunter (learning)"),
    ("LANGUAGE", "Python · Bash"),
    ("FOCUS", "Security tooling & automation"),
    ("REPOS", "6 public"),
    ("FOLLOWERS", "1"),
    ("OS", "Kali Linux"),
    ("CONTACT", "github.com/KazamaNoob"),
]
SCAN_STATUS = "[✓] scan complete: 0 vulnerabilities found in this profile"

# (kind, text, start_seconds, type_duration)
TERMINAL = [
    ("cmd", "$ whoami", 0.5, 0.6),
    ("out", "kazama - student, builder, bug bounty hunter in training", 1.6, 0.9),
    ("cmd", "$ ls ~/tools", 3.0, 0.7),
    ("out", "web-vuln-scanner  log_shield  pw-manager  network-scanner  net-analyzer", 4.1, 1.0),
    ("cmd", "$ python3 log_shield.py --watch /var/log/auth.log", 5.6, 1.8),
    ("dim", "[*] monitoring /var/log/auth.log ...", 7.7, 0.7),
    ("warn", "[!] 5 failed logins from 192.0.2.44 -> threshold exceeded", 8.8, 1.0),
    ("ok", "[+] 192.0.2.44 blocked (IPS rule added)", 10.0, 0.8),
    ("cmd", '$ echo "authorization first. hack ethically."', 11.3, 1.6),
    ("out", "authorization first. hack ethically.", 13.2, 0.7),
]
# ----------------------------------------------------------------------

FONT = "'Courier New', Courier, monospace"
GREEN = "#00ff41"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
COLORS = {"cmd": GREEN, "out": "#e6edf3", "dim": "#8b949e", "warn": "#ffb000", "ok": "#4ade80"}


def esc(s):
    return html.escape(s, quote=True)


def f(n):
    return f"{n:.5f}".rstrip("0").rstrip(".")


def svg(w, h, body, defs="", title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img">\n<title>{esc(title)}</title>\n'
        f"<defs>{defs}</defs>\n{body}\n</svg>\n"
    )


def driver(total):
    """Invisible element whose repeating animation restarts the whole sequence."""
    return (
        f'<rect width="1" height="1" opacity="0"><animate id="loop" attributeName="x" '
        f'from="0" to="1" dur="{f(total)}s" begin="0s;loop.end"/></rect>'
    )


def typed(uid, x, y, text, size, fill, start, dur, total, weight="normal"):
    """Text revealed character by character, held until the loop restarts."""
    n = len(text)
    cw = size * 0.6
    w = n * cw
    span = total - start
    kts = [(i / n) * (dur / span) for i in range(n + 1)] + [1.0]
    vals = [i * cw for i in range(n + 1)]
    vals[-1] = w + 6
    vals.append(w + 6)
    clip = (
        f'<clipPath id="{uid}"><rect x="{f(x - 2)}" y="{f(y - size)}" width="0" height="{f(size * 1.5)}">'
        f'<animate attributeName="width" calcMode="discrete" dur="{f(span)}s" '
        f'begin="loop.begin+{f(start)}s" values="{";".join(f(v) for v in vals)}" '
        f'keyTimes="{";".join(f(k) for k in kts)}"/></rect></clipPath>'
    )
    txt = (
        f'<text x="{f(x)}" y="{f(y)}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" textLength="{f(w)}" clip-path="url(#{uid})" xml:space="preserve">{esc(text)}</text>'
    )
    return clip + txt


def fade(content, start, total, dur=0.35):
    span = total - start
    return (
        f'<g opacity="0">{content}<animate attributeName="opacity" values="0;1;1" '
        f'keyTimes="0;{f(dur / span)};1" dur="{f(span)}s" begin="loop.begin+{f(start)}s"/></g>'
    )


def blink(dur=1.0):
    return f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="{dur}s" repeatCount="indefinite"/>'


COMMON_DEFS = (
    f'<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.5" result="b"/>'
    f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
    f'<path d="M24 0H0V24" fill="none" stroke="{GREEN}" stroke-opacity=".05"/></pattern>'
)


def window(w, h, title):
    return (
        f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="12" fill="#070d09"/>'
        f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="12" fill="url(#grid)"/>'
        f'<path d="M10 22 A12 12 0 0 1 22 10 H{w - 22} A12 12 0 0 1 {w - 10} 22 V44 H10 Z" fill="#0d1a10"/>'
        f'<circle cx="32" cy="27" r="6" fill="#ff5f56"/><circle cx="52" cy="27" r="6" fill="#ffbd2e"/>'
        f'<circle cx="72" cy="27" r="6" fill="#27c93f"/>'
        f'<text x="{w // 2}" y="31" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#8fbf9a">{esc(title)}</text>'
    )


def frame_border(w, h):
    return (
        f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="12" fill="none" '
        f'stroke="{GREEN}" stroke-opacity=".6" stroke-width="1.5"/>'
    )


def scanline(w, h, y0, y1, dur=3.2, opacity=0.12):
    return (
        f'<rect x="10" y="{y0}" width="{w - 20}" height="2" fill="{GREEN}" opacity="{opacity}">'
        f'<animate attributeName="y" from="{y0}" to="{y1}" dur="{dur}s" repeatCount="indefinite"/></rect>'
    )


# ----------------------------- HEADER ---------------------------------
def build_header():
    w, h, total = 900, 240, 10
    random.seed(11)
    glyphs = "0123456789ABCDEF{}<>/\\#$%&*=+;:"
    rain = []
    for i in range(32):
        x = 14 + i * 28
        n = 14
        spans = "".join(
            f'<tspan x="{x}" dy="16" fill-opacity="{(j + 1) / n:.2f}">{esc(random.choice(glyphs))}</tspan>'
            for j in range(n)
        )
        dur = random.uniform(4.5, 9)
        begin = -random.uniform(0, 9)
        base = random.uniform(0.18, 0.5)
        rain.append(
            f'<g opacity="{base:.2f}"><text x="{x}" y="0" font-family="{FONT}" font-size="14" fill="{GREEN}">{spans}</text>'
            f'<animateTransform attributeName="transform" type="translate" from="0 -230" to="0 250" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></g>'
        )

    defs = (
        COMMON_DEFS
        + '<clipPath id="frame"><rect x="10" y="10" width="880" height="220" rx="14"/></clipPath>'
        + '<radialGradient id="vig" cx="50%" cy="50%" r="55%"><stop offset="0" stop-color="#050a07" stop-opacity=".85"/>'
        + '<stop offset="1" stop-color="#050a07" stop-opacity="0"/></radialGradient>'
    )

    def glitch(color, dx):
        kt = "0;0.55;0.56;0.58;0.60;0.62;1"
        return (
            f'<text x="450" y="122" text-anchor="middle" font-family="{FONT}" font-size="70" font-weight="bold" '
            f'fill="{color}" opacity="0">KazamaNoob'
            f'<animate attributeName="opacity" values="0;0;0.75;0;0.6;0;0" keyTimes="{kt}" dur="5s" repeatCount="indefinite"/>'
            f'<animate attributeName="x" values="450;450;{450 + dx};450;{450 - dx};450;450" keyTimes="{kt}" dur="5s" repeatCount="indefinite"/>'
            f"</text>"
        )

    sub_w = len(SUBTITLE) * 18 * 0.6
    sub_x = 450 - sub_w / 2
    body = (
        f'<rect x="10" y="10" width="880" height="220" rx="14" fill="#050a07"/>'
        f'<g clip-path="url(#frame)">{"".join(rain)}'
        f'<rect x="10" y="10" width="880" height="220" fill="url(#vig)"/>'
        f'<rect x="10" y="10" width="880" height="220" fill="url(#grid)"/>'
        + driver(total)
        + glitch("#ff0055", 5)
        + glitch("#00e5ff", -5)
        + f'<text x="450" y="122" text-anchor="middle" font-family="{FONT}" font-size="70" font-weight="bold" '
        f'fill="{GREEN}" filter="url(#glow)">KazamaNoob</text>'
        + typed("sub", sub_x, 172, SUBTITLE, 18, "#c9d1d9", 0.8, 2.4, total)
        + f'<rect x="{f(sub_x + sub_w + 4)}" y="157" width="10" height="19" fill="{GREEN}">{blink()}</rect>'
        + f'<text x="28" y="38" font-family="{FONT}" font-size="12" fill="{GREEN}" opacity=".8">[ ACCESS GRANTED ]'
        f'<animate attributeName="opacity" values=".9;.35;.9" dur="2.4s" repeatCount="indefinite"/></text>'
        + scanline(900, 240, 10, 230, 3.5, 0.18)
        + "</g>"
        + frame_border(w, h)
    )
    return svg(w, h, body, defs, "KazamaNoob animated header")


# --------------------------- PROFILE SCAN -----------------------------
def build_scan():
    w, h, total = 900, 440, 16
    cx, cy, r = 180, 222, 110

    def wedge(angle, op):
        a = math.radians(angle)
        x, y = r * math.cos(a), -r * math.sin(a)
        return f'<path d="M0 0 L{r} 0 A{r} {r} 0 0 0 {x:.2f} {y:.2f} Z" fill="{GREEN}" opacity="{op}"/>'

    radar = (
        f'<g transform="translate({cx} {cy})">'
        + "".join(f'<circle r="{rr}" fill="none" stroke="{GREEN}" stroke-opacity=".35"/>' for rr in (r, 73, 37))
        + f'<line x1="-{r}" y1="0" x2="{r}" y2="0" stroke="{GREEN}" stroke-opacity=".25"/>'
        + f'<line x1="0" y1="-{r}" x2="0" y2="{r}" stroke="{GREEN}" stroke-opacity=".25"/>'
        + "<g>"
        + wedge(50, 0.07)
        + wedge(32, 0.10)
        + wedge(16, 0.16)
        + f'<line x1="0" y1="0" x2="{r}" y2="0" stroke="{GREEN}" stroke-width="2" filter="url(#glow)"/>'
        + '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="4s" repeatCount="indefinite"/>'
        + "</g>"
    )
    blips = [(45, -40, "#ff3860"), (-60, 25, GREEN), (20, 70, GREEN), (-30, -65, "#ffb000"), (75, 30, GREEN)]
    for bx, by, col in blips:
        t = (math.degrees(math.atan2(by, bx)) % 360) / 360 * 4
        radar += (
            f'<circle cx="{bx}" cy="{by}" r="3.5" fill="{col}" opacity=".08" filter="url(#glow)">'
            f'<animate attributeName="opacity" values="1;0.08" dur="4s" begin="{t:.2f}s" repeatCount="indefinite"/></circle>'
        )
    radar += "</g>"

    radar_labels = (
        f'<text x="{cx}" y="360" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{GREEN}">SCANNING PERIMETER'
        f'<animate attributeName="opacity" values="1;.35;1" dur="1.6s" repeatCount="indefinite"/></text>'
        f'<text x="{cx}" y="380" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#6b9a78">threats: 0 | tools online: 6</text>'
    )

    body = [window(w, h, "kazama@kali: ~/profile_scan"), driver(total), radar, radar_labels]
    body.append(f'<line x1="350" y1="58" x2="350" y2="400" stroke="{GREEN}" stroke-opacity=".25" stroke-dasharray="4 5"/>')

    body.append(typed("hdr", 380, 76, "[ PROFILE SCAN ]", 18, GREEN, 0.3, 0.9, total, "bold"))
    body.append(f'<line x1="380" y1="88" x2="860" y2="88" stroke="{GREEN}" stroke-opacity=".4"/>')

    y0, step = 116, 27
    for i, (k, v) in enumerate(SCAN_ROWS):
        y = y0 + i * step
        s = 1.3 + i * 0.7
        key = f'<text x="380" y="{y}" font-family="{FONT}" font-size="14" fill="#3fa55a">{esc(k)}</text>'
        body.append(fade(key, s, total, 0.25))
        body.append(typed(f"v{i}", 520, y, v, 14, "#e6edf3", s + 0.15, 0.5, total))

    s_status = 1.3 + len(SCAN_ROWS) * 0.7 + 0.3
    body.append(typed("stat", 380, 402, SCAN_STATUS, 13, GREEN, s_status, 1.6, total, "bold"))
    cur_x = 380 + len(SCAN_STATUS) * 13 * 0.6 + 4
    body.append(fade(f'<rect x="{f(cur_x)}" y="391" width="8" height="14" fill="{GREEN}">{blink()}</rect>', s_status + 1.7, total, 0.1))

    body.append(scanline(w, h, 44, h - 12, 3.4, 0.12))
    body.append(frame_border(w, h))
    return svg(w, h, "\n".join(body), COMMON_DEFS, "Animated profile scan panel")


# ----------------------------- TERMINAL -------------------------------
def build_terminal():
    w, h, total = 900, 330, 18
    body = [window(w, h, "kazama@kali: ~/hacking"), driver(total)]
    y0, step, size = 72, 22, 13
    for i, (kind, text, start, dur) in enumerate(TERMINAL):
        body.append(typed(f"t{i}", 34, y0 + i * step, text, size, COLORS[kind], start, dur, total))
    y_last = y0 + len(TERMINAL) * step
    prompt = (
        f'<text x="34" y="{y_last}" font-family="{FONT}" font-size="{size}" fill="{GREEN}" xml:space="preserve">$ </text>'
        f'<rect x="{f(34 + 2 * size * 0.6)}" y="{y_last - 12}" width="8" height="15" fill="{GREEN}">{blink()}</rect>'
    )
    body.append(fade(prompt, 14.3, total, 0.1))
    body.append(scanline(w, h, 44, h - 12, 3.8, 0.1))
    body.append(frame_border(w, h))
    return svg(w, h, "\n".join(body), COMMON_DEFS, "Animated terminal session")


# ------------------------------ FOOTER --------------------------------
def build_footer():
    w, h = 900, 70
    text = "// stay curious · hack ethically · build from scratch"
    body = (
        f'<line x1="40" y1="22" x2="860" y2="22" stroke="{GREEN}" stroke-opacity=".35"/>'
        f'<circle cy="22" r="3.5" fill="{GREEN}" filter="url(#glow)"><animate attributeName="cx" values="40;860;40" dur="6s" repeatCount="indefinite"/></circle>'
        f'<text x="450" y="52" text-anchor="middle" font-family="{FONT}" font-size="14" fill="#6b9a78" xml:space="preserve">{esc(text)}</text>'
    )
    return svg(w, h, body, COMMON_DEFS, "Footer")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, fn in [
        ("header.svg", build_header),
        ("profile-scan.svg", build_scan),
        ("terminal.svg", build_terminal),
        ("footer.svg", build_footer),
    ]:
        with open(os.path.join(OUT_DIR, name), "w", encoding="utf-8") as fh:
            fh.write(fn())
        print("wrote", os.path.join("assets", name))
