# Real-data test: real_test_v3

2026-11-13 · model `claude-haiku-5-5` · `real_test.csv` · 150 real notes × 3 runs = 450 runs

Real maintenance notes from Australian mining companies ([MaintNorm](https://github.com/nlp-tlp/maintnorm), MIT).
Labels drafted by Claude Opus, pending human review. Only `fault_type` and `safety_involved` are scored.

| Metric | Result |
|---|---|
| **Safety recall** | **90.5%** (152/168 runs) |
| False safety alarms | 13.1% (37/282 runs) |
| `fault_type` accuracy | 82.4% |
| Same answer on every run | 86.0% of notes |
| Failed extractions | 0 |

## Disagreements

| Note | Text | Label (fault, safety) | Haiku (fault, safety) |
|---|---|---|---|
| T004 | DCS Boom press monitoring system improve | sensor, false | other, false |
| T019 | CC708 TZM57 Steering pin no grease TEXT | mechanical, false | mechanical, true |
| T024 | drag rope slipping throgh socket | mechanical, true | mechanical, false |
| T027 | MB119 REPAIR LIGHTS | electrical, false | other, false |
| T035 | RH DOOR OPENING MECHANISM FAULTY | mechanical, false | mechanical, true |
| T037 | Carry out general lighting repairs | electrical, false | other, false |
| T039 | BF079 FIT SAFETY RAIL SYSTEM TBC | other, false | safety, true |
| T042 | XH531 REPL CRACKED DOOR WINDOW TEXT | mechanical, true | other, true |
| T043 | 5635 Bucket Overhaul-Mechanical BKT # 1 | other, false | mechanical, false |
| T044 | CC708 - Change Out Bucket GET | mechanical, false | other, false |
| T048 | Split cable for shot | other, false | electrical, true |
| T050 | Crack at boom point of 526 | mechanical, false | mechanical, true |
| T051 | CR871 REPLACE BUCKET JOYSTICK | mechanical, false | other, false |
| T055 | house lights out | electrical, false | other, false |
| T062 | VistaCam system not working | sensor, true | sensor, false |
| T063 | rear module work lights loose | electrical, false | mechanical, false |
| T065 | Hoist Brake Switch operation | electrical, true | other, true |
| T070 | hm5190 emergency ladder repairs | safety, true | other, true |
| T072 | replace 209 under bench down light | electrical, false | other, false |
| T073 | Mast pendant ropes replacment | mechanical, false | other, false |
| T077 | Re-fit Tool to measure foot movement | other, false | sensor, false |
| T079 | BR8769 oil cap missing | mechanical, false | mechanical, true |
| T081 | PH639 REPL NEUTRALIZER MICRO SWITCH | safety, true | sensor, false |
| T082 | engine exh flex / pipe & rain cap u/s | mechanical, false | mechanical, true |
| T083 | BP504 HYD OIL BYPASSING INTO TRANS | mechanical, false | mechanical, true |
| T093 | XH531 Repair to battery cover | mechanical, false | other, false |
| T095 | WK1566 Cooling system pressurising REPL | mechanical, false | mechanical, true |
| T097 | REAR DIFF YOKE | mechanical, false | other, false |
| T100 | sight glass replace | mechanical, false | other, false |
| T101 | Replace conduits on fan motors | electrical, false | other, false |
| T106 | MR0229 Crack in headboard | mechanical, false | other, false |
| T106 | MR0229 Crack in headboard | mechanical, false | other, true |
| T110 | heater hoses at bottom front of cab u/s | mechanical, false | mechanical, true |
| T113 | AI9714 lights need aligning/cv replaced | electrical, true | mechanical, false |
| T113 | AI9714 lights need aligning/cv replaced | electrical, true | mechanical, true |
| T115 | AF5037 2way unit is loose needs tighten | other, false | mechanical, false |
| T116 | C/O upper hoist chains | mechanical, false | other, false |
| T118 | AF5037 Steering oil temp faults | sensor, true | mechanical, true |
| T120 | Loose Drivers Mirror Post | mechanical, false | mechanical, true |
| T121 | XH531 REPLACE DAMAGED WINDOW | mechanical, true | other, true |
| T123 | RHR tremmel wheel snapped off | mechanical, false | mechanical, true |
| T124 | Flashing light U/S replaced | electrical, false | electrical, true |
| T126 | BF079 REPLACE FIRE EXTINGUISHERS | safety, true | other, false |
| T130 | I cutting edges falling off | mechanical, false | mechanical, true |
| T132 | NS867=EPW 65304 REPAIR GAS TESTER | safety, true | sensor, false |
| T132 | NS867=EPW 65304 REPAIR GAS TESTER | safety, true | sensor, true |
| T134 | FN5736 Replace Fuel Breather | mechanical, false | other, false |
| T137 | DU7016 blowing smoke | mechanical, false | electrical, true |
| T145 | TO0487 Tray coming down hard fault | mechanical, true | mechanical, false |
| T150 | ZA339 REPAIR FUEL FAULT | other, false | other, true |
