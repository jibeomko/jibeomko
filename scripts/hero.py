# Generates assets/hero.svg. Run: python3 scripts/hero.py
from pathlib import Path

BLUE, VIOLET, TEAL = "#58a6ff", "#a371f7", "#2dd4bf"
EX = [(676, 712), (738, 764), (794, 816), (848, 912)]
ISO = {"A": [0, 1, 2, 3], "B": [0, 1, 3]}
COL = {"A": BLUE, "B": VIOLET}
out = []

# long reads: (y, isoform, 5' trim px, 3' trim px)
reads = [(72, "A", 0, 0), (81, "B", 10, 0), (90, "A", 44, 0), (99, "B", 0, 6), (108, "B", 40, 12), (117, "A", 18, 0), (126, "B", 4, 0)]
for i, (y, iso, t5, t3) in enumerate(reads):
    segs = [list(EX[k]) for k in ISO[iso]]
    start = segs[0][0] + t5
    while segs and segs[0][1] <= start:
        segs.pop(0)
    segs[0][0] = max(segs[0][0], start)
    segs[-1][1] -= t3
    c = COL[iso]
    g = [f'<line x1="{segs[0][0]}" y1="{y}" x2="{segs[-1][1]}" y2="{y}" stroke="{c}" stroke-opacity=".35"/>']
    g += [f'<rect x="{a}" y="{y - 2.5}" width="{b - a}" height="5" rx="2.5" fill="{c}" fill-opacity=".85"/>' for a, b in segs]
    out.append(f'<g class="read" style="animation-delay:{0.08 * i:.2f}s">{"".join(g)}</g>')

# collapsed isoform models with splice arcs
for j, (iso, y) in enumerate([("A", 166), ("B", 206)]):
    ks = ISO[iso]
    out.append(f'<text class="mono" x="620" y="{y + 4}" font-size="12" fill="#7d8590">iso_{iso}</text>')
    out.append(f'<line x1="{EX[ks[0]][0]}" y1="{y}" x2="{EX[ks[-1]][1]}" y2="{y}" stroke="#30363d" stroke-width="1.5"/>')
    for k in ks:
        a, b = EX[k]
        out.append(f'<rect x="{a}" y="{y - 7}" width="{b - a}" height="14" rx="3" fill="{COL[iso]}"/>')
    for k1, k2 in zip(ks, ks[1:]):
        a, b = EX[k1][1], EX[k2][0]
        c = 10 + (b - a) * 0.25
        out.append(f'<path class="arc" style="animation-delay:{0.7 + 0.3 * j:.1f}s" pathLength="1" d="M{a} {y - 7} Q{(a + b) / 2:g} {y - 7 - c:.1f} {b} {y - 7}" stroke="{COL[iso]}"/>')

# isoform usage: normal vs tumor
out.append('<text class="mono" x="700" y="236" font-size="10" fill="#6e7681">isoform usage</text>')
for y, label, fa in [(250, "condition 1", 0.78), (274, "condition 2", 0.24)]:
    w = 212
    out.append(f'<text class="mono" x="620" y="{y + 4}" font-size="11" fill="#7d8590">{label}</text>')
    out.append(f'<g class="bar"><rect x="700" y="{y - 6}" width="{w * fa:.0f}" height="12" rx="2" fill="{BLUE}"/>'
               f'<rect x="{700 + w * fa:.0f}" y="{y - 6}" width="{w * (1 - fa):.0f}" height="12" rx="2" fill="{VIOLET}"/></g>')

# arrow dry -> wet
out.append('<path d="M928 176 H958 M951 170 L958 176 L951 182" fill="none" stroke="#6e7681" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')

# gel: ladder + N + T + T
out.append('<rect x="978" y="66" width="182" height="224" rx="8" fill="#07090d" stroke="#30363d"/>')
lanes = [1004, 1046, 1088, 1130]
for x, lbl in zip(lanes, ["L", "1", "2", "2"]):
    out.append(f'<rect x="{x - 13}" y="74" width="26" height="6" rx="1" fill="#000" stroke="#30363d"/>')
    out.append(f'<text class="mono" x="{x}" y="308" font-size="11" fill="#7d8590" text-anchor="middle">{lbl}</text>')
for y in range(100, 280, 18):
    out.append(f'<rect x="{lanes[0] - 12}" y="{y}" width="24" height="2" rx="1" fill="#c9d1d9" fill-opacity=".35"/>')
