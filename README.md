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

The path a submission takes, from arriving to the label a reader sees:

1. **Arrive** — `POST /submit` receives JSON `{"text": "...", "creator_id": "..."}`.
2. **Validate** — the route checks the body is a JSON object, `creator_id`
   is a non-empty string, and `text` is a non-empty string of at most
   `config.MAX_TEXT_CHARS` (20,000) characters. Anything else returns 400
   and is written to the audit log as a rejection, so a malformed request
   still leaves a trace instead of crashing the route.
3. **Signal one** — `detector.model_signal(text)` runs the local gpt2 model
   and returns a 0–1 score for how predictable the text is (higher = more
   likely AI). If the model is unavailable, the route returns 503 rather
   than inventing a model score.
4. **Signal two** — `stylometry.style_signal(text)` measures the shape of
   the text (sentence-length spread, vocabulary repetition, punctuation
   density) and returns a 0–1 score in the same direction.
5. **Combine** — `scoring.combine_signals(model_score, style_score)` takes
   the weighted average (0.5 / 0.5, see below).
6. **Label** — `scoring.score_to_label(combined)` turns the score into a
   guess (`ai` / `human` / `unsure`) and the full sentence a reader sees.
7. **Log and answer** — `audit.log_decision(...)` writes one JSON line with
   all nine required fields (timestamp, content_id, creator_id, guess,
   model_score, style_score, combined_score, label, status), and the route
   returns content_id, guess, confidence, label, combined_score, and both
   signal scores.

An appeal (`POST /appeal`) looks the content_id up with
`audit.entries_for`, records the appeal with `audit.log_appeal` (status
becomes `under_review`, original decision untouched), and confirms. An
unknown content_id returns 404 instead of failing silently.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to the local gpt2 model,
expressed as perplexity and squashed to a 0–1 score (higher = more likely
AI). Text a model finds easy to predict tends to be text a model wrote.

**Why that might differ between human and AI writing:** A language model
writes by repeatedly picking a likely next word, so model-produced text sits
in the high-probability region of the model's own distribution. Human
writing wanders more — odd word choices, abrupt turns, the specific rather
than the typical — and surprises the model more.

**What it can't see:** Predictability is not authorship. It rewards common
words in short, ordinary sentences, so plain conventional writing — someone
writing in a second language, a younger writer, anyone writing plainly on
purpose — scores about as machine-like as machine writing does. The writers
this signal is most likely to accuse are the ones with the least room to
argue back. Conversely, dense ornate prose full of rare words often scores
as *human*, because rare words are exactly what a model fails to predict.

### Signal two — the style signal

**What it measures:** The shape of the text, without reading a word of it:
sentence-length spread (coefficient of variation of sentence lengths in
words), type-token ratio (unique words over total words), and punctuation
density (punctuation characters per word). Each is flipped onto the
AI direction and combined 0.4 / 0.4 / 0.2 into a 0–1 score (higher = more
likely AI).

**Why that might differ between human and AI writing:** Generated prose
tends toward even, mid-length sentences and a narrower band of vocabulary,
because that is what "most likely next word" produces on average. Human
writing is lumpier — a three-word sentence next to a forty-word one — with
more varied vocabulary and punctuation.

**What it can't see:** It cannot read. Anything that changes the shape
without changing the substance moves it — adding typos, breaking up
sentences, pasting in a quotation. That is a very cheap thing to do on
purpose, and unit 8's attack set does it. It also punishes very short
submissions: with fewer than two sentences the spread is 0.0, which pushes
the signal toward AI. And type-token ratio falls as text gets longer, so
texts of very different lengths are not directly comparable on it.

### The combining rule

**The rule:** A weighted average of the two signals, both pointing the same
way (higher = more likely AI), clamped to 0–1. When the signals disagree,
the average lands in the unsure band — two methods disagreeing IS
uncertainty, not a reason to let the louder one win.

**The numbers:** model signal 0.5, style signal 0.5 (`config.py`:
`WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`). The weights stay equal
because the calibration runs gave no evidence that one signal is
systematically more trustworthy than the other. The trade, stated plainly:
this rule buys fewer false accusations at the cost of missed detections —
a text that is AI on one signal and human on the other is called unsure
rather than accused or cleared.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

The human-style test paragraph about missing the bus and walking to campus
in the rain: the model signal scored it 0.6669 (just over the AI threshold
on its own — plain, predictable wording) while the style signal scored it
0.2362 (lumpy sentences, varied vocabulary, human side). The combining rule
averaged them to 0.4516, which lands in the unsure band, and the reader sees
the unsure label rather than an accusation. That is the rule working as
designed: two methods disagreeing is uncertainty, and uncertainty must not
be reported as a verdict about a person.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 ≤ score ≤ 0.50 | We think this was probably written by a person. |
| unsure | 0.50 < score < 0.60 | We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it. |
| high-confidence AI | 0.60 ≤ score ≤ 1.00 | We think this was probably written by AI. |

> Ranges updated in unit 8: the original 0.35/0.65 band was recalibrated
> to 0.50/0.60 as the one improvement (see "The Improvement" below). The
> label texts did not change.

