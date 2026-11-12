#!/usr/bin/env python3
"""Remove Labyrinth setup.sh section 11 (Forgejo tool mirror) while keeping section 12+."""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: skip_tool_mirror.py <path-to-setup.sh>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    start_marker = "# 11. Mirror offensive tooling repos"
    end_marker = "# 12. Daedalus tooling-build pipeline"
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end <= start:
        print("markers not found; leaving setup.sh unchanged", file=sys.stderr)
        return 0
    replacement = (
        f"{start_marker}\n"
        'echo "[*] Tool mirror skipped (labyrinth_mirror_tooling=false)"\n\n'
    )
    path.write_text(text[:start] + replacement + text[end:], encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
