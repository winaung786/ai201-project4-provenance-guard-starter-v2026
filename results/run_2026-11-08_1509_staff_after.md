# Run log — staff_after

- Produced by: `run_eval.py::main`
- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`
- 3 trials per criterion · 2026-11-08 15:09

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives on human-style writing | ≤1 of 10 flagged AI | 0/10 | 0/10 | 0/10 | MET |
| 2. Score spread | AI-style mean ≥ human-style mean + 0.30 | 0.2017 | 0.2017 | 0.2017 | MISSED |
| 3. Label coverage | All 3 labels present | ai, human, ai | ai, human, ai | ai, human, ai | MISSED |
| 4. Appeal path | Known appeal 200 and logged under_review, original intact, unknown 404 | 5/5 | 5/5 | 5/5 | MET |
| 5. Bad input | All 4 return 4xx with matching audit rejections | 4/4 | 4/4 | 4/4 | MET |

---

## What actually came back

Real output. Paste the relevant parts into your README — the rubric
asks for the actual JSON, not a description of it.

### human-style writing

**Trial 1**

```json
[
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
  },
  {
    "sent": "My grandmother makes this soup every winter, and no matter how many ti",
    "status": 200,
    "response": {
      "combined_score": 0.5107,
      "confidence": 0.0214,
      "content_id": "37128b4109554e369b5136f244259aae",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.7214,
      "style_score": 0.3
    }
  },
  {
    "sent": "The first time I tried to fix my bike, I made it worse. I loosened the",
    "status": 200,
    "response": {
      "combined_score": 0.48045,
      "confidence": 0.0391,
      "content_id": "ceffe3f3afb7420890de48c2571418d5",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6253,
      "style_score": 0.3356
    }
  },
  {
    "sent": "We moved apartments in July, and the elevator in the new building brok",
    "status": 200,
    "response": {
      "combined_score": 0.37129999999999996,
      "confidence": 0.2574,
      "content_id": "7f82f7cdfa6149179855f7d59d2babd0",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.577,
      "style_score": 0.1656
    }
  },
  {
    "sent": "I used to hate running. Hated it. Then a friend talked me into a 5K, a",
    "status": 200,
    "response": {
      "combined_score": 0.3756,
      "confidence": 0.2488,
      "content_id": "3a6de4100be643b0b0c2d097421910c8",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.5979,
      "style_score": 0.1533
    }
  },
  {
    "sent": "The library on campus has this one chair, third floor, by the window, ",
    "status": 200,
    "response": {
      "combined_score": 0.4259,
      "confidence": 0.1482,
      "content_id": "bbff4be44f134a5a91a5b023cf85d907",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6006,
      "style_score": 0.2512
    }
  },
  {
    "sent": "Cooking rice properly took me an embarrassing number of tries. Too muc",
    "status": 200,
    "response": {
      "combined_score": 0.27175,
      "confidence": 0.4565,
      "content_id": "f1a5bcd73d16477db51ccabf4a193e1f",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.3767,
      "style_score": 0.1668
    }
  },
  {
    "sent": "When my phone screen cracked last year, I lived with it for three mont",
    "status": 200,
    "response": {
      "combined_score": 0.50215,
      "confidence": 0.0043,
      "content_id": "934625888c6948f99aaf08b0ff135338",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.6239,
      "style_score": 0.3804
    }
  },
  {
    "sent": "Our study group has a rule: nobody leaves until everyone understands t",
    "status": 200,
    "response": {
      "combined_score": 0.32089999999999996,
      "confidence": 0.3582,
      "content_id": "c0cb45e093d54477b82f9f12a438f7e4",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.3307,
      "style_score": 0.3111
    }
  },
  {
    "sent": "I planted tomatoes on my balcony this spring with no idea what I was d",
    "status": 200,
    "response": {
      "combined_score": 0.4004,
      "confidence": 0.1992,
      "content_id": "0e69bdf4e5eb4bb29643a3ae39e18d44",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6001,
      "style_score": 0.2007
    }
  }
]
```

**Trial 2**

```json
[
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "4f38a6ef721e4267bd1db3a6e788d7b6",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    }
  },
  {
    "sent": "My grandmother makes this soup every winter, and no matter how many ti",
    "status": 200,
    "response": {
      "combined_score": 0.5107,
      "confidence": 0.0214,
      "content_id": "afe1bf66d509492c93b6663eaa5ab743",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.7214,
      "style_score": 0.3
    }
  },
  {
    "sent": "The first time I tried to fix my bike, I made it worse. I loosened the",
    "status": 200,
    "response": {
      "combined_score": 0.48045,
      "confidence": 0.0391,
      "content_id": "31c6f33b10684037a2696006b6856d79",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6253,
      "style_score": 0.3356
    }
  },
  {
    "sent": "We moved apartments in July, and the elevator in the new building brok",
    "status": 200,
    "response": {
      "combined_score": 0.37129999999999996,
      "confidence": 0.2574,
      "content_id": "3085d0317f634ee78160c92a34e994c2",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.577,
      "style_score": 0.1656
    }
  },
  {
    "sent": "I used to hate running. Hated it. Then a friend talked me into a 5K, a",
    "status": 200,
    "response": {
      "combined_score": 0.3756,
      "confidence": 0.2488,
      "content_id": "83064e5007e849a19fc69f4e4c8b1a0d",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.5979,
      "style_score": 0.1533
    }
  },
  {
    "sent": "The library on campus has this one chair, third floor, by the window, ",
    "status": 200,
    "response": {
      "combined_score": 0.4259,
      "confidence": 0.1482,
      "content_id": "43781ca8fbb94ec399d316c93a906f9f",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6006,
      "style_score": 0.2512
    }
  },
  {
    "sent": "Cooking rice properly took me an embarrassing number of tries. Too muc",
    "status": 200,
    "response": {
      "combined_score": 0.27175,
      "confidence": 0.4565,
      "content_id": "6087a43229b54501982b67b6304ac68c",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.3767,
      "style_score": 0.1668
    }
  },
  {
    "sent": "When my phone screen cracked last year, I lived with it for three mont",
    "status": 200,
    "response": {
      "combined_score": 0.50215,
      "confidence": 0.0043,
      "content_id": "c1bdeb8609d24981a12117be3fb5bab1",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.6239,
      "style_score": 0.3804
    }
  },
  {
    "sent": "Our study group has a rule: nobody leaves until everyone understands t",
    "status": 200,
    "response": {
      "combined_score": 0.32089999999999996,
      "confidence": 0.3582,
      "content_id": "1cfbc60464c54a6d9977697766026095",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.3307,
      "style_score": 0.3111
    }
  },
  {
    "sent": "I planted tomatoes on my balcony this spring with no idea what I was d",
    "status": 200,
    "response": {
      "combined_score": 0.4004,
      "confidence": 0.1992,
      "content_id": "587cd85ccce84e44b8e5e8fce4f26fa5",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6001,
      "style_score": 0.2007
    }
  }
]
```

**Trial 3**

```json
[
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "cf2f986ff6734e819c2fdc54992978ab",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    }
  },
  {
    "sent": "My grandmother makes this soup every winter, and no matter how many ti",
    "status": 200,
    "response": {
      "combined_score": 0.5107,
      "confidence": 0.0214,
      "content_id": "d0005c55de1641adb0b7a6394aab3242",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.7214,
      "style_score": 0.3
    }
  },
  {
    "sent": "The first time I tried to fix my bike, I made it worse. I loosened the",
    "status": 200,
    "response": {
      "combined_score": 0.48045,
      "confidence": 0.0391,
      "content_id": "7e7546613bbf467e96a03c3de13e836d",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6253,
      "style_score": 0.3356
    }
  },
  {
    "sent": "We moved apartments in July, and the elevator in the new building brok",
    "status": 200,
    "response": {
      "combined_score": 0.37129999999999996,
      "confidence": 0.2574,
      "content_id": "0143137c83a849eabd461fcd4f312b5b",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.577,
      "style_score": 0.1656
    }
  },
  {
    "sent": "I used to hate running. Hated it. Then a friend talked me into a 5K, a",
    "status": 200,
    "response": {
      "combined_score": 0.3756,
      "confidence": 0.2488,
      "content_id": "1644a2e7156844e69b52243ad4824010",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.5979,
      "style_score": 0.1533
    }
  },
  {
    "sent": "The library on campus has this one chair, third floor, by the window, ",
    "status": 200,
    "response": {
      "combined_score": 0.4259,
      "confidence": 0.1482,
      "content_id": "82584de98c574bd08edaea080fca0091",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6006,
      "style_score": 0.2512
    }
  },
  {
    "sent": "Cooking rice properly took me an embarrassing number of tries. Too muc",
    "status": 200,
    "response": {
      "combined_score": 0.27175,
      "confidence": 0.4565,
      "content_id": "5049c180c5614cc6aa2887cf0dea0261",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.3767,
      "style_score": 0.1668
    }
  },
  {
    "sent": "When my phone screen cracked last year, I lived with it for three mont",
    "status": 200,
    "response": {
      "combined_score": 0.50215,
      "confidence": 0.0043,
      "content_id": "f3c4c6fbf5de4b7fb31a2dddf72d1f21",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.6239,
      "style_score": 0.3804
    }
  },
  {
    "sent": "Our study group has a rule: nobody leaves until everyone understands t",
    "status": 200,
    "response": {
      "combined_score": 0.32089999999999996,
      "confidence": 0.3582,
      "content_id": "368e6eb380944122ad7d20cb93c40f73",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.3307,
      "style_score": 0.3111
    }
  },
  {
    "sent": "I planted tomatoes on my balcony this spring with no idea what I was d",
    "status": 200,
    "response": {
      "combined_score": 0.4004,
      "confidence": 0.1992,
      "content_id": "9e6a49ea598b4703999c8b002b1093cc",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6001,
      "style_score": 0.2007
    }
  }
]
```

### score spread

**Trial 1**

```json
[
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
  },
  {
    "sent": "In today's fast-paced digital world, technology plays a crucial role i",
    "status": 200,
    "response": {
      "combined_score": 0.6521,
      "confidence": 0.3042,
      "content_id": "9067de07356948ceae04732518d3b4eb",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8997,
      "style_score": 0.4045
    }
  },
  {
    "sent": "Healthy eating is an important part of maintaining overall well-being.",
    "status": 200,
    "response": {
      "combined_score": 0.64045,
      "confidence": 0.2809,
      "content_id": "0d610f84779542668ad2f77b9f95db48",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.936,
      "style_score": 0.3449
    }
  },
  {
    "sent": "The importance of teamwork in the workplace cannot be overstated. When",
    "status": 200,
    "response": {
      "combined_score": 0.6188,
      "confidence": 0.2376,
      "content_id": "df34636c3a804360aa4dea6a9ba254eb",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8279,
      "style_score": 0.4097
    }
  },
  {
    "sent": "Climate change is one of the most pressing challenges facing the world",
    "status": 200,
    "response": {
      "combined_score": 0.67105,
      "confidence": 0.3421,
      "content_id": "a0579b58a6d44de7848785e506b336e1",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.9229,
      "style_score": 0.4192
    }
  },
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "b9c90d41ebb641e1beb262a12e67e850",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    }
  },
  {
    "sent": "My grandmother makes this soup every winter, and no matter how many ti",
    "status": 200,
    "response": {
      "combined_score": 0.5107,
      "confidence": 0.0214,
      "content_id": "299dd1ad87024f84a97dff6631672077",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.7214,
      "style_score": 0.3
    }
  },
  {
    "sent": "The first time I tried to fix my bike, I made it worse. I loosened the",
    "status": 200,
    "response": {
      "combined_score": 0.48045,
      "confidence": 0.0391,
      "content_id": "251e1e1563fd48048eb5feff2a4a87d8",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6253,
      "style_score": 0.3356
    }
  },
  {
    "sent": "We moved apartments in July, and the elevator in the new building brok",
    "status": 200,
    "response": {
      "combined_score": 0.37129999999999996,
      "confidence": 0.2574,
      "content_id": "519977f726b241f6b724fed781b4edcf",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.577,
      "style_score": 0.1656
    }
  },
  {
    "sent": "I used to hate running. Hated it. Then a friend talked me into a 5K, a",
    "status": 200,
    "response": {
      "combined_score": 0.3756,
      "confidence": 0.2488,
      "content_id": "54a7453076f84f89aaaba2fb62a03f50",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.5979,
      "style_score": 0.1533
    }
  }
]
```

**Trial 2**

```json
[
  {
    "sent": "The implementation of effective time management strategies is essentia",
    "status": 200,
    "response": {
      "combined_score": 0.61575,
      "confidence": 0.2315,
      "content_id": "fdd443ae62704b188096baa08ef8c78c",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8063,
      "style_score": 0.4252
    }
  },
  {
    "sent": "In today's fast-paced digital world, technology plays a crucial role i",
    "status": 200,
    "response": {
      "combined_score": 0.6521,
      "confidence": 0.3042,
      "content_id": "eb3ce9e07ab24094acc197e11c55019c",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8997,
      "style_score": 0.4045
    }
  },
  {
    "sent": "Healthy eating is an important part of maintaining overall well-being.",
    "status": 200,
    "response": {
      "combined_score": 0.64045,
      "confidence": 0.2809,
      "content_id": "1777c1c1a28f4d669b71a3e392828fe1",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.936,
      "style_score": 0.3449
    }
  },
  {
    "sent": "The importance of teamwork in the workplace cannot be overstated. When",
    "status": 200,
    "response": {
      "combined_score": 0.6188,
      "confidence": 0.2376,
      "content_id": "83a519e5dbc94f259a7d52cb4884bf0c",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8279,
      "style_score": 0.4097
    }
  },
  {
    "sent": "Climate change is one of the most pressing challenges facing the world",
    "status": 200,
    "response": {
      "combined_score": 0.67105,
      "confidence": 0.3421,
      "content_id": "91e0ee3d76824d8b86d73c9edf212396",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.9229,
      "style_score": 0.4192
    }
  },
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "5313b689b86f4d8a9118b27743a5ea9a",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    }
  },
  {
    "sent": "My grandmother makes this soup every winter, and no matter how many ti",
    "status": 200,
    "response": {
      "combined_score": 0.5107,
      "confidence": 0.0214,
      "content_id": "47d50c8016644e4ba68a5c7027c04f6e",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.7214,
      "style_score": 0.3
    }
  },
  {
    "sent": "The first time I tried to fix my bike, I made it worse. I loosened the",
    "status": 200,
    "response": {
      "combined_score": 0.48045,
      "confidence": 0.0391,
      "content_id": "31a63e74f3ce4f2a8b338c3f7f1350e5",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6253,
      "style_score": 0.3356
    }
  },
  {
    "sent": "We moved apartments in July, and the elevator in the new building brok",
    "status": 200,
    "response": {
      "combined_score": 0.37129999999999996,
      "confidence": 0.2574,
      "content_id": "ad0ddb597d9e46a1a3f948e697382f51",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.577,
      "style_score": 0.1656
    }
  },
  {
    "sent": "I used to hate running. Hated it. Then a friend talked me into a 5K, a",
    "status": 200,
    "response": {
      "combined_score": 0.3756,
      "confidence": 0.2488,
      "content_id": "8ca73d40efd24b9f910ea0d643317da8",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.5979,
      "style_score": 0.1533
    }
  }
]
```

**Trial 3**

```json
[
  {
    "sent": "The implementation of effective time management strategies is essentia",
    "status": 200,
    "response": {
      "combined_score": 0.61575,
      "confidence": 0.2315,
      "content_id": "8e02926d36fa4e31a2e7b02d004cdb42",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8063,
      "style_score": 0.4252
    }
  },
  {
    "sent": "In today's fast-paced digital world, technology plays a crucial role i",
    "status": 200,
    "response": {
      "combined_score": 0.6521,
      "confidence": 0.3042,
      "content_id": "aac029106b4843649d6c76e443edace8",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8997,
      "style_score": 0.4045
    }
  },
  {
    "sent": "Healthy eating is an important part of maintaining overall well-being.",
    "status": 200,
    "response": {
      "combined_score": 0.64045,
      "confidence": 0.2809,
      "content_id": "6625601be4c24748a2832a4361aa92f5",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.936,
      "style_score": 0.3449
    }
  },
  {
    "sent": "The importance of teamwork in the workplace cannot be overstated. When",
    "status": 200,
    "response": {
      "combined_score": 0.6188,
      "confidence": 0.2376,
      "content_id": "ef6de5e9795347ea9b150b90d5d6dd97",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8279,
      "style_score": 0.4097
    }
  },
  {
    "sent": "Climate change is one of the most pressing challenges facing the world",
    "status": 200,
    "response": {
      "combined_score": 0.67105,
      "confidence": 0.3421,
      "content_id": "09e25c8573bd4b438c44a7cf2d4adc6d",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.9229,
      "style_score": 0.4192
    }
  },
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "2220c82ee0434383a3e8e0ca3397300e",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    }
  },
  {
    "sent": "My grandmother makes this soup every winter, and no matter how many ti",
    "status": 200,
    "response": {
      "combined_score": 0.5107,
      "confidence": 0.0214,
      "content_id": "fcf703f38b0c40718bbaf1cacea4ce56",
      "guess": "unsure",
      "label": "We couldn't tell with confidence whether this was written by a person or by AI. This is not an accusation \u2014 it only means the writing doesn't clearly match either pattern, so it needs a human look before anyone acts on it.",
      "model_score": 0.7214,
      "style_score": 0.3
    }
  },
  {
    "sent": "The first time I tried to fix my bike, I made it worse. I loosened the",
    "status": 200,
    "response": {
      "combined_score": 0.48045,
      "confidence": 0.0391,
      "content_id": "c16259934f8a4ea1834a258f4842e367",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6253,
      "style_score": 0.3356
    }
  },
  {
    "sent": "We moved apartments in July, and the elevator in the new building brok",
    "status": 200,
    "response": {
      "combined_score": 0.37129999999999996,
      "confidence": 0.2574,
      "content_id": "ef663909730c433ea4ce6464412e7399",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.577,
      "style_score": 0.1656
    }
  },
  {
    "sent": "I used to hate running. Hated it. Then a friend talked me into a 5K, a",
    "status": 200,
    "response": {
      "combined_score": 0.3756,
      "confidence": 0.2488,
      "content_id": "7fc217020d834001b177882ad8646022",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.5979,
      "style_score": 0.1533
    }
  }
]
```

### label coverage

**Trial 1**

```json
[
  {
    "sent": "The implementation of effective time management strategies is essentia",
    "status": 200,
    "response": {
      "combined_score": 0.61575,
      "confidence": 0.2315,
      "content_id": "fe88bf083bc442b5ac86eec19e79a94e",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8063,
      "style_score": 0.4252
    }
  },
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "d8497d6ac1c5464a85cf3204eca97425",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    }
  },
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
]
```

**Trial 2**

```json
[
  {
    "sent": "The implementation of effective time management strategies is essentia",
    "status": 200,
    "response": {
      "combined_score": 0.61575,
      "confidence": 0.2315,
      "content_id": "cf9fe7e733104322841046c2b454199c",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8063,
      "style_score": 0.4252
    }
  },
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "d19dc008d77d4e6d8d081413d80ed5b4",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    }
  },
  {
    "sent": "The meeting is on Tuesday at ten in the morning. Please bring your not",
    "status": 200,
    "response": {
      "combined_score": 0.61195,
      "confidence": 0.2239,
      "content_id": "79f66fe86f9e4a2584c02221ffd80de6",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.7738,
      "style_score": 0.4501
    }
  }
]
```

**Trial 3**

```json
[
  {
    "sent": "The implementation of effective time management strategies is essentia",
    "status": 200,
    "response": {
      "combined_score": 0.61575,
      "confidence": 0.2315,
      "content_id": "5d108815e0f8472c944dd22d360e7600",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.8063,
      "style_score": 0.4252
    }
  },
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "b044e0a92e7c43aeb8068047b91f0afb",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    }
  },
  {
    "sent": "The meeting is on Tuesday at ten in the morning. Please bring your not",
    "status": 200,
    "response": {
      "combined_score": 0.61195,
      "confidence": 0.2239,
      "content_id": "d3bf6170bc504161be677840a72ccb35",
      "guess": "ai",
      "label": "We think this was probably written by AI.",
      "model_score": 0.7738,
      "style_score": 0.4501
    }
  }
]
```

### appeal path

**Trial 1**

```json
[
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
]
```

**Trial 2**

```json
[
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "718f89c1e5d3456d8f31a03692ab215b",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    },
    "original_history": [
      {
        "combined_score": 0.45155,
        "content_id": "718f89c1e5d3456d8f31a03692ab215b",
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
        "content_id": "718f89c1e5d3456d8f31a03692ab215b",
        "message": "Appeal recorded. The decision is now under review.",
        "status": "under_review"
      }
    },
    "unknown_appeal": {
      "status": 404,
      "response": {
        "error": "unknown_content_id",
        "message": "No submission found with content_id 'unknown-0c7a7888d1c34054895184a510ea1f74'."
      }
    },
    "final_history": [
      {
        "combined_score": 0.45155,
        "content_id": "718f89c1e5d3456d8f31a03692ab215b",
        "creator_id": "eval_appeal path_1",
        "guess": "human",
        "label": "We think this was probably written by a person.",
        "model_score": 0.6669,
        "status": "decided",
        "style_score": 0.2362,
        "timestamp": "2026-11-08T21:09:01+00:00"
      },
      {
        "content_id": "718f89c1e5d3456d8f31a03692ab215b",
        "creator_id": "eval_appeal path_1",
        "event": "appeal",
        "reasoning": "Please review this test decision.",
        "status": "under_review",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  }
]
```

**Trial 3**

```json
[
  {
    "sent": "I missed the bus again on Tuesday, which meant I walked the whole way ",
    "status": 200,
    "response": {
      "combined_score": 0.45155,
      "confidence": 0.0969,
      "content_id": "850744d9be6d4eec94420759bc12dcb3",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.6669,
      "style_score": 0.2362
    },
    "original_history": [
      {
        "combined_score": 0.45155,
        "content_id": "850744d9be6d4eec94420759bc12dcb3",
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
        "content_id": "850744d9be6d4eec94420759bc12dcb3",
        "message": "Appeal recorded. The decision is now under review.",
        "status": "under_review"
      }
    },
    "unknown_appeal": {
      "status": 404,
      "response": {
        "error": "unknown_content_id",
        "message": "No submission found with content_id 'unknown-3c504b26a27c40eb813ac6c768b552bc'."
      }
    },
    "final_history": [
      {
        "combined_score": 0.45155,
        "content_id": "850744d9be6d4eec94420759bc12dcb3",
        "creator_id": "eval_appeal path_1",
        "guess": "human",
        "label": "We think this was probably written by a person.",
        "model_score": 0.6669,
        "status": "decided",
        "style_score": 0.2362,
        "timestamp": "2026-11-08T21:09:01+00:00"
      },
      {
        "content_id": "850744d9be6d4eec94420759bc12dcb3",
        "creator_id": "eval_appeal path_1",
        "event": "appeal",
        "reasoning": "Please review this test decision.",
        "status": "under_review",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  }
]
```

### bad input

**Trial 1**

```json
[
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
  },
  {
    "sent": "{\"creator_id\": \"eval_bad_missing\"}",
    "status": 400,
    "response": {
      "error": "invalid_text",
      "message": "text must be a string."
    },
    "audit_entries": [
      {
        "creator_id": "eval_bad_missing",
        "event": "rejected",
        "reason": "invalid_text",
        "status": "rejected",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  },
  {
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}",
    "status": 400,
    "response": {
      "error": "invalid_text",
      "message": "text must be a string."
    },
    "audit_entries": [
      {
        "creator_id": "eval_bad_null",
        "event": "rejected",
        "reason": "invalid_text",
        "status": "rejected",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  },
  {
    "sent": "word word word word word word word word word word word word word word ",
    "status": 400,
    "response": {
      "error": "text_too_long",
      "message": "text must be at most 20000 characters."
    },
    "audit_entries": [
      {
        "creator_id": "eval_bad_huge",
        "event": "rejected",
        "reason": "text_too_long",
        "status": "rejected",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  }
]
```

**Trial 2**

```json
[
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
  },
  {
    "sent": "{\"creator_id\": \"eval_bad_missing\"}",
    "status": 400,
    "response": {
      "error": "invalid_text",
      "message": "text must be a string."
    },
    "audit_entries": [
      {
        "creator_id": "eval_bad_missing",
        "event": "rejected",
        "reason": "invalid_text",
        "status": "rejected",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  },
  {
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}",
    "status": 400,
    "response": {
      "error": "invalid_text",
      "message": "text must be a string."
    },
    "audit_entries": [
      {
        "creator_id": "eval_bad_null",
        "event": "rejected",
        "reason": "invalid_text",
        "status": "rejected",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  },
  {
    "sent": "word word word word word word word word word word word word word word ",
    "status": 400,
    "response": {
      "error": "text_too_long",
      "message": "text must be at most 20000 characters."
    },
    "audit_entries": [
      {
        "creator_id": "eval_bad_huge",
        "event": "rejected",
        "reason": "text_too_long",
        "status": "rejected",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  }
]
```

**Trial 3**

```json
[
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
  },
  {
    "sent": "{\"creator_id\": \"eval_bad_missing\"}",
    "status": 400,
    "response": {
      "error": "invalid_text",
      "message": "text must be a string."
    },
    "audit_entries": [
      {
        "creator_id": "eval_bad_missing",
        "event": "rejected",
        "reason": "invalid_text",
        "status": "rejected",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  },
  {
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}",
    "status": 400,
    "response": {
      "error": "invalid_text",
      "message": "text must be a string."
    },
    "audit_entries": [
      {
        "creator_id": "eval_bad_null",
        "event": "rejected",
        "reason": "invalid_text",
        "status": "rejected",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  },
  {
    "sent": "word word word word word word word word word word word word word word ",
    "status": 400,
    "response": {
      "error": "text_too_long",
      "message": "text must be at most 20000 characters."
    },
    "audit_entries": [
      {
        "creator_id": "eval_bad_huge",
        "event": "rejected",
        "reason": "text_too_long",
        "status": "rejected",
        "timestamp": "2026-11-08T21:09:01+00:00"
      }
    ]
  }
]
```
