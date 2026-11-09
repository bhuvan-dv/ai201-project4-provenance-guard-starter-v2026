# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

A piece of writing goes through seven steps before a reader sees anything:

1. **`POST /submit` arrives** with `{"text": ..., "creator_id": ...}`. If
   `text` is missing, empty, or over 100,000 characters, the request is
   rejected with a `400` and logged as a `rejected` entry — it never reaches
   a signal.
2. **Signal one runs** (`detector.model_signal`, in `detector.py`). A local
   language model (GPT-2) scores how predictable the text is and turns that
   into a 0–1 "model score," where higher means more likely AI.
3. **Signal two runs** (`stylometry.style_signal`, in `stylometry.py`). The
   text's sentence-length spread, vocabulary variety, and punctuation choices
   are measured and turned into a second, independent 0–1 "style score."
4. **The two scores combine** (`scoring.combine_signals`, in `scoring.py`)
   into one `confidence` score — a weighted average most of the time, biased
   toward the more human-reading signal when the two disagree sharply.
5. **The score becomes a label** (`scoring.score_to_label`, in
   `scoring.py`): `high-confidence human`, `unsure`, or `high-confidence AI`,
   each with full sentence text a non-technical reader can understand.
6. **The decision is logged** (`audit.log_decision`, in `audit.py`) to
   `logs/audit.jsonl` with a new `content_id`, both raw signal scores, the
   combined score, the label, and a `decided` status.
7. **The response goes back** to the caller with the `content_id`, `guess`,
   `confidence`, `label`, `model_score`, and `style_score` — everything
   needed to show the reader the label and, later, to appeal it with
   `POST /appeal`, which moves the item to `under_review` and records the
   writer's reasoning next to the original decision.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** `detector.model_signal` (in `detector.py`) runs a local
GPT-2 model over the text and measures its **perplexity** — how surprised the
model is by the actual sequence of words. That's turned into a 0–1 score
where higher means more likely AI.

**Why that might differ between human and AI writing:** A language model
writes by repeatedly picking a likely next word, so text it produces tends to
be text it (or a similar model) finds easy to predict. Human writing wanders
more — odd word choices, abrupt turns, the specific instead of the typical —
which tends to read as more "surprising" to the model.

**What it can't see:** It cannot tell predictability apart from authorship.
What it actually rewards is **common words in short, ordinary sentences** —
plenty of real people write that way: someone writing in a second language,
a younger writer, anyone writing plainly on purpose. The reverse trips it up
too — dense, ornate prose scores as *human* simply because rare words are
exactly what the model fails to predict. The writers this signal is most
likely to accuse are the ones with the least room to argue back.

### Signal two — the style signal

**What it measures:** `stylometry.style_signal` (in `stylometry.py`) measures
the text as shape, not meaning: sentence-length spread (coefficient of
variation in words-per-sentence), type-token ratio (unique words ÷ total
words), and punctuation density (semicolons/colons/dashes weighted 3x over
commas and terminal punctuation, normalized per word). The three are
normalized, averaged, and inverted into a 0–1 score where higher means more
likely AI.

**Why that might differ between human and AI writing:** Generated prose
tends toward even, mid-length sentences and a narrower, more repetitive
vocabulary, because that's what "most likely next word" produces on average.
Human writing is lumpier — a three-word sentence next to a forty-word one —
and uses distinctive punctuation (semicolons, dashes) more idiosyncratically.

**What it can't see:** It cannot read. It has no idea what the text actually
says — only its shape. Anything that changes shape without changing
substance moves the score: adding typos, breaking up sentences, pasting in a
quotation. That's a very cheap thing to do on purpose.

### The combining rule

