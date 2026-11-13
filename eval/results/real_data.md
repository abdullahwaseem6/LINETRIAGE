# Real-data test: MaintNorm

Does LineTriage work on real maintenance notes, not just the ones I wrote? Real notes from Australian mining companies ([MaintNorm](https://github.com/nlp-tlp/maintnorm), MIT), English only. Every note run 3 times with `claude-haiku-5-5`.

Only `fault_type` and `safety_involved` are scored. The real notes don't use our station registry, so every route would be HUMAN_REVIEW.

## Setup

| Set | Notes | Used for |
|---|---|---|
| Dev (`data/real/real_sample.csv`) | 60 | Looking at mistakes and improving the prompt |
| Test (`data/real/real_test.csv`) | 150 | Measuring only, never used for tuning |

Both were picked by `scripts/sample_real.py` (a third with risk words such as leak or brake, the rest random), with no overlap. The test set was labelled **before** any model output on it was seen.

## Results

| | Dev: before | Dev: after | **Test: before** | **Test: after** |
|---|---|---|---|---|
| **Safety recall** | 62.1% | 98.5% | **63.5%** | **91.8%** |
| False safety alarms | 5.3% | 7.9% | 8.9% | 12.4% |
| `fault_type` accuracy | 80.6% | 88.3% | 71.8% | 78.2% |

The 60 handwritten factory reports, re-run with the new prompt: safety recall still **100%**, route accuracy 98.3% → 96.7% (3 more wrong runs out of 180).

## What happened

**Before:** on real notes, safety recall was 62–64%, against 100% on my own reports. Haiku treated "Replace brake hose", "Coolant leak" and "TYRE DAMAGE" as routine repairs. Real technician notes are calm, short and full of abbreviations, and the prompt only described factory risks such as "a leak onto the floor". This is **domain shift**: a system tuned on one kind of data does worse on another.

**The fix:** using only the dev set's mistakes, I added general rules for vehicles and heavy equipment to the prompt:
- common abbreviations
- fluid leaks, brakes, steering, tyres and windows count as safety risks
- broken safety equipment counts as `safety`
- routine inspections are `other`

**After:** test recall rose to 91.8%. The cost was more false alarms (8.9% → 12.4%), which is the right trade for safety triage: a false alarm costs a supervisor a minute, a missed brake fault could cost a life.

## Still missed on the test set

| Note | Why |
|---|---|
| REPL NEUTRALIZER MICRO SWITCH | Specialised safety interlock; the prompt doesn't name it |
| REPAIR GAS TESTER | Gas detector is a safety device; read as a sensor |
| REPLACE FIRE EXTINGUISHERS | Read as routine |
| Hoist Brake Switch operation | Brake-related, read as `other` |
| drag rope slipping through socket | Label is a judgement call |
| Tray coming down hard fault | Label is a judgement call |

The first three are exactly the kind of equipment I deliberately did **not** put in the prompt, because I only saw them in the test set.

## Limits

- **Labels were drafted by Claude Opus**, a close relative of the model being tested, and still need a human review. Borderline cases are explained in each CSV's `notes` column.
- Mining equipment, not a factory line; English only.
- 150 test notes, 53 of them safety cases: still a small sample.
