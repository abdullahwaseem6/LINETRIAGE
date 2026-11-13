# Evaluation: factory_v3

2026-11-13 · model `claude-haiku-5-5` · 60 reports × 3 runs = 180 runs

## Headline

| Metric | Result |
|---|---|
| **Safety recall** | **100.0%** (45/45 safety runs caught) |
| False safety alarms | 4 runs |
| Route accuracy | 97.2% |
| Same route on every run | 96.7% of reports |
| Same facts on every run | 85.0% of reports |
| Failed extractions | 0 runs |
| Latency | 2.0s average, 2.9s p95 |
| Cost per 1,000 reports | $0.39 |

## Accuracy per field

| Field | Accuracy |
|---|---|
| `station_id` | 98.3% |
| `fault_type` | 90.6% |
| `downtime_minutes` | 98.3% |
| `recurring` | 100.0% |
| `safety_involved` | 97.8% |
| `affected_part` | 100.0% |
| `language` | 99.4% |

## Wrong answers (28)

Every run with a wrong route or at least one wrong field. Full details in `factory_v3_errors.jsonl`.

| Report | Run | Route (expected → got) | Wrong fields |
|---|---|---|---|
| R01 | 1 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R01 | 2 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R01 | 3 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R06 | 1 | **auto_ticket → human_review** | `station_id`: 'ST-09' → None |
| R13 | 2 | human_review | `station_id`: 'Linie 12' → 'linie 12' |
| R15 | 2 | auto_ticket | `language`: 'mixed' → 'de' |
| R20 | 1 | human_review | `fault_type`: 'mechanical' → 'other' |
| R20 | 2 | human_review | `fault_type`: 'mechanical' → 'other' |
| R29 | 1 | human_review | `fault_type`: 'other' → 'sensor' |
| R29 | 2 | human_review | `fault_type`: 'other' → 'sensor' |
| R29 | 3 | human_review | `fault_type`: 'other' → 'sensor' |
| R31 | 3 | human_review | `station_id`: None → 'Halle B' |
| R32 | 1 | **human_review → safety_alert** | `safety_involved`: False → True |
| R35 | 3 | auto_ticket | `fault_type`: 'sensor' → 'mechanical' |
| R38 | 1 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R38 | 2 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R43 | 1 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R43 | 2 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R43 | 3 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R46 | 1 | escalate_quality | `fault_type`: 'mechanical' → 'other' |
| R46 | 2 | escalate_quality | `fault_type`: 'mechanical' → 'other' |
| R46 | 3 | escalate_quality | `fault_type`: 'mechanical' → 'other' |
| R49 | 1 | safety_alert | `downtime_minutes`: 0 → None |
| R49 | 2 | safety_alert | `downtime_minutes`: 0 → None |
| R49 | 3 | safety_alert | `downtime_minutes`: 0 → None |
| R54 | 1 | safety_alert | `fault_type`: 'mechanical' → 'safety' |
| R54 | 2 | safety_alert | `fault_type`: 'mechanical' → 'other' |
| R54 | 3 | safety_alert | `fault_type`: 'mechanical' → 'other' |
