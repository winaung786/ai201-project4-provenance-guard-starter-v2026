"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies, as a coefficient of variation.

    Sentence lengths are counted in words. The measure is
    stdev(lengths) / mean(lengths), so a long text and a short one are
    comparable. It is 0.0 when there are fewer than two sentences (there is
    nothing to vary), and it is typically between 0 and ~1 for real prose.

    Direction: HIGHER spread means more human. Human writing is lumpier — a
    three-word sentence next to a forty-word one — while generated prose
    marches in even, mid-length sentences. `style_signal` flips this measure
    for that reason.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.fmean(lengths)
    if mean == 0:
        return 0.0
    return statistics.stdev(lengths) / mean


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, between 0 and 1.

    Higher means more varied vocabulary. Returns 0.0 for empty text.

    Direction: HIGHER ratio means more human. Generated prose reuses a
    narrower band of vocabulary, because "most likely next word" pulls toward
    the common. `style_signal` flips this measure for that reason.

    Caveat (documented, not hidden): this measure falls as text gets longer,
    because common words repeat. Two texts of very different lengths are not
    directly comparable on it — which is why it is only one of three inputs
    to `style_signal`, and why the eval scenarios keep their texts at roughly
    similar lengths.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def punctuation_density(text: str) -> float:
    """
    Punctuation characters per word.

    Every character in `string.punctuation` counts (commas, periods,
    semicolons, dashes, quotes, and so on), divided by the word count.
    Returns 0.0 for text with no words. Typical prose lands roughly between
    0.05 and 0.25.

    Direction: HIGHER density means more human, weakly. Human writers vary
    their punctuation — semicolons, em dashes, parentheses, asides — while
    generated prose sticks to plain commas and periods. This is the weakest
    of the three measures: it moves a lot with topic and formatting, so
    `style_signal` weights it lowest, and a text that only differs here
    should not flip a decision on its own.
    """
    import string

    tokens = words(text)
    if not tokens:
        return 0.0
    punct = sum(1 for ch in text if ch in string.punctuation)
    return punct / len(tokens)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Each measure is flipped onto the AI direction and scaled to 0–1, then
    combined as a weighted average:

        spread component  = 1 - min(sentence_length_spread, 1.0)   weight 0.4
            Even sentences read AI-ish; lumpy sentences read human.
        vocabulary component = 1 - type_token_ratio                weight 0.4
            Repeated vocabulary reads AI-ish; varied vocabulary reads human.
        punctuation component = 1 - min(punctuation_density / 0.20, 1.0)
                                                                  weight 0.2
            Sparse punctuation reads AI-ish; varied punctuation reads human.
            The 0.20 reference is the top of the typical prose range, and the
            weight is lowest because this measure moves most with topic.

    A text with fewer than two sentences scores spread 0.0, which pushes the
    signal toward AI — that is a real limitation, not a neutral default, and
    it is why very short submissions land "unsure" more often than they
    should. It is documented here rather than smoothed over.
    """
    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punct = punctuation_density(text)

    spread_ai = 1.0 - min(spread, 1.0)
    vocab_ai = 1.0 - ttr
    punct_ai = 1.0 - min(punct / 0.20, 1.0)

    score = 0.4 * spread_ai + 0.4 * vocab_ai + 0.2 * punct_ai
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
