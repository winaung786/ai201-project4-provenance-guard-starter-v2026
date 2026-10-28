"""
What your test runs. <- UNIT 8, MILESTONE 3

Each of the five draft criteria in criteria.md needs something run against
it. `run_eval.py` runs everything here three times.

HONESTY NOTE (read this before quoting any paragraph): every paragraph below
is an EVALUATION TEST INPUT written for this evaluation. The "human-style"
paragraphs are test paragraphs written in a human style; the "AI-style"
paragraphs are test paragraphs written in a generic AI style. NONE of them is
Mohammad's own personal writing, and nothing in this repo claims otherwise.
Criterion 1 is therefore a test of false positives on human-style test
writing, not a claim about Mohammad's own prose.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.

Criterion 4 (the appeal path) has no scenario here: an appeal needs a
submission first and then an appeal against the content_id that came back,
which run_eval.py does not do. It is tested by hand (submit, appeal, read the
log) and the evidence is pasted into README.md. Saying which was done by hand
is part of the write-up.
"""

# --- Human-style test paragraphs (evaluation test inputs) -------------------
# Varied, lumpy, specific prose: first person, asides, uneven sentences.

HUMAN_STYLE = [
    "I missed the bus again on Tuesday, which meant I walked the whole way to "
    "campus in the rain, and by the time I got to class my notebook was soaked "
    "through. The professor didn't even look up. I sat in the back, dripping, "
    "trying to dry the pages on the radiator during the break. It didn't work. "
    "Honestly, the worst part wasn't the rain — it was knowing I'd set two "
    "alarms and slept through both of them because I'd stayed up too late "
    "finishing a lab report I probably could have finished on Sunday.",
    "My grandmother makes this soup every winter, and no matter how many times "
    "I watch her, I can't get it right. She doesn't measure anything. A handful "
    "of this, a pinch of that, and then she tastes it, frowns, and adds more "
    "salt. Last December I tried to write the recipe down while she cooked, and "
    "she laughed at me. 'You can't write soup,' she said. She was right, by the "
    "way — mine came out thin and bland, and she fixed it with half a lemon and "
    "something she wouldn't name.",
    "The first time I tried to fix my bike, I made it worse. I loosened the "
    "wrong bolt, the chain came off completely, and grease got all over my "
    "hands and then, somehow, my shirt. A neighbor came over with an actual "
    "wrench set and showed me what I'd done wrong in about thirty seconds. "
    "Thirty seconds! I'd been struggling for an hour. I still think about that "
    "whenever I'm tempted to skip the instructions and just figure it out as "
    "I go. Sometimes figuring it out as you go just means breaking it twice.",
    "We moved apartments in July, and the elevator in the new building broke "
    "on moving day. Of course it did. So we carried everything — couch, "
    "mattress, boxes of books I should have donated years ago — up four "
    "flights of stairs in the heat. My brother kept saying we should have hired "
    "movers. He was right. But by nine o'clock we were sitting on the floor "
    "eating cold pizza out of the box, surrounded by boxes, and it felt, "
    "strangely, like home already. Tired, sweaty, home.",
    "I used to hate running. Hated it. Then a friend talked me into a 5K, and "
    "I trained for it badly — skipped half the runs, went too hard on the "
    "others, got shin splints two weeks before race day. Race morning was cold "
    "and I almost didn't go. But I did, and somewhere around kilometer three, "
    "when my legs stopped complaining and the crowd was cheering for strangers, "
    "I understood why people do this. I still don't love running. But I signed "
    "up for another one, which probably tells you everything.",
    "The library on campus has this one chair, third floor, by the window, "
    "that everyone wants. I got there at eight in the morning once and it was "
    "already taken, by someone's backpack — no person, just a backpack holding "
    "the seat. I waited twenty minutes. Nobody came. I finally moved the "
    "backpack to the next table, sat down, and felt guilty for an hour. The "
    "owner showed up at lunch, looked at me, looked at the backpack, and just "
    "sat somewhere else without a word. I still feel bad about it. I also still "
    "sit in that chair whenever it's free.",
    "Cooking rice properly took me an embarrassing number of tries. Too much "
    "water, burnt bottom, mushy top — every failure you can name, I did it. "
    "My roommate finally showed me: rinse it until the water runs clear, one "
    "part rice to one and a half parts water, bring it to a boil, then the "
    "lowest heat you have, lid on, twenty minutes, no peeking. No peeking was "
    "the hard part. Now it comes out right every time, and I feel weirdly proud "
    "of something most people learned as teenagers. Better late, I guess.",
    "When my phone screen cracked last year, I lived with it for three months "
    "because the repair cost more than I wanted to spend. There was a spiderweb "
    "in the corner that kept catching the light, and I got used to reading "
    "around it. Then one day the touch stopped working on that whole side, and "
    "I couldn't type the letter 'a' without turning the phone sideways. That "
    "fixed my priorities fast. New screen, one afternoon, and I wondered why "
    "I'd waited so long to fix something I used every single day.",
    "Our study group has a rule: nobody leaves until everyone understands the "
    "problem. It sounds nice. In practice it means sessions run long, someone "
    "always orders food halfway through, and we argue about notation for "
    "twenty minutes before solving anything. But it works — last semester all "
    "four of us passed a class that half the section failed. I think the rule "
    "matters less than the fact that we actually show up for each other. "
    "Showing up is the whole trick, really.",
    "I planted tomatoes on my balcony this spring with no idea what I was "
    "doing. Too much sun, then not enough water, then aphids — tiny green "
    "things all over the leaves that I had to pick off by hand, which was "
    "disgusting and weirdly satisfying. One plant died. The other two survived "
    "out of pure stubbornness, I think, and by August I had more tomatoes than "
    "I could eat. I gave bags of them to neighbors. Next year I'm planting "
    "peppers too, and this time I'll actually read about it first. Probably.",
]

