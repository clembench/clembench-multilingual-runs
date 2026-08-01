# clembench-multilingual-runs

Raw model runs for **clembench-multilingual (v4.0)**: nine LLMs evaluated as agents playing
14 goal-directed dialogue games in self-play, across 30 languages.

This repository holds the complete interaction record — every prompt, every response, every
per-episode score — for roughly **108,000 episodes**. It is the evidence behind the leaderboard and
the paper, published so the numbers can be checked rather than taken on trust.

- **Leaderboard:** https://clembench.github.io/leaderboard.html
- **Benchmark code and localised game files:** [clembench-multilingual](https://github.com/clembench/multilingual)
- **Framework:** [clembench](https://github.com/clp-research/clembench) · [clemcore](https://github.com/clp-research/clemcore) (runs produced with clemcore 3.7.2)

## What is in here

| | |
| --- | --- |
| Languages | 30 |
| Models | 9 |
| Games | 14 (13 for Chinese) |
| Episodes | 400 per model per language, 380 for Chinese — about 108,000 in total |

### Models

| Directory | Model | Weights | Vendor |
| --- | --- | --- | --- |
| `gpt-5.4-azure` | GPT-5.4 | closed | OpenAI |
| `claude-opus-4-8-azure` | Claude Opus 4.8 | closed | Anthropic |
| `glm-5.2` | GLM-5.2 | open | Z.ai |
| `deepseek-v4-pro` | DeepSeek-V4-Pro | open | DeepSeek |
| `nemotron-3-ultra` | Nemotron-3-Ultra-550B-A55B | open | NVIDIA |
| `gemma-4-26b-a4b-it` | Gemma-4-26B-A4B | open | Google |
| `Qwen3.6-35B-A3B-FP8-without-reasoning` | Qwen3.6-35B-A3B | open | Alibaba |
| `mistral-large-3-azure` | Mistral-Large-3-675B | open | Mistral |
| `Apertus-v1.5-8B` | Apertus-1.5-8B | open | Swiss AI |

### Languages

The 24 official EU languages plus six others.

**EU-24** — Bulgarian `bg`, Croatian `hr`, Czech `cs`, Danish `da`, Dutch `nl`, English `en`,
Estonian `et`, Finnish `fi`, French `fr`, German `de`, Greek `el`, Hungarian `hu`, Irish `ga`,
Italian `it`, Latvian `lv`, Lithuanian `lt`, Maltese `mt`, Polish `pl`, Portuguese `pt`,
Romanian `ro`, Slovak `sk`, Slovenian `sl`, Spanish `es`, Swedish `sv`

**Others** — Arabic `ar`, Chinese `zh`, Russian `ru`, Serbian `sr`, Turkish `tr`, Ukrainian `uk`

### Games and episode counts

Episodes per model per language. The counts follow the instance counts of the underlying clembench
release rather than being balanced, so games with more pre-compiled instances contribute more.

| Game | Ep. | Game | Ep. |
| --- | ---: | --- | ---: |
| `textmapworld` | 50 | `textmapworld_graphreasoning` | 30 |
| `clean_up` | 45 | `textmapworld_specificroom` | 30 |
| `imagegame` | 40 | `privateshared` | 25 |
| `codenames` | 35 | `matchit_ascii` | 20 |
| `guesswhat` | 30 | `taboo` | 20 |
| `referencegame` | 30 | `wordle` | 20 |
| | | `hot_air_balloon` | 15 |
| | | `dond` | 10 |

**Total: 400.** Chinese totals 380: `wordle` is excluded because the game needs five-letter words
and Chinese is character-based.

## Repository structure

```
results_<lang>/                     one directory per language, e.g. results_de/
├── results.csv                     aggregate scores, one row per model  ← start here
├── raw.csv                         per-episode scores in long form
├── results.html                    the same table rendered
└── <model>/                        e.g. gpt-5.4-azure/
    ├── run.json                    clemcore version, model spec, game paths
    └── <game>/                     e.g. clean_up/
        └── <experiment>/           e.g. 2_hard_7obj_de/
            ├── experiment.json     the experiment's configuration
            └── instance_00000/     one episode
                ├── instance.json          the game instance that was played
                ├── interactions.json      the full dialogue, turn by turn
                ├── scores.json            per-episode metrics
                ├── completed.json         completion status
                ├── player_1.requests.json raw API requests and token usage
                └── player_2.requests.json
```

Experiment names encode the language, so the same game appears as `2_hard_7obj_de` under
`results_de/` and `2_hard_7obj_fr` under `results_fr/`. Instance numbers correspond to the
`game_id` in the benchmark's instance files, so `instance_00003` is the same game instance in
every language and for every model.

## Metrics

Each episode yields two measures, combined into the **clemscore**:

| Measure | Meaning |
| --- | --- |
| **% Played** | share of episodes played to completion without aborting — instruction following and format compliance |
| **Quality** | mean task-specific score over the episodes that were not aborted — how well the task was solved |
| **clemscore** | `(mean % Played / 100) × mean Quality`, in `[0, 100]` |

A model has to do both to score well: following the rules but playing badly, or playing well but
aborting often, are both penalised.

Note that a model's clemscore over several languages is the **mean of the per-language clemscores**,
not the product of pooled averages. The two differ, because the product is not linear.

## Working with the data

```bash
# one language, all models
cat results_de/results.csv

# re-score, transcribe and evaluate a language after adding episodes
clem score      -r results_de
clem transcribe -r results_de
clem eval       -r results_de
```

Scripts for auditing completeness, deploying new runs and rebuilding the aggregate tables live in
the [clembench-multilingual](https://github.com/clembench/clembench-multilingual) repository
(`check_runs.py`, `deploy_runs.sh`, `rescore_runs.sh`, `combine_results.py`).

## Known gaps
- **Thirteen `player_*.requests.json` files are missing.** A handful of Apertus `clean_up` episodes
  wrote runaway request logs of 100–200 MB, over GitHub's per-file limit. Only those logs were
  removed — the `scores.json` and `interactions.json` for those episodes are intact, so no score is
  affected. Token-usage totals for those episodes are.
- **A small number of episodes were never scored.** Where an episode directory has no `scores.json`
  it did not complete; those cells are excluded from the aggregates rather than counted as zero.

## Citation

If you use these runs, please cite the clembench-multilingual paper and the clembench framework.
See the [benchmark repository](https://github.com/clembench/multilingual) for the current
references.

## Licence

See [LICENSE](LICENSE). The game code and the clemcore framework carry their own licences.
