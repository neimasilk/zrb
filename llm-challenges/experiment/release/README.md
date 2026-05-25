# LLM Software Engineering Benchmark — Dataset & Analysis

Replication package for the paper **"Comprehensive Evaluation of Large
Language Models on Software Engineering Tasks: A Multi-Task Benchmark"**
(Gunawan & Amien, 2026).

This repository contains the raw experimental data, computed efficiency
metrics, and the analysis/figure-generation code needed to reproduce every
result, table, and figure in the paper.

## What's inside

| File | Description |
|---|---|
| `results.json` | Raw experiment data: **55 runs** (11 models × 5 SE tasks) with status, duration, tool calls, and exit codes. |
| `efficiency_data.json` | Derived efficiency metrics (Tool Efficiency Ratio, time efficiency, estimated cost) produced by `analyze_efficiency.py`. |
| `analyze_efficiency.py` | Computes efficiency metrics and exports `efficiency_data.json`. |
| `analyze_anomaly.py` | Deep-dive into anomalous runs (e.g., the 917-tool-call loop case). |
| `generate_figures.py` | Regenerates all publication figures (matplotlib + seaborn). |
| `analysis/process_data.py` | Data processing and aggregate metrics. |
| `analysis/stat_tests.py` | Statistical tests (correlation, chi-square, ANOVA). |
| `analysis/visualizations.py` | Additional visualizations. |

## Models evaluated (11)

OpenAI GPT-4o, GPT-5.1, GPT-5.2 · Google Gemini 2.5 Flash/Pro and Gemini 3
Flash/Pro (preview) · DeepSeek-Chat · Ollama-cloud GLM-4.7, Kimi-K2.5,
Qwen3-VL.

> Note: Anthropic Claude models were not evaluated due to budget constraints
> (see the paper's Limitations section).

## Tasks (5)

`bug-fix` · `feature` · `refactor` · `copywriting` · `research`

## Reproduce

```bash
# Python 3.10+
pip install matplotlib seaborn numpy scipy pandas

python analyze_efficiency.py   # -> efficiency_data.json
python analyze_anomaly.py      # -> anomaly report
python generate_figures.py     # -> figures/*.pdf and *.png
```

Each script resolves data paths relative to its own location, so no
configuration is needed — just run from this directory.

## Data schema (`results.json`)

Each entry is one model–task run:

```json
{
  "model": "openai_gpt-4o",
  "challenge": "bug-fix",
  "duration": 45.2,
  "tool_calls": 8,
  "status": "EXCELLENT",
  "exit_code": 0
}
```

## Citation

If you use this dataset, please cite the paper:

```bibtex
@article{gunawan2026llmse,
  title   = {Comprehensive Evaluation of Large Language Models on Software
             Engineering Tasks: A Multi-Task Benchmark},
  author  = {Gunawan, Go Frendi and Amien, Mukhlis},
  journal = {arXiv preprint arXiv:2602.07079},
  year    = {2026}
}
```

## License

- **Code** (`*.py`): MIT License (see `LICENSE`).
- **Data** (`*.json`): released under CC BY 4.0 — attribution requested via
  the citation above.
