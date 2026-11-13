# Acceptance criteria — Capstone (Unit 9)

Five criteria for this unit's extension to Provenance Guard, written before
any capstone results existed. (Unit 7/8's original five criteria are
preserved in git history at commit `23bf34e` and the unit 7/8 README
sections — this file now holds only the capstone's own five.)

**Shape C — add one capability:** a third detection signal, `phrasing.py`,
measuring density of generic AI transition/hedge phrases ("furthermore",
"in conclusion", "it is important to note"). It's wired into
`scoring.combine_signals` as a third input alongside the existing model and
style signals, and into the audit log and `/submit` response. Instrumentation
(`duration_ms` on every log entry) and a cost measurement are new this unit
too, and apply regardless of shape.

---

## 1. The phrasing signal fires on templated text

Text containing at least 4 of the listed transition/hedge phrases per 100
words scores `phrasing_score >= 0.9` in at least 9 of 10 submissions.

**Why this target:** a signal that can't reach its own high end on text built
specifically to trigger it isn't adding real separation — this is the
reachability check Milestone 5 ran on the two existing labels, applied to the
new third signal before it's trusted anywhere downstream.

## 2. The phrasing signal stays quiet on plain writing

Plain narrative text containing none of the listed phrases scores
`phrasing_score <= 0.1` in at least 9 of 10 submissions.

**Why this target:** the signal is only useful if it's quiet on ordinary
writing — if it fires on text that never uses any of its trigger phrases, it
isn't measuring phrasing, it's measuring something else by accident, and
every downstream combined score inherits that noise for free.

## 3. Warm requests stay fast with the third signal added

Once the detector model is loaded (after the first request), `/submit`
returns within 200ms, with `duration_ms` in both the response and the audit
log entry, in at least 9 of 10 trials.

**Why this target:** `phrasing.py` adds a third pure-Python pass over the
text on every request. 200ms leaves wide margin above the ~45-105ms observed
in a pre-test bench of 6 warm requests on this signal's dev machine — if
adding the third signal pushed latency past that margin, the extension would
be measurably changing the run path's cost, not just its output.

## 4. Cost per run stays under a fixed compute ceiling

Average wall-clock duration across 10 warm `/submit` requests stays under
150ms, measured directly from logged `duration_ms` values (not estimated).

**Why this target:** this service has no API spend — its real cost is CPU
time on whatever machine runs it. 150ms per run keeps the hundred-a-day
compute cost trivial (see **What It Costs** in the README for the
arithmetic), and a number drawn from real logged runs is the only honest way
to claim a cost, rather than a guess from the code's shape.

## 5. Malformed input never crashes the service, and the rejection is timed

Submitting `text` missing, `text` empty, and `text` over 100,000 characters
each return a `400` (never a `500`) in 5 of 5 trials per case, and each
rejection produces a `logs/audit.jsonl` entry with `event: "rejected"` and a
non-null `duration_ms`.

**Why this target:** this is the bad-path criterion every unit needs, and
this unit specifically checks that the new `duration_ms` instrumentation
covers the rejection path too, not just successful decisions — a failure
that's invisible to the clock is still invisible.
