#!/usr/bin/env python3
"""Tests for sum21 M1 entry (news-image-20261121, 40 stories).
TDD: written BEFORE render_entry.py / main.py existed.
Run: python3 test_entry.py  (stdlib + Pillow, no network)
"""
import hashlib
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(ROOT, "entry.png")
RENDERER = os.path.join(ROOT, "render_entry.py")
MAIN = os.path.join(ROOT, "main.py")

HERO_FILES = ["hero-h1-crash-bars.png", "hero-h2.png", "hero-h3.png", "hero-h4.png"]
STRIP_FILES = ["strip-a1-vi-pale.png"] + [f"strip-a{i}.png" for i in range(2, 12)] + ["strip-a12-f1-pale.png"]

failures = []


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        failures.append(name)


def png_size(path):
    from PIL import Image
    with Image.open(path) as im:
        return im.size, im.format


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def test_a_entry_png():
    print("== (a) entry.png ==")
    check("entry.png exists", os.path.isfile(ENTRY))
    if not os.path.isfile(ENTRY):
        return
    size = os.path.getsize(ENTRY)
    check("entry.png <= 1 MiB", size <= 1048576, f"{size} bytes")
    with open(ENTRY, "rb") as f:
        sig = f.read(8)
    check("PNG signature", sig == b"\x89PNG\r\n\x1a\n")
    wh, fmt = png_size(ENTRY)
    check("PNG format", fmt == "PNG", fmt)
    check("entry.png 1024x1024", wh == (1024, 1024), str(wh))


def test_b_renderer_report():
    print("== (b) renderer report (subprocess) ==")
    r = subprocess.run([sys.executable, RENDERER], cwd=ROOT,
                       capture_output=True, text=True, timeout=120)
    check("render_entry.py exit 0", r.returncode == 0, r.stderr[-500:] if r.returncode else "")
    out = r.stdout
    print(out.strip()[:600])
    m = re.search(r"cerita unik=(\d+)", out)
    check("40 cerita unik", m and int(m.group(1)) == 40, m.group(0) if m else "no match")
    check("count_ok=True", "count_ok=True" in out)
    check("height_ok=True", "height_ok=True" in out)
    m = re.search(r"total=(\d+)/1024", out)
    check("total tinggi <= 1024", m and int(m.group(1)) <= 1024, m.group(0) if m else "no match")
    m = re.search(r"pelanggaran teks=(\d+)", out)
    check("0 pelanggaran teks", m and int(m.group(1)) == 0, m.group(0) if m else "no match")
    m = re.search(r"pin di luar peta=(\d+)", out)
    check("pin di luar 0", m and int(m.group(1)) == 0, m.group(0) if m else "no match")
    m = re.search(r"pasang pin tumpang tindih=(\d+)", out)
    check("pin tumpang tindih 0", m and int(m.group(1)) == 0, m.group(0) if m else "no match")
    # M9: strip angka besar di atas + tag outlet per kartu Tier A.
    m = re.search(r"numbers_pt=(\d+)", out)
    check("angka besar numbers_pt >= 20", m and int(m.group(1)) >= 20,
          m.group(0) if m else "no match")
    m = re.search(r"source_tags=(\d+)/12", out)
    check("tag outlet 12/12 kartu Tier A", m and int(m.group(1)) == 12,
          m.group(0) if m else "no match")
    m = re.search(r"map_w=(\d+)", out)
    check("peta kecil map_w <= 240", m and int(m.group(1)) <= 240,
          m.group(0) if m else "no match")
    m = re.search(r"brief_font=(\d+)", out)
    check("brief font >= 15pt", m and int(m.group(1)) >= 15,
          m.group(0) if m else "no match")


def test_c_illustrations():
    print("== (c) 16 ilustrasi ==")
    check("16 ilustrasi terdaftar", len(HERO_FILES) + len(STRIP_FILES) == 16)
    for name in HERO_FILES:
        p = os.path.join(ROOT, name)
        check(f"{name} ada", os.path.isfile(p))
        if os.path.isfile(p):
            wh, _ = png_size(p)
            check(f"{name} 180x102", wh == (180, 102), str(wh))
    for name in STRIP_FILES:
        p = os.path.join(ROOT, name)
        check(f"{name} ada", os.path.isfile(p))
        if os.path.isfile(p):
            wh, _ = png_size(p)
            check(f"{name} 151x42", wh == (151, 42), str(wh))


def test_d_main_twice():
    print("== (d) main.py 2x run ==")
    import tempfile
    hashes = []
    for i in range(2):
        outdir = tempfile.mkdtemp(prefix=f"sum21-main-{i}-")
        env = dict(os.environ, MAKEFUN_OUTPUT_DIR=outdir)
        t0 = time.time()
        r = subprocess.run([sys.executable, MAIN], cwd=ROOT, env=env,
                           capture_output=True, text=True, timeout=60)
        dt = time.time() - t0
        check(f"main.py run {i+1} exit 0", r.returncode == 0, r.stderr[-300:] if r.returncode else "")
        check(f"main.py run {i+1} < 60 detik", dt < 60, f"{dt:.1f}s")
        p = os.path.join(outdir, "entry.png")
        check(f"main.py run {i+1} entry.png ada", os.path.isfile(p))
        if os.path.isfile(p):
            hashes.append(sha256(p))
            wh, _ = png_size(p)
            check(f"main.py run {i+1} output 1024x1024", wh == (1024, 1024), str(wh))
    check("main.py 2 run byte-identik", len(hashes) == 2 and hashes[0] == hashes[1],
          hashes[0][:16] if hashes else "no output")


def test_e_render_twice():
    print("== (e) render 2x byte-identik ==")
    h1 = None
    for i in range(2):
        r = subprocess.run([sys.executable, RENDERER], cwd=ROOT,
                           capture_output=True, text=True, timeout=120)
        check(f"render run {i+1} exit 0", r.returncode == 0)
        h = sha256(ENTRY) if os.path.isfile(ENTRY) else None
        if i == 0:
            h1 = h
        else:
            check("render 2x byte-identik", h is not None and h == h1, f"{h1} vs {h}")


if __name__ == "__main__":
    test_a_entry_png()
    test_b_renderer_report()
    test_c_illustrations()
    test_d_main_twice()
    test_e_render_twice()
    print(f"\n{'ALL PASS' if not failures else 'FAILURES: ' + str(len(failures))}")
    for f in failures:
        print("  -", f)
    sys.exit(1 if failures else 0)
