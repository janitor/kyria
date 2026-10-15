#!/usr/bin/env python3
"""Build separate EN and RU macOS input sources from Universal Layout Ortho."""

import argparse
import plistlib
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BUNDLE_NAME = "Universal Ortho Split.bundle"
BUNDLE_ID = "local.raman.keyboardlayout.universalorthosplit"
LAYOUTS = {
    "EN": {"id": -29001, "language": "en", "source_map": 0, "color": "#2467A9"},
    "RU": {"id": -29002, "language": "ru", "source_map": 2, "color": "#A33B59"},
}
MAP_SET_PATTERN = re.compile(r'(<keyMapSet id="16c">)(.*?)(</keyMapSet>)', re.S)
KEY_MAP_PATTERN = re.compile(r'<keyMap index="([0-7])">(.*?)</keyMap>', re.S)


def split_keylayout(original: str, label: str) -> str:
    """Keep all shared maps and actions, replacing only the language maps."""
    setting = LAYOUTS[label]
    match = MAP_SET_PATTERN.search(original)
    if match is None:
        raise ValueError("Missing primary key map set 16c")
    source_maps = {int(index): body for index, body in KEY_MAP_PATTERN.findall(match.group(2))}
    if set(source_maps) != set(range(8)):
        raise ValueError("Expected exactly eight primary key maps")

    def replace_map(found: re.Match) -> str:
        index = int(found.group(1))
        source_index = setting["source_map"] + index % 2 if index < 4 else index
        return f'<keyMap index="{index}">{source_maps[source_index]}</keyMap>'

    primary = KEY_MAP_PATTERN.sub(replace_map, match.group(2))
    result = original[:match.start(2)] + primary + original[match.end(2):]
    root = re.search(r'<keyboard\b[^>]*>', result)
    if root is None:
        raise ValueError("Missing keyboard root element")
    root_tag = root.group()
    root_tag = re.sub(r'\bid="[^"]+"', f'id="{setting["id"]}"', root_tag, count=1)
    root_tag = re.sub(r'\bname="[^"]+"', f'name="Universal Ortho {label}"', root_tag, count=1)
    return result[:root.start()] + root_tag + result[root.end():]


def make_icon(path: Path, label: str, color: str) -> None:
    """Build a distinct EN/RU icon that macOS can show in the Input menu."""
    size = 1024
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((64, 64, 960, 960), radius=220, fill=color)
    font_path = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    font = ImageFont.truetype(str(font_path), 450)
    bounds = draw.textbbox((0, 0), label, font=font)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    draw.text(((size - width) / 2 - bounds[0], (size - height) / 2 - bounds[1] - 12),
              label, font=font, fill="white")

    with tempfile.TemporaryDirectory() as temporary:
        iconset = Path(temporary) / f"Universal Ortho {label}.iconset"
        iconset.mkdir()
        sizes = ((16, 1), (16, 2), (32, 1), (32, 2),
                 (128, 1), (128, 2), (256, 1), (256, 2),
                 (512, 1), (512, 2))
        for points, scale in sizes:
            pixels = points * scale
            suffix = "@2x" if scale == 2 else ""
            filename = f"icon_{points}x{points}{suffix}.png"
            canvas.resize((pixels, pixels), Image.Resampling.LANCZOS).save(iconset / filename)
        subprocess.run(["iconutil", "-c", "icns", str(iconset), "-o", str(path)], check=True)


def build(source: Path, output_dir: Path) -> Path:
    original = source.read_text(encoding="utf-8")
    bundle = output_dir / BUNDLE_NAME
    resources = bundle / "Contents" / "Resources"
    resources.mkdir(parents=True, exist_ok=True)
    info = {
        "CFBundleIdentifier": BUNDLE_ID,
        "CFBundleName": "Universal Ortho Split",
        "CFBundleVersion": "1.0",
    }
    for label, setting in LAYOUTS.items():
        layout_name = f"Universal Ortho {label}"
        (resources / f"{layout_name}.keylayout").write_text(
            split_keylayout(original, label), encoding="utf-8"
        )
        make_icon(resources / f"{layout_name}.icns", label, setting["color"])
        info[f"KLInfo_{layout_name}"] = {
            "TICapsLockLanguageSwitchCapable": False,
            "TISIconIsTemplate": False,
            "TISInputSourceID": f"{BUNDLE_ID}.keylayout.UniversalOrtho{label}",
            "TISIntendedLanguage": setting["language"],
        }
    with (bundle / "Contents" / "Info.plist").open("wb") as stream:
        plistlib.dump(info, stream)
    with (bundle / "Contents" / "version.plist").open("wb") as stream:
        plistlib.dump({"BuildVersion": "1", "SourceVersion": "1"}, stream)
    return bundle


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).with_name("source") / "Universal Layout Ortho.keylayout")
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).with_name("dist"))
    arguments = parser.parse_args()
    print(build(arguments.source, arguments.output_dir))