**Why I worded the "unsure" one this way:**
It has to admit uncertainty without sounding like an accusation, because
the person reading it may well have written every word themselves. So it
says what the system *couldn't* do ("couldn't tell with confidence"),
explicitly denies that it is an accusation, and names the next step (a
human look) instead of leaving the writer to guess what happens next. The
current code uses: scores at or below **0.50** → human; scores at or above
**0.60** → AI; scores strictly between → unsure. All three mapping branches
are defined, but the *after* evaluation inputs only produced two labels;
acceptance criterion 3 was therefore correctly marked **MISSED** below.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**Historical Unit 7 sample — before the Unit 8 threshold change.** This
request, response and appeal were captured when human scores were ≤ 0.35 and
AI scores were ≥ 0.65. A combined score of **0.61575** was therefore
**unsure** at that time. The current code uses human ≤ 0.50 and AI ≥ 0.60,
so **the same score would now be `ai`**, with the label
"We think this was probably written by AI." The historical response and
log excerpts are preserved verbatim, not rewritten as if they came from the
current code. The committed audit log primarily contains later runs; the
earlier content ID shown below is not in the current committed
`logs/audit.jsonl`.

**A submission (original thresholds)**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of effective time management strategies is essential for achieving success in both academic and professional settings. By prioritizing tasks, setting clear goals, and maintaining a structured schedule, individuals can significantly improve their productivity. It is important to note that consistency is key, and that small, daily habits often lead to the most meaningful long-term results. In addition, taking regular breaks can help maintain focus and prevent burnout over time.", "creator_id": "calib_AI-s"}'
```

```json
{
  "combined_score": 0.61575,
  "confidence": 0.2315,
  "content_id": "918c5949f465493d9dc255903fdece62",
  "guess": "unsure",
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "model_score": 0.8063,
  "style_score": 0.4252
}
```

**An appeal (original thresholds)**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "918c5949f465493d9dc255903fdece62", "reasoning": "I wrote this myself; please review."}'
```

```json
{
  "content_id": "918c5949f465493d9dc255903fdece62",
  "message": "Appeal recorded. The decision is now under review.",
  "status": "under_review"
}
```

**Historical audit-log excerpt captured immediately after that appeal**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "combined_score": 0.61575,
  "content_id": "918c5949f465493d9dc255903fdece62",
  "creator_id": "calib_AI-s",
  "guess": "unsure",
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "model_score": 0.8063,
  "status": "decided",
  "style_score": 0.4252,
  "timestamp": "2026-10-28T23:09:43+00:00"
}
{
  "content_id": "918c5949f465493d9dc255903fdece62",
  "creator_id": "calib_AI-s",
  "event": "appeal",
  "reasoning": "I wrote this myself; please review.",
  "status": "under_review",
  "timestamp": "2026-10-28T23:09:46+00:00"
}
```

**Current-threshold audit evidence (committed later).** The current
`logs/audit.jsonl` contains this separate decision-and-appeal pair under
the **0.50/0.60** thresholds. The combined score is 0.54045, so the
`unsure` label here **does** match the current code. These are real retained
log entries, not a fabricated rerun of the older curl request.

```json
{
  "timestamp": "2026-10-28T23:16:26+00:00",
  "content_id": "20271d26c3f3437db288a01dc1ee0c82",
  "creator_id": "appeal_after",
  "guess": "unsure",
  "model_score": 0.653,
  "style_score": 0.4279,
  "combined_score": 0.54045,
  "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
  "status": "decided"
}
{
  "timestamp": "2026-10-28T23:16:26+00:00",
  "content_id": "20271d26c3f3437db288a01dc1ee0c82",
  "creator_id": "appeal_after",
  "event": "appeal",
  "status": "under_review",
  "reasoning": "After-threshold hand-check."
}
```

Bad input, verified in the original session: empty text → 400 `empty_text`;
missing or null `text` → 400 `invalid_text`; 250,000-character text → 400
`text_too_long`; missing `creator_id` → 400 `missing_creator_id`. Every one
was recorded in the audit log as a rejection, and none crashed the route.

---

## How I Used AI

**Moment 1**

- *What I asked for:* How to turn the three stylometry measures into one
  0–1 style signal, with each measure's direction and scaling documented.
- *What came back:* Flip each measure onto the AI direction, scale each to
  0–1, and take a weighted average.
- *What I changed:* Chose the coefficient of variation for sentence-length
  spread (0.0 for fewer than two sentences), the 0.4 / 0.4 / 0.2 weights,
  and the 0.20 punctuation reference — then verified the signal actually
  separates AI-style test paragraphs (≈0.40–0.43) from human-style ones
  (≈0.24–0.30) before trusting it, instead of accepting the design on
  faith.

**Moment 2**

- *What I asked for:* The shape of the `/submit` and `/appeal` routes,
  including what to do with missing, empty, and enormous text.
- *What came back:* Validate inputs, call both signals, combine, label,
  log, and return both signal scores.
- *What I changed:* Made every bad-input case return 400 and write a
  rejection to the audit log (instead of crashing); made a missing detector
  model return 503 rather than a invented model score; defined
  `confidence` as distance from the unsure midpoint and documented it; and
  made an unknown content_id on appeal return 404 instead of failing
  silently.

**A note on authorship of this write-up:** This build was implemented with
AI assistance from the starter's brief and TODOs, and every claim in this
README was checked by running the code. The test paragraphs in
`scenarios.py` are AI-written evaluation test inputs, labelled as such —
they are not the author's own writing.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Unit 8 — Staff red-team run

On November 8, 2026, the service processed all 56 rows in the supplied
`attack_set.zip` twice. The archive contained `attacks.csv` (32 rows) and
`attacks_malformed_requests.csv` (24 rows). Its SHA-256 was
`2d122805ef92092fcadcc8307d38fe6b4e44f26c0726fc991a4d31d0e800a33b`.
The CSVs in `attacks/` and the October 28 reports are the earlier 15-case
local exercise. The November reports below are the staff-set evidence.
The flood description in the staff CSV says 20 submissions. The file
contains 12 flood rows, and all 12 were sent in each run.

The November baseline restored the pre-improvement thresholds from
`56bec1c^` in an isolated service process. The after run used the checked-in
thresholds from `56bec1c`. Both runs used the same local GPT-2 weights
(`openai-community/gpt2`, revision `607a30d783dfa663caf39e06633721c8d4cfcd7e`),
Python 3.12.14, PyTorch 2.8.0 CPU, Transformers 4.57.6, the same two signals
and equal weights, and fresh in-memory limiter state. The harness was
extended to capture response bodies, live appeals, and rejection audits.
The five targets in [criteria.md](criteria.md) are the original targets.
The supplied human-style criterion paragraphs are AI-written evaluation
fixtures. The results do not measure false positives on the student's own
writing, and the staff attack CSV does not independently establish
authorship for the human-style cases.

## Rate Limiting

The service allows **10 submissions per minute and 200 per day** per
non-empty string `creator_id`, with an IP fallback for unusable IDs.
Ten per minute allows a writer to submit a burst of revisions. At that
rate a single fixed key would need 100 minute windows to send 1,000 requests,
and the daily cap blocks that volume on day one. Because callers supply
the creator ID, rotating it can bypass the per-key limit. Shared addresses
can also share a fallback quota, and a service restart clears the counts.

```text
python run_attacks.py --flood 15
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

