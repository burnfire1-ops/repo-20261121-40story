#!/usr/bin/env python3
"""Entry program sum21 (news-image-20261121) — Python stdlib only.
Copies the approved artwork entry.png byte-for-byte into the output
directory and verifies it (PNG signature + IHDR 1024x1024).
No generation, no network, deterministic.
Usage: MAKEFUN_OUTPUT_DIR=/output python3 main.py
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def verify_png(path):
    """Return (width, height) after checking PNG signature + IHDR.

    Note (M1 v1): no sha256 pin yet — entry.png will still change in
    M2/M3, so the pin is added in M4 once the final artwork is sealed.
    """
    with open(path, "rb") as f:
        data = f.read(33)
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file (bad signature)")
    if data[12:16] != b"IHDR":
        raise ValueError("not a PNG file (missing IHDR)")
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not os.path.isfile(SRC):
        print(f"ERROR: entry.png not found at {SRC}", file=sys.stderr)
        return 1
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(SRC, dst)
    w, h = verify_png(dst)
    if (w, h) != (1024, 1024):
        print(f"ERROR: entry.png is {w}x{h}, expected 1024x1024", file=sys.stderr)
        return 1
    size = os.path.getsize(dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    print(f"entry.png -> {dst}")
    print(f"size: {size} bytes")
    print(f"dimensions: {w}x{h}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
