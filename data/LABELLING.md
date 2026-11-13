# Labelling guide

How to fill in the `expected` fields for each report in `reports.jsonl`.

## fault_type

What physically went wrong:

| Value | Use for |
|---|---|
| `mechanical` | Moving parts, belts, hydraulics, leaks |
| `electrical` | Power, cables, breakers, overheating, burning smell |
| `sensor` | Sensors, cameras, scanners, measuring devices |
| `quality` | Bad parts or batches produced |
| `other` | Unclear, or none of the above |
| `safety` | **Only** when a safety device itself is broken, removed or bypassed (guard, interlock, light curtain, emergency stop), or a person was hurt |

A slip hazard from an oil leak is `mechanical`, not `safety`. The leak is what went wrong; the risk is recorded in `safety_involved`.

## station_id

`"ST-NN"` when the station is clear ("st6", "6os allomas", "Station 6" → `"ST-06"`). A station that doesn't exist is still written in that form ("st 11" → `"ST-11"`), or as written if it isn't a number ("Linie 12"). `null` if no station is mentioned, or if it's ambiguous ("the assembly line" when there are two).

## safety_involved

`true` whenever anyone could get hurt, whatever the `fault_type`. Read for hidden risks in casual notes: a removed guard, a burning smell, overheating (fire risk), a leak onto the floor (slip risk), someone slipping, even if the line kept running.

## recurring

`true` if the note says it happened before ("again", "megint", "schon wieder", "3rd time"), or that it happened more than once in this note ("3 times today", "stopped twice", "keeps tripping").

## downtime_minutes

- `0` if the note says the line didn't stop.
- `null` if it's too vague to give a number ("few min idk", "keine ahnung wie lang").
- `null` also for vague amounts with no number: "a bit", "a while", "most of the morning".
- Otherwise the best number: "half an hour" / "fél óra" = 30, "quarter hour" / "negyed óra" = 15, "three quarters of an hour" = 45, "almost an hour" = 60, "all shift" = 480, "2 hrs" = 120, "like 20 min maybe" = 20.
- For a range ("10-15 min"), take the higher number.

## affected_part

The product being made: a part, component or batch, in English and short ("bracket", "housing"). Never the machine, station or tool, so "spindle", "conveyor belt", "torque wrench" or "barcode scanner" are `null`. Only fill it in if a specific product part or batch is named; otherwise `null`.

## Two faults in one note

Label the more serious fault: a safety problem beats a quality problem, which beats the fault that stopped the line. `safety_involved` is `true` if either fault could hurt someone. `affected_part` can come from either fault.
