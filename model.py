import requests
import json
import subprocess
import sys
import re
from dotenv import load_dotenv
import os
import logging
import time

log = logging.getLogger(__name__)


def invoke_func(model, system_prompt, task):
    load_dotenv()
    key = os.getenv("OPENROUTER_KEY")

    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task},
        ],
        "stream": False,
    }
    headers = {
        "Authorization": f"Bearer {key}",
    }

    start_time = time.time()
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        end_time = time.time()
        result = response.json()
        generated_code = result["choices"][0]["message"]["content"].strip()

        if not generated_code:
            return 0

        # Clean up any code block markers or unwanted markdown
        generated_code = re.sub(r"```python\n|```", "", generated_code).strip()

        log.info(f"Generated code {generated_code}")
        log.info(f"Generation took {end_time - start_time:.2f} seconds")
        if "usage" in result:
            usage = result["usage"]
            log.info(
                f"Tokens used: prompt {usage.get('prompt_tokens', 0)}, completion {usage.get('completion_tokens', 0)}, total {usage.get('total_tokens', 0)}"
            )

        if os.path.exists("test.pptx"):
            os.remove("test.pptx")

        with open(".script.py", "w") as f:
            f.write(generated_code)
        try:
            result = subprocess.run(
                ["uv", "run", ".script.py"], capture_output=True, text=True
            )
            if result.returncode == 0:
                log.info("Presentation generated successfully as 'test.pptx'")
                if os.path.exists("test.pptx"):
                    return 1
                else:
                    return 0
            else:
                log.error(f"Error executing generated script:\n{result.stderr}")
                return 0
        except Exception as e:
            log.error(f"Error running script: {e}")
            return 0

    except requests.exceptions.RequestException as e:
        log.error(f"Error connecting: {e}")
        return 0
    except ValueError as e:
        log.error(f"Error: {e}")
        return 0