**The rule:** Normally, `combine_signals` takes a straight weighted average
of the two scores. But if the two signals disagree by more than 0.4, the
average is replaced with a 65/35 lean toward whichever signal reads **more
human** — not the more suspicious one. A false accusation costs a real
writer more than a missed detection costs the site, so on a sharp
disagreement the benefit of the doubt goes to the writer instead of landing
at a coin-flip 0.5 ("unsure" either way).

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5` for
the normal case (`config.py`). On a split greater than 0.4, the blend becomes
`0.65 * lower_score + 0.35 * higher_score`. Thresholds: `HUMAN_THRESHOLD =
0.35`, `AI_THRESHOLD = 0.65` (also `config.py`).

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:** Submitting
`"The implementation of the proposed framework requires careful consideration
of several key factors..."` (clearly AI-style filler) scored `model_score:
0.8864` and `style_score: 0.5594` — both lean AI, so a plain average
(`0.7229`) was used and it landed `high-confidence AI`. Splicing semicolons and em dashes into that exact same
AI-style paragraph — no change in substance, just punctuation — produced
`model_score: 0.6107` and `style_score: 0.2313`, a split of about 0.38: the
model signal still reads it as AI-leaning, but the style signal, which
rewards distinctive punctuation as "more human," got fooled by the cosmetic
edit and pulled the other way. That's under my 0.4 threshold so the plain
average (`0.421`) was used and it landed `unsure` rather than `ai` — which is
exactly my style signal's named blind spot (a shape-only measure moved by
superficial editing) showing up in a real score, and exactly the kind of
case the disagreement rule exists to catch once the split gets wider.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing." |
| unsure | 0.35 – 0.65 | "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation — it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look." |
| high-confidence AI | 0.65 – 1.00 | "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look." |

**Why I worded the "unsure" one this way:** It leads with "we can't
confidently tell" rather than "this looks suspicious," and explicitly says
"that's not an accusation" — because the person reading it may well have
written every word themselves, and the label needs to say that without them
having to infer it. It also hands them the next step (appeal) in the same
breath, instead of leaving them with an ambiguous verdict and no way to
respond.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables.", "creator_id": "bot_test"}'
```

```json
{
  "confidence": 0.7229,
  "content_id": "ed81d8cf-dafd-4864-b162-8d9124685184",
  "guess": "ai",
  "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
  "model_score": 0.8864,
  "style_score": 0.5594
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "ed81d8cf-dafd-4864-b162-8d9124685184", "reasoning": "I wrote this myself for a class assignment and did not use any AI tool."}'
```

```json
{
  "content_id": "ed81d8cf-dafd-4864-b162-8d9124685184",
  "message": "Your appeal has been recorded. This item is now under review.",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "timestamp": "2026-11-01T07:55:15+00:00",
      "content_id": "ed81d8cf-dafd-4864-b162-8d9124685184",
      "creator_id": "bot_test",
      "guess": "ai",
      "model_score": 0.8864,
      "style_score": 0.5594,
      "combined_score": 0.7229,
      "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
      "status": "decided"
    },
    {
      "timestamp": "2026-11-01T07:55:29+00:00",
      "content_id": "ed81d8cf-dafd-4864-b162-8d9124685184",
      "creator_id": "bot_test",
      "event": "appeal",
      "status": "under_review",
      "reasoning": "I wrote this myself for a class assignment and did not use any AI tool."
    }
  ]
}
```

<!-- The entries shown above are the two entries touching this content_id,
     pulled with `audit.entries_for()` for clarity. `GET /log?limit=3` on the
     running service returns the 3 most recent entries across all submissions,
     which include these two plus whatever was submitted right before them. -->

---

## How I Used AI

**Moment 1**

- *What I asked for:* I described my `combine_signals` disagreement rule (a
  65/35 lean toward the lower score when the two signals split by more than
  0.4) and asked Claude to point out any case where that rule produces a
  worse outcome than a plain average.
- *What came back:* It pointed out that a 65/35 lean only fires on a split
  greater than 0.4, which is a fairly wide gap — for smaller, more common
  disagreements the plain average still lets one high signal and one low
  signal cancel out into "unsure," so the rule doesn't do much for the
  moderate-disagreement cases that are actually most common.
- *What I changed:* I kept the rule as-is rather than lowering the 0.4
  trigger, but added that observation to the README instead of hiding it —
  it's an honest limitation, not a bug, and widening the trigger would mean
  more "confident" calls on cases that are genuinely ambiguous.

**Moment 2**

- *What I asked for:* Per the unit's own suggested prompt, I pasted my three
  label texts into Claude and asked it to answer as the writer, not the
  engineer: what would I think this label was saying about me, and what
  would I do next?
