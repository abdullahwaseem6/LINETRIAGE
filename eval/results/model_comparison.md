# Model comparison: LLM vs small model

150 real MaintNorm test notes (`data/real/real_test.csv`), never used for training or tuning the small model.
The small model was trained on 1,076 different real notes labelled by Haiku (distillation).

| | Safety recall | False safety alarms | Missed dangerous notes | `fault_type` accuracy | Time per note | Cost per 1,000 notes |
|---|---|---|---|---|---|---|
| **Haiku (LLM teacher)** | **92.3%** | 13.1% | 4.3 of 56 | 81.3% | ~2,000 ms | $0.39 |
| **Small model** (TF-IDF + logistic regression) | **94.6%** | 53.2% | 3 of 56 | 74.7% | 0.87 ms | $0 |
| **Either flags it** (second opinion) | **98.2%** | 55.3% | 1.0 of 56 | | ~2,000 ms | $0.39 |

Haiku numbers are averaged over 3 runs. The small model's safety threshold (0.18) was picked on the validation set to catch at least 95% of dangerous notes there.

## The fair comparison: same false-alarm level

The small model's high recall comes from flagging over half of all safe notes. Its safety score can be cut at any threshold; here is the trade-off on the test set (shown for reading only; the threshold in the table above was chosen on validation):

| Small model threshold | Safety recall | False alarms |
|---|---|---|
| 0.18 (chosen on validation) | 94.6% | 53.2% |
| 0.30 | 89.3% | 36.2% |
| 0.40 | 78.6% | 22.3% |
| 0.50 | 75.0% | 11.7% |
| 0.60 | 73.2% | 6.4% |

At about Haiku's false-alarm level (~12%), the small model catches **75%** of dangerous notes against Haiku's **92%**. It's free and about 2,000× faster, but clearly worse.

**Best use:** as a **second opinion**. Flag a note if *either* Haiku or the small model says dangerous: recall rises from 92.3% to **98.2%** (1 missed note per pass instead of 4), at the cost of many more false alarms (55%). Whether that's worth it is a business decision: how much does a supervisor's minute cost against a missed brake fault?

## Dangerous notes the small model missed

- AN426 REPLACE AFFF BOTTLE GAUGE
- Seat belt u/s
- VistaCam system not working

## Fault type: confusion matrix

Rows are the correct label, columns what the model said. The diagonal is correct.

**Small model**

| label ↓ / predicted → | mechanical | electrical | sensor | quality | safety | other |
|---|---|---|---|---|---|---|
| **mechanical** | 70 | 0 | 0 | 1 | 1 | 13 |
| **electrical** | 1 | 13 | 0 | 0 | 0 | 6 |
| **sensor** | 2 | 0 | 3 | 0 | 1 | 0 |
| **quality** | 0 | 0 | 0 | 0 | 0 | 0 |
| **safety** | 2 | 0 | 1 | 0 | 6 | 3 |
| **other** | 6 | 0 | 1 | 0 | 0 | 20 |

**Haiku** (all 3 runs)

| label ↓ / predicted → | mechanical | electrical | sensor | safety | other |
|---|---|---|---|---|---|
| **mechanical** | 217 | 2 | 0 | 0 | 36 |
| **electrical** | 6 | 39 | 0 | 0 | 15 |
| **sensor** | 3 | 0 | 12 | 0 | 3 |
| **safety** | 0 | 0 | 5 | 27 | 4 |
| **other** | 4 | 3 | 1 | 2 | 71 |
