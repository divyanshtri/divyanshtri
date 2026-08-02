import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

USERNAME = "divyanshtri"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "contributions.json"

URL = f"https://github.com/users/{USERNAME}/contributions"


# --------------------------------------------------
# FETCH GITHUB
# --------------------------------------------------

print(f"Fetching contributions for @{USERNAME}...")

response = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=20,
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")


# --------------------------------------------------
# FIND CONTRIBUTION CELLS
# --------------------------------------------------

contributions = []

cells = soup.select("td.ContributionCalendar-day")

for cell in cells:

    date = cell.get("data-date")

    level = cell.get("data-level")

    if not date:
        continue

    # GitHub usually stores the contribution description
    # in a tooltip linked through aria-describedby.

    count = 0

    tooltip_id = cell.get("aria-describedby")

    if tooltip_id:

        tooltip = soup.find(id=tooltip_id)

        if tooltip:

            text = tooltip.get_text(" ", strip=True)

            # Examples:
            # "5 contributions on July 20th."
            # "No contributions on July 20th."

            match = re.search(r"(\d+)\s+contribution", text)

            if match:
                count = int(match.group(1))


    contributions.append({
        "date": date,
        "count": count,
        "level": int(level) if level is not None else 0,
    })


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

if not contributions:
    raise RuntimeError(
        "No contribution cells were found. "
        "GitHub may have changed its HTML structure."
    )


# --------------------------------------------------
# SAVE JSON
# --------------------------------------------------

data = {
    "username": USERNAME,
    "total_days": len(contributions),
    "contributions": contributions,
}


OUTPUT.parent.mkdir(parents=True, exist_ok=True)

OUTPUT.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8",
)


# --------------------------------------------------
# RESULT
# --------------------------------------------------

print(f"Found {len(contributions)} contribution days.")
print(f"Saved contribution data to:")
print(OUTPUT)