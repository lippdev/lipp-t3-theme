"""Builds cloud-rain.json from src/theme.css, src/rain.py and assets/clouds.png.

    python src/build.py
"""
import base64
import json
import re
import sys
from pathlib import Path

from rain import rain_svg, texture_svg

ROOT = Path(__file__).resolve().parent.parent
THEME_ID = "cloud-rain"
THEME_NAME = "Cloud Rain"
CSS_LIMIT = 20_000  # T3 rejects theme CSS longer than this

COLORS = {
    "canvas": "#040828",
    "chrome": "#040828",
    "toolbar": "#040828",
    "sidebar": "#040828",
    "sidebarBorder": "#121c4a",
    "border": "#1c2a6a",
    "accent": "#8fa2ff",
    "accentForeground": "#040828",
    "focus": "#8fa2ff",
    "surface": "#0a1238",
    "surfaceRaised": "#0e1846",
    "surfaceOverlay": "#0a1236",
    "input": "#1a2660",
    "messageSurface": "#1a2a78",
    "secondary": "#14205a",
    "secondaryForeground": "#eef1ff",
    "muted": "#121c50",
    "mutedForeground": "#a3acd6",
    "secondaryLabel": "#a3acd6",
    "sidebarMutedForeground": "#9aa4d0",
    "sidebarControlSurface": "#040828",
    "sidebarRowHover": "#16225e",
    "update": "#8fa2ff",
    "updateSurface": "#14205a",
    "codeBackground": "#050a2a",
    "terminalBackground": "#040824",
    "terminalCursor": "#cdd6ff",
    "terminalSelection": "#26388a",
}


def minify(css: str) -> str:
    strings: list[str] = []

    def stash(match: re.Match) -> str:
        strings.append(match.group(0))
        return f"\x00{len(strings) - 1}\x00"

    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r'"[^"]*"', stash, css)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = re.sub(r"\s*!important", "!important", css)
    css = css.replace(";}", "}")
    css = re.sub(r"\x00(\d+)\x00", lambda m: strings[int(m.group(1))], css)
    return css.strip()


def build() -> dict:
    clouds = base64.b64encode((ROOT / "assets" / "clouds.png").read_bytes()).decode()
    css = minify((ROOT / "src" / "theme.css").read_text(encoding="utf-8"))
    css = (
        css.replace("__CLOUDS__", f"data:image/png;base64,{clouds}")
        .replace("__RAIN__", f"data:image/svg+xml,{rain_svg()}")
        .replace("__TEXTURE__", f"data:image/svg+xml,{texture_svg()}")
    )
    if len(css) > CSS_LIMIT:
        sys.exit(f"theme css is {len(css)} characters; T3 accepts at most {CSS_LIMIT}")
    return {"version": 1, "name": THEME_NAME, "appearance": "dark", "colors": COLORS, "css": css}


if __name__ == "__main__":
    theme = build()
    out = ROOT / f"{THEME_ID}.json"
    out.write_text(json.dumps(theme, indent=2) + "\n", encoding="utf-8")
    print(f"{out.name}: {len(theme['css'])} css characters")
