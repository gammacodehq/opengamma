# opengamma

Presentation generation Agent (real **pptx**, not md/latex). Part of [@gamma_gpt_bot](https://t.me/gamma_gpt_bot) system.

```mermaid
flowchart TD
    A[📚 Documentation] --> B{System Prompt}
    C[📋 Markdown Requirements] --> D{User Prompt}

    B --> E[🤖 LLM Model]
    D --> E

    E --> F[🐍 Output Python Code]

    F --> G[⚙️ Execution]
    G --> H[📊 pptx File]

    %% Styling with colors
    class A,C noteColor;
    class B,D promptColor;
    class E modelColor;
    class F codeColor;
    class G execColor;
    class H outputColor;

    %% Define CSS classes for colors
    classDef noteColor fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef promptColor fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef modelColor fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#000
    classDef codeColor fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef execColor fill:#ffebee,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef outputColor fill:#fce4ec,stroke:#880e4f,stroke-width:3px,color:#000
```

## Setup

[install uv](https://docs.astral.sh/uv/getting-started/installation/)

```
uv sync
```

create .env:
```
OPENROUTER_KEY=ключ в чате проекта
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




## Formal requirements

Название проекта: `python-pptx генерация презентаций в автоматическом режиме по тексту`

Ссылка на github проекта: `https://github.com/gammacodehq/opengamma`

Ссылка на презентацию проекта: `https://docs.google.com/presentation/d/1xNGmIQmVbMGyG5r6yaQFNNY93qbrNZqSkrlWhbbuvyo/edit`
