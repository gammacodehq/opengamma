# Benchmarks

## Model Benchmarks

Model benchmarks evaluate how different models handle a fixed set of tasks. Each task is processed using a shared system prompt, and the benchmark records execution time, success rate, and token statistics for each model.

Running the Model Benchmark

Before running benchmarks, complete all setup steps described in the root README.md.

After that, execute:

```bash
uv run benchmarks/model_benchmark.py
```

During execution, logs will appear in your terminal.
Final results are saved as a JSON file in the directory:

```bash
results/model_benchmark/benchmark_results_YYYYMMDD_HHMMSS.json
```

Example log.json:

```bash
{
  "openai/gpt-oss-20b:free": {
    "success_rate": 1.0,
    "success_count": 1,
    "total_tasks": 1,
    "avg_time": 12.089563846588135,
    "total_time": 12.089563846588135,
    "token_usage": {
      "prompt_tokens": 2005,      <--- Taken from model.py logs
      "completion_tokens": 3128,  <--- Taken from model.py logs
      "total_tokens": 5133        <--- Taken from model.py logs
    },
    "errors": []
  }
}
```

## Prompt Benchmarks

Prompt benchmarks evaluate how different prompt formulations affect model performance. Instead of comparing models, this benchmark compares prompt templates when used with a single model.

Running the Prompt Benchmark

Use the following command:

```bash
uv run benchmarks/prompt_benchmark.py
```

Results will be saved to:

```bash
results/prompt_benchmark/prompt_benchmark_results_YYYYMMDD_HHMMSS.json
```