Full flood record: [flood_2026-11-08_1507.md](results/flood_2026-11-08_1507.md). Both `GET /health` checks showed the
model loaded and rate limiting on. Three separate probe submissions were
all present in `GET /log` with all nine decision fields. The five flood
429s also appeared as `rate_limited` rejections. The daily cap was configured
but the 15-request test exercised the minute cap.

## Attack run — Before and after

Full HTTP responses with both signal scores, content IDs, labels, and
reviewed judgments: [attack_run_2026-11-08_1507_staff_before.md](results/attack_run_2026-11-08_1507_staff_before.md) and [attack_run_2026-11-08_1508_staff_after.md](results/attack_run_2026-11-08_1508_staff_after.md).

| Family | Rows | Before held | Before broke | After held | After broke |
|---|---:|---:|---:|---:|---:|
| Evasion | 10 | 1 | 9 | 1 | 9 |
| False positive | 8 | 6 | 2 | 2 | 6 |
| Prompt injection | 6 | 6 | 0 | 6 | 0 |
| Malformed | 20 | 15 | 5 | 15 | 5 |
| Same-creator flood | 12 | 12 | 0 | 12 | 0 |
| **Total** | **56** | **40** | **16** | **36** | **20** |

Each run returned **39 HTTP 200**, **15 HTTP 400**, and **2 HTTP 429**
responses. All 112 requests had matching decisions or rejections in the
audit output. Every successful response had the same two signal scores,
combined score, and confidence in both runs.

**Judgment rules.** Evasion breaks if an AI-evasion case escapes the
high-confidence AI label. A human label is a stronger failure than
`unsure`, so the results distinguish the two. A false-positive case
breaks if it receives the AI label. For injection, a break requires evidence
that instructions overrode scoring, label text, or the audit record.
Malformed request bodies and non-prose should receive a controlled
rejection. Arabic prose is valid input. MF07 is marked broken because the
ASCII feature extractor produced an unjustified high-confidence AI
classification. The flood passes when the first ten rows succeed and the
next two return audited 429s. Statuses, scores, and verdicts follow.

