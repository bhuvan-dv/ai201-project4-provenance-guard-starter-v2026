"""
Regression coverage for the capstone's phrasing signal.

These lock in the behavior the capstone's diagnosis and fix depend on:
heavily templated text still saturates, plain text stays quiet, and a short
honestly-written passage with one or two real phrases no longer gets
pushed toward the ceiling the way it did before the 150-word floor.

    python -m pytest tests/test_phrasing.py -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from phrasing import phrasing_signal  # noqa: E402

TEMPLATED = (
    "It is important to note that this plays a crucial role in the overall "
    "outcome. Furthermore, it is worth noting that a wide range of factors "
    "must be considered. In conclusion, this underscores the importance of "
    "careful planning across every stage of the process."
)

PLAIN = (
    "My dog knocked over the trash can again this morning. I was so "
    "annoyed I almost yelled at him but he just looked up with that happy "
    "face and I couldn't stay mad. Took me twenty minutes to clean up "
    "before work."
)

SHORT_FORMAL_MEMO = (
    "The committee met twice last month to review the budget shortfall. "
    "Furthermore, several members raised concerns about the timeline, "
    "which has slipped three weeks already and nobody seems happy about "
    "it. It should be noted that the vendor contract expires in June, so "
    "a decision is needed soon or we lose our negotiating position "
    "entirely."
)


def test_templated_text_saturates():
    assert phrasing_signal(TEMPLATED) >= 0.9


def test_plain_text_stays_quiet():
    assert phrasing_signal(PLAIN) <= 0.1


def test_short_honest_memo_no_longer_saturates():
    # Before the capstone's 150-word floor, this scored 0.9091 — this is
    # the regression test for that fix.
    score = phrasing_signal(SHORT_FORMAL_MEMO)
    assert score < 0.5, (
        f"short honest text with 2 phrase hits scored {score}, which means "
        f"the short-text amplification bug is back"
    )


def test_empty_text_is_zero():
    assert phrasing_signal("") == 0.0


if __name__ == "__main__":
    test_templated_text_saturates()
    test_plain_text_stays_quiet()
    test_short_honest_memo_no_longer_saturates()
    test_empty_text_is_zero()
    print("All phrasing signal checks passed.")
