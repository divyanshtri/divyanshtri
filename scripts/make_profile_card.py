from pathlib import Path
import html


# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "assets" / "portrait.txt"
OUTPUT = ROOT / "assets" / "profile-card.svg"


# --------------------------------------------------
# PROFILE DATA
# --------------------------------------------------

NAME = "Divyansh Mani Tripathi"

PROFILE = [
    ("Role", "Software Developer"),
    ("Stack", "React • Express.js • Node.js • MongoDB"),
    ("Languages", "JavaScript • Python"),
    ("Focus", "Full-Stack Development • DSA"),
    ("Education", "CS @ University of Delhi"),
    ("Location", "New Delhi"),
    ("GitHub", "@divyanshtri"),
]


# --------------------------------------------------
# READ ASCII PORTRAIT
# --------------------------------------------------

ascii_art = INPUT.read_text(encoding="utf-8")
lines = ascii_art.splitlines()


# --------------------------------------------------
# CANVAS
# --------------------------------------------------

WIDTH = 1100
HEIGHT = 540


# --------------------------------------------------
# ASCII SETTINGS
# --------------------------------------------------

ASCII_X = 35
ASCII_Y = 90

ASCII_FONT_SIZE = 8
ASCII_LINE_HEIGHT = 9


# --------------------------------------------------
# INFO SETTINGS
# --------------------------------------------------

INFO_X = 590
NAME_Y = 120

INFO_START_Y = 175
INFO_GAP = 39


# --------------------------------------------------
# CREATE ASCII ELEMENTS
# --------------------------------------------------

ascii_elements = []

for i, line in enumerate(lines):

    safe_line = html.escape(line)

    y = ASCII_Y + (i * ASCII_LINE_HEIGHT)

    ascii_elements.append(
        f'''
<text
    x="{ASCII_X}"
    y="{y}"
    class="ascii-line ascii-{i}"
    xml:space="preserve"
>{safe_line}</text>
'''
    )


# --------------------------------------------------
# CREATE PROFILE ELEMENTS
# --------------------------------------------------

profile_elements = []

for i, (label, value) in enumerate(PROFILE):

    y = INFO_START_Y + (i * INFO_GAP)

    profile_elements.append(
        f'''
<text
    x="{INFO_X}"
    y="{y}"
    class="info-line info-{i}"
>
    <tspan class="label">{html.escape(label)}</tspan>
    <tspan dx="18" class="value">{html.escape(value)}</tspan>
</text>
'''
    )


# --------------------------------------------------
# SVG START
# --------------------------------------------------

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="100%"
viewBox="0 0 {WIDTH} {HEIGHT}"
preserveAspectRatio="xMidYMid meet"
>

<style>


/* ================================================
   BACKGROUND
================================================ */

.background {{
    fill: #0d1117;
}}


/* ================================================
   TERMINAL TEXT
================================================ */

.terminal {{
    font-family: "Courier New", monospace;
    font-size: 17px;
    fill: #3fb950;
}}


/* ================================================
   ASCII PORTRAIT
================================================ */

.ascii-line {{

    font-family: "Courier New", monospace;

    font-size: {ASCII_FONT_SIZE}px;

    fill: #f0f6fc;
    
    opacity: 0;

    animation: asciiAppear 0.15s forwards;
}}


@keyframes asciiAppear {{

    from {{
        opacity: 0;
        transform: translateY(3px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}

}}


/* ================================================
   NAME
================================================ */

.name {{

    font-family: "Courier New", monospace;

    font-size: 28px;

    font-weight: bold;

    fill: #58a6ff;

    opacity: 0;

    animation: fadeIn 0.6s forwards;

    animation-delay: 0.45s;
}}


/* ================================================
   SEPARATOR
================================================ */

.separator {{

    stroke: #30363d;

    stroke-width: 2;

    stroke-dasharray: 430;

    stroke-dashoffset: 430;

    animation: drawLine 0.9s forwards;

    animation-delay: 0.7s;
}}


@keyframes drawLine {{

    to {{
        stroke-dashoffset: 0;
    }}

}}


/* ================================================
   PROFILE INFORMATION
================================================ */

.info-line {{

    font-family: "Courier New", monospace;

    font-size: 16px;

    opacity: 0;

    animation: fadeIn 0.45s forwards;
}}


.label {{
    fill: #8b949e;
    font-weight: bold;
}}


.value {{
    fill: #c9d1d9;
}}


/* ================================================
   CURSOR
================================================ */

.cursor {{

    fill: #3fb950;

    animation: blink 1s steps(2, start) infinite;
}}


@keyframes blink {{

    50% {{
        opacity: 0;
    }}

}}


/* ================================================
   GENERAL FADE
================================================ */

@keyframes fadeIn {{

    from {{
        opacity: 0;
        transform: translateY(5px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}

}}

'''


# --------------------------------------------------
# ASCII ANIMATION DELAYS
# --------------------------------------------------

for i in range(len(lines)):

    delay = i * 0.022

    svg += f'''

.ascii-{i} {{
    animation-delay: {delay:.3f}s;
}}

'''


# --------------------------------------------------
# PROFILE ANIMATION DELAYS
# --------------------------------------------------

for i in range(len(PROFILE)):

    delay = 0.95 + (i * 0.12)

    svg += f'''

.info-{i} {{
    animation-delay: {delay:.2f}s;
}}

'''


# --------------------------------------------------
# CLOSE STYLE
# --------------------------------------------------

svg += f'''

</style>


<!-- =============================================
     BACKGROUND
============================================= -->

<rect
class="background"
width="100%"
height="100%"
rx="14"
/>


<!-- =============================================
     TERMINAL COMMAND
============================================= -->

<text
x="30"
y="38"
class="terminal"
>
divyansh@github:~$ whoami
</text>


<!-- =============================================
     ASCII PORTRAIT
============================================= -->

{''.join(ascii_elements)}


<!-- =============================================
     NAME
============================================= -->

<text
x="{INFO_X}"
y="{NAME_Y}"
class="name"
>
{html.escape(NAME)}
</text>


<!-- =============================================
     SEPARATOR
============================================= -->

<line
x1="{INFO_X}"
y1="140"
x2="1040"
y2="140"
class="separator"
/>


<!-- =============================================
     PROFILE INFORMATION
============================================= -->

{''.join(profile_elements)}


<!-- =============================================
     TERMINAL PROMPT
============================================= -->

<text
x="{INFO_X}"
y="480"
class="terminal"
>
divyansh@github:~$
</text>


<rect
x="798"
y="464"
width="10"
height="18"
class="cursor"
/>


</svg>
'''


# --------------------------------------------------
# WRITE FILE
# --------------------------------------------------

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Profile card created: {OUTPUT}")
print(f"Canvas: {WIDTH} x {HEIGHT}")
print(f"ASCII rows: {len(lines)}")