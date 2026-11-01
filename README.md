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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



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
