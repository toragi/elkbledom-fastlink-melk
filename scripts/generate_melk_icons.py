#!/usr/bin/env python3
"""Generate unique brand icons for elkbledom_melk (rainbow LED bulb)."""
import math
import os
import struct
import zlib

OUT_DIR = os.path.join("brands", "elkbledom_melk")


def write_png(path, width, height, rgba_func):
    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    raw = bytearray()
    for y in range(height):
        raw.append(0)
        for x in range(width):
            r, g, b, a = rgba_func(x, y, width, height)
            raw.extend(
                [
                    max(0, min(255, int(r))),
                    max(0, min(255, int(g))),
                    max(0, min(255, int(b))),
                    max(0, min(255, int(a))),
                ]
            )
    compressed = zlib.compress(bytes(raw), 9)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)
    print(f"wrote {path} ({len(png)} bytes)")


def smooth_hue(h):
    h = h % 1.0
    s, v = 0.9, 1.0
    i = int(h * 6)
    f = h * 6 - i
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    segs = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
    r, g, b = segs[i % 6]
    return r * 255, g * 255, b * 255


def bulb_mask(nx, ny):
    cx, cy = 0.5, 0.38
    rx, ry = 0.28, 0.30
    dx, dy = (nx - cx) / rx, (ny - cy) / ry
    d = math.hypot(dx, dy)
    glass = d <= 1.0
    glass_edge = max(0.0, min(1.0, (1.0 - d) * 20))
    neck = (0.44 <= nx <= 0.56) and (0.64 <= ny <= 0.72)
    base = (0.41 <= nx <= 0.59) and (0.72 <= ny <= 0.88)
    inside = glass or neck or base
    edge = glass_edge if glass else (1.0 if (neck or base) else 0.0)
    return inside, edge, d, cx, cy


def icon_px(x, y, w, h):
    nx, ny = (x + 0.5) / w, (y + 0.5) / h
    inside, edge, d, cx, cy = bulb_mask(nx, ny)
    if not inside:
        return (0, 0, 0, 0)
    if ny >= 0.64:
        shade = 95 + int(25 * math.sin(ny * 90))
        band = int(ny * 55) % 5
        if band == 0:
            shade += 40
        return (shade - 5, shade, shade + 20, 255)
    ang = (math.atan2(ny - cy, nx - cx) + math.pi) / (2 * math.pi)
    rr, gg, bb = smooth_hue(ang * 0.85 + 0.08)
    hx, hy = cx - 0.09, cy - 0.11
    hd = math.hypot(nx - hx, ny - hy)
    if hd < 0.16:
        t = (1 - hd / 0.16) ** 1.4
        rr = rr + (255 - rr) * t * 0.7
        gg = gg + (255 - gg) * t * 0.7
        bb = bb + (255 - bb) * t * 0.7
    return (rr, gg, bb, 255 * edge)


def logo_px(x, y, w, h):
    nx, ny = (x + 0.5) / w, (y + 0.5) / h
    if nx < 0.025 or nx > 0.975 or ny < 0.025 or ny > 0.975:
        return (0, 0, 0, 0)
    r, g, b, a = icon_px(x, y, w, h)
    if a < 1:
        return (255, 255, 255, 255)
    return (r, g, b, a)


def main():
    write_png(os.path.join(OUT_DIR, "icon.png"), 256, 256, icon_px)
    write_png(os.path.join(OUT_DIR, "icon@2x.png"), 512, 512, icon_px)
    write_png(os.path.join(OUT_DIR, "logo.png"), 256, 256, logo_px)
    write_png(os.path.join(OUT_DIR, "logo@2x.png"), 512, 512, logo_px)


if __name__ == "__main__":
    main()
