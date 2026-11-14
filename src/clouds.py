"""Turns a cloud photo into the pixel-art sky in assets/clouds.png.

Only needed to change the picture or its colours; build.py uses the PNG as it is.

    python src/clouds.py path/to/photo.jpg

The picture is cover-fitted to 240x135, regraded with the "midnight" colours,
ordered-dithered, posterised and reduced to 8 colours so it stays near 9 KB as base64.
"""
import sys
from pathlib import Path

from PIL import Image

WIDTH, HEIGHT = 240, 135
STEP, CONTRAST = 20, 1.14
SKY = [(4, 8, 40), (30, 46, 112)]                       # top of frame -> horizon
CLOUD = [(10, 14, 44), (62, 78, 146), (206, 216, 255)]  # shadow -> mid -> highlight
BAYER = [(v + 0.5) / 16 for v in (0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5)]


def mix(a, b, t):
    return a + (b - a) * t


def grade(r, g, b, v):
    sky = min(1, max(0, (b - max(r, g)) / 160))           # how much of the cell is open blue sky
    light = min(1, max(0, ((r * 0.3 + g * 0.59 + b * 0.11) / 255 - 0.25) / 0.7))
    lo, hi = (CLOUD[0], CLOUD[1]) if light < 0.5 else (CLOUD[1], CLOUD[2])
    t = light * 2 if light < 0.5 else light * 2 - 1
    h = min(1, v * 1.4)
    return [mix(mix(lo[i], hi[i], t), mix(SKY[0][i], SKY[1][i], h), sky) for i in range(3)]


def quantise(value, threshold):
    return max(0, min(255, round(((value - 128) * CONTRAST + 131 + (threshold - 0.5) * STEP) / STEP) * STEP))


def build(source: Path, out: Path) -> None:
    img = Image.open(source).convert("RGB")
    k = max(WIDTH / img.width, HEIGHT / img.height)
    sw, sh = WIDTH / k, HEIGHT / k
    box = ((img.width - sw) / 2, (img.height - sh) / 2, (img.width + sw) / 2, (img.height + sh) / 2)
    small = img.resize((WIDTH, HEIGHT), Image.LANCZOS, box=box)
    src, art = small.load(), Image.new("RGB", (WIDTH, HEIGHT))
    dst = art.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            b = BAYER[(y & 3) << 2 | (x & 3)]
            dst[x, y] = tuple(quantise(c, b) for c in grade(*src[x, y], y / HEIGHT))
    art.quantize(colors=8, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(out, optimize=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python src/clouds.py path/to/photo.jpg")
    target = Path(__file__).resolve().parent.parent / "assets" / "clouds.png"
    build(Path(sys.argv[1]), target)
    print(f"wrote {target}")
