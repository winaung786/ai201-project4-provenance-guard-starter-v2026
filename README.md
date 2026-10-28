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
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.65 | We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation — it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it. |
| high-confidence AI | 0.65 – 1.00 | We think this was probably written by AI. |

**Why I worded the "unsure" one this way:**
It has to admit uncertainty without sounding like an accusation, because
the person reading it may well have written every word themselves. So it
says what the system *couldn't* do ("couldn't tell with confidence"),
explicitly denies that it is an accusation, and names the next step (a
human look) instead of leaving the writer to guess what happens now. All
three labels are reachable: scores at or below 0.35 are human, at or above
0.65 are AI, and everything between is unsure — verified by submitting
texts that land in each band.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

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

**An appeal**

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

**What the log shows afterwards**

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

Bad input, verified in the same session: empty text → 400 `empty_text`;
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
