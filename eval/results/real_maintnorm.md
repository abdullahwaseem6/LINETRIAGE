# Real-data test: MaintNorm

2026-11-13 · model `claude-haiku-5-5` · 60 real notes × 3 runs = 180 runs

Real maintenance notes from Australian mining companies ([MaintNorm](https://github.com/nlp-tlp/maintnorm), MIT).
Labels drafted by Claude Opus, pending human review. Only `fault_type` and `safety_involved` are scored.

| Metric | Result |
|---|---|
| **Safety recall** | **62.1%** (41/66 runs) |
| False safety alarms | 5.3% (6/114 runs) |
| `fault_type` accuracy | 80.6% |
| Same answer on every run | 66.7% of notes |
| Failed extractions | 0 |

## Disagreements

| Note | Text | Label (fault, safety) | Haiku (fault, safety) |
|---|---|---|---|
| M01 | AN426 TEMP REP TO TRANS DROP BOX LEAK | mechanical, true | mechanical, false |
| M03 | Replace brake hose | mechanical, true | mechanical, false |
| M05 | Coolant leak | mechanical, true | mechanical, false |
| M07 | Drag g/box output shaft leaking | mechanical, true | mechanical, false |
| M10 | 3M Mech Cond Ball Stut Crack Test RZ2293 | other, false | mechanical, false |
| M10 | 3M Mech Cond Ball Stut Crack Test RZ2293 | other, false | quality, false |
| M11 | LD3192- replace brake cooling hoses | mechanical, true | mechanical, false |
| M17 | BP504 C/O POS 5 TYRE DAMAGE | mechanical, true | mechanical, false |
| M17 | BP504 C/O POS 5 TYRE DAMAGE | mechanical, true | quality, false |
| M18 | CC708 REPLACE BROKEN /CRACKED WINDOWS | mechanical, true | other, true |
| M18 | CC708 REPLACE BROKEN /CRACKED WINDOWS | mechanical, true | safety, true |
| M19 | 1000H Insp Hyd Cyl Rip Lift LH CC0233 | other, false | mechanical, false |
| M19 | 1000H Insp Hyd Cyl Rip Lift LH CC0233 | other, false | mechanical, true |
| M21 | PH639 REP RIDE CONTROL | mechanical, false | other, false |
| M23 | AN426 REPL CRACKED FRT 1/4 & REAR WINDOW | mechanical, true | quality, false |
| M23 | AN426 REPL CRACKED FRT 1/4 & REAR WINDOW | mechanical, true | quality, true |
| M24 | CR871 REPAIR EXHAUST LEAK TEXT | mechanical, true | mechanical, false |
| M25 | 3M Mech Cond Ball Stub Crack Test VU1914 | other, false | quality, false |
| M26 | WJ525 P/BRAKE FAULT | mechanical, true | mechanical, false |
| M26 | WJ525 P/BRAKE FAULT | mechanical, true | other, true |
| M27 | OQ524 LEAKING RADIATOR | mechanical, true | mechanical, false |
| M28 | hoist slack rope sensor repairs improve | safety, true | sensor, false |
| M28 | hoist slack rope sensor repairs improve | safety, true | sensor, true |
| M30 | BC4051 cover ard park brake button broke | mechanical, false | mechanical, true |
| M30 | BC4051 cover ard park brake button broke | mechanical, false | other, true |
| M30 | BC4051 cover ard park brake button broke | mechanical, false | safety, true |
| M36 | PY9512-C/out Starter Motor UPR | electrical, false | other, false |
| M40 | JZ9248 rear brake cooling hose leak | mechanical, true | mechanical, false |
| M41 | CC708 REPL POS 2 TYRE DAMAGE | mechanical, true | mechanical, false |
| M41 | CC708 REPL POS 2 TYRE DAMAGE | mechanical, true | quality, false |
| M49 | AN426 REMOVE/RESEAL TRANSFER PUMP TBC | mechanical, false | other, false |
| M50 | OQ524 REPLACE RADIATOR | mechanical, false | other, false |
| M54 | UN7986 coolant leak from water pump pipe | mechanical, true | mechanical, false |
| M59 | 3M Mech Cond Ball Stut Crack Test JZ9248 | other, false | mechanical, false |
| M59 | 3M Mech Cond Ball Stut Crack Test JZ9248 | other, false | mechanical, true |