BAND = {"A": (146, "#79c0ff"), "B": (200, "#d2a8ff")}
levels = {1046: (0.95, 0.18), 1088: (0.22, 0.95), 1130: (0.28, 0.9)}
for n, (x, (oa, ob)) in enumerate(levels.items()):
    for iso, o in (("A", oa), ("B", ob)):
        y, c = BAND[iso]
        out.append(f'<g class="band" style="animation-delay:{1.4 + 0.15 * n:.2f}s" opacity="{o}">'
                   f'<rect x="{x - 14}" y="{y - 1}" width="28" height="7" rx="3" fill="{c}" filter="url(#glow-band)"/>'
                   f'<rect x="{x - 13}" y="{y}" width="26" height="5" rx="2.5" fill="{c}"/></g>')
for iso, (y, c) in BAND.items():
    out.append(f'<text class="mono" x="1166" y="{y + 5}" font-size="10" fill="{c}">{iso}</text>')

art = "\n    ".join(out)

def pill(x, w, color, text):
    return (f'<rect x="{x}" y="271" width="{w}" height="26" rx="13" fill="{color}" fill-opacity=".1" stroke="{color}" stroke-opacity=".45"/>'
            f'<circle cx="{x + 14}" cy="284" r="4" fill="{color}"/>'
            f'<text x="{x + 25}" y="288.5" font-size="13" fill="#c9d1d9">{text}</text>')

pills = "\n    ".join([pill(64, 160, BLUE, "long-read analysis"), pill(234, 122, VIOLET, "tool building"), pill(366, 160, TEAL, "wet-lab validation")])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340" role="img" aria-labelledby="t d">
  <title id="t">Jibeom Ko</title>
  <desc id="d">Long-read RNA-seq and isoform analysis at KIST, Seoul. Illustration: long reads collapse into two isoforms whose usage switches between two conditions, then an RT-PCR gel shows the same switch at the bench.</desc>
  <style>
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .read {{ animation: slide .6s ease-out backwards; }}
    .arc {{ fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-dasharray: 1; animation: draw 1s ease-out backwards; }}
    .bar {{ transform-box: fill-box; transform-origin: left; animation: grow .8s 1.1s ease-out backwards; }}
    .band {{ animation: fade .7s ease-out backwards; }}
    .cursor {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes slide {{ from {{ opacity: 0; transform: translateX(-14px); }} }}
    @keyframes draw {{ from {{ stroke-dashoffset: 1; }} }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} }}
    @keyframes fade {{ from {{ opacity: 0; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#161b22"/>
    </linearGradient>
    <radialGradient id="glow" cx="880" cy="180" r="420" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#1f6feb" stop-opacity=".16"/><stop offset="1" stop-color="#1f6feb" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bar" x1="0" x2="1">
      <stop offset="0" stop-color="#58a6ff"/><stop offset=".5" stop-color="#a371f7"/><stop offset="1" stop-color="#2dd4bf"/>
    </linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#ffffff" fill-opacity=".05"/>
    </pattern>
    <filter id="glow-band" x="-50%" y="-200%" width="200%" height="500%"><feGaussianBlur stdDeviation="3"/></filter>
    <clipPath id="card"><rect width="1200" height="340" rx="16"/></clipPath>
  </defs>

  <g clip-path="url(#card)">
    <rect width="1200" height="340" fill="url(#bg)"/>
    <rect width="1200" height="340" fill="url(#dots)"/>
    <rect width="1200" height="340" fill="url(#glow)"/>
    <rect y="336" width="1200" height="4" fill="url(#bar)"/>
  </g>
  <rect x=".5" y=".5" width="1199" height="339" rx="15.5" fill="none" stroke="#30363d"/>

  <g class="sans">
    <text class="mono" x="64" y="88" font-size="14" fill="#7d8590">jibeomko@kist<tspan fill="#484f58">:</tspan><tspan fill="#58a6ff">~</tspan><tspan fill="#484f58">$</tspan> whoami <tspan class="cursor" fill="#2dd4bf">▍</tspan></text>
    <text x="63" y="140" font-size="42" font-weight="700" fill="#e6edf3" letter-spacing="-.5">Jibeom Ko</text>
    <text x="64" y="180" font-size="21" font-weight="600" fill="#c9d1d9">Long-read RNA-seq  ·  isoform analysis</text>
    <text x="64" y="208" font-size="16" fill="#8b949e">Computational &amp; experimental biologist  ·  KIST, Seoul</text>
    <text x="64" y="250" font-size="17" fill="#c9d1d9">Isoforms found in long reads, <tspan fill="#2dd4bf">then tested at the bench.</tspan></text>
    {pills}
  </g>

  <line x1="596" y1="56" x2="596" y2="296" stroke="#21262d"/>
  <text class="mono" x="620" y="50" font-size="11" fill="#6e7681">dry · long reads → isoforms</text>
  <text class="mono" x="978" y="50" font-size="11" fill="#6e7681">wet · RT-PCR</text>
  <g>
    {art}
  </g>
</svg>
'''
open(Path(__file__).resolve().parent.parent / "assets" / "hero.svg", "w").write(svg)
