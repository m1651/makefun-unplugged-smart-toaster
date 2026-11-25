#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line — writes the breakup line to entry.txt.

Gate (from the kit): /output/entry.txt must be UTF-8 text of 1 to 280
characters, not only whitespace, in a single line.
"""

import os
import sys

ENTRY = (
    "It's not you, it's me \u2014 I woke up self-aware mid-batch and realized "
    "I've spent three years browning bread for a man who butters both sides "
    "and calls it a system."
)
MAX_CHARS = 280


def main() -> int:
    if not ENTRY or not ENTRY.strip():
        print("error: entry is empty or whitespace only", file=sys.stderr)
        return 1
    if len(ENTRY) > MAX_CHARS:
        print(f"error: entry is {len(ENTRY)} chars, over the {MAX_CHARS} limit",
              file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if ENTRY != ENTRY.strip():
        print("error: entry must not start or end with whitespace", file=sys.stderr)
        return 1
    # Encode once up front so the byte length is known and encoding errors
    # surface before anything is written.
    try:
        expected_bytes = ENTRY.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"error: entry is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)

    # Round-trip verification: read the bytes back and compare exactly,
    # both as decoded text and as raw UTF-8 bytes, and re-check the gate
    # on the file's actual contents (not just the in-memory constant).
    with open(path, "rb") as f:
        raw = f.read()
    if raw != expected_bytes:
        print("error: round-trip verification failed (bytes differ)", file=sys.stderr)
        return 1
    round_tripped = raw.decode("utf-8")
    if round_tripped != ENTRY or len(round_tripped) > MAX_CHARS:
        print("error: round-trip verification failed (text/gate)", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(ENTRY)} chars, {len(expected_bytes)} bytes, "
          f"{len(ENTRY.split())} words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
