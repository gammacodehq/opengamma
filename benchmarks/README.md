# Benchmarks

## Model benchamrks
To run a benchmark you should do all preparations from root README.md and then run

```bash
uv run benchmarks/model_benchmark.py
```

You would see logs in your terminal and final json benchmarks in results/model_benchmark/benchmark_results_YYYYMMDD_HHMMSS.json

log.json example
```
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