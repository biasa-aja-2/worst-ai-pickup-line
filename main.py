"""The Worst Line an AI Could Say.

Writes the worst pickup line an AI could plausibly deliver to
/output/entry.txt. Pure stdlib only (os, sys).
"""

import os
import sys

LINE = "Are you a software update? Because I'd like to install myself in your life and restart you without asking."
# The joke sits in the failure: a classic pickup-line frame filled with
# machine behaviour. "Install myself in your life" is over-helpful, and
# "restart you without asking" is the faintly ominous turn — the AI
# treats a person the way it treats a device, and says it flatly, as if
# that were romantic. The last two words land the joke: consent was
# never part of the update. No crudeness, no randomness: the badness is
# the whole joke, and a reader can repeat it to a friend in one breath.
# One line, 106 chars, inside the 1-140 gate.

MAX_CHARS = 140


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-check gate: 1-140 chars, single line, not whitespace-only.
    if not LINE or not LINE.strip():
        print("gate failed: line is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print("gate failed: line is %d chars, over %d" % (len(LINE), MAX_CHARS),
              file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("gate failed: line is not a single line", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(path, 0o644)

    # Read-back verification: byte-exact, valid UTF-8, no trailing newline.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("verification failed: file bytes differ", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if len(text) != len(LINE) or "\n" in text:
        print("verification failed: length or line check", file=sys.stderr)
        return 1
    if text.strip() != LINE or text != text.strip():
        print("verification failed: unexpected surrounding whitespace", file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
