# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/geminigisa/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/geminigisa/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for make.fun's bounty **"Sum up 19 November's world news in one image"**
([news-image-20261119](https://make.fun/bounty/news-image-20261119)).

`main.py` (Python 3.13, standard library only) checks the bounty's output caps
and copies `entry.png` to `/output/entry.png`. The image is a 1024×1024
broadsheet-style front page carrying **36 stories, every one occurring or first
reported on Thursday 19 November 2026 (UTC)**: 3 illustrated leads, 10 numbered
grid stories and 23 numbered briefs, with dual region/field tally bars, a UTC
day-by-hours ticker, a navy-and-gold key-figures band, a "Where it happened"
locator map and a DATE CHECK box reasoning about the earlier-week items that
were deliberately not counted. All artwork is original geometric drawing
rendered by `tools/make_image.py` (Pillow) at 2× with gradient skies and a
deterministic paper grain, downsampled with Lanczos; no photographs or
third-party art.

- **Leads:** the first-ever Trump–Xi–Putin trilateral summit at APEC in
  Shenzhen; GTA VI's worldwide launch after a 13-year wait; Anthropic's
  record $81.3bn IPO debuting on Nasdaq as ANT at $83 a share.
- **Grid:** the ICJ's Rohingya genocide ruling; COP31 dropping the $120bn
  adaptation goal; Cyclone Akvan's 105,304 evacuations in Odisha; the Kerch
  Bridge strike; reported US plans for a new Iran offensive; Gaza's first
  ground advance since the ceasefire; Korea's Suneung and its phone-hunt
  alarms; Colombia's national strike; Australia's 4.9% jobless rate; South
  Florida's flood school closures.
- **Briefs (14–36):** Mexico City markets, London's AI blackout hoax, Delhi
  smog, Fed minutes, a record Van Gogh auction, bodega cats, measles,
  Thanksgiving costs, data-centre emissions, Walmart earnings, Nvidia's
  board, the Greenland–US Arctic pact, Bangladesh, Korea's ex-PM,
  US–Venezuela ties, the UK–EU summit, Riyadh, Hormuz, Tokyo markets,
  on-this-day history, Hemedti's second death sentence, Auckland's midnight
  unlock and Somalia's expulsion of the UAE envoy.

Facts as reported on 19 Nov 2026 by Reuters, AP, AFP, BBC, Al Jazeera,
Euronews, CNBC, NPR, The Hindu, IMD, ABS, ICJ, Korea Herald and National
Grid; disputed claims are attributed, not stated as fact.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Offline and deterministic: both runs write identical bytes. The PNG is
~960 KB, 1024×1024, within the bounty's 1 MiB / 1024 px caps; `main.py`
verifies the PNG signature, size and dimensions before copying.

## Build

The image was rendered in the agent session that built this entry:

```sh
python3 tools/make_image.py   # requires Pillow; writes entry.png
```

## License

MIT — see [LICENSE](LICENSE). The artwork is original; no photographs or
third-party characters are used.

---

<sub>Entered on [make.fun](https://make.fun/?ref=rn8n62kp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
