"""Notes From a Passive-Aggressive Fridge — make.fun entry.

Writes one passive-aggressive note from a smart fridge to its owner
to entry.txt in the directory named by MAKEFUN_OUTPUT_DIR (then
/output when it exists, then the folder holding this program).
"""

import os
import sys

LINE = "The ice maker has made 312 cubes this week. You have used four. At this rate I will be an ice sculpture by Christmas."

MAX_CHARS = 200


def output_dir() -> str:
    if len(sys.argv) > 1 and sys.argv[1]:
        return sys.argv[1]
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    line = LINE.strip()
    if not line or len(line) > MAX_CHARS:
        raise SystemExit(f"entry must be 1-{MAX_CHARS} characters, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    with open(target, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != line:
        raise SystemExit("round-trip check failed: entry.txt does not match the note")
    if len(written) != len(line) or len(written) > MAX_CHARS:
        raise SystemExit("round-trip check failed: entry.txt length is wrong")
    print(f"wrote {len(line)} characters to {target}")


if __name__ == "__main__":
    main()
