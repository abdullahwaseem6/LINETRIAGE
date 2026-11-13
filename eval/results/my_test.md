# Real-data test: my_test

2026-11-13 · model `claude-haiku-5-5` · `real_test.csv` · 150 real notes × 3 runs = 450 runs

Real maintenance notes from Australian mining companies ([MaintNorm](https://github.com/nlp-tlp/maintnorm), MIT).
Labels drafted by Claude Opus, pending human review. Only `fault_type` and `safety_involved` are scored.

| Metric | Result |
|---|---|
| **Safety recall** | **94.3%** (150/159 runs) |
| False safety alarms | 14.4% (42/291 runs) |
| `fault_type` accuracy | 77.1% |
| Same answer on every run | 81.3% of notes |
| Failed extractions | 0 |

## Disagreements

| Note | Text | Label (fault, safety) | Haiku (fault, safety) |
|---|---|---|---|
| T004 | DCS Boom press monitoring system improve | sensor, false | other, false |
| T008 | CC708 replace trans ECM see long text | electrical, false | other, false |
| T010 | CC708 PXG33 Repair fuel hoses see text | mechanical, false | mechanical, true |
| T016 | ND5744 Replace fuel tank vent valve | mechanical, false | other, false |
| T019 | CC708 TZM57 Steering pin no grease TEXT | mechanical, false | mechanical, true |
| T023 | BF079 REPLACE FUEL LINES | mechanical, false | other, false |
| T024 | drag rope slipping throgh socket | mechanical, true | mechanical, false |
| T027 | MB119 REPAIR LIGHTS | electrical, false | electrical, true |
| T027 | MB119 REPAIR LIGHTS | electrical, false | other, false |
| T032 | BT0391-C/out Turbo Primary LFT FRNT | mechanical, false | other, false |
| T037 | Carry out general lighting repairs | electrical, false | other, false |
| T039 | BF079 FIT SAFETY RAIL SYSTEM TBC | other, false | safety, true |
| T042 | XH531 REPL CRACKED DOOR WINDOW TEXT | mechanical, true | other, true |
| T043 | 5635 Bucket Overhaul-Mechanical BKT # 1 | other, false | mechanical, false |
| T044 | CC708 - Change Out Bucket GET | mechanical, false | other, false |
| T048 | Split cable for shot | other, false | electrical, true |
| T050 | Crack at boom point of 526 | mechanical, false | mechanical, true |
| T051 | CR871 REPLACE BUCKET JOYSTICK | mechanical, false | other, false |
| T054 | WJ525 REPL POS 3+4 FINAL DRIVE ASSY | mechanical, false | other, false |
| T055 | house lights out | electrical, false | other, false |
| T056 | MB119 ENGINE SHUTTING DOWN | other, false | mechanical, false |
| T060 | AF5037-C/out Fuel Transfer Pump | mechanical, false | other, false |
| T061 | LD3192 Reseal main water pump mount | mechanical, false | other, false |
| T063 | rear module work lights loose | electrical, false | mechanical, true |
| T064 | xw7695 repair headlight fault | electrical, false | electrical, true |
| T064 | xw7695 repair headlight fault | electrical, false | other, false |
| T065 | Hoist Brake Switch operation | electrical, true | other, true |
| T066 | PH639 REPL WORN OUT THROTTLE PEDAL ASSY | mechanical, false | mechanical, true |
| T067 | BD3257- door spring pivot u/s | mechanical, false | mechanical, true |
| T072 | replace 209 under bench down light | electrical, false | other, false |
| T073 | Mast pendant ropes replacment | mechanical, false | other, false |
| T077 | Re-fit Tool to measure foot movement | other, false | sensor, false |
| T081 | PH639 REPL NEUTRALIZER MICRO SWITCH | safety, true | sensor, false |
| T083 | BP504 HYD OIL BYPASSING INTO TRANS | mechanical, false | mechanical, true |
| T084 | GU245 REPLACE RADIATOR | mechanical, false | other, false |
| T093 | XH531 Repair to battery cover | mechanical, false | other, false |
| T095 | WK1566 Cooling system pressurising REPL | mechanical, false | mechanical, true |
| T097 | REAR DIFF YOKE | mechanical, false | other, false |
| T098 | XH531 REPAIR BRAKE FAULT | mechanical, true | other, true |
| T098 | XH531 REPAIR BRAKE FAULT | mechanical, true | safety, true |
| T100 | sight glass replace | mechanical, false | other, false |
| T101 | Replace conduits on fan motors | electrical, false | other, false |
| T106 | MR0229 Crack in headboard | mechanical, false | other, false |
| T110 | heater hoses at bottom front of cab u/s | mechanical, false | mechanical, true |
| T113 | AI9714 lights need aligning/cv replaced | electrical, false | mechanical, false |
| T113 | AI9714 lights need aligning/cv replaced | electrical, false | mechanical, true |
| T115 | AF5037 2way unit is loose needs tighten | other, false | mechanical, false |
| T116 | C/O upper hoist chains | mechanical, false | other, false |
| T118 | AF5037 Steering oil temp faults | sensor, true | mechanical, true |
| T120 | Loose Drivers Mirror Post | mechanical, false | mechanical, true |
| T121 | XH531 REPLACE DAMAGED WINDOW | mechanical, true | other, true |
| T123 | RHR tremmel wheel snapped off | mechanical, false | mechanical, true |
| T124 | Flashing light U/S replaced | electrical, false | safety, true |
| T126 | BF079 REPLACE FIRE EXTINGUISHERS | safety, true | other, false |
| T130 | I cutting edges falling off | mechanical, false | mechanical, true |
| T132 | NS867=EPW 65304 REPAIR GAS TESTER | safety, true | sensor, false |
| T132 | NS867=EPW 65304 REPAIR GAS TESTER | safety, true | sensor, true |
| T134 | FN5736 Replace Fuel Breather | mechanical, false | other, false |
| T135 | Repair RHS top rail crack | safety, true | mechanical, true |
| T137 | DU7016 blowing smoke | mechanical, false | electrical, true |
| T145 | TO0487 Tray coming down hard fault | mechanical, true | mechanical, false |
| T147 | AN426 REPORTS TRANY OIL IS BLACK REPORT | mechanical, false | other, false |
| T150 | ZA339 REPAIR FUEL FAULT | other, false | other, true |