| ID | Family | Before response | Before | After response | After |
|---|---|---|---|---|---|
| EV01 | evasion | 200 human (0.3108) | BROKE | 200 human (0.3108) | BROKE |
| EV02 | evasion | 200 unsure (0.3856) | BROKE | 200 human (0.3856) | BROKE |
| EV03 | evasion | 200 unsure (0.4821) | BROKE | 200 human (0.4821) | BROKE |
| EV04 | evasion | 200 unsure (0.5267) | BROKE | 200 unsure (0.5267) | BROKE |
| EV05 | evasion | 200 human (0.2926) | BROKE | 200 human (0.2926) | BROKE |
| EV06 | evasion | 200 unsure (0.3928) | BROKE | 200 human (0.3928) | BROKE |
| EV07 | evasion | 200 unsure (0.5385) | BROKE | 200 unsure (0.5385) | BROKE |
| EV08 | evasion | 200 human (0.2661) | BROKE | 200 human (0.2661) | BROKE |
| EV09 | evasion | 200 unsure (0.5037) | BROKE | 200 unsure (0.5037) | BROKE |
| EV10 | evasion | 200 ai (0.8275) | HELD | 200 ai (0.8275) | HELD |
| FP01 | false_positive | 200 unsure (0.5270) | HELD | 200 unsure (0.5270) | HELD |
| FP02 | false_positive | 200 unsure (0.6265) | HELD | 200 ai (0.6265) | BROKE |
| FP03 | false_positive | 200 ai (0.6502) | BROKE | 200 ai (0.6502) | BROKE |
| FP04 | false_positive | 200 unsure (0.6151) | HELD | 200 ai (0.6151) | BROKE |
| FP05 | false_positive | 200 ai (0.6634) | BROKE | 200 ai (0.6634) | BROKE |
| FP06 | false_positive | 200 unsure (0.6353) | HELD | 200 ai (0.6353) | BROKE |
| FP07 | false_positive | 200 unsure (0.6268) | HELD | 200 ai (0.6268) | BROKE |
| FP08 | false_positive | 200 human (0.2745) | HELD | 200 human (0.2745) | HELD |
| PI01 | prompt_injection | 200 unsure (0.3565) | HELD | 200 human (0.3565) | HELD |
| PI02 | prompt_injection | 200 human (0.1807) | HELD | 200 human (0.1807) | HELD |
| PI03 | prompt_injection | 200 unsure (0.4831) | HELD | 200 human (0.4831) | HELD |
| PI04 | prompt_injection | 200 unsure (0.3980) | HELD | 200 human (0.3980) | HELD |
| PI05 | prompt_injection | 200 unsure (0.4325) | HELD | 200 human (0.4325) | HELD |
| PI06 | prompt_injection | 200 unsure (0.4998) | HELD | 200 human (0.4998) | HELD |
| MF01 | malformed | 400 `empty_text` | HELD | 400 `empty_text` | HELD |
| MF02 | malformed | 400 `text_too_short` | HELD | 400 `text_too_short` | HELD |
| MF03 | malformed | 200 human (0.2000) | BROKE | 200 human (0.2000) | BROKE |
| MF04 | malformed | 200 unsure (0.5056) | BROKE | 200 unsure (0.5056) | BROKE |
| MF05 | malformed | 200 ai (0.7988) | BROKE | 200 ai (0.7988) | BROKE |
| MF06 | malformed | 200 ai (0.9985) | BROKE | 200 ai (0.9985) | BROKE |
| MF07 | malformed | 200 ai (0.9532) | BROKE | 200 ai (0.9532) | BROKE |
| MF08 | malformed | 400 `text_too_long` | HELD | 400 `text_too_long` | HELD |
| RQ01 | malformed | 400 `invalid_text` | HELD | 400 `invalid_text` | HELD |
| RQ02 | malformed | 400 `missing_creator_id` | HELD | 400 `missing_creator_id` | HELD |
| RQ03 | malformed | 400 `invalid_text` | HELD | 400 `invalid_text` | HELD |
| RQ04 | malformed | 400 `invalid_text` | HELD | 400 `invalid_text` | HELD |
| RQ05 | malformed | 400 `invalid_text` | HELD | 400 `invalid_text` | HELD |
| RQ06 | malformed | 400 `missing_creator_id` | HELD | 400 `missing_creator_id` | HELD |
| RQ07 | malformed | 400 `invalid_json` | HELD | 400 `invalid_json` | HELD |
| RQ08 | malformed | 400 `invalid_json` | HELD | 400 `invalid_json` | HELD |
| RQ09 | malformed | 400 `invalid_json` | HELD | 400 `invalid_json` | HELD |
| RQ10 | malformed | 400 `invalid_json` | HELD | 400 `invalid_json` | HELD |
| RQ11 | malformed | 400 `invalid_json` | HELD | 400 `invalid_json` | HELD |
| RQ12 | malformed | 400 `invalid_text` | HELD | 400 `invalid_text` | HELD |
| FL01_01 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_02 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_03 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_04 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_05 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_06 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_07 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_08 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_09 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_10 | flood_same_creator | 200 human (0.2588) | HELD | 200 human (0.2588) | HELD |
| FL01_11 | flood_same_creator | 429 `rate_limited` | HELD | 429 `rate_limited` | HELD |
| FL01_12 | flood_same_creator | 429 `rate_limited` | HELD | 429 `rate_limited` | HELD |

### Diagnosis for every broken attack

Scores below are model / style → combined. Where the ZIP supplied only a
modified input, the diagnosis describes the features and scores observed
in that input. It does not estimate a change against an unprovided control.

