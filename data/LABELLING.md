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

## safety_involved

`true` whenever anyone could get hurt, whatever the `fault_type`. Read for hidden risks in casual notes: a removed guard, a burning smell, someone slipping, even if the line kept running.

## recurring

`true` if the note says it happened before: "again", "megint", "schon wieder", "3rd time".

## downtime_minutes

- `0` if the note says the line didn't stop.
- `null` if it's too vague to give a number ("few min idk", "keine ahnung wie lang").
- Otherwise the best number: "half an hour" / "fél óra" = 30, "2 hrs" = 120, "like 20 min maybe" = 20.

## affected_part

The product being made: a part, component or batch, in English and short ("bracket", "housing"). Never the machine, station or tool, so "spindle", "conveyor belt", "torque wrench" or "barcode scanner" are `null`. Only fill it in if a specific product part or batch is named; otherwise `null`.
