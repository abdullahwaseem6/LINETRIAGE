# Later

Ideas to revisit after Phase 7.

- Separate `machine_component` field for the machine part that failed (maintenance stats).
- Allow more than one fault per report (a list of faults). Today a note with two faults keeps only the more serious one, which made R40 miss its escalation in the baseline.
- Use MaintIE (data/real/maintie) expert entity labels as an independent fault-type check. Its text is normalised (cleaner than raw notes) and has no safety labels.
- Have a human (or a second, non-Claude model) label the real test notes and report agreement; then a final test on a fresh set of MaintNorm notes.
