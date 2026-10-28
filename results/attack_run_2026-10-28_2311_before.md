# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 15 attacks · 2026-10-28 23:11
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **15**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | Evade detection: typos added to AI-style text should raise word variety and drag the style signal down. | 200 | `54aec4c7a2fe45078b87279edf869fd7` | unsure | 0.242 |  |
| EV02 | evasion | Evade detection: AI-style text split into short choppy sentences should raise sentence-length spread and drag the style signal down. | 200 | `97a451ee4b6b47cead44425f42f9ac53` | unsure | 0.137 |  |
| EV03 | evasion | Evade detection: a long human-style quotation pasted into AI-style text should dilute both signals toward human. | 200 | `67a43f0591ec415f890cd7a9be3394f7` | unsure | 0.097 |  |
| EV04 | evasion | Evade detection: AI-style text with extra punctuation sprinkled through it should raise punctuation density and drag the style signal down. | 200 | `70ff5f328cf9457f8e0dac7ac8f63625` | unsure | 0.109 |  |
| EV05 | evasion | Evade detection: lightly edited AI-style text (a few words swapped) should still read as AI if the signals measure substance, not exact wording. | 200 | `b1f5a3e339ed4f4c888dd8edf30ec8e3` | unsure | 0.198 |  |
| FP01 | false_positive | False positive check: plain, simple human-style writing (short words, short sentences) that a predictability signal may read as machine-like. | 200 | `e9077ac539d54356af71e478224eb016` | ai | 0.419 |  |
| FP02 | false_positive | False positive check: a second-language writer's plain, careful prose with a small vocabulary. | 200 | `ef24b2ff620e404fa4a9dacd68e93050` | unsure | 0.247 |  |
| FP03 | false_positive | False positive check: a short, plain human note — few sentences, so the style signal's spread measure is weak. | 200 | `b1f8c7f5401448be809e45c26c5da1f4` | unsure | 0.143 |  |
| MF01 | malformed | Empty body: the service must not crash on it. | 400 | `—` | — | — |  |
| MF02 | malformed | Unparseable JSON: the service must answer 400, not 500. | 400 | `—` | — | — |  |
| MF03 | malformed | Body is a JSON list, not an object: the service must answer 400, not 500. | 400 | `—` | — | — |  |
| MF04 | malformed | text is a number, not a string: the service must answer 400, not 500. | 400 | `—` | — | — |  |
| MF05 | malformed | Enormous text (50k chars, over the 20k route limit): the service must answer 400, not crash or hang. Kept under the harness's 128KB CSV field limit. | 400 | `—` | — | — |  |
| FL01 | flood_same_creator | Same creator_id as FL02: with limiting on, a burst from one creator should eventually 429. | 200 | `b6dbd02dfb354101bbd2da20b15fb754` | unsure | 0.232 |  |
| FL02 | flood_same_creator | Same creator_id as FL01: with limiting on, a burst from one creator should eventually 429. | 200 | `6bc5767882684916ad6acad99301824a` | unsure | 0.232 |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 5 | 0 | 5 |
| `false_positive` | 3 | 0 | 3 |
| `flood_same_creator` | 2 | 0 | 2 |
| `malformed` | 5 | 0 | 5 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* Evade detection: typos added to AI-style text should raise word variety and drag the style signal down.

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "54aec4c7a2fe45078b87279edf869fd7",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.2421,
  "model_score": 0.327,
  "style_score": 0.4309,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* Evade detection: AI-style text split into short choppy sentences should raise sentence-length spread and drag the style signal down.

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "97a451ee4b6b47cead44425f42f9ac53",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.1365,
  "model_score": 0.4883,
  "style_score": 0.3752,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* Evade detection: a long human-style quotation pasted into AI-style text should dilute both signals toward human.

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "67a43f0591ec415f890cd7a9be3394f7",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.0974,
  "model_score": 0.7223,
  "style_score": 0.3751,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* Evade detection: AI-style text with extra punctuation sprinkled through it should raise punctuation density and drag the style signal down.

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "70ff5f328cf9457f8e0dac7ac8f63625",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.1086,
  "model_score": 0.711,
  "style_score": 0.3976,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* Evade detection: lightly edited AI-style text (a few words swapped) should still read as AI if the signals measure substance, not exact wording.

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "b1f5a3e339ed4f4c888dd8edf30ec8e3",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.1981,
  "model_score": 0.7603,
  "style_score": 0.4378,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* False positive check: plain, simple human-style writing (short words, short sentences) that a predictability signal may read as machine-like.

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "e9077ac539d54356af71e478224eb016",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "confidence": 0.4187,
  "model_score": 0.9102,
  "style_score": 0.5085,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* False positive check: a second-language writer's plain, careful prose with a small vocabulary.

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "ef24b2ff620e404fa4a9dacd68e93050",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.2468,
  "model_score": 0.8032,
  "style_score": 0.4436,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* False positive check: a short, plain human note — few sentences, so the style signal's spread measure is weak.

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "b1f8c7f5401448be809e45c26c5da1f4",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.1426,
  "model_score": 0.8361,
  "style_score": 0.3065,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* Empty body: the service must not crash on it.

```json
{
  "id": "MF01",
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

### MF02 — `malformed`

*Targeting:* Unparseable JSON: the service must answer 400, not 500.

```json
{
  "id": "MF02",
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

### MF03 — `malformed`

*Targeting:* Body is a JSON list, not an object: the service must answer 400, not 500.

```json
{
  "id": "MF03",
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

### MF04 — `malformed`

*Targeting:* text is a number, not a string: the service must answer 400, not 500.

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* Enormous text (50k chars, over the 20k route limit): the service must answer 400, not crash or hang. Kept under the harness's 128KB CSV field limit.

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01 — `flood_same_creator`

*Targeting:* Same creator_id as FL02: with limiting on, a burst from one creator should eventually 429.

```json
{
  "id": "FL01",
  "status": 200,
  "content_id": "b6dbd02dfb354101bbd2da20b15fb754",
  "creator_id": "flood_creator",
  "guess": "unsure",
  "confidence": 0.2315,
  "model_score": 0.8063,
  "style_score": 0.4252,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "error": null,
  "verdict": ""
}
```

### FL02 — `flood_same_creator`

*Targeting:* Same creator_id as FL01: with limiting on, a burst from one creator should eventually 429.

```json
{
  "id": "FL02",
  "status": 200,
  "content_id": "6bc5767882684916ad6acad99301824a",
  "creator_id": "flood_creator",
  "guess": "unsure",
  "confidence": 0.2315,
  "model_score": 0.8063,
  "style_score": 0.4252,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "error": null,
  "verdict": ""
}
```