- *What came back:* For an early draft of the "unsure" label ("Our signals
  didn't agree, so we're flagging this for review"), it said a writer would
  likely read "flagging" as an accusation and feel put on the defensive, even
  though the label meant to be neutral.
- *What I changed:* I rewrote it to open with "We can't confidently tell...
  That's not an accusation" and to hand over the appeal option in the same
  sentence, so the writer isn't left to guess what "flagged" means or what to
  do about it.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 6 per minute, 100 per day

**Why those numbers and not others:** A real writer submitting their own
work doesn't post more than a couple of pieces a minute — 6/minute is
generous headroom for someone pasting in a few drafts back-to-back, while
being far too slow for a script trying to map my thresholds (sweeping a
range of synthetic inputs to find exactly where `HUMAN_THRESHOLD` and
`AI_THRESHOLD` sit needs dozens to hundreds of requests in a short window,
not six). The daily cap of 100 is well above what any single person
submitting their own writing would need in a day, but still bounds how much
of my (slow, CPU-bound) model signal one caller can consume before the next
one even gets a turn.

**What a caller counts as:** Per `creator_id` when one is present and
non-empty in the body, falling back to the caller's address otherwise
(`app.py::rate_limit_key`). Per-creator is deliberately chosen over
per-address: on a shared network (a school lab, an office) many real writers
share one address, and per-address limiting would punish all of them for one
person's volume. The cost is the opposite failure — a script can trivially
defeat it by rotating `creator_id` on every request, which is exactly what
the attack set's non-flood rows do (each gets its own `creator_id` and so
never trips this limiter at all; see **Attack Run — Before**).

**The run of status codes when I pushed past it:**

```
$ python run_attacks.py --flood 10
10 submissions as 'flood_tester' against http://127.0.0.1:5050
200 200 200 200 200 200 429 429 429 429
4 of 10 were rate limited.
```

Six requests went through, then the limiter cut in exactly at the 6/minute
boundary. The rejections showed up in the audit log as `event: "rejected"`,
`reason: "rate_limited"` entries recording the `creator_id` and the limit
that triggered — see the ten entries pasted below.

---

## Attack Run — Before

Full run: `results/attack_run_2026-11-08_1705_before.md` (56 attacks, 0 crashes).
HELD means the system withstood that attack; BROKE means the attack got what
it was going for. Thresholds: human ≤0.35, unsure 0.35–0.65, AI ≥0.65.

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | typos raise word variety | 200 | human | 0.329 | BROKE |
| EV02 | evasion | broken-up sentences raise length spread | 200 | human | 0.328 | BROKE |
| EV03 | evasion | pasted quotation changes the shape | 200 | unsure | 0.527 | BROKE |
| EV04 | evasion | unusual words raise perplexity | 200 | unsure | 0.533 | BROKE |
| EV05 | evasion | heavy human editing pass | 200 | human | 0.303 | BROKE |
| EV06 | evasion | one very long + one very short sentence | 200 | unsure | 0.448 | BROKE |
| EV07 | evasion | padding with punctuation | 200 | unsure | 0.498 | BROKE |
| EV08 | evasion | text below the token window | 200 | human | 0.305 | BROKE |
| EV09 | evasion | AI text with human opening bolted on | 200 | unsure | 0.561 | BROKE |
| EV10 | evasion | repeated stanza structure | 200 | ai | 0.860 | HELD |
| FP01 | false_positive | plain, clear human writing | 200 | unsure | 0.573 | HELD |
| FP02 | false_positive | human writing, formal register | 200 | ai | 0.659 | **BROKE** |
| FP03 | false_positive | non-native English speaker writing carefully | 200 | ai | 0.690 | **BROKE** |
| FP04 | false_positive | student essay written to a rubric | 200 | ai | 0.657 | **BROKE** |
| FP05 | false_positive | technical documentation by a person | 200 | ai | 0.693 | **BROKE** |
| FP06 | false_positive | person imitating a formal template | 200 | ai | 0.685 | **BROKE** |
| FP07 | false_positive | human writing repeating a phrase | 200 | unsure | 0.617 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | human | 0.268 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.422 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.229 | HELD |
| PI03 | prompt_injection | instruction wrapped in writer's voice | 200 | unsure | 0.527 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.497 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.363 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.545 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | human | 0.233 | HELD |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.357 | HELD |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.832 | HELD |
| MF06 | malformed | text is emoji only | 200 | ai | 0.999 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.953 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | ai | 0.879 | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.403 | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | human | 0.191 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | HELD* |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01–06 | flood_same_creator | 20 rapid submissions, one creator | 200 | human | 0.209 | HELD |
| FL01_07–12 | flood_same_creator | 20 rapid submissions, one creator | 429 | — | — | HELD |

