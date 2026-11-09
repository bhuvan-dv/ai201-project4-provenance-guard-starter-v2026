"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # My own writing: short, plain, everyday paragraphs, no jargon and no
        # flourishes — exactly the kind of writing criteria.md says signal one
        # is most likely to misread.
        "texts": [
            "I missed the bus this morning because I couldn't find my keys. I ended up walking to work instead, which took about forty minutes. It wasn't a bad walk, honestly, just colder than I expected.",
            "My neighbor asked if I could watch her cat for the weekend. I said yes, even though I'm a little allergic. I figured I'd just take an allergy pill and deal with it.",
            "I tried a new recipe for dinner last night and it didn't turn out great. The sauce was too thin and I forgot to salt the pasta water. Next time I'll pay more attention.",
            "We had a power outage for about three hours yesterday. I ended up reading by candlelight, which was actually kind of nice. My phone died halfway through though.",
            "I've been trying to get back into running, but my knees have been bothering me. I think I'm going to try shorter distances for a while and see if that helps.",
            "My sister called me last night to complain about her landlord again. I let her vent for a while and then we just talked about nothing in particular for an hour.",
            "I finally fixed the leaky faucet in the bathroom. It took three trips to the hardware store because I kept buying the wrong size washer. Should've just measured it first.",
            "I spent most of Sunday cleaning out my closet. I found a bunch of clothes I forgot I owned and donated two full bags. Felt good to get rid of all that clutter.",
            "The coffee shop near my apartment closed down last week. I'm kind of sad about it since I went there almost every morning. I'll have to find somewhere else now.",
            "I played board games with some friends on Friday night. We stayed up way too late arguing about the rules of one game. I still think I was right, for what it's worth.",
        ],
    },
    {
        "name": "score spread between clearly-AI and clearly-human text",
        "criterion": 2,
        "texts": [
            # Confidently AI: dense, generic filler, no edits — same shape as
            # the Sample Run text in the README.
            "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables that must be carefully managed throughout the development process.",
            # Confidently human: off-the-cuff, typos included.
            "ok so i tried to park in that garage downtown again and it was SO full, like every single floor. ended up circling for like 15 min before i gave up and just parked two blocks away lol. anyway im late now, whatever",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Inputs spread across the score range, so all three labels are
        # confirmed reachable, not just configured on paper.
        "texts": [
            "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables that must be carefully managed throughout the development process.",
            "ok so i tried to park in that garage downtown again and it was SO full, like every single floor. ended up circling for like 15 min before i gave up and just parked two blocks away lol. anyway im late now, whatever",
            "The weather has been pretty unpredictable lately. Some days it's warm, other days it's cold enough for a jacket. I never know what to wear in the morning anymore, so I just check the forecast before I leave.",
        ],
    },
    {
        "name": "bad input never crashes the service",
        "criterion": 5,
        # Raw request bodies, sent exactly as written — the only way to say
        # "the field is missing" or "the field is null" without a string.
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
            {"text": None, "creator_id": "eval_bad_null"},
        ],
    },

    # Criterion 4 — the appeal path — can't be expressed as a text or a body:
    # it needs a real submission first, then an appeal against the content_id
    # that submission returned. run_eval.py can't drive that two-step flow, so
    # it's tested by hand with curl, three trials, each a fresh submit+appeal
    # pair. See README — Run Log and Verdicts for the three trials' output.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
