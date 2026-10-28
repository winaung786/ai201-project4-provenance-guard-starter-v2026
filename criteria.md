# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives on human-style writing

Of 10 human-style test paragraphs, at most 1 is labelled high-confidence AI
in each of three trials.

**Why this target:** A wrong accusation costs a real writer far more than a
missed detection costs a site, so the false-positive budget is tight — but
not zero, because plain conventional writing can read as machine-like and
one borderline case in ten is the honest allowance for that.

## 2. Score spread between AI-style and human-style writing

The mean combined score of 5 AI-style test paragraphs is at least 0.30 above
the mean combined score of 5 human-style test paragraphs, in each of three
trials.

**Why this target:** If the two kinds of writing do not separate by a clear
margin, the labels are noise no matter how the thresholds are set. 0.30 is
wide enough that a single borderline paragraph cannot fake a pass.

## 3. Label coverage

All three labels — high-confidence human, unsure, high-confidence AI —
appear across the label-coverage inputs in each of three trials.

**Why this target:** A label no input can reach is a dead band in the
scoring: it means the thresholds or the signals are not doing what the
README claims they do, and a reader can never actually receive that verdict.

## 4. The appeal path

Every appeal against a real content_id returns a confirmation and is
recorded in the audit log with status `under_review`, with the original
decision left untouched in the log; an appeal against an unknown content_id
returns 404. All appeal checks pass in each trial.

**Why this target:** The appeal path is the only thing standing between a
wrong accusation and nothing at all. If it silently drops appeals, or
overwrites the original decision, there is no recourse and no audit trail.

## 5. Bad input

All four malformed bodies — empty text, missing `text` field, null text, and
huge text — return a 4xx status (never a 5xx, never a crash) and each is
recorded in the audit log as a rejection.

**Why this target:** Malformed input is the most common real failure of a
web service. A crash on it is worse than a wrong label, because it takes the
whole service down for everyone else, and an unlogged rejection is an attack
nobody can find later.

---

> **STATUS: DRAFTS — proposed by the build coordinator for Mohammad's
> approval, not Mohammad's own words.** In unit 2 he wrote his own criteria;
> these are proposals he may edit or replace. The test paragraphs in
> `scenarios.py` are evaluation test inputs written for this evaluation
> (AI-style and human-style test paragraphs) — they are NOT Mohammad's own
> personal writing, and nothing in this repo claims they are.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
