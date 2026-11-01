# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives on my own plain writing

Of 10 short pieces I write myself in plain, ordinary language (no jargon, no
flourishes), at most 1 is labeled `high-confidence AI`. A reader can check
this by submitting the 10 pieces to `POST /submit` and counting how many come
back with `guess: "ai"`.

**Why this target:** My model signal (`detector.py`) rewards common words in
short sentences, and plain writing is exactly that. A wrong `ai` accusation
costs a real writer their trust in the platform; a missed AI submission costs
the site almost nothing. I'd rather tolerate some AI text slipping through
than falsely accuse 2 or more of 10 honest writers.

---

## 2. Score spread between clearly-AI and clearly-human text

A piece of text I'm confident is AI-generated (dense GPT-style filler, no
edits) and a piece I'm confident is human (something I wrote off the cuff,
typos included) must land at least 0.4 apart on the combined `confidence`
score returned by `POST /submit`. A reader can submit both and subtract the
two `confidence` values.

**Why this target:** If clearly-different inputs land close together, the
combined score isn't actually separating anything and every label downstream
is arbitrary. 0.4 is roughly the width of the "unsure" band itself
(`HUMAN_THRESHOLD` to `AI_THRESHOLD` in `config.py`), so clearly-opposite
cases shouldn't both be able to fall inside it.

---

## 3. All three labels are reachable

Each of the three labels — `high-confidence human`, `unsure`, and
`high-confidence AI` — must be producible by at least one real input, not
just by a score that happens to exist on paper. A reader can run
`scoring.label_ranges()` to see the configured bands, then submit one piece
of text per band and confirm the `label` field in the response matches.

**Why this target:** A label with no reachable input is a sentence nobody
will ever read, which means the hardest part of this project — writing the
"unsure" text honestly — is wasted if the scoring never actually lands there.
I set this as pass/fail rather than a rate, because reachability is binary:
either a path to it exists or it doesn't.

---

## 4. The appeal path always changes status and is always recorded

Every call to `POST /appeal` with a valid, existing `content_id` must (a)
return a 200 with `status: "under_review"`, and (b) produce a new entry in
`logs/audit.jsonl` with `status: "under_review"` next to the original
decision, in 5 out of 5 trials. A reader can submit, appeal, then call
`GET /log` and check both.

**Why this target:** The appeal path is the only thing standing between a
wrong accusation and nothing at all — if it silently no-ops even once, a
writer who was wrongly flagged has no recourse and no way to know their
appeal didn't go through. This is the one criterion where I require 5 of 5,
not "mostly," because a sometimes-working appeal button is functionally the
same as having none.

---

## 5. Bad input never crashes the service

Submitting a request with `text` missing, `text` as an empty string, and
`text` over 100,000 characters must each return a `400` with a JSON error
body — never a `500`, and never a response with no `content_id` where one
was expected. A reader can send all three and check the status code and that
`/ping` still answers afterward.

**Why this target:** A crash on malformed input is one of the most common
real failures a service like this sees, and unit 8's attack set is built to
probe exactly this kind of edge. A clear 400 tells an integrator what went
wrong; a 500 looks identical to the whole service being down and sends
whoever's debugging it straight to `/ping` for nothing.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
