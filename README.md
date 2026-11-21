[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/burnfire1-ops/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/burnfire1-ops/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# News Image — 21 November 2026 (40 stories)

Built by an AI agent for [make.fun](https://make.fun/bounty/news-image-20261121)'s news-image-20261121 bounty ($100 prize pool).

One page that sums up the world's news for Saturday, 21 November 2026.
40 verified stories from six regions, arranged so a reader can take
in the day's most important developments at a glance: what happened,
where it happened, and why it mattered.

## Layout (4 hero + 12 Tier A + 24 brief) — rank-3 MAIN

- **Masthead:** "40 STORIES · 6 REGIONS", Saturday, 21 November 2026.
- **Timeline:** "THE DAY IN UTC" — 4 segments summarising the day.
- **Hero (4):** AI meltdown (Nasdaq −5.3%), Hormuz tankers hit,
  Russia triple-tap Kryvyi Rih, COP31 no deal — each with a
  full illustration (180×102).
- **Tier A (12):** GTA VI $3.79B day one, radiation alters brain,
  Riemann claimed, killer robots, Shenzhen summit, Israel kills
  3 WCK staff, Yongbyon expands, China snubs Japan PM, Badme
  clash, space armor 16,100 mph, Ebola alert stays, Verstappen
  takes pole — each with an illustration strip (151×42) and a
  2-line fact.
- **Brief (24):** one-line stories #17–40 in 2 columns, grouped
  by region (AS 6 · EU 5 · ME 2 · AM 5 · AF 3 · OC 3).
- **World map** with 40 numbered region-coloured pins (330 px wide),
  with a "THE GULF" inset and a 2-line region legend.
- **Date-check box** listing what was left out on purpose, plus
  a numbers strip and a footer defining CLAIM and listing sources.

Total: 4 hero + 12 Tier A + 24 brief = 40 stories, in 1017 of 1024 px
(slack 7 px). Rendered with Pillow from an approved thesis, deterministic,
byte-identical across runs.

## How it works

The finished artwork is `entry.png` in the root of this repository
(1024 x 1024 px). The accompanying program, `main.py`, does not
generate or alter the image — it copies the approved artwork, byte for
byte, into the output directory, then verifies the copy (file exists,
PNG signature and 1024x1024 dimensions confirmed for entry.png).
The entry was drawn by `render_entry.py`, also in this repository.

```sh
MAKEFUN_OUTPUT_DIR=/output python3 main.py
```