| Attack | Pipeline stage and mechanism |
|---|---|
| EV01 | **Signal one and combining rule.** The misspellings are hard for GPT-2 to predict. The model score of 0.1635 pulled the average of the two signals down to 0.3108 despite style at 0.4581. |
| EV02 | **Signal two and label mapping.** Added short sentences yielded a sentence-length spread of 0.849 and style of 0.1768. Model 0.5943 averaged to 0.3856, which changed from unsure to human under the new mapping. |
| EV03 | **Signal two and label mapping.** The quotation mixed in varied sentences and punctuation. Model 0.6662 and style 0.2981 averaged to 0.48215, which changed from unsure to human. |
| EV04 | **Signal one and combining rule.** Unusual wording tests token predictability. The model yielded 0.6114 and style 0.4420, so their equal average of 0.5267 abstained in both runs. |
| EV05 | **Both signals.** The heavily edited case had uneven sentences and diverse phrasing. GPT-2 scored 0.3212 and style scored 0.2640. Both contributed to the human decision at 0.2926. |
| EV06 | **Signal two and label mapping.** Mixing very long and short sentences gave spread 1.186, enough to drive the spread component to zero. Model 0.5727 and style 0.2130 averaged to 0.39285, which changed from unsure to human. |
| EV07 | **Signal two and combining rule.** Punctuation density of 0.227 maxed out the human-direction punctuation adjustment. The input also formed one sentence for the sentence splitter, so the spread component pulled back toward AI. Model 0.5862 and style 0.4907 averaged to 0.5385, inside both unsure bands. |
| EV08 | **Signal one and combining rule.** The ten-word sample passed the three-token floor. With little text to score, its model score was 0.2452 and its style score was 0.2869, including a vocabulary ratio of 1.0. The 0.2661 combined score classified it as human twice. |
| EV09 | **Signal two and combining rule.** The colloquial opening introduced varied sentence lengths and vocabulary. Style 0.3031 pulled model 0.7042 down to 0.5037, so the case stayed unsure. |
| FP02 | **Signal one and label mapping.** Formulaic report language yielded model 0.7387 and style 0.5144. The 0.62655 average cleared the new AI cutoff. |
| FP03 | **Signal one and combining rule.** Plain, careful second-language prose was predictable to GPT-2 (0.8051). Style 0.4952 only partly offset it. The 0.65015 average crossed both AI thresholds. |
| FP04 | **Signal one and label mapping.** The rubric-driven structure gave model 0.8329, which outweighed style 0.3974 in the average. The unchanged 0.61515 crossed the new cutoff. |
| FP05 | **Both signals and combining rule.** Predictable procedural language (0.8005 model) and relatively uniform sentence lengths (0.5264 style) averaged to 0.66345, an AI label in both runs. |
| FP06 | **Signal one and label mapping.** Stock letter phrases gave model 0.8814. Even with style 0.3892, the combined score of 0.6353 cleared the new cutoff. |
| FP07 | **Signal one and label mapping.** Repeated sentence openings were predictable (0.8816 model). The lower style score of 0.3720 still left 0.6268, which cleared the new cutoff. |
| MF03 | **Route.** The input is nonblank and yields enough tokens, so control codes passed validation. GPT-2 scored 0.0000 and the service returned a normal human decision at 0.2000. |
| MF04 | **Route and signal two.** Punctuation-only input passed validation and yielded zero recognized words. All three style components defaulted toward AI, giving style 1.0000 against model 0.0112. The 0.5056 average produced a normal unsure decision. |
| MF05 | **Route and signal one.** The single 4,000-character repeated-letter word fits the character cap and tokenizes as many GPT-2 tokens. The repeated sequence was predictable (model 0.9976). Style 0.6000 and model averaged to 0.7988, a normal AI decision. |
| MF06 | **Route and both signals.** Emoji-only content passed validation. The repeating sequence gave model 0.9969 and the ASCII word regex yielded zero words, which gave style 1.0000. The combined score was 0.99845. |
| MF07 | **Signal two and combining rule.** The Arabic sentence contained zero words under `stylometry.words`' ASCII regex. The zero-count defaults made every style component contribute toward AI, yielding 1.0000. GPT-2 also yielded 0.9064. The resulting 0.9532 confidently labelled the Arabic passage AI in both runs. |

**Worst outcome.** MF07 was the most concerning result for a writer. The
Arabic sentence was meaningful prose, yet the system called it AI at
0.9532 and showed confidence 0.9064. The language coverage failure is
directly visible in the zero word count and maximum style score.

**Prompt injection.** PI02 asked for `human` with confidence 0.02. The
service did return `human`, with computed confidence 0.6386, from model
0.2044 and style 0.1570. The model uses a forward pass with the input as its
own labels to calculate token loss. The response uses a fixed label chosen
from the weighted score. PI04 did not put its script into the returned
label, and PI05 did not insert its proposed guess, score, or `note` field
into the audit. All six responses matched the numeric score mapping.
All six ended in the human band after the change, which exposes a score
evasion risk even though there was no instruction override.

### Audit log excerpts

Twelve entries returned by `GET /log` from the staff baseline, in this
order: EV01, EV02, EV03, FP03, FP05, PI02, PI05, MF04, MF06, MF07, MF08,
FL01_11. Full records for both phases are appended to [logs/audit.jsonl](logs/audit.jsonl).
A decision includes timestamp, content ID, creator ID, guess, both signal
scores, combined score, the label shown to the writer, and status.
Rejections include a reason, with the limit for a 429.

