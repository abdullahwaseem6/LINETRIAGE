"""Pick 60 real maintenance notes from MaintNorm's test split for hand-labelling.

Writes data/real/real_sample.csv with empty label columns to fill in by hand.
20 notes are picked from those with risk-related words, so the sample has enough
possible safety cases; the other 40 are random.
"""

import csv
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "real" / "maintnorm" / "test.norm"
OUT = ROOT / "data" / "real" / "real_sample.csv"
RISKY = re.compile(r"leak|fire|smoke|burn|guard|hot|injur|oil|fuel|brake|stop|smell|crack|handrail|walkway", re.I)


def read_notes(path: Path) -> list[str]:
    """The file has one word per line (original<TAB>normalised); a blank line ends a note."""
    notes, words = [], []
    for line in path.read_text(encoding="utf-8").splitlines() + [""]:
        if line.strip():
            words.append(line.split("\t")[0])
        elif words:
            notes.append(" ".join(words))
            words = []
    return notes


def main() -> None:
    notes = sorted(set(read_notes(SOURCE)))
    rng = random.Random(42)
    risky = [n for n in notes if RISKY.search(n)]
    picked = rng.sample(risky, 20)
    rest = [n for n in notes if n not in picked]
    picked += rng.sample(rest, 40)
    rng.shuffle(picked)

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "fault_type", "safety_involved", "notes"])
        for i, text in enumerate(picked, 1):
            writer.writerow([f"M{i:02d}", text, "", "", ""])
    print(f"Wrote {len(picked)} notes to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
