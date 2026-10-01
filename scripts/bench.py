# Generates the bench schematics in assets/ (drawings only, no experimental data). Run: python3 scripts/bench.py
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
BLUE, VIOLET, AMBER, GREEN, ORANGE, RED, LINE = "#58a6ff", "#a371f7", "#f2cc60", "#2da44e", "#f0883e", "#e5534b", "#9aa5b1"


DEFS = f'''  <defs>
    <filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#1f2328" flood-opacity=".14"/></filter>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
    <radialGradient id="cellg" cx=".38" cy=".35" r=".75"><stop offset="0" stop-color="#ffe3e9"/><stop offset="1" stop-color="#f4a9b8"/></radialGradient>
    <radialGradient id="tissueg" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#f7b3b3"/><stop offset="1" stop-color="#e07c7c"/></radialGradient>
    <radialGradient id="enzg" cx=".38" cy=".35" r=".8"><stop offset="0" stop-color="#9be9a8"/><stop offset="1" stop-color="#2da44e"/></radialGradient>
    <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{LINE}"/></marker>
  </defs>
'''


def frame(name, title, desc, body):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">{desc}</desc>
{DEFS}  <rect x=".5" y=".5" width="1199" height="319" rx="15.5" fill="#ffffff" stroke="#d0d7de"/>
  <g font-family="{FONT}">
    <text x="32" y="46" font-size="17" font-weight="600" fill="#1f2328">{title}</text>
    <text x="1168" y="46" font-size="12.5" fill="#8c959f" text-anchor="end">schematic</text>
    {"".join(body)}
  </g>