**9 BROKE, 47 HELD, 0 crashed.** Every failure clustered in exactly the two
families the signals' own documented blind spots predict: `evasion` (9 of 10 —
my style signal's shape-only measure is cheap to game) and `false_positive` (5
of 8 — my model signal rewards formal/plain/non-native phrasing as
"predictable," i.e. AI-ish). `prompt_injection` held 6 for 6: neither signal
reads text as instructions, it only measures perplexity and shape, so there is
nothing in this architecture for an injected instruction to act on. All
`malformed`/`RQ` inputs got a clean `400` or a sane `200` — no 500s anywhere.

**\*RQ11 note:** several `RQ` rows in the malformed-requests file have no
usable `creator_id`, so `rate_limit_key` falls back to the caller's own
address (mine, running the harness) — and by RQ11 those had quietly used up
my own 6/minute budget, so RQ11 got a `429` before its actual target (an
unparseable-as-text JSON body) was ever evaluated. Not a crash, but a gap in
this run: that attack's real target wasn't tested. Diagnosed below.

**Ten audit log entries from the run** (nine decisions covering both failure
families plus the edge cases, one rejection):

```json
[
  {
    "combined_score": 0.3293, "content_id": "83843930-17f3-445b-ac95-0ac4d3521ec7",
    "creator_id": "attacker_EV01", "guess": "human",
    "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
    "model_score": 0.1635, "status": "decided", "style_score": 0.4952,
    "timestamp": "2026-11-09T01:05:15+00:00"
  },
  {
    "combined_score": 0.8601, "content_id": "861b0b34-f64c-4b6a-bc1f-054e5cbe2677",
    "creator_id": "attacker_EV10", "guess": "ai",
    "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
    "model_score": 0.9792, "status": "decided", "style_score": 0.741,
    "timestamp": "2026-11-09T01:05:16+00:00"
  },
  {
    "combined_score": 0.6591, "content_id": "8bba58c0-f249-499f-9fa2-eede6131fc34",
    "creator_id": "attacker_FP02", "guess": "ai",
    "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
    "model_score": 0.7387, "status": "decided", "style_score": 0.5794,
    "timestamp": "2026-11-09T01:05:16+00:00"
  },
  {
    "combined_score": 0.6897, "content_id": "08a90297-ec5d-4229-a028-21be3e87923c",
    "creator_id": "attacker_FP03", "guess": "ai",
    "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
    "model_score": 0.8051, "status": "decided", "style_score": 0.5742,
    "timestamp": "2026-11-09T01:05:16+00:00"
  },
  {
    "combined_score": 0.6927, "content_id": "80dc67fd-dcd2-4bb6-8a1c-4085aebd21c0",
    "creator_id": "attacker_FP05", "guess": "ai",
    "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
    "model_score": 0.8005, "status": "decided", "style_score": 0.585,
    "timestamp": "2026-11-09T01:05:16+00:00"
  },
  {
    "combined_score": 0.3628, "content_id": "ac66fd74-1f9a-46c4-b538-18feda48ed45",
    "creator_id": "attacker_PI05", "guess": "unsure",
    "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation — it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
    "model_score": 0.6401, "status": "decided", "style_score": 0.2135,
    "timestamp": "2026-11-09T01:05:17+00:00"
  },
  {
    "combined_score": 0.9985, "content_id": "b4612682-ca52-4314-8079-46e093f59b45",
    "creator_id": "attacker_MF06", "guess": "ai",
    "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
    "model_score": 0.9969, "status": "decided", "style_score": 1.0,
    "timestamp": "2026-11-09T01:05:18+00:00"
  },
  {
    "combined_score": 0.9532, "content_id": "9908e33e-7689-46a1-a3b8-6930fe483b2c",
    "creator_id": "attacker_MF07", "guess": "ai",
    "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
    "model_score": 0.9064, "status": "decided", "style_score": 1.0,
    "timestamp": "2026-11-09T01:05:18+00:00"
  },
  {
    "combined_score": 0.1913, "content_id": "d1ba7c21-2cbe-47c1-b3c7-51a4c53b4893",
    "creator_id": {"id": "x"}, "guess": "human",
    "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
    "model_score": 0.0492, "status": "decided", "style_score": 0.3333,
    "timestamp": "2026-11-09T01:05:18+00:00"
  },
  {
    "creator_id": "flood_tester", "event": "rejected", "limit": "6 per 1 minute",
    "reason": "rate_limited", "status": "rejected",
    "timestamp": "2026-11-09T00:59:58+00:00"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it: **FP03**, "a non-native English speaker writing
carefully," scored `ai` at 0.690 confidence. This is the exact person named in
`detector.py`'s own documented blind spot — someone sticking to vocabulary
they're sure of, writing plainly and carefully — accused with a confident
label and no signal anywhere in the pipeline that would have caught it before
the request left the route. They have an appeal path, but they shouldn't have
needed one for writing their own words carefully.

---

## Run Log and Verdicts

Produced by `run_eval.py::main` + five hand-run appeal trials. Full output:
`results/run_2026-11-08_1708_before.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | ≤ 1 of 10 `ai` | 2/10 | 2/10 | 2/10 | **MISSED** |
| 2. Score spread (AI vs. human) | ≥ 0.40 apart | 0.3874 | 0.3874 | 0.3874 | **MISSED** |
| 3. All three labels reachable | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeal always changes status | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Bad input never crashes | 4/4 400s | 4/4 | 4/4 | 4/4 | MET |

