#!/usr/bin/env python3
"""
Generates the home-screen icons (icon-192.png, icon-512.png).

Writes PNGs by hand with zlib + struct so there are no dependencies to
install. Run once; re-run only if you want to change the icon.

    python make_icons.py
"""

import os
import zlib
import struct

os.chdir(os.path.dirname(os.path.abspath(__file__)))

BLUE = (42, 120, 214)      # --series, the app's one data color
WHITE = (255, 255, 255)

# Three ascending bars — the same mark as the Progress tab.
BARS = [  # (x_left, y_top) in unit coords; all share width/baseline below
    (0.260, 0.520),
    (0.445, 0.410),
    (0.630, 0.300),
]
BAR_W = 0.110
BASELINE = 0.700
CORNER = 0.220             # background rounded-square radius


def rounded_rect(px, py, x0, y0, x1, y1, r):
    """Signed coverage test for a rounded rectangle, in unit coords."""
    cx = min(max(px, x0 + r), x1 - r)
    cy = min(max(py, y0 + r), y1 - r)
    dx, dy = px - cx, py - cy
    return (dx * dx + dy * dy) <= r * r


def sample(px, py):
    """Return the color at a unit-square point, or None for transparent."""
    if not rounded_rect(px, py, 0.0, 0.0, 1.0, 1.0, CORNER):
        return None
    r = BAR_W / 2.0
    for bx, by in BARS:
        if rounded_rect(px, py, bx, by, bx + BAR_W, BASELINE, r):
            return WHITE
    return BLUE


def render(size, ss=3):
    """Render at `size` px with `ss`×`ss` supersampling for clean edges."""
    rows = []
    step = 1.0 / (size * ss)
    for y in range(size):
        row = bytearray()
        row.append(0)                       # PNG filter: none
        for x in range(size):
            rs = gs = bs = a = 0
            for sy in range(ss):
                for sx in range(ss):
                    px = (x * ss + sx + 0.5) * step
                    py = (y * ss + sy + 0.5) * step
                    c = sample(px, py)
                    if c:
                        rs += c[0]; gs += c[1]; bs += c[2]; a += 255
            n = ss * ss
            if a == 0:
                row.extend((0, 0, 0, 0))
            else:
                hit = a // 255
                row.extend((rs // hit, gs // hit, bs // hit, a // n))
        rows.append(bytes(row))
    return b"".join(rows)


def chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


def write_png(path, size):
    raw = render(size)
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)   # 8-bit RGBA
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    print(f"  wrote {path}  ({size}×{size}, {len(png)/1024:.1f} KB)")


if __name__ == "__main__":
    print("Generating icons...")
    write_png("icon-192.png", 192)
    write_png("icon-512.png", 512)
    print("Done.")
