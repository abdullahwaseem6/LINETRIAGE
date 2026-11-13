# Real maintenance notes

`maintnorm/` holds the combined split of **MaintNorm**: 12,000 real maintenance short texts from three Australian mining and mineral processing companies (heavy mobile equipment). Identifiers are replaced with mock values by the authors.

- Source: https://github.com/nlp-tlp/maintnorm
- License: MIT (see `maintnorm/LICENSE.md`)
- Files are one word per line (`original<TAB>normalised`); a blank line ends a note.

`real_sample.csv` (dev set, 60 notes, used to improve the prompt) and `real_test.csv` (test set, 150 different notes, never used for tuning) come from the test split, picked by `scripts/sample_real.py` and labelled for `fault_type` and `safety_involved` using `../LABELLING.md`. **Labels were drafted by Claude Opus and still need a human review**; borderline cases are explained in the `notes` column.

These notes are used for testing only, never for training.
