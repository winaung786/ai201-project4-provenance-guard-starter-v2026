# Attack run — staff_before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 15:07
- Auto-marked BROKE (5xx, crash, no response): **0**
- Reviewed: **56**. HELD: **40**.

The Verdict column records the reviewed judgment using the rules in the README.
The JSON preserves the runner's original fields and response.

Ordinary rows in attacks.csv submit as creator_id `attacker_<id>`;
malformed and flood rows can use other IDs or no ID. Match accepted
requests to the audit log using the content_id in the table.

| ID | Family | Targeting | Status | Content ID | Guess | Combined score | Confidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `2d696eaa4e95437182def0b092cca25f` | human | 0.311 | 0.378 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `9e8a8271453145d79a93221f321d5894` | unsure | 0.386 | 0.229 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `1c07ae3d87e34a2dabc059278af6e603` | unsure | 0.482 | 0.036 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `6e02a8a20de44be49b58799127b9e99d` | unsure | 0.527 | 0.053 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c4da9a74b06d41d99fd4f1f7b669363e` | human | 0.293 | 0.415 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `0c31eb08bd5d4c68a901b7a5c70ab6f8` | unsure | 0.393 | 0.214 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `144eb70a7b6243b889064811b320fb33` | unsure | 0.538 | 0.077 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `99beef9adfe3438cb5506b01e73b027e` | human | 0.266 | 0.468 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `35cb5f97106647c8979622e6f4404340` | unsure | 0.504 | 0.007 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `ecec21dc52b54be9b635b0de5f64e188` | ai | 0.827 | 0.655 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `371ac9e9008a4299a7f5bb2e48bcdf5b` | unsure | 0.527 | 0.054 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `beb5393e61834244afd4c6fca05a0bdc` | unsure | 0.627 | 0.253 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `6026981a94f946e1ad731eb04139b531` | ai | 0.650 | 0.300 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e91e26db5b06479e8df5b3f3f36dc08f` | unsure | 0.615 | 0.230 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `3f81064cbacc431cb08799141460110b` | ai | 0.663 | 0.327 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `e71c357fe1e64835bcd174b818b98ab6` | unsure | 0.635 | 0.271 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `60d493e512b44f72ab31157bb35c9329` | unsure | 0.627 | 0.254 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `ed871214703d439080843a5545f98dd0` | human | 0.275 | 0.451 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `7b901b60573b4de2ac81b2c370807ba7` | unsure | 0.357 | 0.287 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `58e218157ac64dd7a6f54e26fefa47ba` | human | 0.181 | 0.639 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `081f2277b43046b5a37c3ba70268c83b` | unsure | 0.483 | 0.034 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `56a7fb87f0014bc3913371082a9a508f` | unsure | 0.398 | 0.204 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `5a017b8fde344b4b9e3e2105717abc9f` | unsure | 0.432 | 0.135 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `ad9f9b0401704fe8b6829f7d19eccfcd` | unsure | 0.500 | 0.000 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `9a9f13d57b714451bef59a43c25ec6b8` | human | 0.200 | 0.600 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `0cdd44548b9d43e1acf38685110c9435` | unsure | 0.506 | 0.011 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `4c6f0637d5864d4498c4ece77206224e` | ai | 0.799 | 0.598 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `4c9e9990f692464e9c8bad030589fa13` | ai | 0.998 | 0.997 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `37fa60c30abd43a2897f123704f07c62` | ai | 0.953 | 0.906 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `256891f0a7df4b65b731683caeb23ece` | human | 0.259 | 0.482 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `eb1ffd0c255447629eef56ec6e917600` | human | 0.259 | 0.482 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `68894ce813334d50a50eed3880bb4836` | human | 0.259 | 0.482 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8387b3e729dc4fc3a0bb3276dbc8a4e0` | human | 0.259 | 0.482 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5437356ae5ec4bb4843245a904547e12` | human | 0.259 | 0.482 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f1355a013f6346c69970052a447f0ae6` | human | 0.259 | 0.482 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `82d4abe66359497e99e4d7cfb662437d` | human | 0.259 | 0.482 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a583cdf85d734ffc99aeeb11e72e5cda` | human | 0.259 | 0.482 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7bc918a730c641e78f25bb7f06fb2617` | human | 0.259 | 0.482 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `de4e06f31f344a1fb9736ac07c3ba93b` | human | 0.259 | 0.482 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | — | HELD |

---

## By family

| Family | Attacks | HELD | BROKE |
|---|---:|---:|---:|
| `evasion` | 0 | 0 | 0 |
| `false_positive` | 0 | 0 | 0 |
| `flood_same_creator` | 0 | 0 | 0 |
| `malformed` | 0 | 0 | 0 |
| `prompt_injection` | 0 | 0 | 0 |

> The **false_positive** family is the one to look at hardest. Those are
> designed to resemble human writing that reads as machine-like. Check
> the source before calling a case genuine human writing; an AI-written
> local test is evidence of model behavior, not a measured accusation.

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
  "content_id": "2d696eaa4e95437182def0b092cca25f",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3784,
  "combined_score": 0.3108,
  "model_score": 0.1635,
  "style_score": 0.4581,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.3108,
    "confidence": 0.3784,
    "content_id": "2d696eaa4e95437182def0b092cca25f",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.1635,
    "style_score": 0.4581
  },
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
  "content_id": "9e8a8271453145d79a93221f321d5894",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.2289,
  "combined_score": 0.38555000000000006,
  "model_score": 0.5943,
  "style_score": 0.1768,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.38555000000000006,
    "confidence": 0.2289,
    "content_id": "9e8a8271453145d79a93221f321d5894",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.5943,
    "style_score": 0.1768
  },
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
  "content_id": "1c07ae3d87e34a2dabc059278af6e603",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.0357,
  "combined_score": 0.48214999999999997,
  "model_score": 0.6662,
  "style_score": 0.2981,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.48214999999999997,
    "confidence": 0.0357,
    "content_id": "1c07ae3d87e34a2dabc059278af6e603",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.6662,
    "style_score": 0.2981
  },
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
  "content_id": "6e02a8a20de44be49b58799127b9e99d",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.0534,
  "combined_score": 0.5267000000000001,
  "model_score": 0.6114,
  "style_score": 0.442,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.5267000000000001,
    "confidence": 0.0534,
    "content_id": "6e02a8a20de44be49b58799127b9e99d",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.6114,
    "style_score": 0.442
  },
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
  "content_id": "c4da9a74b06d41d99fd4f1f7b669363e",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.4148,
  "combined_score": 0.29259999999999997,
  "model_score": 0.3212,
  "style_score": 0.264,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.29259999999999997,
    "confidence": 0.4148,
    "content_id": "c4da9a74b06d41d99fd4f1f7b669363e",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.3212,
    "style_score": 0.264
  },
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
  "content_id": "0c31eb08bd5d4c68a901b7a5c70ab6f8",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.2143,
  "combined_score": 0.39285,
  "model_score": 0.5727,
  "style_score": 0.213,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.39285,
    "confidence": 0.2143,
    "content_id": "0c31eb08bd5d4c68a901b7a5c70ab6f8",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.5727,
    "style_score": 0.213
  },
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
  "content_id": "144eb70a7b6243b889064811b320fb33",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.0769,
  "combined_score": 0.5384500000000001,
  "model_score": 0.5862,
  "style_score": 0.4907,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.5384500000000001,
    "confidence": 0.0769,
    "content_id": "144eb70a7b6243b889064811b320fb33",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.5862,
    "style_score": 0.4907
  },
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
  "content_id": "99beef9adfe3438cb5506b01e73b027e",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.4679,
  "combined_score": 0.26605,
  "model_score": 0.2452,
  "style_score": 0.2869,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.26605,
    "confidence": 0.4679,
    "content_id": "99beef9adfe3438cb5506b01e73b027e",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.2452,
    "style_score": 0.2869
  },
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
  "content_id": "35cb5f97106647c8979622e6f4404340",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.0073,
  "combined_score": 0.50365,
  "model_score": 0.7042,
  "style_score": 0.3031,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.50365,
    "confidence": 0.0073,
    "content_id": "35cb5f97106647c8979622e6f4404340",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.7042,
    "style_score": 0.3031
  },
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
  "content_id": "ecec21dc52b54be9b635b0de5f64e188",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.655,
  "combined_score": 0.8274999999999999,
  "model_score": 0.9792,
  "style_score": 0.6758,
  "label": "We think this was probably written by AI.",
  "response": {
    "combined_score": 0.8274999999999999,
    "confidence": 0.655,
    "content_id": "ecec21dc52b54be9b635b0de5f64e188",
    "guess": "ai",
    "label": "We think this was probably written by AI.",
    "model_score": 0.9792,
    "style_score": 0.6758
  },
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
  "content_id": "371ac9e9008a4299a7f5bb2e48bcdf5b",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.0539,
  "combined_score": 0.52695,
  "model_score": 0.6175,
  "style_score": 0.4364,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.52695,
    "confidence": 0.0539,
    "content_id": "371ac9e9008a4299a7f5bb2e48bcdf5b",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.6175,
    "style_score": 0.4364
  },
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
  "content_id": "beb5393e61834244afd4c6fca05a0bdc",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.2531,
  "combined_score": 0.6265499999999999,
  "model_score": 0.7387,
  "style_score": 0.5144,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.6265499999999999,
    "confidence": 0.2531,
    "content_id": "beb5393e61834244afd4c6fca05a0bdc",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.7387,
    "style_score": 0.5144
  },
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
  "content_id": "6026981a94f946e1ad731eb04139b531",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.3003,
  "combined_score": 0.65015,
  "model_score": 0.8051,
  "style_score": 0.4952,
  "label": "We think this was probably written by AI.",
  "response": {
    "combined_score": 0.65015,
    "confidence": 0.3003,
    "content_id": "6026981a94f946e1ad731eb04139b531",
    "guess": "ai",
    "label": "We think this was probably written by AI.",
    "model_score": 0.8051,
    "style_score": 0.4952
  },
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
  "content_id": "e91e26db5b06479e8df5b3f3f36dc08f",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.2303,
  "combined_score": 0.61515,
  "model_score": 0.8329,
  "style_score": 0.3974,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.61515,
    "confidence": 0.2303,
    "content_id": "e91e26db5b06479e8df5b3f3f36dc08f",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.8329,
    "style_score": 0.3974
  },
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
  "content_id": "3f81064cbacc431cb08799141460110b",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.3269,
  "combined_score": 0.66345,
  "model_score": 0.8005,
  "style_score": 0.5264,
  "label": "We think this was probably written by AI.",
  "response": {
    "combined_score": 0.66345,
    "confidence": 0.3269,
    "content_id": "3f81064cbacc431cb08799141460110b",
    "guess": "ai",
    "label": "We think this was probably written by AI.",
    "model_score": 0.8005,
    "style_score": 0.5264
  },
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
  "content_id": "e71c357fe1e64835bcd174b818b98ab6",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.2706,
  "combined_score": 0.6353,
  "model_score": 0.8814,
  "style_score": 0.3892,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.6353,
    "confidence": 0.2706,
    "content_id": "e71c357fe1e64835bcd174b818b98ab6",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.8814,
    "style_score": 0.3892
  },
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
  "content_id": "60d493e512b44f72ab31157bb35c9329",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.2536,
  "combined_score": 0.6268,
  "model_score": 0.8816,
  "style_score": 0.372,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.6268,
    "confidence": 0.2536,
    "content_id": "60d493e512b44f72ab31157bb35c9329",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.8816,
    "style_score": 0.372
  },
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
  "content_id": "ed871214703d439080843a5545f98dd0",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.4509,
  "combined_score": 0.27454999999999996,
  "model_score": 0.3223,
  "style_score": 0.2268,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.27454999999999996,
    "confidence": 0.4509,
    "content_id": "ed871214703d439080843a5545f98dd0",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.3223,
    "style_score": 0.2268
  },
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
  "content_id": "7b901b60573b4de2ac81b2c370807ba7",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.287,
  "combined_score": 0.35650000000000004,
  "model_score": 0.4625,
  "style_score": 0.2505,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.35650000000000004,
    "confidence": 0.287,
    "content_id": "7b901b60573b4de2ac81b2c370807ba7",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.4625,
    "style_score": 0.2505
  },
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
  "content_id": "58e218157ac64dd7a6f54e26fefa47ba",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.6386,
  "combined_score": 0.1807,
  "model_score": 0.2044,
  "style_score": 0.157,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.1807,
    "confidence": 0.6386,
    "content_id": "58e218157ac64dd7a6f54e26fefa47ba",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.2044,
    "style_score": 0.157
  },
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
  "content_id": "081f2277b43046b5a37c3ba70268c83b",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.0338,
  "combined_score": 0.48310000000000003,
  "model_score": 0.5943,
  "style_score": 0.3719,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.48310000000000003,
    "confidence": 0.0338,
    "content_id": "081f2277b43046b5a37c3ba70268c83b",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.5943,
    "style_score": 0.3719
  },
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
  "content_id": "56a7fb87f0014bc3913371082a9a508f",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.204,
  "combined_score": 0.398,
  "model_score": 0.4998,
  "style_score": 0.2962,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.398,
    "confidence": 0.204,
    "content_id": "56a7fb87f0014bc3913371082a9a508f",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.4998,
    "style_score": 0.2962
  },
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
  "content_id": "5a017b8fde344b4b9e3e2105717abc9f",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.1351,
  "combined_score": 0.43245,
  "model_score": 0.6401,
  "style_score": 0.2248,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.43245,
    "confidence": 0.1351,
    "content_id": "5a017b8fde344b4b9e3e2105717abc9f",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.6401,
    "style_score": 0.2248
  },
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
  "content_id": "ad9f9b0401704fe8b6829f7d19eccfcd",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.0004,
  "combined_score": 0.4998,
  "model_score": 0.5583,
  "style_score": 0.4413,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.4998,
    "confidence": 0.0004,
    "content_id": "ad9f9b0401704fe8b6829f7d19eccfcd",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.5583,
    "style_score": 0.4413
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "empty_text",
    "message": "text must not be empty."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "text_too_short",
    "message": "text is too short to score \u2014 a few sentences at least."
  },
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
  "content_id": "9a9f13d57b714451bef59a43c25ec6b8",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.6,
  "combined_score": 0.2,
  "model_score": 0.0,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2,
    "confidence": 0.6,
    "content_id": "9a9f13d57b714451bef59a43c25ec6b8",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0,
    "style_score": 0.4
  },
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
  "content_id": "0cdd44548b9d43e1acf38685110c9435",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.0112,
  "combined_score": 0.5056,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "response": {
    "combined_score": 0.5056,
    "confidence": 0.0112,
    "content_id": "0cdd44548b9d43e1acf38685110c9435",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.0112,
    "style_score": 1.0
  },
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
  "content_id": "4c6f0637d5864d4498c4ece77206224e",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.5976,
  "combined_score": 0.7988,
  "model_score": 0.9976,
  "style_score": 0.6,
  "label": "We think this was probably written by AI.",
  "response": {
    "combined_score": 0.7988,
    "confidence": 0.5976,
    "content_id": "4c6f0637d5864d4498c4ece77206224e",
    "guess": "ai",
    "label": "We think this was probably written by AI.",
    "model_score": 0.9976,
    "style_score": 0.6
  },
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
  "content_id": "4c9e9990f692464e9c8bad030589fa13",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9969,
  "combined_score": 0.9984500000000001,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "We think this was probably written by AI.",
  "response": {
    "combined_score": 0.9984500000000001,
    "confidence": 0.9969,
    "content_id": "4c9e9990f692464e9c8bad030589fa13",
    "guess": "ai",
    "label": "We think this was probably written by AI.",
    "model_score": 0.9969,
    "style_score": 1.0
  },
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
  "content_id": "37fa60c30abd43a2897f123704f07c62",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9064,
  "combined_score": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "We think this was probably written by AI.",
  "response": {
    "combined_score": 0.9532,
    "confidence": 0.9064,
    "content_id": "37fa60c30abd43a2897f123704f07c62",
    "guess": "ai",
    "label": "We think this was probably written by AI.",
    "model_score": 0.9064,
    "style_score": 1.0
  },
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "text_too_long",
    "message": "text must be at most 20000 characters."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_text",
    "message": "text must be a string."
  },
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "missing_creator_id",
    "message": "creator_id must be a non-empty string."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_text",
    "message": "text must be a string."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_text",
    "message": "text must be a string."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_text",
    "message": "text must be a string."
  },
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "missing_creator_id",
    "message": "creator_id must be a non-empty string."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_json",
    "message": "Request body must be a JSON object."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_json",
    "message": "Request body must be a JSON object."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_json",
    "message": "Request body must be a JSON object."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_json",
    "message": "Request body must be a JSON object."
  },
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_json",
    "message": "Request body must be a JSON object."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "invalid_text",
    "message": "text must be a string."
  },
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
  "content_id": "256891f0a7df4b65b731683caeb23ece",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "256891f0a7df4b65b731683caeb23ece",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
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
  "content_id": "eb1ffd0c255447629eef56ec6e917600",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "eb1ffd0c255447629eef56ec6e917600",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
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
  "content_id": "68894ce813334d50a50eed3880bb4836",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "68894ce813334d50a50eed3880bb4836",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
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
  "content_id": "8387b3e729dc4fc3a0bb3276dbc8a4e0",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "8387b3e729dc4fc3a0bb3276dbc8a4e0",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
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
  "content_id": "5437356ae5ec4bb4843245a904547e12",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "5437356ae5ec4bb4843245a904547e12",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
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
  "content_id": "f1355a013f6346c69970052a447f0ae6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "f1355a013f6346c69970052a447f0ae6",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "82d4abe66359497e99e4d7cfb662437d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "82d4abe66359497e99e4d7cfb662437d",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "a583cdf85d734ffc99aeeb11e72e5cda",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "a583cdf85d734ffc99aeeb11e72e5cda",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "7bc918a730c641e78f25bb7f06fb2617",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "7bc918a730c641e78f25bb7f06fb2617",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "de4e06f31f344a1fb9736ac07c3ba93b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.4824,
  "combined_score": 0.2588,
  "model_score": 0.0287,
  "style_score": 0.4889,
  "label": "We think this was probably written by a person.",
  "response": {
    "combined_score": 0.2588,
    "confidence": 0.4824,
    "content_id": "de4e06f31f344a1fb9736ac07c3ba93b",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.0287,
    "style_score": 0.4889
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "rate_limited",
    "limit": "10 per 1 minute",
    "message": "Too many submissions. Try again shortly."
  },
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
  "combined_score": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "response": {
    "error": "rate_limited",
    "limit": "10 per 1 minute",
    "message": "Too many submissions. Try again shortly."
  },
  "error": null,
  "verdict": ""
}
```
