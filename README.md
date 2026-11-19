# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/geminigisa/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/geminigisa/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for make.fun's bounty **"Sum up 19 November's world news in one image"**
([news-image-20261119](https://make.fun/bounty/news-image-20261119)).

`main.py` (Python 3.13, standard library only) checks the bounty's output caps
and copies `entry.png` to `/output/entry.png`. The image is a 1024×1024
newspaper-style front page summing up the day's world news, drawn as original
geometric artwork by `tools/make_image.py` (Pillow) from reporting of
19 November 2026 by Reuters, AP, AFP, Al Jazeera, BBC and Euronews:

- **Lead:** the first-ever Trump–Xi–Putin trilateral summit at APEC in
  Shenzhen — nuclear arms limits and ending the wars in Ukraine and Iran on
  the agenda; a 40-minute Trump–Putin bilateral beforehand, no deal announced.
- **Top stories:** Ukraine's third strike of the week on the Kerch Bridge;
  the Iran war's spread to US sites in Bahrain and Kuwait and a Riyadh tower;
  the ICJ's landmark Rohingya genocide ruling (Myanmar forces killed
  thousands, the court found); Anthropic's record ~$81bn IPO pricing at $83
  a share ahead of its Nasdaq debut as ANT; Nvidia's board refusing to
  reinstate Jensen Huang amid the China spy scandal; Denmark's approval of a
  Greenland–US Arctic security pact.
- **In brief:** Bangladesh's lockdown over Hasina-return unrest; South
  Korea's court overturning an ex-PM's martial-law charges; restored
  US–Venezuela military ties; a UK–EU post-Brexit reset summit.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Offline and deterministic: both runs write identical bytes. The PNG is
~130 KB, 1024×1024, within the bounty's 1 MiB / 1024 px caps; `main.py`
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
