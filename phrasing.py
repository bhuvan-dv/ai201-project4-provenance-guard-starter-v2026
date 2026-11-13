"""
Signal three: the phrasing signal. ← CAPSTONE EXTENSION (Unit 9)

Signals one and two both measure HOW the text is put together — perplexity
reads token-level predictability, stylometry reads sentence shape and
punctuation. Neither one reads what the words actually say. This signal does:
it counts generic AI discourse markers and hedge phrases — "it is important
to note", "in conclusion", "furthermore", "overall, this demonstrates" — the
stock connective tissue that shows up disproportionately in LLM output
because a model trained to sound comprehensive reaches for the same small set
of transitions.

    from phrasing import phrasing_signal
    score = phrasing_signal("some text")     # 0.0 human-ish … 1.0 AI-ish

What it measures: density of a fixed phrase list, in occurrences per 100
words, clipped at a ceiling and scaled onto 0-1. Higher means more likely AI,
same direction as the other two signals.

Why that might differ between human and AI writing: these phrases are
genuinely useful connective tissue, so most writing uses a few. A model
asked to write "about" a topic tends to reach for the same handful of
templated transitions over and over, because they are safe, generic, and
score well against "sounds thorough." A person free-associating rarely
stacks more than one or two per paragraph.

What it can't see: it has no concept of whether a phrase is being used
honestly or ironically, and it rewards exactly the register that academic
and business writing already uses on purpose. Someone writing a formal memo,
a literature review, or ESL-formal prose will legitimately use "furthermore"
and "it should be noted" without an AI anywhere near the keyboard — this
signal's blind spot is the same shape as the model signal's: it mistakes a
REGISTER for a SOURCE. And it is trivially dodged: a model told not to use
transition words produces text this signal can't see at all.
"""

import re

# Deliberately generic, deliberately short — these are the phrases that show
# up as connective filler across unrelated topics, not topic-specific jargon.
PHRASES = [
    "it is important to note",
    "it's important to note",
    "it should be noted",
    "in conclusion",
    "in summary",
    "overall,",
    "furthermore",
    "moreover",
    "additionally",
    "on the other hand",
    "that being said",
    "with that in mind",
    "in today's world",
    "in today's society",
    "plays a crucial role",
    "plays a significant role",
    "it is worth noting",
    "as a result",
    "in order to",
    "a wide range of",
    "a variety of",
    "delve into",
    "navigate the complexities",
    "underscores the importance",
    "it is essential to",
]

_PATTERNS = [re.compile(re.escape(p), re.IGNORECASE) for p in PHRASES]


def phrase_count(text: str) -> int:
    """How many times any listed phrase appears. Overlaps count separately."""
    return sum(len(p.findall(text)) for p in _PATTERNS)


def phrasing_signal(text: str) -> float:
    """
    The signal, as a 0-1 score. **Higher means more likely AI.**

    Density is phrases per 100 words, so a short and a long submission with
    the same habit score the same. Four hits per 100 words is already a
    heavily templated paragraph, so that's the ceiling — anything at or above
    it clips to 1.0 rather than letting one outlier dominate.

    The word count used for normalization is floored at 150. Without the
    floor, a 60-word submission with one or two ordinary, honestly-used
    phrases (a memo that happens to say "furthermore" once) gets divided by
    a tiny denominator and saturates near 1.0 on real-world text that was
    only ever meant to catch text repeating these phrases over and over. The
    floor means short text needs the SAME absolute number of hits a longer
    templated passage would, rather than getting graded on a curve that
    punishes brevity.
    """
    words = re.findall(r"[a-z0-9']+", text.lower())
    if not words:
        return 0.0

    normalizing_words = max(len(words), 150)
    density = phrase_count(text) / (normalizing_words / 100)
    ceiling = 4.0
    return round(min(density / ceiling, 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "It is important to note that this approach plays a crucial role in "
        "the overall process. Furthermore, it is worth noting that a wide "
        "range of factors must be considered. In conclusion, this "
        "underscores the importance of careful planning."
    )

    print(f"phrase_count      {phrase_count(text)}")
    print(f"phrasing_signal   {phrasing_signal(text)}   (higher = more likely AI)")