# --- AI-style test paragraphs (evaluation test inputs) ----------------------
# Generic, even, stock-phrase prose of the kind a language model produces.

AI_STYLE = [
    "The implementation of effective time management strategies is essential "
    "for achieving success in both academic and professional settings. By "
    "prioritizing tasks, setting clear goals, and maintaining a structured "
    "schedule, individuals can significantly improve their productivity. It "
    "is important to note that consistency is key, and that small, daily "
    "habits often lead to the most meaningful long-term results. In addition, "
    "taking regular breaks can help maintain focus and prevent burnout over "
    "time.",
    "In today's fast-paced digital world, technology plays a crucial role in "
    "shaping how we communicate, work, and learn. From smartphones to cloud "
    "computing, technological advancements have transformed nearly every "
    "aspect of modern life. As a result, it is more important than ever for "
    "individuals and organizations to stay informed about emerging trends. "
    "Moreover, embracing innovation can provide a significant competitive "
    "advantage in an increasingly connected global economy.",
    "Healthy eating is an important part of maintaining overall well-being. "
    "A balanced diet that includes a variety of fruits, vegetables, whole "
    "grains, and lean proteins can provide the body with the nutrients it "
    "needs to function properly. In addition, staying hydrated and limiting "
    "processed foods can further support long-term health. It is also worth "
    "noting that regular physical activity, combined with good nutrition, is "
    "widely recognized as one of the most effective ways to improve quality "
    "of life.",
    "The importance of teamwork in the workplace cannot be overstated. When "
    "team members collaborate effectively, they are able to combine their "
    "unique skills and perspectives to solve complex problems. Furthermore, "
    "open communication and mutual respect are essential for building trust "
    "within a team. Organizations that foster a collaborative culture often "
    "see higher levels of employee engagement, creativity, and overall "
    "performance. In conclusion, investing in teamwork is an investment in "
    "success.",
    "Climate change is one of the most pressing challenges facing the world "
    "today. Rising global temperatures, changing weather patterns, and "
    "melting ice caps are all clear indicators of its impact. To address this "
    "issue, governments, businesses, and individuals must work together to "
    "reduce greenhouse gas emissions. This includes transitioning to "
    "renewable energy sources, improving energy efficiency, and adopting "
    "more sustainable practices. The time to act is now, before the "
    "consequences become irreversible.",
]

SCENARIOS = [
    {
        "name": "human-style writing",
        "criterion": 1,
        # 10 human-style evaluation test inputs. Criterion 1 allows at most
        # 1 of 10 labelled high-confidence AI per trial.
        "texts": HUMAN_STYLE,
    },
    {
        "name": "score spread",
        "criterion": 2,
        # First 5 texts are AI-style, last 5 are human-style. Criterion 2
        # compares the mean combined score of the two groups per trial.
        "texts": AI_STYLE + HUMAN_STYLE[:5],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # One input expected to land in each band: AI-style, human-style,
        # and plain conventional prose that is genuinely borderline.
        "texts": [
            AI_STYLE[0],
            HUMAN_STYLE[0],
            "The meeting is on Tuesday at ten in the morning. Please bring "
            "your notes from last week and be ready to discuss the budget. "
            "The report is due on Friday. Let me know if you have any "
            "questions before then. We will go over the main points and "
            "decide on the next steps together.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        # Raw request bodies, sent exactly as written.
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
