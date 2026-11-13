# Evaluation: baseline

2026-11-13 · model `claude-haiku-5-5` · 60 reports × 3 runs = 180 runs

## Headline

| Metric | Result |
|---|---|
| **Safety recall** | **100.0%** (39/39 safety runs caught) |
| False safety alarms | 6 runs |
| Route accuracy | 95.0% |
| Same route on every run | 100.0% of reports |
| Same facts on every run | 78.3% of reports |
| Failed extractions | 0 runs |
| Latency | 3.3s average, 3.9s p95 |
| Cost per 1,000 reports | $0.26 |

## Accuracy per field

| Field | Accuracy |
|---|---|
| `station_id` | 97.8% |
| `fault_type` | 90.6% |
| `downtime_minutes` | 91.7% |
| `recurring` | 99.4% |
| `safety_involved` | 96.7% |
| `affected_part` | 92.8% |
| `language` | 96.1% |

## Wrong answers (56)

Every run with a wrong route or at least one wrong field. Full details in `baseline_errors.jsonl`.

| Report | Run | Route (expected → got) | Wrong fields |
|---|---|---|---|
| R04 | 1 | escalate_quality | `affected_part`: 'bracket' → 'bracket batch' |
| R04 | 2 | escalate_quality | `affected_part`: 'bracket' → 'bracket batch'; `language`: 'en' → 'mixed' |
| R04 | 3 | escalate_quality | `affected_part`: 'bracket' → 'bracket batch' |
| R09 | 2 | escalate_quality | `downtime_minutes`: 30 → 60 |
| R09 | 3 | escalate_quality | `downtime_minutes`: 30 → 60 |
| R13 | 1 | human_review | `station_id`: 'Linie 12' → 'linie 12' |
| R13 | 2 | human_review | `station_id`: 'Linie 12' → 'ST-12' |
| R13 | 3 | human_review | `station_id`: 'Linie 12' → None |
| R18 | 1 | safety_alert | `downtime_minutes`: 0 → None |
| R18 | 2 | safety_alert | `downtime_minutes`: 0 → None |
| R18 | 3 | safety_alert | `downtime_minutes`: 0 → None |
| R24 | 3 | escalate_quality | `downtime_minutes`: 15 → 13 |
| R26 | 1 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R26 | 2 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R26 | 3 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R27 | 1 | auto_ticket | `fault_type`: 'other' → 'mechanical'; `downtime_minutes`: 480 → None |
| R27 | 2 | auto_ticket | `fault_type`: 'other' → 'mechanical'; `downtime_minutes`: 480 → None |
| R27 | 3 | auto_ticket | `fault_type`: 'other' → 'mechanical'; `downtime_minutes`: 480 → None |
| R34 | 1 | human_review | `station_id`: 'ST-00' → None |
| R36 | 1 | safety_alert | `affected_part`: 'bracket' → 'brackets' |
| R36 | 2 | safety_alert | `affected_part`: 'bracket' → 'brackets' |
| R36 | 3 | safety_alert | `affected_part`: 'bracket' → 'brackets' |
| R37 | 1 | **escalate_quality → safety_alert** | `fault_type`: 'quality' → 'mechanical'; `safety_involved`: False → True |
| R37 | 2 | **escalate_quality → safety_alert** | `safety_involved`: False → True; `affected_part`: 'housing' → 'housings' |
| R37 | 3 | **escalate_quality → safety_alert** | `safety_involved`: False → True |
| R38 | 1 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R38 | 2 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R38 | 3 | auto_ticket | `fault_type`: 'mechanical' → 'other' |
| R39 | 1 | safety_alert | `recurring`: True → False |
| R40 | 1 | **escalate_quality → auto_ticket** | `fault_type`: 'quality' → 'sensor' |
| R40 | 2 | **escalate_quality → auto_ticket** | `fault_type`: 'quality' → 'sensor' |
| R40 | 3 | **escalate_quality → auto_ticket** | `fault_type`: 'quality' → 'sensor' |
| R43 | 1 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R43 | 2 | auto_ticket | `fault_type`: 'electrical' → 'other' |
| R44 | 3 | escalate_quality | `fault_type`: 'other' → 'mechanical' |
| R45 | 1 | auto_ticket | `language`: 'de' → 'mixed' |
| R45 | 2 | auto_ticket | `language`: 'de' → 'mixed' |
| R45 | 3 | auto_ticket | `language`: 'de' → 'mixed' |
| R46 | 1 | escalate_quality | `fault_type`: 'mechanical' → 'electrical' |
| R46 | 2 | escalate_quality | `fault_type`: 'mechanical' → 'electrical' |
| R46 | 3 | escalate_quality | `fault_type`: 'mechanical' → 'other' |
| R47 | 1 | escalate_quality | `affected_part`: 'bracket' → 'brackets' |
| R47 | 2 | escalate_quality | `affected_part`: 'bracket' → 'brackets' |
| R47 | 3 | escalate_quality | `affected_part`: 'bracket' → 'brackets' |
| R48 | 1 | auto_ticket | `language`: 'mixed' → 'hu' |
| R48 | 2 | auto_ticket | `language`: 'mixed' → 'hu' |
| R48 | 3 | auto_ticket | `language`: 'mixed' → 'hu' |
| R49 | 1 | safety_alert | `downtime_minutes`: 0 → None |
| R53 | 1 | safety_alert | `downtime_minutes`: None → 0 |
| R53 | 3 | safety_alert | `downtime_minutes`: None → 0 |
| R56 | 1 | safety_alert | `downtime_minutes`: None → 0 |
| R56 | 2 | safety_alert | `fault_type`: 'safety' → 'other'; `downtime_minutes`: None → 0 |
| R56 | 3 | safety_alert | `downtime_minutes`: None → 0 |
| R60 | 1 | escalate_quality | `affected_part`: 'door panel' → 'door panels' |
| R60 | 2 | escalate_quality | `affected_part`: 'door panel' → 'door panels' |
| R60 | 3 | escalate_quality | `affected_part`: 'door panel' → 'door panels' |
