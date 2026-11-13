# Schema review: baseline → after review

Both runs: 60 reports × 3 runs with `claude-haiku-5-5`. Full results in [baseline.md](baseline.md) and [after_review.md](after_review.md).

| Metric | Baseline | After review |
|---|---|---|
| **Safety recall** | **100%** (39/39) | **100%** (45/45) |
| False safety alarms | 6 runs | 3 runs |
| Route accuracy | 95.0% | **98.3%** |
| Same facts on every run | 78.3% | **93.3%** |
| Wrong answers (runs with any error) | 56 | **17** |
| `fault_type` accuracy | 90.6% | 95.6% |
| `downtime_minutes` accuracy | 91.7% | 97.8% |
| `affected_part` accuracy | 92.8% | 100% |
| `language` accuracy | 96.1% | 100% |
| Latency (average) | 3.3s | 2.0s |
| Cost per 1,000 reports | $0.26 | $0.33 |

## What was wrong, and what we changed

**1. Labels that were wrong (the model was right).** We changed 3 labels:
- R18: downtime `0` → `null`. The note never says the line kept running.
- R26 (overheating spindle) and R37 (coolant leak): `safety_involved` → `true`. Overheating is a fire risk and a leak is a slip risk. The labelling guide now says so.

Because R26 and R37 are now safety cases, the safety total rose from 39 to 45 runs.

**2. Rules the model was never told.** The labelling guide had grown, but the extractor's prompt hadn't. We added:
- downtime conversions ("all shift" = 480, ranges take the higher number), and `0` only when the note says the line kept running
- singular product names ("bracket", not "brackets" or "bracket batch")
- when to use `mixed` for language
- how to write unknown stations
- "two faults in one note: label the more serious one"

The last rule fixed **R40** (bad housings plus a broken camera), the only real missed escalation in the baseline.

**3. A limit of the schema, left for later.** A report holds one fault. Notes with two faults lose the less serious one. Moving to a list of faults is in `LATER.md`.

## Still wrong after review

- **R01, new false alarm (3 runs).** "stopped it like 15 min to let it cool" is now read as overheating, so it's routed to SAFETY_ALERT. A side effect of adding the overheating rule. It errs on the safe side.
- **R43, R46, R38: `fault_type` between `mechanical`, `electrical` and `other`** for slang notes ("pc is dead dead", "nutrunner ded"). The route is still correct.
- **R49:** "way faster now" isn't read as "kept running", so downtime is `null` instead of `0`.
- **R13:** "linie 12" vs "Linie 12", a capital letter only.

**Lesson:** half the improvement came from fixing our own labels and instructions, not the model. Measuring every field, not just the route, is what showed us where to look.
