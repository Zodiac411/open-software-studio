#!/usr/bin/env python3
"""Render the deterministic Opal Seed icon family from the Studio catalog."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]


def hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def svg_glyph(glyph: str, accent: str, graph: str, mono: bool = False) -> str:
    color = graph if mono else accent
    secondary = graph if mono else "#DDE8E4"
    if glyph == "orbit":
        return "".join(f'<circle cx="{x}" cy="{y}" r="10" fill="{graph}"/>' for x, y in ((256, 84), (390, 176), (348, 378), (164, 378), (122, 176)))
    if glyph == "compass":
        return f'<path d="M256 110L292 238L256 272L220 238Z" fill="{color}"/><path d="M256 272V386M184 316H328" stroke="{graph}" stroke-width="12" stroke-linecap="round"/>'
    if glyph == "planes":
        return f'<path d="M142 300L234 152L334 300Z" fill="{secondary}" stroke="{graph}" stroke-width="10"/><path d="M208 348L300 200L400 348Z" fill="{color}" fill-opacity=".76" stroke="{graph}" stroke-width="10"/>'
    if glyph == "lens":
        return f'<circle cx="236" cy="232" r="76" fill="none" stroke="{color}" stroke-width="18"/><path d="M292 288L374 370" stroke="{graph}" stroke-width="18" stroke-linecap="round"/>'
    if glyph == "leaf":
        return f'<path d="M164 334C164 224 238 158 350 146C338 258 284 342 164 334Z" fill="{color}" stroke="{graph}" stroke-width="10"/><path d="M174 326L326 174" stroke="{graph}" stroke-width="10" stroke-linecap="round"/>'
    if glyph == "aperture":
        return f'<path d="M256 122L292 214L382 170L334 260L424 296L328 310L348 408L256 348L164 408L184 310L88 296L178 260L130 170L220 214Z" fill="{color}" fill-opacity=".72" stroke="{graph}" stroke-width="9" stroke-linejoin="round"/>'
    if glyph == "blocks":
        return f'<rect x="134" y="182" width="138" height="138" rx="18" fill="{secondary}" stroke="{graph}" stroke-width="10"/><rect x="240" y="276" width="138" height="138" rx="18" fill="{color}" fill-opacity=".85" stroke="{graph}" stroke-width="10"/>'
    if glyph == "halo":
        return f'<path d="M142 266C142 178 192 126 256 126C320 126 370 178 370 266" fill="none" stroke="{color}" stroke-width="22" stroke-linecap="round"/><path d="M176 284L256 386L336 284" fill="none" stroke="{graph}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
    if glyph == "path":
        return f'<path d="M132 344C188 290 210 338 250 274C290 210 320 250 380 158" fill="none" stroke="{color}" stroke-width="16" stroke-linecap="round"/><circle cx="132" cy="344" r="14" fill="{graph}"/><circle cx="250" cy="274" r="14" fill="{graph}"/><circle cx="380" cy="158" r="14" fill="{graph}"/>'
    raise ValueError(f"unknown icon glyph: {glyph}")


def svg_icon(role: str, glyph: str, accent: str, palette: dict[str, str], mono: bool = False) -> str:
    paper = "#FFFFFF" if mono else palette["paper"]
    porcelain = "#FFFFFF" if mono else palette["porcelain"]
    graphite = "#111111" if mono else palette["graphite"]
    opal = "#FFFFFF" if mono else palette["opal"]
    accent_value = graphite if mono else palette[accent]
    noise = "" if mono else '<path d="M86 420H426" stroke="#FFFFFF" stroke-opacity=".28" stroke-width="3" stroke-linecap="round"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="{role} Opal Seed icon">
  <rect x="18" y="18" width="476" height="476" rx="86" fill="{paper}"/>
  <rect x="48" y="48" width="416" height="416" rx="68" fill="{porcelain}" stroke="{graphite}" stroke-opacity=".20" stroke-width="4"/>
  <circle cx="256" cy="256" r="156" fill="none" stroke="{graphite}" stroke-opacity=".20" stroke-width="4"/>
  <circle cx="256" cy="256" r="126" fill="{opal}" stroke="{graphite}" stroke-opacity=".48" stroke-width="6"/>
  <path d="M256 144C302 144 342 184 342 230C342 294 294 350 256 378C218 350 170 294 170 230C170 184 210 144 256 144Z" fill="{opal}" stroke="{accent_value}" stroke-width="8"/>
  <path d="M218 178C240 160 275 163 296 182" fill="none" stroke="#FFFFFF" stroke-opacity=".84" stroke-width="10" stroke-linecap="round"/>
  {svg_glyph(glyph, accent_value, graphite, mono)}
  {noise}
</svg>\n'''


def draw_scaled_line(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: tuple[int, int, int, int], width: int, scale: float, joint: str = "curve") -> None:
    draw.line([(round(x * scale), round(y * scale)) for x, y in points], fill=fill, width=max(1, width), joint=joint)


def draw_glyph(draw: ImageDraw.ImageDraw, glyph: str, accent: tuple[int, int, int, int], graph: tuple[int, int, int, int], white: tuple[int, int, int, int], scale: float) -> None:
    def p(value: float) -> int:
        return round(value * scale)

    width = max(2, p(10))
    if glyph == "orbit":
        for x, y in ((256, 84), (390, 176), (348, 378), (164, 378), (122, 176)):
            draw.ellipse((p(x - 10), p(y - 10), p(x + 10), p(y + 10)), fill=graph)
    elif glyph == "compass":
        draw.polygon([(p(256), p(110)), (p(292), p(238)), (p(256), p(272)), (p(220), p(238))], fill=accent)
        draw_scaled_line(draw, [(256, 272), (256, 386)], graph, width, scale)
        draw_scaled_line(draw, [(184, 316), (328, 316)], graph, width, scale)
    elif glyph == "planes":
        draw.polygon([(p(142), p(300)), (p(234), p(152)), (p(334), p(300))], fill=white, outline=graph)
        draw.polygon([(p(208), p(348)), (p(300), p(200)), (p(400), p(348))], fill=accent, outline=graph)
        draw_scaled_line(draw, [(142, 300), (234, 152), (334, 300)], graph, width, scale)
        draw_scaled_line(draw, [(208, 348), (300, 200), (400, 348)], graph, width, scale)
    elif glyph == "lens":
        draw.ellipse((p(160), p(156), p(312), p(308)), outline=accent, width=max(2, p(18)))
        draw_scaled_line(draw, [(292, 288), (374, 370)], graph, max(2, p(18)), scale)
    elif glyph == "leaf":
        draw.polygon([(p(164), p(334)), (p(238), p(158)), (p(350), p(146)), (p(284), p(342))], fill=accent, outline=graph)
        draw_scaled_line(draw, [(174, 326), (326, 174)], graph, width, scale)
    elif glyph == "aperture":
        points = [(256, 122), (292, 214), (382, 170), (334, 260), (424, 296), (328, 310), (348, 408), (256, 348), (164, 408), (184, 310), (88, 296), (178, 260), (130, 170), (220, 214)]
        draw.polygon([(p(x), p(y)) for x, y in points], fill=accent, outline=graph)
    elif glyph == "blocks":
        draw.rounded_rectangle((p(134), p(182), p(272), p(320)), radius=p(18), fill=white, outline=graph, width=width)
        draw.rounded_rectangle((p(240), p(276), p(378), p(414)), radius=p(18), fill=accent, outline=graph, width=width)
    elif glyph == "halo":
        draw.arc((p(142), p(126), p(370), p(354)), 180, 360, fill=accent, width=max(2, p(22)))
        draw_scaled_line(draw, [(176, 284), (256, 386), (336, 284)], graph, width, scale)
    elif glyph == "path":
        draw_scaled_line(draw, [(132, 344), (188, 290), (210, 338), (250, 274), (290, 210), (320, 250), (380, 158)], accent, max(2, p(16)), scale)
        for x, y in ((132, 344), (250, 274), (380, 158)):
            draw.ellipse((p(x - 14), p(y - 14), p(x + 14), p(y + 14)), fill=graph)
    else:
        raise ValueError(f"unknown icon glyph: {glyph}")


def raster_icon(glyph: str, accent_name: str, palette: dict[str, str], size: int, mono: bool = False) -> Image.Image:
    canvas = round(size * 4.0)
    scale = canvas / 512.0
    def p(value: float) -> int:
        return round(value * scale)

    paper = (255, 255, 255, 255) if mono else (*hex_rgb(palette["paper"]), 255)
    porcelain = (255, 255, 255, 255) if mono else (*hex_rgb(palette["porcelain"]), 255)
    graphite = (17, 17, 17, 255) if mono else (*hex_rgb(palette["graphite"]), 255)
    opal = (255, 255, 255, 255) if mono else (*hex_rgb(palette["opal"]), 255)
    accent = graphite if mono else (*hex_rgb(palette[accent_name]), 255)
    white = (255, 255, 255, 215)
    image = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    def box(values: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
        return tuple(round(v * scale) for v in values)  # type: ignore[return-value]

    draw.rounded_rectangle(box((18, 18, 494, 494)), radius=round(86 * scale), fill=paper)
    draw.rounded_rectangle(box((48, 48, 464, 464)), radius=round(68 * scale), fill=porcelain, outline=(*graphite[:3], 52), width=max(1, round(4 * scale)))
    draw.ellipse(box((100, 100, 412, 412)), outline=(*graphite[:3], 52), width=max(1, round(4 * scale)))
    draw.ellipse(box((130, 130, 382, 382)), fill=opal, outline=(*graphite[:3], 125), width=max(1, round(6 * scale)))
    seed = [(256, 144), (302, 144), (342, 184), (342, 230), (294, 350), (256, 378), (218, 350), (170, 294), (170, 230), (170, 184), (210, 144)]
    draw.polygon([(p(x), p(y)) for x, y in seed], fill=opal, outline=accent)
    draw_scaled_line(draw, [(218, 178), (240, 160), (275, 163), (296, 182)], white, max(2, round(10 * scale)), scale)
    draw_glyph(draw, glyph, accent, graphite, white, scale)
    if not mono:
        draw_scaled_line(draw, [(86, 420), (426, 420)], (255, 255, 255, 72), max(1, round(3 * scale)), scale)
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    return image


def save_raster(image: Image.Image, path: Path) -> None:
    # The source is deliberately simple; a fixed 16-colour RGB palette keeps
    # mobile/plugin assets below the existing 10KB budget without changing the
    # authored geometry or introducing a runtime image dependency.
    compact = image.quantize(colors=16, dither=Image.Dither.NONE).convert("RGBA")
    compact.save(path, format="PNG", optimize=True, compress_level=9)


def render_all(catalog: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    icon_root = root / "brand" / "icon-system"
    masters = icon_root / "masters"
    glyphs = icon_root / "glyphs"
    monochrome = icon_root / "monochrome"
    generated = icon_root / "generated"
    qa = icon_root / "qa"
    for path in (masters, glyphs, monochrome, generated, qa):
        path.mkdir(parents=True, exist_ok=True)
    palette = catalog["icon_system"]["palette"]
    roles = catalog["icon_system"]["roles"]
    role_ids = list(roles)
    for role in role_ids:
        glyph = roles[role]["glyph"]
        accent = roles[role]["accent"]
        master = svg_icon(role, glyph, accent, palette)
        mono = svg_icon(role, glyph, accent, palette, mono=True)
        (masters / f"{role}.svg").write_text(master, encoding="utf-8")
        (monochrome / f"{role}.svg").write_text(mono, encoding="utf-8")
        (glyphs / f"{role}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{svg_glyph(glyph, palette[accent], palette["graphite"])}</svg>\n', encoding="utf-8")
        for size in [24, *catalog["icon_system"]["sizes"]]:
            save_raster(raster_icon(glyph, accent, palette, size), generated / f"{role}-{size}.png")
        for size in [24, *catalog["icon_system"]["sizes"]]:
            save_raster(raster_icon(glyph, accent, palette, size, mono=True), generated / f"{role}-mono-{size}.png")

    cell = 180
    sheet = Image.new("RGB", (cell * 3, cell * 3), hex_rgb(palette["paper"]))
    for index, role in enumerate(role_ids):
        source = raster_icon(roles[role]["glyph"], roles[role]["accent"], palette, 144)
        icon = Image.new("RGB", source.size, hex_rgb(palette["paper"]))
        icon.paste(source, mask=source.getchannel("A"))
        x = (index % 3) * cell + 18
        y = (index // 3) * cell + 18
        sheet.paste(icon, (x, y))
    sheet.save(icon_root / "contact-sheet.png", format="PNG", optimize=False, compress_level=9)
    (icon_root / "material-tokens.json").write_text(json.dumps(palette, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    groups: list[str] = []
    for index, role in enumerate(role_ids):
        row, col = divmod(index, 3)
        inner = svg_icon(role, roles[role]["glyph"], roles[role]["accent"], palette).split(">", 1)[1].rsplit("</svg>", 1)[0]
        groups.append(f'<g transform="translate({col * 512},{row * 512})">{inner}</g>')
    grid = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1536 1536">{"".join(groups)}</svg>\n'
    (icon_root / "icon-grid.svg").write_text(grid, encoding="utf-8")
    return {"roles": role_ids, "sizes": [24, *catalog["icon_system"]["sizes"]], "contact_sheet": "brand/icon-system/contact-sheet.png"}


if __name__ == "__main__":
    catalog_path = ROOT / "catalog" / "studio.yaml"
    render_all(json.loads(catalog_path.read_text(encoding="utf-8")))
    print("Rendered Opal Seed icons")