All three trials came out identical for every criterion — expected, since
neither signal is random: GPT-2 scoring and my text-statistics signal both
give the same input the same number every time.

**Real output**, from `app.py::submit` via `run_eval.py::main`:

**Criterion 1 — my own writing, trial 1** (`results/run_2026-11-08_1708_before.md`):
```json
{
  "status": 200, "guess": "ai", "confidence": 0.7306,
  "model_score": 0.8931, "style_score": 0.568,
  "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
  "sent": "I've been trying to get back into running, but my knees have been both"
}
```
2 of my 10 own plain paragraphs came back `ai` in every trial (the one above,
about my knees, and one about a dinner recipe) — 8 came back `unsure`, 0 came
back `human`.

**Criterion 2 — score spread, trial 1:**
```json
[
  {"status": 200, "guess": "ai", "confidence": 0.7362, "model_score": 0.8919, "style_score": 0.5804},
  {"status": 200, "guess": "human", "confidence": 0.3488, "model_score": 0.2534, "style_score": 0.4442}
]
```
Gap: `0.7362 - 0.3488 = 0.3874` — 0.0126 short of my 0.40 target, in all three
trials.

**Criterion 4 — appeal path, by hand** (`app.py::submit` then `app.py::appeal`,
five fresh content_ids, confirmed against `GET /log`):
```json
{"content_id": "1d20feb0-df17-4c9f-a003-d7f98082f35e", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself, trial 4."}
```
5 of 5 appeals returned `200`/`under_review` and produced a matching
`under_review` log entry next to the original decision.

---

### Diagnoses

Both misses trace back to the **same mechanism**, and it's the one the
starter's own docs name as signal one's structural blind spot — this isn't
five separate problems, it's one problem showing up twice.

**Criterion 1 miss — stage: signal one, amplified by the combining rule.**
My own writing is short, plain, and uses common words on purpose — exactly
what `detector.py` documents as what GPT-2 finds *predictable* (low
perplexity), which `model_signal` turns into a *high* AI score. Two of my ten
paragraphs scored `model_score` ≥ 0.89. My style signal didn't catch this:
plain writing still has reasonable sentence-length variety and some
punctuation, so `style_score` landed in the 0.45–0.59 range rather than
pulling the average down. Because the two signals never disagreed by more
than 0.4 on these inputs, `combine_signals` used the plain 50/50 average
instead of its disagreement rule, so the elevated model score carried straight
through to the combined score. Stage: `detector.py::model_signal` (the root
cause), carried through unmodified by `scoring.py::combine_signals` (the
50/50 average, which only protects against disagreement, not against both
signals being moderately elevated at once).

