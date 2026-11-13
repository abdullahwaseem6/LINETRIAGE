# Real-data test: real_test_before

2026-11-13 · model `claude-haiku-5-5` · `real_test.csv` · 150 real notes × 3 runs = 450 runs

Real maintenance notes from Australian mining companies ([MaintNorm](https://github.com/nlp-tlp/maintnorm), MIT).
Labels drafted by Claude Opus, pending human review. Only `fault_type` and `safety_involved` are scored.

| Metric | Result |
|---|---|
| **Safety recall** | **63.5%** (101/159 runs) |
| False safety alarms | 8.9% (26/291 runs) |
| `fault_type` accuracy | 71.8% |
| Same answer on every run | 75.3% of notes |
| Failed extractions | 0 |

## Disagreements

| Note | Text | Label (fault, safety) | Haiku (fault, safety) |
|---|---|---|---|
| T001 | CC0233 r/h rear axle fiter housing leak | mechanical, true | mechanical, false |
| T004 | DCS Boom press monitoring system improve | sensor, false | other, false |
| T005 | trace & repair hyd oil leak RH steer ram | mechanical, true | mechanical, false |
| T006 | UQ9701 hoist screen hose leaking | mechanical, true | mechanical, false |
| T007 | AN426 REPL CAB SEAT SHOCKIE | mechanical, false | other, false |
| T009 | LR2095 Trans hose leaks | mechanical, true | mechanical, false |
| T010 | CC708 PXG33 Repair fuel hoses see text | mechanical, false | mechanical, true |
| T012 | TQ598 REPL ALTERNATOR | electrical, false | other, false |
| T015 | OK5862 engine hard to start | other, false | mechanical, false |
| T016 | ND5744 Replace fuel tank vent valve | mechanical, false | other, false |
| T017 | BF079 REPL RH LEAKING LIFT CYLINDER | mechanical, true | mechanical, false |
| T024 | drag rope slipping throgh socket | mechanical, true | mechanical, false |
| T027 | MB119 REPAIR LIGHTS | electrical, false | other, false |
| T028 | both rear diff oils need replacing | other, false | mechanical, false |
| T031 | AN426 REPLACE AFFF BOTTLE GAUGE | safety, true | sensor, false |
| T032 | BT0391-C/out Turbo Primary LFT FRNT | mechanical, false | other, false |
| T034 | Seat belt u/s | safety, true | mechanical, false |
| T034 | Seat belt u/s | safety, true | other, false |
| T036 | WK1566 Fuel breather filter missing | mechanical, false | other, false |
| T036 | WK1566 Fuel breather filter missing | mechanical, false | quality, false |
| T037 | Carry out general lighting repairs | electrical, false | other, false |
| T039 | BF079 FIT SAFETY RAIL SYSTEM TBC | other, false | other, true |
| T039 | BF079 FIT SAFETY RAIL SYSTEM TBC | other, false | safety, true |
| T042 | XH531 REPL CRACKED DOOR WINDOW TEXT | mechanical, true | safety, true |
| T043 | 5635 Bucket Overhaul-Mechanical BKT # 1 | other, false | mechanical, false |
| T044 | CC708 - Change Out Bucket GET | mechanical, false | other, false |
| T048 | Split cable for shot | other, false | electrical, true |
| T050 | Crack at boom point of 526 | mechanical, false | mechanical, true |
| T051 | CR871 REPLACE BUCKET JOYSTICK | mechanical, false | other, false |
| T054 | WJ525 REPL POS 3+4 FINAL DRIVE ASSY | mechanical, false | other, false |
| T055 | house lights out | electrical, false | other, false |
| T056 | MB119 ENGINE SHUTTING DOWN | other, false | mechanical, false |
| T060 | AF5037-C/out Fuel Transfer Pump | mechanical, false | other, false |
| T063 | rear module work lights loose | electrical, false | mechanical, false |
| T063 | rear module work lights loose | electrical, false | mechanical, true |
| T064 | xw7695 repair headlight fault | electrical, false | other, false |
| T065 | Hoist Brake Switch operation | electrical, true | other, false |
| T065 | Hoist Brake Switch operation | electrical, true | other, true |
| T069 | 7897 Repair Walkways & Handrails | safety, true | other, true |
| T070 | hm5190 emergency ladder repairs | safety, true | other, true |
| T071 | MB119 PARK BRAKE WILL NOT RELEASE | mechanical, true | mechanical, false |
| T072 | replace 209 under bench down light | electrical, false | other, false |
| T077 | Re-fit Tool to measure foot movement | other, false | sensor, false |
| T080 | CR871 REPL MAIN STEERING PRESSURE HOSE | mechanical, true | mechanical, false |
| T081 | PH639 REPL NEUTRALIZER MICRO SWITCH | safety, true | sensor, false |
| T084 | GU245 REPLACE RADIATOR | mechanical, false | other, false |
| T090 | damaged cable work | electrical, true | electrical, false |
| T093 | XH531 Repair to battery cover | mechanical, false | other, false |
| T094 | PH639 REPLACE LHS LIFT CYL LEAK | mechanical, true | mechanical, false |
| T095 | WK1566 Cooling system pressurising REPL | mechanical, false | mechanical, true |
| T096 | 1000H Mech Insp Hyd Cyl Bucket RH TY8010 | other, false | mechanical, false |
| T097 | REAR DIFF YOKE | mechanical, false | other, false |
| T099 | XH1714 Replace Pos 4 brake cooling hose | mechanical, true | mechanical, false |
| T100 | sight glass replace | mechanical, false | other, false |
| T101 | Replace conduits on fan motors | electrical, false | other, false |
| T106 | MR0229 Crack in headboard | mechanical, false | quality, false |
| T107 | HF338 diagnose/repair slow steering | mechanical, true | mechanical, false |
| T108 | Swing brakes coming on now and then | mechanical, true | mechanical, false |
| T111 | XF3996 c/o blown pos 3 tyre | mechanical, true | mechanical, false |
| T112 | replace missing RH handrail bolt | safety, true | mechanical, true |
| T113 | AI9714 lights need aligning/cv replaced | electrical, false | sensor, false |
| T115 | AF5037 2way unit is loose needs tighten | other, false | mechanical, false |
| T118 | AF5037 Steering oil temp faults | sensor, true | mechanical, true |
| T121 | XH531 REPLACE DAMAGED WINDOW | mechanical, true | other, false |
| T121 | XH531 REPLACE DAMAGED WINDOW | mechanical, true | other, true |
| T123 | RHR tremmel wheel snapped off | mechanical, false | mechanical, true |
| T124 | Flashing light U/S replaced | electrical, false | other, false |
| T128 | 10000H Mech Insp Cam SFT BC4051 | other, false | sensor, false |
| T130 | I cutting edges falling off | mechanical, false | mechanical, true |
| T132 | NS867=EPW 65304 REPAIR GAS TESTER | safety, true | other, false |
| T132 | NS867=EPW 65304 REPAIR GAS TESTER | safety, true | sensor, false |
| T134 | FN5736 Replace Fuel Breather | mechanical, false | other, false |
| T135 | Repair RHS top rail crack | safety, true | mechanical, false |
| T135 | Repair RHS top rail crack | safety, true | other, true |
| T137 | DU7016 blowing smoke | mechanical, false | electrical, true |
| T138 | HF338 Park brake won't release | mechanical, true | mechanical, false |
| T139 | JA0341 Minor ENG oil leak top rear eng | mechanical, true | mechanical, false |
| T140 | WK1566 Replace leaking brake cooling hos | mechanical, true | mechanical, false |
| T141 | 526 # 3 air comp leaking from oil cooler | mechanical, true | mechanical, false |
| T144 | Resample oil on both compressors | other, false | mechanical, false |
| T145 | TO0487 Tray coming down hard fault | mechanical, true | mechanical, false |
| T146 | AF5037 Switch/control to overide pump u/ | electrical, false | other, false |
| T149 | NF4651 change out oil and filters BAD | other, false | mechanical, false |
| T150 | ZA339 REPAIR FUEL FAULT | other, false | other, true |
