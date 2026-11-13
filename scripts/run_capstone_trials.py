"""
The three-trial harness behind the capstone's Run Log and Verdicts table.

Runs all five capstone criteria (templated-text phrasing reachability,
plain-text phrasing quiet floor, warm-request latency, average cost per
run, and the three bad-input cases) three times each against a running
local instance, and prints the per-trial counts plus sample output.

Requires the service already running (`python app.py`) in another terminal.

    python scripts/run_capstone_trials.py
"""

import json
import time
import uuid

import requests

BASE = "http://127.0.0.1:5000"

TEMPLATED_TEXTS = [
    "It is important to note that this plays a crucial role in the overall "
    "outcome. Furthermore, it is worth noting that a wide range of factors "
    "must be considered. In conclusion, this underscores the importance of "
    "careful planning across every stage of the process.",
    "Moreover, it should be noted that a variety of approaches exist. "
    "Additionally, in order to succeed, one must delve into the complexities "
    "involved. Overall, this plays a significant role in the final result, "
    "and it is essential to navigate the complexities with care.",
    "In today's world, it is important to note that technology plays a "
    "crucial role in everyday life. On the other hand, it is worth noting "
    "that a wide range of challenges remain. In summary, this underscores "
    "the importance of continued research in the field.",
    "Furthermore, it is important to note that communication plays a "
    "significant role in any organization. Additionally, in order to "
    "improve outcomes, teams must delve into a variety of strategies. That "
    "being said, it should be noted that results may vary.",
    "It is important to note that education plays a crucial role in society. "
    "Moreover, a wide range of methods exist to improve learning outcomes. "
    "In conclusion, it is essential to navigate the complexities of modern "
    "classrooms with care and in order to help every student.",
    "With that in mind, it is worth noting that nutrition plays a crucial "
    "role in overall health. Furthermore, a variety of diets exist, and it "
    "is important to note that results vary. Overall, this underscores the "
    "importance of a balanced approach to eating.",
    "In today's society, it is important to note that social media plays a "
    "significant role in communication. Additionally, it should be noted "
    "that a wide range of platforms exist. In summary, it is essential to "
    "navigate the complexities of digital life thoughtfully.",
    "Moreover, exercise plays a crucial role in mental health, and it is "
    "important to note that a variety of activities can help. On the other "
    "hand, it is worth noting that consistency matters most. In conclusion, "
    "this underscores the importance of a sustainable routine.",
    "It is important to note that climate plays a crucial role in "
    "agriculture. Furthermore, a wide range of crops are affected, and in "
    "order to adapt, farmers must delve into new techniques. That being "
    "said, it is essential to note that outcomes vary by region.",
    "Additionally, it is worth noting that sleep plays a significant role in "
    "cognitive function. Moreover, a variety of factors affect sleep "
    "quality, and it is important to note that habits matter. In summary, "
    "this underscores the importance of a consistent schedule.",
]

PLAIN_TEXTS = [
    "My dog knocked over the trash can again this morning. I was so annoyed "
    "I almost yelled at him but he just looked up with that happy face and "
    "I couldn't stay mad. Took me twenty minutes to clean up before work.",
    "We drove up to the lake on Saturday and the water was freezing. Jake "
    "jumped in anyway and came out shivering within ten seconds flat. We "
    "laughed about it the whole ride home.",
    "The coffee machine at work broke again. Someone taped a sign on it "
    "that just says 'RIP' and nobody has fixed it in three days. I'm "
    "bringing my own thermos tomorrow.",
    "Grandma's recipe calls for way too much salt if you ask me. I cut it "
    "in half last time and it still tasted like the ocean. Going to try "
    "again this weekend with even less.",
    "Rained all day so we just stayed in and watched movies. Picked three "
    "bad ones in a row on purpose because that's funnier somehow. Fell "
    "asleep during the last one.",
    "The bus was twenty minutes late and packed. Some guy's backpack kept "
    "hitting me in the face every time the bus turned. Walking next time, "
    "rain or not.",
    "Tried baking bread for the first time. It came out flat and dense but "
    "I ate it anyway with way too much butter. Going to look up what I did "
    "wrong before round two.",
    "My phone died halfway through the hike and I had no idea what time it "
    "was. Just kept walking until the trail ended, took about an hour "
    "longer than expected.",
    "The neighbor's cat keeps getting into our yard and digging up the "
    "flower bed. I don't even mind that much, he's kind of funny to watch "
    "when he does it.",
    "Spent way too long trying to fix a wobbly table leg with a folded "
    "napkin. It worked for about a day before the napkin gave out "
    "completely.",
]

