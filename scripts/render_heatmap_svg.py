import json
from datetime import datetime
from pathlib import Path


# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "assets" / "contrib-heatmap.svg"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

data = json.loads(
    INPUT.read_text(encoding="utf-8")
)

username = data["username"]
contributions = data["contributions"]


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

CELL_SIZE = 12
CELL_GAP = 4
STEP = CELL_SIZE + CELL_GAP

LEFT_MARGIN = 45
TOP_MARGIN = 85

WIDTH = 950
HEIGHT = 260


# GitHub-inspired dark theme
COLORS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}


# --------------------------------------------------
# PREPARE DATES
# --------------------------------------------------

parsed = []

for item in contributions:

    date = datetime.strptime(
        item["date"],
        "%Y-%m-%d"
    ).date()

    parsed.append({
        "date": date,
        "count": item["count"],
        "level": item["level"],
    })


parsed.sort(
    key=lambda item: item["date"]
)


if not parsed:
    raise RuntimeError(
        "No contribution data found."
    )


# --------------------------------------------------
# ALIGN FIRST DATE TO WEEK
# --------------------------------------------------

first_date = parsed[0]["date"]

# Python:
# Monday = 0
# Sunday = 6
#
# GitHub calendar:
# Sunday = first row

first_weekday = (
    first_date.weekday() + 1
) % 7


# --------------------------------------------------
# GENERATE CELLS
# --------------------------------------------------

cells = []


for index, item in enumerate(parsed):

    position = index + first_weekday

    week = position // 7
    day = position % 7

    x = LEFT_MARGIN + week * STEP
    y = TOP_MARGIN + day * STEP

    level = max(
        0,
        min(4, int(item["level"]))
    )

    color = COLORS[level]

    date_text = item["date"].strftime(
        "%Y-%m-%d"
    )

    count = item["count"]

    delay = week * 0.025 + day * 0.008


    cells.append(
        f'''
        <rect
            x="{x}"
            y="{y}"
            width="{CELL_SIZE}"
            height="{CELL_SIZE}"
            rx="2"
            fill="{color}"
            class="day"
            style="animation-delay:{delay:.3f}s"
        >
            <title>{date_text}: {count} contributions</title>
        </rect>
        '''
    )


# --------------------------------------------------
# SVG
# --------------------------------------------------

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="100%"
viewBox="0 0 {WIDTH} {HEIGHT}"
preserveAspectRatio="xMidYMid meet"
>

<style>

.background {{
    fill: #0d1117;
}}


.title {{
    font-family: "Courier New", monospace;
    font-size: 18px;
    fill: #3fb950;
}}


.subtitle {{
    font-family: "Courier New", monospace;
    font-size: 13px;
    fill: #8b949e;
}}


.day {{
    opacity: 0;

    animation:
        appear 0.35s forwards;
}}


@keyframes appear {{

    from {{
        opacity: 0;
        transform: translateY(5px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}

}}


.cursor {{
    fill: #3fb950;

    animation:
        blink 1s steps(2, start) infinite;
}}


@keyframes blink {{

    50% {{
        opacity: 0;
    }}

}}

</style>


<!-- BACKGROUND -->

<rect
class="background"
width="100%"
height="100%"
rx="14"
/>


<!-- TERMINAL COMMAND -->

<text
x="30"
y="35"
class="title"
>
divyansh@github:~$ ./contributions.sh
</text>


<text
x="30"
y="58"
class="subtitle"
>
@{username} • GitHub contribution activity
</text>


<!-- CONTRIBUTION CELLS -->

{''.join(cells)}


<!-- TERMINAL CURSOR -->

<rect
x="30"
y="220"
width="9"
height="16"
class="cursor"
/>


</svg>
'''


# --------------------------------------------------
# SAVE
# --------------------------------------------------

OUTPUT.write_text(
    svg,
    encoding="utf-8"
)

print(
    f"Contribution heatmap created: {OUTPUT}"
)

print(
    f"Rendered {len(parsed)} contribution days."
)