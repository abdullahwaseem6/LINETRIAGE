# Evaluation: after_real_rules

2026-11-13 · model `claude-haiku-5-5` · 60 reports × 3 runs = 180 runs

## Headline

| Metric | Result |
|---|---|
| **Safety recall** | **100.0%** (45/45 safety runs caught) |
| False safety alarms | 4 runs |
| Route accuracy | 96.7% |
| Same route on every run | 96.7% of reports |
| Same facts on every run | 88.3% of reports |
| Failed extractions | 0 runs |
| Latency | 2.0s average, 2.9s p95 |
| Cost per 1,000 reports | $0.36 |

## Accuracy per field

| Field | Accuracy |
|---|---|
| `station_id` | 97.2% |
| `fault_type` | 94.4% |
| `downtime_minutes` | 97.2% |
| `recurring` | 100.0% |
| `safety_involved` | 97.8% |
| `affected_part` | 100.0% |
| `language` | 96.7% |

## Wrong answers (30)

Every run with a wrong route or at least one wrong field. Full details in `after_real_rules_errors.jsonl`.

| Report | Run | Route (expected → got) | Wrong fields |
|---|---|---|---|
| R01 | 1 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R01 | 2 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R01 | 3 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R06 | 2 | **auto_ticket → human_review** | `station_id`: 'ST-09' → None |
| R06 | 3 | **auto_ticket → human_review** | `station_id`: 'ST-09' → None |
| R13 | 1 | human_review | `station_id`: 'Linie 12' → 'linie 12' |
| R13 | 2 | human_review | `station_id`: 'Linie 12' → 'linie 12' |
| R13 | 3 | human_review | `station_id`: 'Linie 12' → 'linie 12' |
| R38 | 1 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R38 | 2 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R38 | 3 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R42 | 1 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R43 | 1 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R43 | 2 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R43 | 3 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R45 | 1 | auto_ticket | `language`: 'de' → 'mixed' |
| R45 | 3 | auto_ticket | `language`: 'de' → 'mixed' |
| R46 | 1 | escalate_quality | `fault_type`: 'mechanical' → 'electrical' |
| R46 | 2 | escalate_quality | `fault_type`: 'mechanical' → 'other' |
| R46 | 3 | escalate_quality | `fault_type`: 'mechanical' → 'electrical' |
| R47 | 1 | escalate_quality | `language`: 'en' → 'mixed' |
| R47 | 2 | escalate_quality | `language`: 'en' → 'mixed' |
| R47 | 3 | escalate_quality | `language`: 'en' → 'mixed' |
| R49 | 1 | safety_alert | `downtime_minutes`: 0 → None |
| R49 | 2 | safety_alert | `downtime_minutes`: 0 → None |
| R49 | 3 | safety_alert | `downtime_minutes`: 0 → None |
| R54 | 2 | safety_alert | `fault_type`: 'mechanical' → 'safety' |
| R55 | 3 | safety_alert | `language`: 'mixed' → 'en' |
| R56 | 1 | safety_alert | `downtime_minutes`: None → 0 |
| R56 | 3 | safety_alert | `downtime_minutes`: None → 0 |
