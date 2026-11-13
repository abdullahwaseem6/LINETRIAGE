# Evaluation: after_review

2026-11-13 · model `claude-haiku-5-5` · 60 reports × 3 runs = 180 runs

## Headline

| Metric | Result |
|---|---|
| **Safety recall** | **100.0%** (45/45 safety runs caught) |
| False safety alarms | 3 runs |
| Route accuracy | 98.3% |
| Same route on every run | 100.0% of reports |
| Same facts on every run | 93.3% of reports |
| Failed extractions | 0 runs |
| Latency | 2.0s average, 2.9s p95 |
| Cost per 1,000 reports | $0.33 |

## Accuracy per field

| Field | Accuracy |
|---|---|
| `station_id` | 98.9% |
| `fault_type` | 95.6% |
| `downtime_minutes` | 97.8% |
| `recurring` | 100.0% |
| `safety_involved` | 98.3% |
| `affected_part` | 100.0% |
| `language` | 100.0% |

## Wrong answers (17)

Every run with a wrong route or at least one wrong field. Full details in `after_review_errors.jsonl`.

| Report | Run | Route (expected → got) | Wrong fields |
|---|---|---|---|
| R01 | 1 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R01 | 2 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R01 | 3 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R13 | 2 | human_review | `station_id`: 'Linie 12' → 'linie 12' |
| R13 | 3 | human_review | `station_id`: 'Linie 12' → 'linie 12' |
| R38 | 1 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R38 | 2 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R43 | 1 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R43 | 2 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R43 | 3 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R46 | 1 | escalate_quality | `fault_type`: 'mechanical' → 'electrical' |
| R46 | 2 | escalate_quality | `fault_type`: 'mechanical' → 'other' |
| R46 | 3 | escalate_quality | `fault_type`: 'mechanical' → 'other' |
| R49 | 1 | safety_alert | `downtime_minutes`: 0 → None |
| R49 | 2 | safety_alert | `downtime_minutes`: 0 → None |
| R49 | 3 | safety_alert | `downtime_minutes`: 0 → None |
| R56 | 2 | safety_alert | `downtime_minutes`: None → 0 |
