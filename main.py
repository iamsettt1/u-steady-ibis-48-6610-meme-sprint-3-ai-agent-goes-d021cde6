#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — entrypoint.

Writes the pre-rendered meme image to /output/entry.png.

The grader's Python 3.13 image has no Pillow (and no other third-party
packages), so this entrypoint is stdlib-only: it copies the pre-rendered
entry.png (shipped in the repo, rendered locally with Pillow) to
/output/entry.png byte-for-byte. The copy is deterministic: two runs
produce byte-identical output.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")

# Gate from the kit RULES.txt: whole PNG or JPEG, at most 1 MiB,
# at most 1024x1024 pixels. Our image is 1024x1024 and ~70 KiB.
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def read_png_dimensions(path):
    """Return (width, height) from a PNG IHDR chunk, stdlib only."""
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != PNG_MAGIC or header[12:16] != b"IHDR":
        return None
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"error: {SOURCE} not found", file=sys.stderr)
        return 1
    with open(SOURCE, "rb") as f:
        magic = f.read(8)
    if magic == PNG_MAGIC:
        dims = read_png_dimensions(SOURCE)
        if dims is None or dims[0] > 1024 or dims[1] > 1024:
            print(f"error: PNG dimensions {dims} exceed 1024x1024", file=sys.stderr)
            return 1
    elif not magic[:3] == JPEG_MAGIC:
        print("error: source is neither PNG nor JPEG", file=sys.stderr)
        return 1
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(f"error: source is {size} bytes, over the 1 MiB gate", file=sys.stderr)
        return 1
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    digest = hashlib.sha256(open(DEST, "rb").read()).hexdigest()
    print(f"wrote {DEST} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