MISSING_TEXT_PAYLOADS = [{}, {"creator_id": "x"}, {"text": None}, {"text": 123}, {"text": ""}]
EMPTY_TEXT_PAYLOADS = [{"text": "   "}, {"text": ""}, {"text": "\n\n"}, {"text": "\t"}, {"text": "  \n "}]
HUGE_TEXT = "x " * 60000  # well over 100,000 chars


def submit(text, creator_id):
    r = requests.post(f"{BASE}/submit", json={"text": text, "creator_id": creator_id})
    return r


def run_signal_batch(texts, label_prefix, trial):
    results = []
    for i, t in enumerate(texts):
        cid = f"{label_prefix}_trial{trial}_{i}_{uuid.uuid4().hex[:6]}"
        r = submit(t, cid)
        body = r.json()
        results.append(body)
    return results


def criterion_1_and_2(trial):
    templated = run_signal_batch(TEMPLATED_TEXTS, "cap_c1", trial)
    plain = run_signal_batch(PLAIN_TEXTS, "cap_c2", trial)
    c1_hits = sum(1 for b in templated if b.get("phrasing_score", 0) >= 0.9)
    c2_hits = sum(1 for b in plain if b.get("phrasing_score", 1) <= 0.1)
    return c1_hits, c2_hits, templated, plain


def criterion_3_and_4(trial):
    durations = []
    sample = None
    for i in range(10):
        cid = f"cap_c34_trial{trial}_{i}_{uuid.uuid4().hex[:6]}"
        r = submit(
            f"Routine latency benchmark submission number {i} for trial {trial}, "
            f"used only to measure typical warm request duration and cost.",
            cid,
        )
        body = r.json()
        durations.append(body.get("duration_ms"))
        if i == 0:
            sample = body
    under_200 = sum(1 for d in durations if d is not None and d < 200)
    avg = sum(d for d in durations if d is not None) / len([d for d in durations if d is not None])
    return under_200, avg, durations, sample


def criterion_5(trial):
    counts = {"missing": 0, "empty": 0, "huge": 0}
    samples = {}
    for i, payload in enumerate(MISSING_TEXT_PAYLOADS):
        cid = f"cap_c5_missing_trial{trial}_{i}"
        payload = {**payload, "creator_id": cid}
        r = requests.post(f"{BASE}/submit", json=payload)
        if r.status_code == 400:
            counts["missing"] += 1
        if i == 0:
            samples["missing"] = (r.status_code, r.json())
    for i, payload in enumerate(EMPTY_TEXT_PAYLOADS):
        cid = f"cap_c5_empty_trial{trial}_{i}"
        payload = {**payload, "creator_id": cid}
        r = requests.post(f"{BASE}/submit", json=payload)
        if r.status_code == 400:
            counts["empty"] += 1
        if i == 0:
            samples["empty"] = (r.status_code, r.json())
    for i in range(5):
        cid = f"cap_c5_huge_trial{trial}_{i}"
        r = submit(HUGE_TEXT, cid)
        if r.status_code == 400:
            counts["huge"] += 1
        if i == 0:
            samples["huge"] = (r.status_code, r.json())
    return counts, samples


if __name__ == "__main__":
    import sys

    all_results = {"c1": [], "c2": [], "c3": [], "c4": [], "c5": []}
    samples = {}

    for trial in (1, 2, 3):
        c1, c2, templated, plain = criterion_1_and_2(trial)
        all_results["c1"].append(c1)
        all_results["c2"].append(c2)
        if trial == 1:
            samples["c1_templated"] = templated[0]
            samples["c2_plain"] = plain[0]

        under_200, avg, durations, sample3 = criterion_3_and_4(trial)
        all_results["c3"].append(under_200)
        all_results["c4"].append(round(avg, 1))
        if trial == 1:
            samples["c3_sample"] = sample3
            samples["c3_durations"] = durations

        counts, c5_samples = criterion_5(trial)
        all_results["c5"].append(counts)
        if trial == 1:
            samples["c5"] = c5_samples

        time.sleep(1)

    print(json.dumps({"results": all_results, "samples": samples}, indent=2, default=str))