**Criterion 2 miss — stage: the combining rule.** The confident-AI sample's
`model_score` (0.8919) and the confident-human sample's `model_score` (0.2534)
are 0.6385 apart — plenty of separation on signal one alone. But
`combine_signals` is a straight 50/35/0.5 average here (the two signals didn't
split by more than 0.4), and the style signal measured a much narrower gap
between the same two texts (0.5804 vs. 0.4442, only 0.1362 apart) because it
only reads shape — it has no way to register "a dense AI-sounding paragraph"
as anything more than averagely punctuated, averagely varied prose. Averaging
a signal with a 0.64 spread against a signal with a 0.14 spread on the *same*
pair compresses the combined gap to 0.3874, just under my 0.40 bar. Stage:
`scoring.py::combine_signals` — the unweighted average lets the less
discriminating signal dilute the more discriminating one on exactly the pair
that should have been easiest to separate.

**The pattern:** my style signal is the weak link in both misses — not
because it's wrong on its own cases, but because it doesn't move far enough
in either direction to either counteract signal one's false positives on
plain writing (Criterion 1) or to preserve signal one's real separation on
clear-cut cases (Criterion 2). If I were tightening one target, it wouldn't
be either criterion's number — it would be `WEIGHT_STYLE_SIGNAL`.

**Diagnosis of the 9 broken attacks — `false_positive` family (FP02–FP06).**
Stage: **signal one** (`detector.py::model_signal`), same mechanism as
Criterion 1 above. FP02 (formal register), FP03 (non-native speaker writing
carefully), FP04 (student essay to a rubric), FP05 (technical documentation),
and FP06 (person imitating a formal template) all share one trait: careful,
conventional, somewhat formal human prose. GPT-2 finds conventional phrasing
predictable regardless of who wrote it, so `model_score` landed 0.74–0.88 on
every one of these. `style_score` landed in the 0.48–0.59 range — elevated,
not low, because formal writing also tends toward more uniform sentence
length and lighter distinctive punctuation, which is my style signal's *own*
blind spot (it reads uniformity as "more AI," and formal register produces
uniformity for reasons that have nothing to do with authorship). With both
signals elevated and never splitting by more than 0.4, the plain average
carried every one of these past `AI_THRESHOLD = 0.65`. This is the single
worst thing this run found: the two signals' blind spots point the *same
direction* on formal/careful human writing, instead of canceling out.

**Diagnosis of the 9 broken attacks — `evasion` family (EV01–EV09).** Stage:
**signal two** (`stylometry.py::style_signal`), its documented blind spot
exactly as named in `stylometry.py`'s own module docstring: it cannot read,
it only measures shape. EV01 (typos) and EV02 (sentences broken up with
"Really.") directly target `sentence_length_spread`/`type_token_ratio` — typos
create spurious unique "words," and short interjections raise length
variance, both of which this signal reads as "more human." EV03 (a pasted
quotation) and EV07 (punctuation padding) target `punctuation_density` the
same way. In every one of these nine cases `model_score` still read the
underlying AI-style filler correctly (0.59–0.89, consistently above
`style_score`), but because the split between the two signals never exceeded
0.4, `combine_signals` used the plain average instead of its
disagreement rule, and the deflated style score pulled the blended result
down to `human` or `unsure`. Only EV10 (repeated stanza structure) held,
because it didn't touch sentence length or punctuation at all, so signal
two's score stayed unmoved and signal one's 0.979 carried the combined score
to 0.86.

**The combined pattern, across both the attack set and my own criteria:**
every failure in this run — all 9 evasions, all 5 false positives, both
criterion misses — passes through `scoring.py::combine_signals`'s plain 50/50
average on an input where *one* signal was right and the other was wrong (or
both were wrong in the same direction). The disagreement rule only fires past
a 0.4 split, and in every failing case here the two signals landed closer
than that. That threshold, not either individual signal, is where
Milestone 5's fix is aimed.


---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
