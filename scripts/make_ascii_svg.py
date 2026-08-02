from pathlib import Path
import html


# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "assets" / "portrait.txt"
OUTPUT = ROOT / "assets" / "animated-portrait.svg"


# --------------------------------------------------
# READ ASCII PORTRAIT
# --------------------------------------------------

ascii_art = INPUT.read_text(encoding="utf-8")

lines = ascii_art.splitlines()


# --------------------------------------------------
# SVG SETTINGS
# --------------------------------------------------

FONT_SIZE = 10
LINE_HEIGHT = 11

# 80 ASCII columns × roughly 6px per character
WIDTH = 520

# Automatically calculate height from number of ASCII rows
HEIGHT = len(lines) * LINE_HEIGHT + 30


# --------------------------------------------------
# CREATE SVG TEXT ROWS
# --------------------------------------------------

svg_lines = []

for i, line in enumerate(lines):

    # Escape XML special characters such as &, < and >
    safe_line = html.escape(line)

    # Vertical position of this ASCII row
    y = 15 + (i * LINE_HEIGHT)

    svg_lines.append(
        f'''
    <text
        x="10"
        y="{y}"
        class="ascii-line line-{i}"
        xml:space="preserve"
    >{safe_line}</text>
'''
    )


# --------------------------------------------------
# SVG HEADER + CSS
# --------------------------------------------------

svg = f'''<svg
    xmlns="http://www.w3.org/2000/svg"
    width="100%"
    viewBox="0 0 {WIDTH} {HEIGHT}"
    preserveAspectRatio="xMinYMin meet"
>

<style>

    .background {{
        fill: #0d1117;
    }}

    .ascii-line {{
        font-family: "Courier New", monospace;
        font-size: {FONT_SIZE}px;
        fill: #39ff14;

        opacity: 0;

        animation: appear 0.15s forwards;
    }}

    @keyframes appear {{

        from {{
            opacity: 0;
            transform: translateY(3px);
        }}

        to {{
            opacity: 1;
            transform: translateY(0);
        }}

    }}

'''


# --------------------------------------------------
# ANIMATION DELAYS
# --------------------------------------------------

# Each ASCII row appears slightly after the previous row.

for i in range(len(lines)):

    delay = i * 0.035

    svg += f'''
    .line-{i} {{
        animation-delay: {delay:.3f}s;
    }}
'''


# --------------------------------------------------
# CLOSE CSS
# --------------------------------------------------

svg += '''
</style>


<!-- Terminal-style background -->

<rect
    class="background"
    width="100%"
    height="100%"
    rx="10"
/>


<!-- ASCII PORTRAIT -->

'''


# Add all ASCII rows
svg += "\n".join(svg_lines)


# --------------------------------------------------
# CLOSE SVG
# --------------------------------------------------

svg += '''

</svg>
'''


# --------------------------------------------------
# SAVE SVG
# --------------------------------------------------

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Animated SVG created: {OUTPUT}")
print(f"SVG size: {WIDTH} x {HEIGHT}")
print(f"ASCII rows: {len(lines)}")