</svg>
'''
    open(f"{OUT}/{name}.svg", "w").write(svg)


def arrow(x1, x2, label, y=160):
    return (f'<path d="M{x1} {y} Q{(x1 + x2) / 2} {y - 14} {x2} {y}" fill="none" stroke="{LINE}" stroke-width="2" marker-end="url(#ah)"/>'
            f'<text x="{(x1 + x2) / 2}" y="{y - 16}" font-size="12" fill="#6b7280" text-anchor="middle" font-style="italic">{label}</text>')


def steps(items):
    out = []
    for n, (cx, title, sub) in enumerate(items, 1):
        bx = round(cx + 8 - len(title) * 4.3 - 16)
        out.append(f'<circle cx="{bx}" cy="263" r="10" fill="#2f81f7"/>'
                   f'<text x="{bx}" y="267.5" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">{n}</text>'
                   f'<text x="{cx + 8}" y="268" font-size="15" font-weight="600" fill="#1f2328" text-anchor="middle">{title}</text>'
                   f'<text x="{cx}" y="290" font-size="12.5" fill="#6b7280" text-anchor="middle">{sub.replace("&", "&amp;")}</text>')
    return out


def wave(x, y, length, color, amp=2.5, period=8, width=2):
    pts = " ".join(f"{x + t:.1f},{y + amp * math.sin(2 * math.pi * t / period):.1f}" for t in range(0, length + 1))
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def tube(cx, fill):
    x0, x1 = cx - 20, cx + 20
    return (f'<g filter="url(#sh)"><rect x="{x0 - 2}" y="84" width="44" height="10" rx="3" fill="#e9eef4" stroke="{LINE}" stroke-width="1.2"/>'
            f'<path d="M{x1 + 2} 89 q12 0 12 12" fill="none" stroke="{LINE}" stroke-width="1.2"/>'
            f'<path d="M{x0} 96 H{x1} V140 C{x1} 170 {cx + 10} 196 {cx} 222 C{cx - 10} 196 {x0} 170 {x0} 140 Z" fill="#f3f6fa" stroke="{LINE}" stroke-width="1.5"/>'
            f'<path d="M{x0 + 1.5} 158 H{x1 - 1.5} C{x1 - 2} 178 {cx + 9} 199 {cx} 219 C{cx - 9} 199 {x0 + 2} 178 {x0 + 1.5} 158 Z" fill="{fill}"/></g>')


def primer(x1, x2, y, color):
    d = 1 if x2 > x1 else -1
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 4 * d}" y2="{y}" stroke="{color}" stroke-width="3.5" stroke-linecap="round"/>'
            f'<path d="M{x2} {y} L{x2 - 8 * d} {y - 5} L{x2 - 8 * d} {y + 5} Z" fill="{color}"/>')


def axes(x0, x1, y0, y1):
    return f'<path d="M{x0} {y0} V{y1} H{x1}" fill="none" stroke="#57606a" stroke-width="1.3"/>'


def cell(x, y, r=4.5):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#cellg)" stroke="#e48aa0" stroke-width=".8"/>'
            f'<circle cx="{x + .6}" cy="{y + .4}" r="{r * .4:.1f}" fill="#7b5ea7"/>')


# ---------------------------------------------------------------- isoform-specific RT-PCR
b = [tube(140, "#dbeafe")]
b += [wave(128, 172, 24, RED), wave(126, 186, 28, RED), wave(131, 200, 18, RED)]
# RNA template + cDNA + reverse transcriptase
b.append(f'<line x1="290" y1="146" x2="432" y2="146" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>')
b += [f'<line x1="{x}" y1="149" x2="{x}" y2="156" stroke="{RED}" stroke-width="2" opacity=".7"/>' for x in range(296, 430, 9)]
b.append('<line x1="340" y1="172" x2="432" y2="172" stroke="#2f81f7" stroke-width="4" stroke-linecap="round"/>')
b += [f'<line x1="{x}" y1="162" x2="{x}" y2="169" stroke="#2f81f7" stroke-width="2" opacity=".7"/>' for x in range(344, 430, 9)]
b.append('<g filter="url(#sh)"><ellipse cx="326" cy="159" rx="22" ry="19" fill="url(#enzg)" stroke="#1a7f37" stroke-width="1"/></g>'
         '<text x="326" y="163.5" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">RT</text>')
b += ['<text x="286" y="150" font-size="11" fill="#8c959f" text-anchor="end">5′</text>', '<text x="437" y="150" font-size="11" fill="#8c959f">3′</text>',
      '<text x="437" y="176" font-size="11" fill="#8c959f">5′</text>',
      f'<text x="362" y="133" font-size="11" fill="{RED}" text-anchor="middle">RNA</text>', '<text x="390" y="194" font-size="11" fill="#2f81f7" text-anchor="middle">cDNA</text>']
# isoform mRNAs with isoform-specific primers
for lab, y, ex in [("A", 128, [(520, 565, "#79c0ff"), (565, 605, AMBER), (605, 680, "#79c0ff")]), ("B", 196, [(520, 565, "#79c0ff"), (565, 640, "#79c0ff")])]:
    b.append(f'<text x="510" y="{y + 4.5}" font-size="13" font-weight="700" fill="#57606a" text-anchor="end">{lab}</text>')
    b.append('<g filter="url(#sh)">' + "".join(f'<rect x="{a}" y="{y - 9}" width="{c - a}" height="18" rx="2" fill="{col}" stroke="#ffffff" stroke-width="1"/>' for a, c, col in ex) + '</g>')
    b.append(f'<text x="{ex[-1][1] + 4}" y="{y + 3.5}" font-size="9" fill="#8c959f" font-family="ui-monospace, Menlo, Consolas, monospace">AAAA</text>')
    b.append(primer(526, 556, y - 17, ORANGE))
b += [primer(598, 572, 145, GREEN), primer(582, 550, 213, GREEN),
      f'<line x1="565" y1="185" x2="565" y2="220" stroke="{LINE}" stroke-dasharray="2 2"/>']
# agarose gel
b.append('<g filter="url(#sh)"><rect x="780" y="88" width="120" height="140" rx="6" fill="#2d333b" stroke="#1f2328"/></g>')
lanes = [798, 826, 854, 882]
b += [f'<rect x="{x - 9}" y="96" width="18" height="4" rx="1" fill="#11151a"/>' for x in lanes]
b += [f'<rect x="790" y="{y}" width="16" height="2" rx="1" fill="#e6edf3" opacity=".5"/>' for y in range(116, 222, 13)]
for x, (oa, ob) in zip(lanes[1:], [(.95, .2), (.25, .95), (.6, .6)]):
    for y, o in ((140, oa), (176, ob)):
        b.append(f'<g opacity="{o}"><rect x="{x - 10}" y="{y - 2}" width="20" height="8" rx="3" fill="#f0f6fc" filter="url(#blur)"/>'
                 f'<rect x="{x - 9}" y="{y}" width="18" height="4" rx="2" fill="#f0f6fc"/></g>')
# densitometry profile
b.append(axes(1004, 1126, 100, 212))
prof = lambda x: 78 * math.exp(-((x - 1038) / 9) ** 2) + 46 * math.exp(-((x - 1090) / 9) ** 2)
for lo, hi, col in ((1006, 1064, BLUE), (1064, 1124, VIOLET)):
    pts = " ".join(f"{x},{212 - prof(x):.1f}" for x in range(lo, hi + 1))
    b.append(f'<polygon points="{lo},212 {pts} {hi},212" fill="{col}" opacity=".35"/>')
b.append('<polyline points="' + " ".join(f"{x},{212 - prof(x):.1f}" for x in range(1006, 1125)) + '" fill="none" stroke="#57606a" stroke-width="1.6"/>')
b += [f'<text x="1038" y="126" font-size="11" font-weight="700" fill="{BLUE}" text-anchor="middle">A</text>',
      f'<text x="1090" y="158" font-size="11" font-weight="700" fill="{VIOLET}" text-anchor="middle">B</text>',
      '<text x="1065" y="227" font-size="10" fill="#8c959f" text-anchor="middle">migration →</text>']
b += [arrow(182, 280, "RT"), arrow(450, 494, "design"), arrow(700, 772, "PCR"), arrow(910, 996, "quantify")]
b += steps([(140, "RNA", "tissue or organoids"), (360, "cDNA", "reverse transcription"), (600, "Primer design", "isoform-specific, junction-spanning"),
            (840, "Agarose gel", "end-point PCR products"), (1062, "Densitometry", "isoform ratio")])
frame("rt-pcr", "Isoform-specific RT-PCR",
      "Schematic: RNA is reverse-transcribed to cDNA, isoform-specific primers (one spanning the exon-skipping junction) amplify each isoform, products run on an agarose gel and band densitometry gives the isoform ratio.", b)

# ---------------------------------------------------------------- qPCR
q = ['<path d="M140 210 C134 196 127 180 125.5 160 H154.5 C153 180 146 196 140 210 Z" fill="#56d364" opacity=".7" filter="url(#blur)"/>',
     '<g filter="url(#sh)"><path d="M122 101 Q122 84 140 84 Q158 84 158 101 Z" fill="#e9eef4" stroke="#9aa5b1" stroke-width="1.2"/>'
     '<path d="M124 103 H156 V138 C156 170 147 198 140 216 C133 198 124 170 124 138 Z" fill="#f3f6fa" stroke="#9aa5b1" stroke-width="1.5"/></g>',
     '<path d="M125.5 160 H154.5 C153 182 146 200 140 213 C134 200 127 182 125.5 160 Z" fill="#3fb950" opacity=".85"/>']
q += [f'<circle cx="{x}" cy="{y}" r="{r}" fill="#aff5b4"/>' for x, y, r in [(166, 150, 2.2), (172, 166, 1.5), (110, 172, 1.8)]]
# plate + pipette
q.append('<g filter="url(#sh)"><rect x="296" y="132" width="128" height="74" rx="6" fill="#f3f6fa" stroke="#9aa5b1" stroke-width="1.5"/></g>')
for r in range(4):
    for c in range(8):
        q.append(f'<circle cx="{308 + c * 15.5}" cy="{146 + r * 16}" r="5" fill="{"#7ee787" if c < 6 else "#e5e9ef"}" stroke="#9aa5b1" stroke-width=".6"/>')
q.append('<g filter="url(#sh)"><rect x="335" y="44" width="8" height="12" rx="2" fill="#4a90d9"/><rect x="331" y="54" width="16" height="44" rx="7" fill="#e9eef4" stroke="#9aa5b1" stroke-width="1.2"/>'
         '<path d="M333 98 L345 98 L341 112 L337 112 Z" fill="#d0d7de" stroke="#9aa5b1" stroke-width=".8"/>'
         '<path d="M337 112 L341 112 L339.6 136 L338.4 136 Z" fill="#fde68a" stroke="#e2b85a" stroke-width=".8"/></g>')
# thermocycler
q.append('<g filter="url(#sh)"><rect x="536" y="96" width="128" height="32" rx="8" fill="#d8dee6" stroke="#9aa5b1" stroke-width="1.2"/>'
         '<rect x="528" y="120" width="144" height="92" rx="10" fill="#e9eef4" stroke="#9aa5b1" stroke-width="1.5"/></g>')
q += [f'<line x1="{x}" y1="104" x2="{x}" y2="116" stroke="#b8c4d2" stroke-width="2" stroke-linecap="round"/>' for x in range(572, 632, 10)]
q.append('<rect x="544" y="138" width="78" height="42" rx="4" fill="#1f2328"/>')
prof_pts, x = [], 550
for _ in range(3):
    for t, w in ((150, 6), (164, 6), (157, 6)):
        prof_pts += [f"{x},{t}", f"{x + w},{t}"]
        x += w
q.append(f'<polyline points="{" ".join(prof_pts)}" fill="none" stroke="#7ee787" stroke-width="1.6" stroke-linejoin="round"/>')
q.append('<text x="583" y="175" font-size="10" fill="#7ee787" text-anchor="middle" font-family="ui-monospace, Menlo, Consolas, monospace">×40</text>')
q += [f'<circle cx="{x}" cy="{y}" r="5" fill="{c}"/>' for x, y, c in [(640, 150, "#4a90d9"), (656, 150, "#d0d7de"), (648, 168, "#d0d7de")]]
q += [f'<rect x="{x}" y="212" width="16" height="5" rx="2" fill="#b8c4d2"/>' for x in (540, 644)]
# amplification curves
q.append(axes(776, 904, 100, 212))
q.append(f'<line x1="778" y1="180" x2="904" y2="180" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="5 4"/>')
for ct, col in ((818, "#2dd4bf"), (842, BLUE), (866, VIOLET)):
    f = lambda x: 210 - 96 / (1 + math.exp(-(x - ct) / 6))
    q.append('<polyline points="' + " ".join(f"{x},{f(x):.1f}" for x in range(778, 905)) + f'" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round"/>')
    xc = ct - 6 * math.log(96 / 30 - 1)
    q.append(f'<line x1="{xc:.1f}" y1="180" x2="{xc:.1f}" y2="212" stroke="{col}" stroke-width="1.2" stroke-dasharray="2 2"/>')
q += [f'<text x="782" y="174" font-size="10" fill="{ORANGE}">threshold</text>',
      '<text x="840" y="227" font-size="10" fill="#8c959f" text-anchor="middle">cycle →</text>']
# relative expression
q.append(axes(1004, 1124, 100, 212))
for x, h, col, lab, dots in ((1026, 46, BLUE, "N", (-6, 4, -1)), (1078, 92, VIOLET, "T", (8, -7, 2))):
    top = 212 - h
    q.append(f'<rect x="{x}" y="{top}" width="30" height="{h}" rx="3" fill="{col}" opacity=".85"/>')
    q.append(f'<path d="M{x + 15} {top - 9} V{top + 9} M{x + 9} {top - 9} H{x + 21} M{x + 9} {top + 9} H{x + 21}" stroke="#57606a" stroke-width="1.3"/>')
    q += [f'<circle cx="{x + 8 + 7 * i}" cy="{top + 14 + d}" r="2.6" fill="#fff" stroke="#57606a" stroke-width="1"/>' for i, d in enumerate(dots)]
    q.append(f'<text x="{x + 15}" y="226" font-size="11" fill="#57606a" text-anchor="middle">{lab}</text>')
q.append('<text x="1064" y="98" font-size="10" fill="#8c959f" text-anchor="middle">relative expression</text>')
q += [arrow(176, 288, "load"), arrow(432, 520, "run"), arrow(680, 764, "read"), arrow(914, 994, "normalize")]
q += steps([(140, "Reaction mix", "cDNA · primers · master mix"), (360, "Plate setup", "technical replicates"), (600, "Thermal cycling", "denature · anneal · extend"),
            (840, "Amplification", "threshold → Ct"), (1062, "Quantification", "ΔΔCt vs reference gene")])
frame("qpcr", "qPCR",
      "Schematic: cDNA, primers and master mix are loaded into a plate, thermal-cycled, read out as amplification curves with a threshold and Ct, and normalised by delta-delta Ct.", q)

# ---------------------------------------------------------------- western blot
w = [tube(140, "#fde7ef")]
w += [f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity=".85"/>' for x, y, rx, ry, c in
      [(130, 172, 4, 3, VIOLET), (146, 168, 3, 3, ORANGE), (138, 184, 4.5, 3, "#2dd4bf"), (150, 182, 3, 2.5, BLUE), (128, 190, 3, 2.5, ORANGE), (142, 200, 3.5, 2.5, VIOLET)]]
# SDS-PAGE cassette
w.append('<g filter="url(#sh)"><rect x="304" y="84" width="112" height="144" rx="4" fill="#eef6ff" stroke="#9aa5b1" stroke-width="1.5"/></g>'
         '<rect x="312" y="100" width="96" height="120" fill="#dbe9f7"/>')
pl = [324, 342, 360, 378, 396]
w += [f'<rect x="{x - 6}" y="100" width="12" height="6" fill="#eef6ff" stroke="#b6c6d8" stroke-width=".8"/>' for x in pl]
w += [f'<rect x="{pl[0] - 6}" y="{y}" width="12" height="3" rx="1" fill="{c}"/>' for y, c in zip([116, 128, 142, 158, 176, 196], ["#2f81f7", "#2f81f7", RED, "#2f81f7", GREEN, "#2f81f7"])]
for x in pl[1:]:
    w += [f'<rect x="{x - 6}" y="{y}" width="12" height="3" rx="1" fill="#2f81f7" opacity="{o}"/>' for y, o in [(122, .3), (138, .55), (150, .25), (166, .45), (186, .3)]]
w += ['<rect x="314" y="211" width="92" height="2" fill="#2f81f7" opacity=".5"/>',
      '<text x="298" y="98" font-size="14" fill="#8c959f" text-anchor="end">−</text>', '<text x="298" y="226" font-size="14" fill="#8c959f" text-anchor="end">+</text>']
# transfer sandwich
layers, y = [("sponge", 14, "#6e7681", ""), ("paper", 8, "#f6e7c1", ""), ("gel", 20, "#dbe9f7", "gel"), ("membrane", 16, "#ffffff", "membrane"), ("paper", 8, "#f6e7c1", ""), ("sponge", 14, "#6e7681", "")], 112
sw = ['<g filter="url(#sh)">']
for _, h, col, lab in layers:
    sw.append(f'<rect x="536" y="{y}" width="128" height="{h}" rx="2" fill="{col}" stroke="#9aa5b1" stroke-width=".8"/>')
    if lab:
        sw.append(f'<text x="600" y="{y + h / 2 + 3.5}" font-size="10" fill="#57606a" text-anchor="middle">{lab}</text>')
    if col == "#6e7681":
        sw += [f'<circle cx="{x}" cy="{y + h / 2}" r="1.6" fill="#8b949e"/>' for x in range(544, 660, 9)]
    y += h + 2
sw.append('</g>')
w += sw
w += [f'<path d="M{x} 140 V150 M{x - 3} 147 L{x} 151 L{x + 3} 147" fill="none" stroke="#2f81f7" stroke-width="1.4" stroke-linecap="round"/>' for x in (556, 644)]
w += [f'<line x1="676" y1="114" x2="676" y2="196" stroke="{LINE}" stroke-width="1.6" marker-end="url(#ah)"/>',
      '<text x="676" y="108" font-size="13" fill="#8c959f" text-anchor="middle">−</text>', '<text x="676" y="214" font-size="13" fill="#8c959f" text-anchor="middle">+</text>']
# immunoblotting
w.append('<g filter="url(#sh)"><rect x="776" y="200" width="128" height="14" rx="3" fill="#ffffff" stroke="#9aa5b1" stroke-width="1.2"/></g>')
w.append(f'<ellipse cx="840" cy="195" rx="10" ry="6" fill="{VIOLET}"/>')
w.append('<path d="M831 188 L840 172 L849 188 M840 172 V148" fill="none" stroke="#2f81f7" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
w.append(f'<path d="M833 144 L840 130 L847 144 M840 130 V112" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
w += [f'<line x1="{840 + 12 * math.cos(a):.1f}" y1="{102 + 12 * math.sin(a):.1f}" x2="{840 + 19 * math.cos(a):.1f}" y2="{102 + 19 * math.sin(a):.1f}" stroke="#f2cc60" stroke-width="2" stroke-linecap="round"/>'
      for a in [math.radians(d) for d in (-150, -110, -70, -30, 10, 170)]]
w.append(f'<circle cx="840" cy="102" r="8" fill="url(#enzg)" stroke="#1a7f37"/>')
w += ['<text x="862" y="106" font-size="10" fill="#57606a">HRP</text>', f'<text x="854" y="128" font-size="10" fill="{ORANGE}">2° Ab</text>',
      '<text x="856" y="168" font-size="10" fill="#2f81f7">1° Ab</text>', f'<text x="790" y="190" font-size="10" fill="{VIOLET}">target</text>']
# detection
w.append('<g filter="url(#sh)"><rect x="1000" y="100" width="124" height="106" rx="4" fill="#ffffff" stroke="#9aa5b1" stroke-width="1.2"/></g>')
w += [f'<rect x="1008" y="{y}" width="14" height="3" rx="1" fill="{c}"/>' for y, c in zip([112, 126, 142, 160, 180, 194], ["#2f81f7", "#2f81f7", RED, "#2f81f7", GREEN, "#2f81f7"])]
for x, o in zip([1042, 1066, 1090, 1114], [.9, .4, .85, .3]):
    w += [f'<rect x="{x - 9}" y="140" width="18" height="5" rx="2.5" fill="#1f2328" opacity="{o}"/>',
          f'<rect x="{x - 9}" y="178" width="18" height="5" rx="2.5" fill="#1f2328" opacity=".8"/>']
w += ['<text x="1130" y="146" font-size="10" fill="#8c959f">target</text>', '<text x="1130" y="184" font-size="10" fill="#8c959f">control</text>']
w += [arrow(176, 294, "load"), arrow(426, 526, "blot"), arrow(692, 768, "probe"), arrow(912, 994, "ECL")]
w += steps([(140, "Lysate", "tissue or cells"), (360, "SDS-PAGE", "separation by size"), (600, "Transfer", "gel → membrane"),
            (840, "Immunoblotting", "primary + HRP secondary"), (1062, "Detection", "ECL · densitometry")])
frame("western", "Western blot",
      "Schematic: protein lysate is separated by SDS-PAGE, transferred to a membrane, probed with a primary and an HRP-conjugated secondary antibody, and detected by ECL with a loading control.", w)

# ---------------------------------------------------------------- organoid culture
def organoid(cx, cy, R, n, rx, ry):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R - ry + 1}" fill="#fff7ef"/>']
    for k in range(n):
        t = 2 * math.pi * k / n
        x, y = cx + R * math.cos(t), cy + R * math.sin(t)
        nx, ny = cx + (R + ry * .35) * math.cos(t), cy + (R + ry * .35) * math.sin(t)
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" transform="rotate({math.degrees(t) - 90:.1f} {x:.1f} {y:.1f})" fill="url(#cellg)" stroke="#e48aa0" stroke-width=".8"/>')
        out.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{rx * .42:.1f}" fill="#7b5ea7"/>')
    return "".join(out)

o = ['<g filter="url(#sh)"><ellipse cx="140" cy="196" rx="82" ry="26" fill="#eef3f8" stroke="#b8c4d2" stroke-width="1.5"/>'
     '<ellipse cx="140" cy="192" rx="70" ry="19" fill="#f7fafc" stroke="#d3dbe5"/></g>',
     '<path filter="url(#sh)" d="M104 182 C100 160 128 146 150 151 C174 155 188 166 181 184 C176 198 150 201 129 198 C111 196 106 192 104 182 Z" fill="url(#tissueg)" stroke="#d26b6b" stroke-width="1.2"/>']
o += [f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fbd0d0" opacity=".8"/>' for x, y, r in [(125, 172, 3), (141, 165, 2.4), (158, 176, 3.2), (146, 186, 2.2), (166, 166, 2)]]
o.append('<g filter="url(#sh)"><path d="M340 98 H380 V196 L360 230 L340 196 Z" fill="#f3f6fa" stroke="#9aa5b1" stroke-width="1.5"/>'
         '<path d="M341.5 146 H378.5 V195.5 L360 227 L341.5 195.5 Z" fill="#f7c6cf" opacity=".75"/>'
         '<rect x="335" y="84" width="50" height="16" rx="3" fill="#4a90d9"/><rect x="335" y="84" width="50" height="5" rx="2" fill="#6aa8e8"/></g>')
o += [cell(x, y, 3.6) for x, y in [(350, 158), (366, 162), (357, 174), (371, 180), (349, 186), (362, 196), (356, 210), (368, 150)]]
o.append('<g filter="url(#sh)"><path d="M520 108 V206 Q520 224 538 224 H662 Q680 224 680 206 V108" fill="#f3f6fa" stroke="#9aa5b1" stroke-width="1.5"/>'
         '<path d="M523 136 H677 V206 Q677 221 662 221 H538 Q523 221 523 206 Z" fill="#f9c9d3" opacity=".55"/>'
         '<path d="M548 221 Q548 168 600 166 Q652 168 652 221 Z" fill="#fde7b0" stroke="#e2b85a" stroke-width="1.2" opacity=".95"/></g>')
o += [cell(x, y, 3.4) for x, y in [(578, 205), (592, 190), (606, 207), (620, 194), (632, 210), (600, 180), (568, 213)]]
o.append('<circle filter="url(#sh)" cx="840" cy="160" r="70" fill="#fde7b0" opacity=".55"/>')
o.append(organoid(840, 160, 44, 18, 7.2, 11.5))
o.append('<text x="840" y="164" font-size="11" fill="#b7a07a" text-anchor="middle" font-style="italic">lumen</text>')
o.append('<g filter="url(#sh)"><rect x="1010" y="92" width="104" height="62" rx="6" fill="#f3f6fa" stroke="#9aa5b1" stroke-width="1.5"/></g>')
for r in range(3):
    for c in range(6):
        o.append(f'<circle cx="{1025 + c * 15}" cy="{108 + r * 15}" r="5" fill="{"#7ee0c3" if (r * 6 + c) % 4 != 3 else "#e5e9ef"}" stroke="#9aa5b1" stroke-width=".6"/>')
o.append('<g filter="url(#sh)"><rect x="1010" y="170" width="104" height="54" rx="4" fill="#ffffff" stroke="#9aa5b1" stroke-width="1.5"/></g>')
o += [f'<rect x="{1018 + i * 24}" y="{186 + (i % 2) * 3}" width="18" height="5" rx="2.5" fill="#3b3f46" opacity="{op}"/>'
      f'<rect x="{1018 + i * 24}" y="208" width="18" height="4" rx="2" fill="#3b3f46" opacity=".75"/>' for i, op in enumerate([.9, .55, .8, .35])]
o += [arrow(228, 326, "digest"), arrow(398, 512, "embed"), arrow(688, 760, "culture"), arrow(920, 1000, "harvest")]
o += steps([(140, "Tissue", "patient or mouse"), (360, "Single cells", "enzymatic dissociation"), (600, "Matrigel dome", "3D embedding"),
            (840, "Organoids", "expansion & passaging"), (1062, "Readouts", "qPCR · western · RNA-seq")])
frame("organoid", "Organoid culture",
      "Schematic: tissue is dissociated into single cells, embedded in a Matrigel dome, grown into organoids, then harvested for qPCR, western blot and RNA-seq.", o)


# ---------------------------------------------------------------- shared bits for the cards below
def ab_up(x, base, col, h=16, arm=8):  # Y with arms up, stem down to `base`
    return f'<path d="M{x} {base} V{base - h} M{x - arm} {base - h - 11} L{x} {base - h} L{x + arm} {base - h - 11}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'


def ab_down(x, tip, col, h=18, arm=8):  # Y with arms down onto `tip`
    return f'<path d="M{x - arm} {tip} L{x} {tip - 12} L{x + arm} {tip} M{x} {tip - 12} V{tip - 12 - h}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'


def hrp(x, y, r=6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#enzg)" stroke="#1a7f37"/>'


def well(cx, liquid=None):
    out = f'<g filter="url(#sh)"><path d="M{cx - 50} 96 V198 Q{cx - 50} 216 {cx - 32} 216 H{cx + 32} Q{cx + 50} 216 {cx + 50} 198 V96" fill="#f3f6fa" stroke="{LINE}" stroke-width="1.5"/></g>'
    if liquid:
        out += f'<path d="M{cx - 48} 124 H{cx + 48} V198 Q{cx + 48} 214 {cx + 32} 214 H{cx - 32} Q{cx - 48} 214 {cx - 48} 198 Z" fill="{liquid}"/>'
    return out


def rng(seed):
    while True:
        seed = (seed * 1103515245 + 12345) % 2 ** 31
        yield seed / 2 ** 31


# ---------------------------------------------------------------- IHC
BROWN, HEMA = "#8b5a2b", "#5b6ee1"
h = ['<g filter="url(#sh)"><rect x="90" y="116" width="100" height="88" rx="6" fill="#cfe3fb" stroke="#9aa5b1" stroke-width="1.2"/>'
     '<rect x="90" y="116" width="20" height="88" rx="4" fill="#b6d0f2"/></g>']
h += [f'<line x1="95" y1="{y}" x2="105" y2="{y}" stroke="#8fb3e3" stroke-width="1.5"/>' for y in range(128, 196, 8)]
h += ['<rect x="118" y="124" width="64" height="72" rx="4" fill="#fbf3dc" stroke="#e2c98f" stroke-width="1.2"/>',
      '<path d="M134 168 C130 150 146 140 158 144 C172 148 172 166 164 174 C156 182 138 180 134 168 Z" fill="url(#tissueg)" stroke="#d26b6b" stroke-width="1"/>']
# microtome: block, blade, ribbon, slide
h += ['<g filter="url(#sh)"><rect x="296" y="116" width="40" height="52" rx="3" fill="#fbf3dc" stroke="#e2c98f" stroke-width="1.2"/>'
      '<path d="M336 108 L350 108 L338 174 Z" fill="#c9d1d9" stroke="#8c959f" stroke-width="1"/></g>',
      '<ellipse cx="316" cy="142" rx="10" ry="8" fill="url(#tissueg)"/>']
h += [f'<g><rect x="{350 + i * 18}" y="{170 + i * 1.5}" width="18" height="8" fill="#fbf3dc" stroke="#e2c98f" stroke-width=".8"/>'
      f'<ellipse cx="{359 + i * 18}" cy="{174 + i * 1.5}" rx="4.5" ry="2.5" fill="#efa3a3"/></g>' for i in range(4)]
h += ['<g filter="url(#sh)"><rect x="306" y="196" width="108" height="20" rx="2" fill="#eaf4fb" stroke="#9aa5b1" stroke-width="1.2"/>'
      '<rect x="306" y="196" width="26" height="20" rx="2" fill="#dfe6ee"/></g>',
      '<ellipse cx="372" cy="206" rx="20" ry="6" fill="#efa3a3" opacity=".9"/>']
# antigen retrieval: heated jar with slides
h += [f'<path d="M{x} 106 q-4 -5 0 -10 q4 -5 0 -10" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-linecap="round" opacity=".8"/>' for x in (580, 600, 620)]
h += ['<g filter="url(#sh)"><rect x="548" y="212" width="104" height="14" rx="4" fill="#57606a"/><rect x="556" y="112" width="88" height="100" rx="8" fill="#eef6ff" stroke="#9aa5b1" stroke-width="1.5"/></g>',
      '<rect x="557.5" y="134" width="85" height="76.5" rx="7" fill="#cfe8ff"/>',
      f'<rect x="560" y="220" width="80" height="2" rx="1" fill="{ORANGE}"/>']
h += [f'<rect x="{x}" y="120" width="9" height="84" rx="1.5" fill="#f6fbff" stroke="#9aa5b1" stroke-width=".8"/>'
      f'<ellipse cx="{x + 4.5}" cy="176" rx="3" ry="6" fill="#efa3a3"/>' for x in (570, 588, 606, 624)]
# staining at the antigen
h += ['<g filter="url(#sh)"><rect x="776" y="196" width="128" height="28" rx="4" fill="#f9d5dc" stroke="#e48aa0" stroke-width="1"/></g>']
h += [f'<line x1="{x}" y1="197" x2="{x}" y2="223" stroke="#e48aa0" stroke-width="1"/>' for x in (808, 872)]
h += [f'<ellipse cx="{x}" cy="212" rx="8" ry="5" fill="{HEMA}" opacity=".75"/>' for x in (792, 840, 888)]
h += [f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BROWN}" opacity=".85"/>' for x, y, r in [(826, 192, 3), (852, 191, 3.5), (833, 186, 2.2), (858, 184, 2), (820, 186, 1.8)]]
h += [f'<ellipse cx="840" cy="194" rx="9" ry="5" fill="{VIOLET}"/>', ab_down(840, 188, "#2f81f7", h=16),
      f'<path d="M833 158 L840 146 L847 158 M840 146 V132" fill="none" stroke="{ORANGE}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
      f'<path d="M818 128 Q829 120 840 128 T862 128" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-linecap="round"/>']
h += [hrp(x, 118, 5.5) for x in (820, 840, 860)]
h += ['<text x="870" y="122" font-size="10" fill="#57606a">HRP polymer</text>', '<text x="852" y="168" font-size="10" fill="#2f81f7">1° Ab</text>',
      f'<text x="782" y="184" font-size="10" fill="{BROWN}">DAB</text>']
# brightfield field of view
h.append('<defs><clipPath id="fov"><circle cx="1062" cy="158" r="58"/></clipPath></defs>')
h.append('<g filter="url(#sh)"><circle cx="1062" cy="158" r="60" fill="#3b3f46"/></g><circle cx="1062" cy="158" r="58" fill="#fbf2ee"/>')
r = rng(7)
fov = ['<g clip-path="url(#fov)">']
for gy in range(102, 220, 16):
    for gx in range(1002, 1124, 18):
        x, y = gx + next(r) * 8, gy + next(r) * 6
        if next(r) < .32:
            fov.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="none" stroke="{BROWN}" stroke-width="3" opacity=".75"/>')
        fov.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="4.2" ry="3.4" fill="{HEMA}" opacity=".6"/>')
fov.append('</g>')
h += fov
h.append('<line x1="1078" y1="200" x2="1102" y2="200" stroke="#1f2328" stroke-width="2.5"/>')
h += [arrow(206, 290, "section"), arrow(434, 540, "retrieve"), arrow(664, 766, "stain"), arrow(914, 992, "image")]
h += steps([(140, "FFPE block", "fixation & embedding"), (360, "Sectioning", "thin sections on slides"), (600, "Antigen retrieval", "heat-induced"),
            (840, "Staining", "primary Ab · HRP polymer · DAB"), (1062, "Imaging", "brightfield · scoring")])
frame("ihc", "Immunohistochemistry (IHC)",
      "Schematic: formalin-fixed paraffin-embedded tissue is sectioned onto slides, antigen is retrieved by heat, stained with a primary antibody, HRP polymer and DAB, and scored under brightfield.", h)

# ---------------------------------------------------------------- ELISA
e = [well(140)] + [ab_up(x, 212, "#2f81f7") for x in (118, 140, 162)]
e += [well(360, "#fde7ef")] + [ab_up(x, 212, "#2f81f7") for x in (338, 360, 382)]
e += [f'<ellipse cx="{x}" cy="181" rx="7" ry="5" fill="{VIOLET}"/>' for x in (338, 360, 382)]
e += [f'<ellipse cx="{x}" cy="{y}" rx="6" ry="4.5" fill="{VIOLET}" opacity=".6"/>' for x, y in ((344, 142), (378, 152))]
e += [well(600)] + [ab_up(x, 212, "#2f81f7") for x in (578, 600, 622)]
e += [f'<ellipse cx="{x}" cy="181" rx="7" ry="5" fill="{VIOLET}"/>' + ab_down(x, 172, ORANGE, h=14) + hrp(x, 136) for x in (578, 600, 622)]
e += ['<text x="636" y="140" font-size="10" fill="#57606a">HRP</text>']
e.append('<g filter="url(#sh)"><rect x="776" y="112" width="128" height="94" rx="6" fill="#f3f6fa" stroke="#9aa5b1" stroke-width="1.5"/></g>')
for row in range(5):
    for col in range(7):
        a = [1, .7, .45, .25, .1][row] if col < 2 else [.85, .3, .6, .5, .2, .75, .4][(row + col) % 7]
        e.append(f'<circle cx="{792 + col * 16}" cy="{126 + row * 16}" r="5.8" fill="#f2cc60" fill-opacity="{a}" stroke="#d4a72c" stroke-width=".6"/>')
e.append('<text x="840" y="224" font-size="10" fill="#8c959f" text-anchor="middle">read at 450 nm</text>')
e.append(axes(1004, 1124, 100, 212))
f4 = lambda x: 210 - 98 / (1 + math.exp(-(x - 1060) / 12))
e.append('<polyline points="' + " ".join(f"{x},{f4(x):.1f}" for x in range(1006, 1123)) + '" fill="none" stroke="#2f81f7" stroke-width="2.2"/>')
e += [f'<circle cx="{x}" cy="{f4(x) + d:.1f}" r="3" fill="#fff" stroke="#2f81f7" stroke-width="1.4"/>' for x, d in ((1016, 1), (1036, -2), (1052, 2), (1068, -2), (1086, 1), (1108, -1))]
ys = f4(1074)
e += [f'<path d="M1004 {ys:.1f} H1074 V212" fill="none" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="4 3"/>',
      f'<circle cx="1074" cy="{ys:.1f}" r="3.2" fill="{ORANGE}"/>',
      '<text x="1064" y="227" font-size="10" fill="#8c959f" text-anchor="middle">concentration →</text>',
      '<text x="1010" y="98" font-size="10" fill="#8c959f">OD</text>']
e += [arrow(196, 304, "sample"), arrow(416, 544, "detect"), arrow(656, 766, "substrate"), arrow(912, 994, "fit")]
e += steps([(140, "Capture", "coat capture antibody"), (360, "Sample", "antigen binds"), (600, "Detection", "detection Ab · HRP"),
            (840, "Substrate", "TMB · stop solution"), (1062, "Standard curve", "4PL fit → concentration")])
frame("elisa", "ELISA",
      "Schematic: sandwich ELISA with capture antibody, sample antigen, HRP-labelled detection antibody, TMB substrate read at 450 nm, and a four-parameter standard curve to interpolate concentration.", e)

# ---------------------------------------------------------------- cell culture and transfection
c = ['<g filter="url(#sh)"><path d="M174 142 L200 128 L206 140 L180 154 Z" fill="#f3f6fa" stroke="#9aa5b1" stroke-width="1.2"/>'
     '<rect x="194" y="114" width="16" height="22" rx="3" fill="#4a90d9" transform="rotate(-28 202 125)"/>'
     '<rect x="80" y="124" width="98" height="82" rx="8" fill="#f3f6fa" stroke="#9aa5b1" stroke-width="1.5"/></g>',
     '<path d="M81.5 168 H176.5 V197 Q176.5 204.5 170 204.5 H88 Q81.5 204.5 81.5 197 Z" fill="#f9c9d3" opacity=".75"/>']
c += [f'<ellipse cx="{x}" cy="200" rx="6" ry="2.6" fill="url(#cellg)" stroke="#e48aa0" stroke-width=".6"/>' for x in range(90, 172, 11)]
c.append('<g filter="url(#sh)"><rect x="290" y="112" width="140" height="96" rx="8" fill="#f3f6fa" stroke="#9aa5b1" stroke-width="1.5"/></g>')
r = rng(3)
for wy in (136, 184):
    for wx in (314, 360, 406):
        c.append(f'<circle cx="{wx}" cy="{wy}" r="19" fill="#f9c9d3" fill-opacity=".8" stroke="#9aa5b1" stroke-width="1"/>')
        c += [f'<circle cx="{wx + (next(r) - .5) * 24:.1f}" cy="{wy + (next(r) - .5) * 24:.1f}" r="2.2" fill="#e48aa0"/>' for _ in range(7)]


def lipoplex(cx, cy, R, n):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R - 4}" fill="#fff8e1"/>']
    for k in range(n):
        t = 2 * math.pi * k / n
        out.append(f'<line x1="{cx + (R - 2) * math.cos(t):.1f}" y1="{cy + (R - 2) * math.sin(t):.1f}" x2="{cx + (R - 9) * math.cos(t):.1f}" y2="{cy + (R - 9) * math.sin(t):.1f}" stroke="#c9b37a" stroke-width="1.2"/>')
        out.append(f'<circle cx="{cx + R * math.cos(t):.1f}" cy="{cy + R * math.sin(t):.1f}" r="{max(2.2, R / 11):.1f}" fill="#f2cc60" stroke="#d4a72c" stroke-width=".6"/>')
    return "".join(out)


c.append('<g filter="url(#sh)">' + lipoplex(600, 160, 38, 28) + '</g>')
c += [f'<circle cx="594" cy="164" r="13" fill="none" stroke="#2f81f7" stroke-width="3.5"/>',
      f'<path d="M594 151 A13 13 0 0 1 607 164" fill="none" stroke="{ORANGE}" stroke-width="3.5"/>',
      f'<path d="M604 144 h14 M604 148 h14" stroke="{RED}" stroke-width="2.4" stroke-linecap="round"/>']
c += ['<g filter="url(#sh)"><ellipse cx="840" cy="164" rx="68" ry="54" fill="#fde2e7" stroke="#e48aa0" stroke-width="1.5"/></g>',
      '<ellipse cx="856" cy="170" rx="24" ry="19" fill="#d8c8f0" stroke="#7b5ea7" stroke-width="1.2"/>',
      '<g>' + lipoplex(792, 122, 12, 14) + '</g>',
      '<circle cx="814" cy="150" r="9" fill="none" stroke="#c9b37a" stroke-width="1.2" stroke-dasharray="2 2"/>',
      f'<path d="M810 150 h9 M810 153 h9" stroke="{RED}" stroke-width="2" stroke-linecap="round"/>',
      f'<path d="M812 186 h10 M812 189 h10 M880 140 h10 M880 143 h10" stroke="{RED}" stroke-width="2" stroke-linecap="round"/>',
      '<circle cx="858" cy="170" r="7" fill="none" stroke="#2f81f7" stroke-width="2.6"/>']
c.append(axes(1004, 1124, 100, 212))
for x, hgt, col, lab, dots in ((1026, 92, BLUE, "ctrl", (-5, 4, -1)), (1078, 28, VIOLET, "si", (6, -4, 1))):
    top = 212 - hgt
    c.append(f'<rect x="{x}" y="{top}" width="30" height="{hgt}" rx="3" fill="{col}" opacity=".85"/>')
    c.append(f'<path d="M{x + 15} {top - 8} V{top + 8} M{x + 9} {top - 8} H{x + 21} M{x + 9} {top + 8} H{x + 21}" stroke="#57606a" stroke-width="1.3"/>')
    c += [f'<circle cx="{x + 8 + 7 * i}" cy="{top + 14 + d}" r="2.6" fill="#fff" stroke="#57606a" stroke-width="1"/>' for i, d in enumerate(dots)]
    c.append(f'<text x="{x + 15}" y="226" font-size="11" fill="#57606a" text-anchor="middle">{lab}</text>')
c.append('<text x="1064" y="98" font-size="10" fill="#8c959f" text-anchor="middle">target mRNA</text>')
c += [arrow(214, 284, "seed"), arrow(436, 552, "transfect"), arrow(648, 764, "incubate"), arrow(914, 994, "measure")]
c += steps([(140, "Cell culture", "maintenance & passaging"), (360, "Seeding", "6-well plate"), (600, "Transfection", "siRNA or plasmid · lipid reagent"),
            (840, "Uptake", "knockdown or overexpression"), (1062, "Readout", "qPCR · western · phenotype")])
frame("transfection", "Cell culture &amp; transfection",
      "Schematic: cells are maintained in a flask, seeded into a 6-well plate, transfected with siRNA or plasmid in a lipid complex, take it up, and knockdown is checked against a control.", c)


# ---------------------------------------------------------------- compact strip: one representative panel per technique
def art(lst):
    return [x for x in lst if 'url(#ah)' not in x and 'cy="263"' not in x]


tiles = [(b, 765, "Isoform RT-PCR"), (q, 765, "qPCR"), (w, 765, "Western blot"), (h, 987, "IHC"), (e, 525, "ELISA"), (c, 765, "Transfection"), (o, 765, "Organoids")]
parts = []
for i, (lst, vx, title) in enumerate(tiles):
    tx = 24 + i * 166
    parts.append(f'<rect x="{tx}" y="8" width="156" height="200" rx="12" fill="#ffffff" stroke="#d0d7de"/>'
                 f'<svg x="{tx + 3}" y="16" width="150" height="150" viewBox="{vx} 80 150 150">{"".join(art(lst))}</svg>'
                 f'<text x="{tx + 78}" y="192" font-size="14" font-weight="600" fill="#1f2328" text-anchor="middle">{title}</text>')
open(f"{OUT}/bench.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="216" viewBox="0 0 1200 216" role="img" aria-labelledby="t d">
  <title id="t">At the bench</title>
  <desc id="d">Schematic icons of bench techniques: isoform-specific RT-PCR, qPCR, western blot, immunohistochemistry, ELISA, transfection and organoid culture.</desc>
{DEFS}  <g font-family="{FONT}">
    {"".join(parts)}
  </g>
</svg>
''')
