from pathlib import Path
from rembg import remove
from PIL import Image


ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "assets" / "source-photo.png"
OUTPUT = ROOT / "assets" / "source-no-bg.png"


# Open original image
img = Image.open(INPUT).convert("RGBA")

# Remove background
result = remove(img)

# Save with transparency
result.save(OUTPUT)

print(f"Background removed: {OUTPUT}")