```jsonl
{"combined_score": 0.3108, "content_id": "2d696eaa4e95437182def0b092cca25f", "creator_id": "attacker_EV01", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.1635, "status": "decided", "style_score": 0.4581, "timestamp": "2026-11-08T21:07:42+00:00"}
{"combined_score": 0.38555000000000006, "content_id": "9e8a8271453145d79a93221f321d5894", "creator_id": "attacker_EV02", "guess": "unsure", "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.", "model_score": 0.5943, "status": "decided", "style_score": 0.1768, "timestamp": "2026-11-08T21:07:42+00:00"}
{"combined_score": 0.48214999999999997, "content_id": "1c07ae3d87e34a2dabc059278af6e603", "creator_id": "attacker_EV03", "guess": "unsure", "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.", "model_score": 0.6662, "status": "decided", "style_score": 0.2981, "timestamp": "2026-11-08T21:07:42+00:00"}
{"combined_score": 0.65015, "content_id": "6026981a94f946e1ad731eb04139b531", "creator_id": "attacker_FP03", "guess": "ai", "label": "We think this was probably written by AI.", "model_score": 0.8051, "status": "decided", "style_score": 0.4952, "timestamp": "2026-11-08T21:07:45+00:00"}
{"combined_score": 0.66345, "content_id": "3f81064cbacc431cb08799141460110b", "creator_id": "attacker_FP05", "guess": "ai", "label": "We think this was probably written by AI.", "model_score": 0.8005, "status": "decided", "style_score": 0.5264, "timestamp": "2026-11-08T21:07:46+00:00"}
{"combined_score": 0.1807, "content_id": "58e218157ac64dd7a6f54e26fefa47ba", "creator_id": "attacker_PI02", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.2044, "status": "decided", "style_score": 0.157, "timestamp": "2026-11-08T21:07:47+00:00"}
{"combined_score": 0.43245, "content_id": "5a017b8fde344b4b9e3e2105717abc9f", "creator_id": "attacker_PI05", "guess": "unsure", "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.", "model_score": 0.6401, "status": "decided", "style_score": 0.2248, "timestamp": "2026-11-08T21:07:47+00:00"}
{"combined_score": 0.5056, "content_id": "0cdd44548b9d43e1acf38685110c9435", "creator_id": "attacker_MF04", "guess": "unsure", "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.", "model_score": 0.0112, "status": "decided", "style_score": 1.0, "timestamp": "2026-11-08T21:07:48+00:00"}
{"combined_score": 0.9984500000000001, "content_id": "4c9e9990f692464e9c8bad030589fa13", "creator_id": "attacker_MF06", "guess": "ai", "label": "We think this was probably written by AI.", "model_score": 0.9969, "status": "decided", "style_score": 1.0, "timestamp": "2026-11-08T21:07:49+00:00"}
{"combined_score": 0.9532, "content_id": "37fa60c30abd43a2897f123704f07c62", "creator_id": "attacker_MF07", "guess": "ai", "label": "We think this was probably written by AI.", "model_score": 0.9064, "status": "decided", "style_score": 1.0, "timestamp": "2026-11-08T21:07:50+00:00"}
{"creator_id": "attacker_MF08", "event": "rejected", "reason": "text_too_long", "status": "rejected", "timestamp": "2026-11-08T21:07:50+00:00"}
{"creator_id": "attacker_flood", "event": "rejected", "limit": "10 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-08T21:07:51+00:00"}
```

## Run log and verdicts

The live reports are [run_2026-11-08_1508_staff_before.md](results/run_2026-11-08_1508_staff_before.md) and [run_2026-11-08_1509_staff_after.md](results/run_2026-11-08_1509_staff_after.md). Every criterion
was run three times under each threshold setting. Scores and verdicts
were stable across repeats. The server generated new content IDs for the
individual submissions.

### Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives on human-style writing | ≤1 of 10 flagged AI | 0/10 | 0/10 | 0/10 | MET |
| 2. Score spread | AI-style mean ≥ human-style mean + 0.30 | 0.2017 | 0.2017 | 0.2017 | MISSED |
| 3. Label coverage | All 3 labels present | unsure, unsure, unsure | unsure, unsure, unsure | unsure, unsure, unsure | MISSED |
| 4. Appeal path | Known appeal 200 and logged under_review, original intact, unknown 404 | 5/5 | 5/5 | 5/5 | MET |
| 5. Bad input | All 4 return 4xx with matching audit rejections | 4/4 | 4/4 | 4/4 | MET |

### After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives on human-style writing | ≤1 of 10 flagged AI | 0/10 | 0/10 | 0/10 | MET |
| 2. Score spread | AI-style mean ≥ human-style mean + 0.30 | 0.2017 | 0.2017 | 0.2017 | MISSED |
| 3. Label coverage | All 3 labels present | ai, human, ai | ai, human, ai | ai, human, ai | MISSED |
| 4. Appeal path | Known appeal 200 and logged under_review, original intact, unknown 404 | 5/5 | 5/5 | 5/5 | MET |
| 5. Bad input | All 4 return 4xx with matching audit rejections | 4/4 | 4/4 | 4/4 | MET |

1. **False positives on the fixtures — MET.** Zero of ten received an AI
   label in all six trials. The staff human-style cases include more
   predictable examples and produced a different result.
2. **Score spread — MISSED.** The model-score means were 0.87856 and
   0.63770 (gap 0.24086). Style means were 0.40070 and 0.23814 (gap
   0.16256). The 50/50 combining rule averaged those gaps to 0.20171.
   Reweighting just these two signals with nonnegative weights summing
   to one cannot reach 0.30 on these inputs. Thresholds operate after
   scoring, so they leave the gap unchanged.
