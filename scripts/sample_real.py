"""Pick real maintenance notes from MaintNorm's test split for hand-labelling.

Writes a CSV with empty label columns to fill in by hand. A share of the notes
is picked from those with risk-related words, so the sample has enough possible
safety cases; the rest are random. Notes already in --exclude files are skipped.

    python scripts/sample_real.py                                   # dev set: 60 notes
    python scripts/sample_real.py --n 150 --risky 50 \\
        --out data/real/real_test.csv --exclude data/real/real_sample.csv --seed 7
"""

import argparse
import csv
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "real" / "maintnorm" / "test.norm"
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
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n", type=int, default=60)
    parser.add_argument("--risky", type=int, default=20, help="how many notes to pick from risk-word matches")
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "real" / "real_sample.csv")
    parser.add_argument("--exclude", type=Path, nargs="*", default=[])
    parser.add_argument("--prefix", default="M")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    taken = {row["text"] for path in args.exclude for row in csv.DictReader(path.open(encoding="utf-8"))}
    notes = sorted(set(read_notes(SOURCE)) - taken)
    rng = random.Random(args.seed)
    risky = [n for n in notes if RISKY.search(n)]
    picked = rng.sample(risky, args.risky)
    rest = [n for n in notes if n not in picked]
    picked += rng.sample(rest, args.n - args.risky)
    rng.shuffle(picked)

    with args.out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "fault_type", "safety_involved", "notes"])
        for i, text in enumerate(picked, 1):
            writer.writerow([f"{args.prefix}{i:03d}" if args.n > 99 else f"{args.prefix}{i:02d}", text, "", "", ""])
    print(f"Wrote {len(picked)} notes to {args.out}")


if __name__ == "__main__":
    main()
