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

# sha256 pin of the sealed final artwork (entry.png v3, M3-fix).
# main.py refuses to publish any other bytes: a mismatched sha exits
# non-zero before anything is copied to the output directory.
ENTRY_SHA256 = "e8825c175587679d9b40ffaef25827abb61a53a50a5902c43342dd30f48f67b9"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def verify_png(path):
    """Return (width, height) after checking PNG signature + IHDR.

    Note (M4a): the sha256 pin of the sealed entry.png v3 is verified in
    main() before copying; verify_png itself only checks structure.
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
    actual = sha256_file(SRC)
    if actual != ENTRY_SHA256:
        print("ERROR: entry.png sha256 mismatch", file=sys.stderr)
        print(f"  expected: {ENTRY_SHA256}", file=sys.stderr)
        print(f"  actual:   {actual}", file=sys.stderr)
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