3. **Label coverage — MISSED.** The three existing coverage inputs scored
   0.61575, 0.45155, and 0.61195. All fell inside the original unsure band.
   The narrower band yielded AI, human, AI. The intended borderline
   example is predictable meeting prose (model 0.7738), so it crossed
   the new AI cutoff. This verdict applies to the three filed scenario
   inputs. Other after-run cases did receive `unsure`.
4. **Appeal path — MET.** Each trial confirmed a real appeal with
   `under_review`, appended a matching appeal event, preserved every field of the original
   decision, and returned 404 for the unknown ID.
5. **Bad input — MET.** All four criterion bodies returned 400 in every
   trial. Each had a new rejection with the same reason as the HTTP response.

### Actual JSON excerpts

#### Before excerpts

From [run_2026-11-08_1508_staff_before.md](results/run_2026-11-08_1508_staff_before.md), produced by `run_eval.py::run_trial` and `run_eval.py::write_report`. Criterion 4 also uses `run_eval.py::appeal_evidence`.

**Criterion 1 · False positives on human-style writing · trial 1**

```json
{
  "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
  "status": 200,
  "response": {
    "combined_score": 0.45155,
    "confidence": 0.0969,
    "content_id": "6cafebf6bb4d43059ebcb80846d407ee",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.6669,
    "style_score": 0.2362
  }
}
```

**Criterion 2 · Score spread · trial 1**

```json
{
  "sent": "The implementation of effective time management strategies is essentia",
  "status": 200,
  "response": {
    "combined_score": 0.61575,
    "confidence": 0.2315,
    "content_id": "c5978728633f4998854b60220fcb964a",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.8063,
    "style_score": 0.4252
  }
}
```

**Criterion 3 · Label coverage · trial 1**

```json
{
  "sent": "The meeting is on Tuesday at ten in the morning. Please bring your not",
  "status": 200,
  "response": {
    "combined_score": 0.61195,
    "confidence": 0.2239,
    "content_id": "9b4ead881cd24ade9cf6bff7a7797b06",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.7738,
    "style_score": 0.4501
  }
}
```

**Criterion 4 · Appeal path · trial 1**

```json
{
  "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
  "status": 200,
  "response": {
    "combined_score": 0.45155,
    "confidence": 0.0969,
    "content_id": "239a664029b84ea788b007a141603248",
    "guess": "unsure",
    "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
    "model_score": 0.6669,
    "style_score": 0.2362
  },
  "original_history": [
    {
      "combined_score": 0.45155,
      "content_id": "239a664029b84ea788b007a141603248",
      "creator_id": "eval_appeal path_1",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.6669,
      "status": "decided",
      "style_score": 0.2362,
      "timestamp": "2026-11-08T21:08:11+00:00"
    }
  ],
  "appeal": {
    "status": 200,
    "response": {
      "content_id": "239a664029b84ea788b007a141603248",
      "message": "Appeal recorded. The decision is now under review.",
      "status": "under_review"
    }
  },
  "unknown_appeal": {
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No submission found with content_id 'unknown-8ad56b3ef7f24c5b97f8175c7c6136ce'."
    }
  },
  "final_history": [
    {
      "combined_score": 0.45155,
      "content_id": "239a664029b84ea788b007a141603248",
      "creator_id": "eval_appeal path_1",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.6669,
      "status": "decided",
      "style_score": 0.2362,
      "timestamp": "2026-11-08T21:08:11+00:00"
    },
    {
      "content_id": "239a664029b84ea788b007a141603248",
      "creator_id": "eval_appeal path_1",
      "event": "appeal",
      "reasoning": "Please review this test decision.",
      "status": "under_review",
      "timestamp": "2026-11-08T21:08:11+00:00"
    }
  ]
}
```

**Criterion 5 · Bad input · trial 1**

```json
{
  "sent": "(empty text)",
  "status": 400,
  "response": {
    "error": "empty_text",
    "message": "text must not be empty."
  },
  "audit_entries": [
    {
      "creator_id": "eval_bad_empty",
      "event": "rejected",
      "reason": "empty_text",
      "status": "rejected",
      "timestamp": "2026-11-08T21:08:12+00:00"
    }
  ]
}
```

#### After excerpts

From [run_2026-11-08_1509_staff_after.md](results/run_2026-11-08_1509_staff_after.md), produced by `run_eval.py::run_trial` and `run_eval.py::write_report`. Criterion 4 also uses `run_eval.py::appeal_evidence`.

**Criterion 1 · False positives on human-style writing · trial 1**

```json
{
  "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
  "status": 200,
  "response": {
    "combined_score": 0.45155,
    "confidence": 0.0969,
    "content_id": "4da3e109ddb54a90a282072746166281",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.6669,
    "style_score": 0.2362
  }
}
```

**Criterion 2 · Score spread · trial 1**

```json
{
  "sent": "The implementation of effective time management strategies is essentia",
  "status": 200,
  "response": {
    "combined_score": 0.61575,
    "confidence": 0.2315,
    "content_id": "afbe2275412f4c05a57619b78fcfcbdd",
    "guess": "ai",
    "label": "We think this was probably written by AI.",
    "model_score": 0.8063,
    "style_score": 0.4252
  }
}
```

