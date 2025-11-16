# opengamma

## Setup

[install uv](https://docs.astral.sh/uv/getting-started/installation/)

```
uv sync
```

create .env:
```
OPENROUTER_KEY=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
```


## Run
```
uv run main.py
```

To enable logging:
```
uv run main.py --log
```

## Experiments

1. Models:
benchmark generation quality across different models

2. Rag:
change how system prompt is constructed in respect to prompt

## Metrics

SR - Success Rate
Out of 100 presentation prompts how many produce valid running python?
