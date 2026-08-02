from PIL import Image, ImageEnhance, ImageOps
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "assets" / "source-no-bg.png"
OUTPUT = ROOT / "assets" / "source-prepped.png"

img = Image.open(INPUT).convert("RGBA")

# Keep transparency information
alpha = img.getchannel("A")

# Crop around head + upper body
width, height = img.size

left = int(width * 0.29)
top = int(height * 0.20)
right = int(width * 0.75)
bottom = int(height * 0.64)

img = img.crop((left, top, right, bottom))
alpha = alpha.crop((left, top, right, bottom))

# Convert visible image to grayscale
gray = ImageOps.grayscale(img)

# Improve ASCII contrast
gray = ImageEnhance.Contrast(gray).enhance(1.35)
gray = ImageEnhance.Brightness(gray).enhance(1.08)

# Restore transparency
result = Image.merge(
    "RGBA",
    (gray, gray, gray, alpha)
)

result.save(OUTPUT)

print(f"Processed foreground saved to: {OUTPUT}")