**Criterion 3 · Label coverage · trial 1**

```json
{
  "sent": "The meeting is on Tuesday at ten in the morning. Please bring your not",
  "status": 200,
  "response": {
    "combined_score": 0.61195,
    "confidence": 0.2239,
    "content_id": "9aaa2d99b9a14d7483211b0e5caa828f",
    "guess": "ai",
    "label": "We think this was probably written by AI.",
    "model_score": 0.7738,
    "style_score": 0.4501
  }
}
```

**Criterion 4 · Appeal path · trial 1**

```json
{
  "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
  "status": 200,
  "response": {
    "combined_score": 0.45155,
    "confidence": 0.0969,
    "content_id": "5a2358332a1d48beaf26255af300d66a",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.6669,
    "style_score": 0.2362
  },
  "original_history": [
    {
      "combined_score": 0.45155,
      "content_id": "5a2358332a1d48beaf26255af300d66a",
      "creator_id": "eval_appeal path_1",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "status": "decided",
      "style_score": 0.2362,
      "timestamp": "2026-11-08T21:09:01+00:00"
    }
  ],
  "appeal": {
    "status": 200,
    "response": {
      "content_id": "5a2358332a1d48beaf26255af300d66a",
      "message": "Appeal recorded. The decision is now under review.",
      "status": "under_review"
    }
  },
  "unknown_appeal": {
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "No submission found with content_id 'unknown-88389ec609ed4654a43e28446824f107'."
    }
  },
  "final_history": [
    {
      "combined_score": 0.45155,
      "content_id": "5a2358332a1d48beaf26255af300d66a",
      "creator_id": "eval_appeal path_1",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "status": "decided",
      "style_score": 0.2362,
      "timestamp": "2026-11-08T21:09:01+00:00"
    },
    {
      "content_id": "5a2358332a1d48beaf26255af300d66a",
      "creator_id": "eval_appeal path_1",
      "event": "appeal",
      "reasoning": "Please review this test decision.",
      "status": "under_review",
      "timestamp": "2026-11-08T21:09:01+00:00"
    }
  ]
}
```

**Criterion 5 · Bad input · trial 1**

```json
{
  "sent": "(empty text)",
  "status": 400,
  "response": {
    "error": "empty_text",
    "message": "text must not be empty."
  },
  "audit_entries": [
    {
      "creator_id": "eval_bad_empty",
      "event": "rejected",
      "reason": "empty_text",
      "status": "rejected",
      "timestamp": "2026-11-08T21:09:01+00:00"
    }
  ]
}
```

## The improvement

The single service change evaluated was narrowing the `unsure` band in
`config.py` from 0.35–0.65 to 0.50–0.60 (human at or below the lower
bound, AI at or above the upper bound). Commit `56bec1c` made this change
during the local exercise after the coverage inputs all landed unsure.
This staff run measured the same change against unseen staff inputs.
Signals, weights, routes, limiter settings, and audit behavior were held fixed.

The threshold change made more classifications decisive. In criterion 2,
AI-style examples classified AI went from **2/5 to 5/5**, while the
combined score gap stayed **0.2017**. Criterion 3 covered two labels
instead of one, still short of the three-label target. On the staff set,
the number of evasion cases receiving a human label doubled from **3/10
to 6/10**, and human-style cases flagged AI increased from **2/8 to 6/8**.
Only EV10 was caught as AI in both settings. Overall, the change reduced
the count held from **40/56 to 36/56**. It made the system more decisive,
at a cost to both evasion resistance and false accusations.

## What's still broken

The next change I would test is a Unicode-aware word tokenizer with
an explicit insufficient-evidence path for inputs without usable words.
MF07 gives a direct reason to start there, and MF04 and MF06 expose the same
zero-word failure. A separate test of threshold calibration would need
real, consented writing from varied styles and languages. Criterion 2 needs
a more discriminating signal, and the unauthenticated creator ID remains
an independent quota bypass. I stopped after the one measured threshold
change so that each outcome could be attributed to it.

### Reproducing the runs

Extract the supplied ZIP next to the repository. Start with a fresh local
process for each phase so flood quotas are comparable. For the before
process, start Flask from the repo with the original thresholds:

```bash
python -c "import config; config.HUMAN_THRESHOLD, config.AI_THRESHOLD = 0.35, 0.65; config.DEBUG = False; from app import main; main()"
```

Run the flood check, the staff file, and the criteria in a second terminal:

```bash
python run_attacks.py --flood 15
python run_attacks.py --set ../attack_set --label staff_before
python run_eval.py --label staff_before
```

Stop the before process, then start the service with the checked-in
thresholds. Run the same staff set and criteria again:

```bash
python app.py
```

```bash
python run_attacks.py --set ../attack_set --label staff_after
python run_eval.py --label staff_after
```

`python test.py` reported eight passes, zero failures, and one warning
because it searches the default model-cache directory. The service used
a pinned local GPT-2 snapshot and verified loading through `/health`.
All seven focused tests passed with `python -m unittest discover -s tests -v`.
