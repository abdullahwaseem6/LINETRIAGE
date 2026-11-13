# Cleaning log

Raw rows: 1500 real MaintNorm notes (train split), labelled by the teacher (`claude-haiku-5-5`).

| Step | Rows in | Removed | Rows out | Why |
|---|---|---|---|---|
| normalise whitespace | 1500 | 0 | 1500 | formatting only |
| drop failed labels | 1500 | 0 | 1500 | teacher returned no valid label |
| drop too-short notes | 1500 | 0 | 1500 | fewer than 2 words |
| drop exact duplicates | 1500 | 0 | 1500 | same text, ignoring case |
| drop near-duplicates | 1500 | 123 | 1377 | similarity >= 95 after removing IDs |
| remove test-set leaks | 1377 | 32 | 1345 | same or similar (>= 90) to a dev/test note |

**Clean: 1345** · train 1076 · val 269

## Class balance (clean)

| Label | Count |
|---|---|
| safe | 748 |
| dangerous | 597 |
| `mechanical` | 670 |
| `other` | 434 |
| `electrical` | 106 |
| `safety` | 82 |
| `sensor` | 49 |
| `quality` | 4 |

Hand-check sample: `hand_check.csv` (100 rows), not yet checked by a person.
