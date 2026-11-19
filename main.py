#!/usr/bin/env python3
"""make.fun news-image-20261119 entry — Python 3.13, standard library only.

The image is entry.png beside this file: a front page summing up the world's
news of Thursday 19 November 2026, rendered by tools/make_image.py from the
day's reporting (Reuters, AP, AFP, Al Jazeera, BBC, Euronews). The program
copies it to /output/entry.png; outside the grader's container,
MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Runs offline and deterministically: a byte-for-byte copy, identical every run.
"""
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # the bounty's 1 MiB output cap
MAX_SIDE = 1024          # the bounty's 1024 px side cap


def check_png(path: Path) -> None:
    """Verify the bounty's output caps before publishing: PNG, <= 1 MiB, <= 1024 px."""
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit("entry.png does not carry the PNG signature")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"entry.png is {width}x{height}, over the 1024 px cap")


def main() -> None:
    check_png(SOURCE)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    if target.read_bytes() != SOURCE.read_bytes():
        raise SystemExit("copy verification failed: output differs from source")


if __name__ == "__main__":
    main()
