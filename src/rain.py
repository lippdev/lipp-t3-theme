"""Draws the digit rain tile and the faint digit texture as SVG.

The output is deterministic (fixed seed), so a rebuild gives the same theme.
"""
import random

CELL_W, CELL_H = 8, 12          # one character cell, CSS px
COLS, ROWS = 60, 80             # rain tile: 480 x 960
DENSITY = 0.3                   # share of columns that carry a drop
TRAIL = (6, 20)                 # drop length range, in cells
TEXTURE = (15, 10)              # texture tile: 15 x 10 cells

FILLS = {
    "tail": "fill='%234d63d6' fill-opacity='.55'",
    "body": "fill='%23aebcff' fill-opacity='.8'",
    "head": "fill='%23fff'",
}


def rain_svg(seed: int = 11) -> str:
    rnd = random.Random(seed)
    width, height = COLS * CELL_W, ROWS * CELL_H
    layers = {k: [] for k in FILLS}
    for col in range(COLS):
        if rnd.random() > DENSITY:
            continue
        n = rnd.randint(*TRAIL)
        row0 = rnd.randint(0, ROWS - 1)
        digits = "".join(rnd.choice("0123456789") for _ in range(n))
        tail = max(1, int(n * 0.45))
        segments = [("tail", 0, digits[:tail]), ("body", tail, digits[tail:-1]), ("head", n - 1, digits[-1])]
        # Draw each drop twice, one tile apart, so drops crossing the bottom edge wrap seamlessly.
        for offset in (0, -ROWS):
            for layer, start, text in segments:
                if not text:
                    continue
                y = (row0 + offset + start) * CELL_H
                if y + len(text) * CELL_H <= 0 or y >= height:
                    continue
                # textLength pins the vertical advance to the cell height in any font.
                length = f" textLength='{len(text) * CELL_H}'" if len(text) > 1 else ""
                layers[layer].append(f"<text x='{col * CELL_W + 4}' y='{y}'{length}>{text}</text>")
    groups = "".join(f"<g {FILLS[k]}>" + "".join(layers[k]) + "</g>" for k in ("tail", "body", "head"))
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        "font-family='Consolas,monospace' font-weight='700' font-size='12' "
        "style='writing-mode:vertical-lr;text-orientation:upright'>" + groups + "</svg>"
    )


# The texture rows that shipped in the first release. Kept fixed so rebuilds match it.
TEXTURE_ROWS = [
    "789906764869458", "474844003902660", "560951367430817", "239109671305821", "572679496582423",
    "718489544999343", "338300044609013", "841128357753557", "211793764625295", "482659175181699",
]


def texture_svg() -> str:
    cols, rows = TEXTURE
    lines = []
    for r, digits in enumerate(TEXTURE_ROWS[:rows]):
        lines.append(f"<text y='{(r + 1) * CELL_H - 2}' textLength='{cols * CELL_W}'>{digits}</text>")
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{cols * CELL_W}' height='{rows * CELL_H}'>"
        "<g fill='%23fff' fill-opacity='.07' font-family='Consolas,monospace' font-weight='700' font-size='11'>"
        + "".join(lines) + "</g></svg>"
    )


if __name__ == "__main__":
    print(len(rain_svg()), "rain chars")
    print(len(texture_svg()), "texture chars")
