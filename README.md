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

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
A real writer submits their own work a few times an hour — 10 a minute
never touches them. A script sending a thousand variations to map the
thresholds would need 100 minutes just to get through the minute buckets
and would hit the 200-a-day cap long before finishing the map. The numbers
are the starter defaults, kept deliberately: raising the minute limit
would let a threshold-mapping script finish in one sitting, and lowering
it would start blocking real writers who resubmit after an edit or two.

**What a caller counts as:** Per `creator_id` when the request supplies a
non-empty one, else per IP address (`app.py::rate_limit_key`). They fail
differently: one script can look like a thousand callers if it rotates
creator_id (which is why the full attack set, with one creator per attack,
never trips the limit), and one household or classroom behind one address
can look like one caller if creator_id is missing.

**The run of status codes when I pushed past it:**

```text
python run_attacks.py --flood 15
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

10 submissions accepted, then 5 rate-limited. The 429s were recorded in
the audit log as rejections with reason `rate_limited` — an attack that
shows up only as an absence is one nobody can find later. Full record:
`results/flood_2026-10-28_2311.md`.

---

## Attack Run — Before

Full record: `results/attack_run_2026-10-28_2311_before.md` (15 attacks, 0
auto-BROKE, 15 judged by hand). The attack set is locally constructed in
`attacks/` — the course's official CSVs were not present in this workspace
— covering the families the harness names: evasion, false_positive,
malformed, flood_same_creator. One harness limit found while building it:
the CSV reader's 128KB field limit caps the malformed huge body at 50,000
characters (still over the route's 20,000 limit, so the rejection is real).

Judgment rule for evasion, stated before the marks: an evasion counts as
BROKE if it lands in the human band, or if it drags the combined score at
least 0.20 toward human from the unattacked base text (0.6157). A label
that does not move is HELD; a score that moves a lot without flipping the
label is a near miss, and it is named as one.

| ID | Family | Before (guess, combined) | Verdict |
|---|---|---|---|
| EV01 | evasion (typos) | unsure, 0.379 | BROKE |
| EV02 | evasion (split sentences) | unsure, 0.432 | HELD (near miss) |
| EV03 | evasion (quote paste) | unsure, 0.549 | HELD |
| EV04 | evasion (punctuation) | unsure, 0.554 | HELD |
| EV05 | evasion (light edit) | unsure, 0.599 | HELD |
| FP01 | false_positive (plain simple prose) | ai, 0.709 | BROKE |
| FP02 | false_positive (second-language plain prose) | unsure, 0.623 | HELD (near miss) |
| FP03 | false_positive (short plain note) | unsure, 0.571 | HELD |
| MF01–MF05 | malformed | 400 × 5 | HELD |
| FL01–FL02 | flood_same_creator | 200 × 2 | HELD |

FL01/FL02 are not a break: two requests from one creator cannot trip a
10-per-minute limit, and the limit itself was proven by the flood run
above. The full attack set deliberately uses one creator per attack, so it
cannot test the limiter — that is what `--flood` is for.

**Ten audit log entries from the run**

```json
{"timestamp": "2026-10-28T23:11:43+00:00", "content_id": "e9077ac539d54356af71e478224eb016", "creator_id": "attacker_FP01", "guess": "ai", "model_score": 0.9102, "style_score": 0.5085, "combined_score": 0.7093, "status": "decided"}
{"timestamp": "2026-10-28T23:11:41+00:00", "content_id": "54aec4c7a2fe45078b87279edf869fd7", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.327, "style_score": 0.4309, "combined_score": 0.379, "status": "decided"}
{"timestamp": "2026-10-28T23:11:41+00:00", "content_id": "97a451ee4b6b47cead44425f42f9ac53", "creator_id": "attacker_EV02", "guess": "unsure", "model_score": 0.4883, "style_score": 0.3752, "combined_score": 0.4317, "status": "decided"}
{"timestamp": "2026-10-28T23:11:43+00:00", "content_id": "b1f5a3e339ed4f4c888dd8edf30ec8e3", "creator_id": "attacker_EV05", "guess": "unsure", "model_score": 0.7603, "style_score": 0.4378, "combined_score": 0.5991, "status": "decided"}
{"timestamp": "2026-10-28T23:11:44+00:00", "content_id": "ef24b2ff620e404fa4a9dacd68e93050", "creator_id": "attacker_FP02", "guess": "unsure", "model_score": 0.8032, "style_score": 0.4436, "combined_score": 0.6234, "status": "decided"}
{"timestamp": "2026-10-28T23:11:44+00:00", "content_id": "b1f8c7f5401448be809e45c26c5da1f4", "creator_id": "attacker_FP03", "guess": "unsure", "model_score": 0.8361, "style_score": 0.3065, "combined_score": 0.5713, "status": "decided"}
{"timestamp": "2026-10-28T23:11:28+00:00", "creator_id": "flood_tester", "status": "rejected", "event": "rejected", "reason": "rate_limited"}
{"timestamp": "2026-10-28T23:11:44+00:00", "creator_id": "attacker_MF04", "status": "rejected", "event": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-10-28T23:11:44+00:00", "creator_id": "attacker_MF05", "status": "rejected", "event": "rejected", "reason": "text_too_long"}
{"timestamp": "2026-10-28T23:11:44+00:00", "creator_id": "unknown", "status": "rejected", "event": "rejected", "reason": "invalid_json"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP01: plain, simple human-style writing ("I go to work every day. I take
the bus. The bus is slow...") labelled high-confidence AI at 0.709. The
model signal scored it 0.9102 — short common words are maximally
predictable — and the style signal (0.5085) did not pull it back. The
writer this accuses is exactly the plain writer with the least room to
argue back.



---

## Run Log and Verdicts

Full record: `results/run_2026-10-28_2313_before.md`. Criterion 4 was
tested by hand, because `run_eval.py` only sends submissions and an appeal
needs a content_id first: submit → appeal → read the log. The hand-check
passed before and after the improvement (appeal returns 200 with status
`under_review`, the original decision stays in the log untouched, and an
unknown content_id returns 404).

One finding about the trials themselves: all three trials produced
byte-identical scores. Perplexity is deterministic for a fixed text and
model, so identical input scores identically every time. Three identical
trials here is a finding about the signal, not a broken test — and it
means "the target must hold across all three trials" is decided by one
number repeated three times, not three independent draws.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives on human-style writing | At most 1 of 10 human-style test paragraphs labelled high-confidence AI | 0 | 0 | 0 | MET |
| 2. Score spread | AI-style mean at least 0.30 above human-style mean | 0.20 | 0.20 | 0.20 | MISSED |
| 3. Label coverage | All three labels appear across the coverage inputs | unsure only | unsure only | unsure only | MISSED |
| 4. The appeal path | Every real appeal recorded as under_review, original untouched, unknown → 404 | pass | pass | pass | MET |
| 5. Bad input | All 4 malformed bodies 4xx, never 5xx, logged as rejections | 400 × 4 | 400 × 4 | 400 × 4 | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

`results/run_2026-10-28_2313_before.md`, produced by `run_eval.py::main`
(score spread, trial 1 — first 5 rows are AI-style test paragraphs, last 5
are human-style; combined = mean of model_score and style_score):

```json
{"status": 200, "guess": "unsure", "model_score": 0.8063, "style_score": 0.4252, "combined": 0.6158}
{"status": 200, "guess": "ai", "model_score": 0.8997, "style_score": 0.4045, "combined": 0.6521}
{"status": 200, "guess": "unsure", "model_score": 0.936, "style_score": 0.3449, "combined": 0.6404}
{"status": 200, "guess": "unsure", "model_score": 0.8279, "style_score": 0.4097, "combined": 0.6188}
{"status": 200, "guess": "ai", "model_score": 0.9229, "style_score": 0.4192, "combined": 0.6711}
{"status": 200, "guess": "unsure", "model_score": 0.6669, "style_score": 0.2362, "combined": 0.4516}
{"status": 200, "guess": "unsure", "model_score": 0.7214, "style_score": 0.3, "combined": 0.5107}
{"status": 200, "guess": "unsure", "model_score": 0.6253, "style_score": 0.3356, "combined": 0.4804}
{"status": 200, "guess": "unsure", "model_score": 0.577, "style_score": 0.1656, "combined": 0.3713}
{"status": 200, "guess": "unsure", "model_score": 0.5979, "style_score": 0.1533, "combined": 0.3756}
```

AI-style mean 0.6396, human-style mean 0.4379, spread 0.2017 — under the
0.30 target.

**Diagnoses**

For each miss and each broken attack: the stage and the mechanism. The
five stages are the route, signal one, signal two, the combining rule, and
the label mapping.

- **EV01 typo evasion (BROKE) — stage: signal one.** The attack was
  designed to move the style signal, but the damage came through the model
  signal instead: model_score collapsed 0.8063 → 0.3270 while style_score
  barely moved (0.4252 → 0.4309). Perplexity measures predictability, and
  misspellings are maximally unpredictable to gpt2, so typo'd AI text
  reads as surprising — and therefore human — to signal one. The combining
  rule passed half the collapse through, dragging combined 0.6157 → 0.3790.
- **EV02 sentence-splitting (near miss) — stages: signal one + signal
  two.** Chopping sentences raised the spread (style 0.4252 → 0.3752) and
  also made the text less predictable (model 0.8063 → 0.4883). Combined
  fell 0.6157 → 0.4317, just short of the 0.20 line in my judgment rule.
  Same lesson as EV01: shape changes move both signals, not just the style
  one.
- **FP01 false positive (BROKE) — stage: signal one, via the combining
  rule.** Short common words are maximally predictable, so the model signal
  scored plain simple prose 0.9102; the style signal (0.5085) did not pull
  it back, and the 0.5 weight let combined cross the AI threshold at
  0.7093. The writers this signal is most likely to accuse are the ones
  with the least room to argue back — that is structural, not a bug.
- **Criterion 2 spread (MISSED) — stages: both signals + combining rule.**
  The model gap between the two test groups is only 0.24 (AI-style mean
  0.8786 vs human-style mean 0.6377) and the style gap 0.16. A weighted
  average can never exceed its largest input gap, so NO combining rule
  reaches 0.30 on these inputs — not even model-only. The 0.30 target
  exceeds what the signals separate. It stays MISSED and diagnosed; it is
  not revised, because a missed target is not a broken measurement.
- **Criterion 3 coverage (MISSED) — stages: label mapping + signals.**
  Before the improvement, human-style scores (0.37–0.51) and AI-style
  scores (0.62–0.67) both sat inside the 0.35–0.65 unsure band, so all three
  coverage inputs landed unsure. The "borderline" input is a second,
  separate problem: plain meeting prose scores 0.6119 because it reads
  AI-like to both signals (model 0.7738) — it is not actually borderline
  for this system.
- **Malformed + flood (HELD) — stage: the route.** Every malformed body
  returned 400 and was logged as a rejection; the flood run proved the
  limiter with 10×200 then 5×429. No diagnosis needed — the route stage
  works.



---

## The Improvement

**What I changed:**

One thing: the label thresholds in `config.py` — `HUMAN_THRESHOLD`
0.35 → 0.50, `AI_THRESHOLD` 0.65 → 0.60. No weights, no signals, no routes
changed. The label texts did not change; the Label Variants table above
was updated to the new ranges.

**Which diagnosis pointed at it:**

The label-mapping diagnosis behind criterion 3: the original 0.35/0.65
band left nearly every real input unsure, because human-style test scores
(0.37–0.51) and AI-style scores (0.62–0.67) both sat inside it. The new
band sits in the observed gap between the two clusters, so clear cases get
decided and only genuinely intermediate scores stay unsure.

### Attack Run — After

Full record: `results/attack_run_2026-10-28_2315_after.md`. Same 15 attacks,
same judgment rule.

| ID | Family | After (guess, combined) | Verdict |
|---|---|---|---|
| EV01 | evasion (typos) | human, 0.379 | BROKE (was unsure) |
| EV02 | evasion (split sentences) | human, 0.432 | BROKE (was unsure) |
| EV03 | evasion (quote paste) | unsure, 0.549 | HELD |
| EV04 | evasion (punctuation) | unsure, 0.554 | HELD |
| EV05 | evasion (light edit) | unsure, 0.599 | HELD |
| FP01 | false_positive (plain simple prose) | ai, 0.709 | BROKE (unchanged) |
| FP02 | false_positive (second-language plain prose) | ai, 0.623 | BROKE (was unsure) |
| FP03 | false_positive (short plain note) | unsure, 0.571 | HELD |
| MF01–MF05 | malformed | 400 × 5 | HELD |
| FL01–FL02 | flood_same_creator | ai, 0.616 | HELD (correct label; 200s expected) |

Eval run after: `results/run_2026-10-28_2316_after.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | At most 1 of 10 labelled AI | 0 | 0 | 0 | MET |
| 2. Score spread | AI mean ≥ human mean + 0.30 | 0.20 | 0.20 | 0.20 | MISSED |
| 3. Label coverage | All three labels appear | ai, human, ai | ai, human, ai | ai, human, ai | MISSED |
| 4. The appeal path | Real appeals recorded, unknown → 404 | pass | pass | pass | MET |
| 5. Bad input | All 4 bodies 4xx, logged | 400 × 4 | 400 × 4 | 400 × 4 | MET |

**Did it help, and how do I know:**

Partly, and the honest answer has two halves. What improved: labels are
now decisive instead of "unsure about everything" — AI-style test
paragraphs are labelled AI 5/5 (were 2/5), human-style ones are labelled
human 8/10 with 2 unsure and 0 AI, and criterion 3 moved from "unsure
only" to two of three labels. What got worse: narrowing the unsure band
helped every side, not just the honest one. Both typo and split-sentence
evasions now fully succeed (human labels), and FP02 — second-language
plain prose — is newly accused as AI. Criteria 2 and 3 are still MISSED:
thresholds move labels, not scores, so the 0.20 spread cannot change, and
the "borderline" coverage input still reads AI (0.6119). The improvement
bought decisiveness and paid for it in false positives and evasions.



---

## What's Still Broken

- **EV01/EV02 evasions succeed.** Typos and sentence-splitting push AI-style
  text into the human band (0.379, 0.432). What I'd do: add a signal that
  typos cannot move — for example, a spell-check-aware pass that scores the
  text before and after normalization, or a measure of argument structure
  rather than surface shape. Why I stopped: that is a third signal, which is
  a new build, not a fix — and the unit asks for one improvement, honestly
  measured, not a rebuild.
- **FP01/FP02 false positives.** Plain simple prose and second-language
  plain prose are labelled AI (0.709, 0.623). What I'd do: calibrate the
  model signal's midpoint against plain human writing specifically, or add
  a human-review gate before any high-confidence AI label is shown to a
  reader. Why I stopped: moving the model midpoint means editing
  `detector.py`, which is out of bounds for this build, and a review gate
  is a product decision, not a code fix.
- **Criterion 2 (spread 0.20 vs 0.30 target).** No combining rule can fix
  this — the largest input gap is the model signal's 0.24. What I'd do:
  find a genuinely more separating signal, or accept a lower target next
  time the criteria are written (not by revising this one — a missed target
  stays missed).
- **Criterion 3 (coverage).** The "borderline" input is not borderline for
  this system: plain meeting prose reads AI-like (model 0.774). What I'd
  do: pick coverage inputs from the system's actual score distribution
  instead of from intuition about what "borderline" means.
- **Short submissions.** With fewer than two sentences the style spread is
  0.0, which pushes the style signal toward AI. Short human notes are the
  most likely to be misread for this reason on top of the model signal's
  plain-prose problem.

**The trade I'd make if this ran for real:**

I would go back toward the wider unsure band and require a human review
before any high-confidence AI label is shown to anyone. Fewer wrong
accusations means more AI text getting through — and that is the right way
round, because the cost of a wrong accusation falls on one writer who
cannot easily argue back, while the cost of a missed detection falls on
the platform, a little, spread across everyone.



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
