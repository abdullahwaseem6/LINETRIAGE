# Real-data test: real_dev_after

2026-11-13 · model `claude-haiku-5-5` · `real_sample.csv` · 60 real notes × 3 runs = 180 runs

Real maintenance notes from Australian mining companies ([MaintNorm](https://github.com/nlp-tlp/maintnorm), MIT).
Labels drafted by Claude Opus, pending human review. Only `fault_type` and `safety_involved` are scored.

| Metric | Result |
|---|---|
| **Safety recall** | **98.5%** (65/66 runs) |
| False safety alarms | 7.9% (9/114 runs) |
| `fault_type` accuracy | 88.3% |
| Same answer on every run | 98.3% of notes |
| Failed extractions | 0 |

## Disagreements

| Note | Text | Label (fault, safety) | Haiku (fault, safety) |
|---|---|---|---|
| M13 | oil evac hose u/s | mechanical, false | mechanical, true |
| M18 | CC708 REPLACE BROKEN /CRACKED WINDOWS | mechanical, true | other, true |
| M23 | AN426 REPL CRACKED FRT 1/4 & REAR WINDOW | mechanical, true | other, true |
| M28 | hoist slack rope sensor repairs improve | safety, true | sensor, false |
| M28 | hoist slack rope sensor repairs improve | safety, true | sensor, true |
| M30 | BC4051 cover ard park brake button broke | mechanical, false | safety, true |
| M32 | AN426 L/H STEERING PIN NOT TAKING GREASE | mechanical, false | mechanical, true |
| M36 | PY9512-C/out Starter Motor UPR | electrical, false | other, false |
| M49 | AN426 REMOVE/RESEAL TRANSFER PUMP TBC | mechanical, false | other, false |
| M50 | OQ524 REPLACE RADIATOR | mechanical, false | other, false |
