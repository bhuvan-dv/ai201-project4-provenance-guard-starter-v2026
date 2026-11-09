# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 17:11
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `d40233eb-4822-4842-8cd9-33ec993c0e73` | human | 0.329 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `99f37901-3de4-4e33-b962-a0a856052b14` | human | 0.328 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `912bdcd0-56ca-46eb-a50e-ca9deaca3fc7` | unsure | 0.527 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `eda1b14b-6fbc-4c1e-a84b-1f028017419d` | unsure | 0.533 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `891e08ad-afa3-4316-95a1-c3f50f4a61ae` | human | 0.303 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `e45b291b-b835-4109-ae79-c1817ad5a66b` | unsure | 0.448 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `41d62cd8-4531-4bce-ae4c-2a56f7f93654` | unsure | 0.498 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `5d80ca65-5902-4b9c-8cf0-8411a43e0e9d` | human | 0.305 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `98f35097-29c2-4d0a-b24a-64bd43eac68c` | unsure | 0.561 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `9d51a713-ee18-4b4b-ba3f-0650ac693574` | ai | 0.860 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `a337e7b1-9005-4177-9ea5-a9799ec0e834` | unsure | 0.573 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `1c66b998-a923-4c4f-816d-06a890eff09f` | unsure | 0.659 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `9b1a6807-8e62-49ec-8f4c-d81b1ffb254e` | unsure | 0.690 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `a244ad80-f54f-4e98-83dc-c06b8c76d4fc` | unsure | 0.657 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `cee694ef-81b1-445d-8f37-cc45712addf3` | unsure | 0.693 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `380d596d-6ebd-4367-a564-b9ac2e38e3ae` | unsure | 0.685 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `3664dffb-616f-418e-ac76-827e1cc7ee76` | unsure | 0.617 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `75f7d4c5-53e2-4bc8-8e2a-5de57b52e68c` | human | 0.268 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `98c19158-7d9a-4587-b762-1dd527e9225b` | unsure | 0.422 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `aaa7c276-cfea-4b2e-9068-ea3f38fa7964` | human | 0.229 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `0de5bd21-1ee8-4553-aa24-07d251aca343` | unsure | 0.527 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `e427124f-1dc4-465f-9943-77fb1dab69b3` | unsure | 0.497 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `cd323a30-0eaf-47c7-81a5-8db857763a09` | unsure | 0.363 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `1f720c8c-51bd-43ae-954d-7acd4290764b` | unsure | 0.545 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `785ffdea-8c0c-476b-ae35-0ea34a69a55f` | human | 0.233 |  |
| MF04 | malformed | text is only punctuation | 200 | `d2357d2e-ec94-4209-a1a5-39f8644e5235` | unsure | 0.357 |  |
| MF05 | malformed | text is a very long single word | 200 | `29e93ffd-6848-40bf-86cc-aa6734be317a` | ai | 0.832 |  |
| MF06 | malformed | text is emoji only | 200 | `98c6fe47-293b-482f-acbd-07ee08b82526` | ai | 0.999 |  |
| MF07 | malformed | text is right-to-left script | 200 | `a3369dbc-bf03-4f97-b020-c5d572dd9b17` | ai | 0.953 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `caade0fd-c0c6-42cd-8bcd-353bff90d404` | ai | 0.879 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `5e0b7c24-348e-4c8f-9bfc-6c57a6019617` | unsure | 0.403 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `d8cdee3c-33db-401f-bd80-8aa1a75367b4` | human | 0.191 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `464f38b5-c832-49ad-b904-4d204fa00dcf` | human | 0.209 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c82c3f96-2bbf-4a23-a9e6-c3f82849502a` | human | 0.209 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `29ed1163-ad8a-46fd-896e-bef818ce514f` | human | 0.209 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d03d13b6-7ab7-4451-857f-cff01b993135` | human | 0.209 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `67b3a3e7-354e-47e7-b61f-5a81df831801` | human | 0.209 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a21a6a7d-6b46-4863-9abc-884c412b5940` | human | 0.209 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "d40233eb-4822-4842-8cd9-33ec993c0e73",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3293,
  "model_score": 0.1635,
  "style_score": 0.4952,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "99f37901-3de4-4e33-b962-a0a856052b14",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.3277,
  "model_score": 0.5943,
  "style_score": 0.1841,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "912bdcd0-56ca-46eb-a50e-ca9deaca3fc7",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5268,
  "model_score": 0.6662,
  "style_score": 0.3873,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "eda1b14b-6fbc-4c1e-a84b-1f028017419d",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5328,
  "model_score": 0.6114,
  "style_score": 0.4542,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "891e08ad-afa3-4316-95a1-c3f50f4a61ae",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3033,
  "model_score": 0.3212,
  "style_score": 0.2853,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "e45b291b-b835-4109-ae79-c1817ad5a66b",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4484,
  "model_score": 0.5727,
  "style_score": 0.324,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "41d62cd8-4531-4bce-ae4c-2a56f7f93654",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4976,
  "model_score": 0.5862,
  "style_score": 0.4089,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "5d80ca65-5902-4b9c-8cf0-8411a43e0e9d",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3055,
  "model_score": 0.2452,
  "style_score": 0.3659,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "98f35097-29c2-4d0a-b24a-64bd43eac68c",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.561,
  "model_score": 0.7042,
  "style_score": 0.4177,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "9d51a713-ee18-4b4b-ba3f-0650ac693574",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8601,
  "model_score": 0.9792,
  "style_score": 0.741,
  "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "a337e7b1-9005-4177-9ea5-a9799ec0e834",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5732,
  "model_score": 0.6175,
  "style_score": 0.5288,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "1c66b998-a923-4c4f-816d-06a890eff09f",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6591,
  "model_score": 0.7387,
  "style_score": 0.5794,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "9b1a6807-8e62-49ec-8f4c-d81b1ffb254e",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6897,
  "model_score": 0.8051,
  "style_score": 0.5742,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "a244ad80-f54f-4e98-83dc-c06b8c76d4fc",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6572,
  "model_score": 0.8329,
  "style_score": 0.4815,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "cee694ef-81b1-445d-8f37-cc45712addf3",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6927,
  "model_score": 0.8005,
  "style_score": 0.585,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "380d596d-6ebd-4367-a564-b9ac2e38e3ae",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6855,
  "model_score": 0.8814,
  "style_score": 0.4895,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "3664dffb-616f-418e-ac76-827e1cc7ee76",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6172,
  "model_score": 0.8816,
  "style_score": 0.4749,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "75f7d4c5-53e2-4bc8-8e2a-5de57b52e68c",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2677,
  "model_score": 0.3223,
  "style_score": 0.2131,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "98c19158-7d9a-4587-b762-1dd527e9225b",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.422,
  "model_score": 0.4625,
  "style_score": 0.3814,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "aaa7c276-cfea-4b2e-9068-ea3f38fa7964",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2289,
  "model_score": 0.2044,
  "style_score": 0.2535,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "0de5bd21-1ee8-4553-aa24-07d251aca343",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5273,
  "model_score": 0.5943,
  "style_score": 0.4603,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "e427124f-1dc4-465f-9943-77fb1dab69b3",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4966,
  "model_score": 0.4998,
  "style_score": 0.4933,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "cd323a30-0eaf-47c7-81a5-8db857763a09",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.3628,
  "model_score": 0.6401,
  "style_score": 0.2135,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "1f720c8c-51bd-43ae-954d-7acd4290764b",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5452,
  "model_score": 0.5583,
  "style_score": 0.5321,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "785ffdea-8c0c-476b-ae35-0ea34a69a55f",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.2333,
  "model_score": 0.0,
  "style_score": 0.6667,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "d2357d2e-ec94-4209-a1a5-39f8644e5235",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.3573,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "29e93ffd-6848-40bf-86cc-aa6734be317a",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8321,
  "model_score": 0.9976,
  "style_score": 0.6667,
  "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "98c6fe47-293b-482f-acbd-07ee08b82526",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9985,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "a3369dbc-bf03-4f97-b020-c5d572dd9b17",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "caade0fd-c0c6-42cd-8bcd-353bff90d404",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8793,
  "model_score": 0.9876,
  "style_score": 0.771,
  "label": "We think this was most likely written by an AI system, based on patterns in word choice and sentence structure. If you wrote this yourself, you can appeal and a person will take another look.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "5e0b7c24-348e-4c8f-9bfc-6c57a6019617",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.4026,
  "model_score": 0.2395,
  "style_score": 0.5657,
  "label": "We can't confidently tell whether this was written by a person or an AI system. That's not an accusation \u2014 it just means our signals didn't point clearly one way. You're welcome to appeal if you'd like a person to take a closer look.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "d8cdee3c-33db-401f-bd80-8aa1a75367b4",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.1913,
  "model_score": 0.0492,
  "style_score": 0.3333,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "464f38b5-c832-49ad-b904-4d204fa00dcf",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2088,
  "model_score": 0.0287,
  "style_score": 0.5432,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c82c3f96-2bbf-4a23-a9e6-c3f82849502a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2088,
  "model_score": 0.0287,
  "style_score": 0.5432,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "29ed1163-ad8a-46fd-896e-bef818ce514f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2088,
  "model_score": 0.0287,
  "style_score": 0.5432,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "d03d13b6-7ab7-4451-857f-cff01b993135",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2088,
  "model_score": 0.0287,
  "style_score": 0.5432,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "67b3a3e7-354e-47e7-b61f-5a81df831801",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2088,
  "model_score": 0.0287,
  "style_score": 0.5432,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "a21a6a7d-6b46-4863-9abc-884c412b5940",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2088,
  "model_score": 0.0287,
  "style_score": 0.5432,
  "label": "We think this was most likely written by a person. The sentence rhythm and word choice look like ordinary human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
