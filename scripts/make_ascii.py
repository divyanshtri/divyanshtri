from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "assets" / "source-prepped.png"
OUTPUT = ROOT / "assets" / "portrait.txt"

ASCII_CHARS = "@%#*+=-:. "


def image_to_ascii(image, width=80):

    original_width, original_height = image.size
    aspect_ratio = original_height / original_width

    # Compensate for terminal character proportions
    height = int(width * aspect_ratio * 0.45)

    image = image.resize((width, height))

    pixels = image.load()

    lines = []

    for y in range(height):

        line = ""

        for x in range(width):

            r, g, b, alpha = pixels[x, y]

            # Transparent background = blank space
            if alpha < 80:
                line += " "
                continue

            # Image is grayscale, so R represents brightness
            brightness = r

            index = brightness * (len(ASCII_CHARS) - 1) // 255

            line += ASCII_CHARS[index]

        lines.append(line.rstrip())

    return "\n".join(lines)


img = Image.open(INPUT).convert("RGBA")

ascii_art = image_to_ascii(img)

OUTPUT.write_text(ascii_art, encoding="utf-8")

print(ascii_art)
print(f"\nASCII portrait saved to: {OUTPUT}")