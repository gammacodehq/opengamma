import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import json
import logging
from datetime import datetime
from pathlib import Path
from datasets import load_dataset
from model import invoke_func

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

class ModelBenchmark:
    # Инициализация
    def __init__(self, system_prompt=None):
        self.system_prompt = system_prompt or self.get_default_prompt()
        self.dataset = load_dataset("mikeoxmaul/opengamma-prs", streaming=True)
        self.results_dir = Path("results/model_benchmark")
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    # Возвращием промпт для тестинга
    def get_default_prompt(self):
        return """Generate Python code for python-pptx presentation. OUTPUT MUST BE PURE PYTHON CODE ONLY.

                CRITICAL:
                - NO comments (# comment)
                - NO explanations
                - NO markdown (```python or ```)
                - NO text outside code
                - NO example usage
                - NO instructions

                REQUIREMENTS:
                - Use python-pptx
                - Create multiple slides with different layouts  
                - Save as 'test.pptx'
                - Code must run without errors

                VALID OUTPUT EXAMPLE:
                from pptx import Presentation
                prs = Presentation()
                slide = prs.slides.add_slide(prs.slide_layouts[0])
                slide.shapes.title.text = "Title"
                prs.save('test.pptx')

                NOW GENERATE PURE PYTHON CODE:"""
    
    # Непосредственно бенчмарк
    def benchmark_models(self, models, num_tasks=20):        
        results = {}
        
        for model_name in models:
            log.info(f"==== Testing model: {model_name}")
            
            model_results = {
                'success_count': 0,
                'total_tasks': 0,
                'total_time': 0,
                'token_usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0},
                'errors': []
            }
            
            tasks = self.dataset["train"].take(num_tasks)
            
            for i, task in enumerate(tasks):
                task_text = task["text"]
                log.info(f"==== Task {i+1}/{num_tasks}: {task_text[:100]}...")
                
                try:
                    start_time = time.time()
                    result, token_stats = invoke_func(model_name, self.system_prompt, task_text)
                    execution_time = time.time() - start_time
                    
                    model_results['total_tasks'] += 1
                    model_results['total_time'] += execution_time
                    model_results['token_usage']['prompt_tokens'] += token_stats['prompt_tokens']
                    model_results['token_usage']['completion_tokens'] += token_stats['completion_tokens']
                    model_results['token_usage']['total_tokens'] += token_stats['total_tokens']
                    
                    if result == 1:
                        model_results['success_count'] += 1
                        log.info(f"==== Success ({execution_time:.2f}с)")
                    else:
                        log.info(f"==== Error ({execution_time:.2f}с)")
                        
                except Exception as e:
                    log.error(f"==== Exception: {e}")
                    model_results['errors'].append(str(e))
            
            # Считаем метрки
            if model_results['total_tasks'] > 0:
                model_results['success_rate'] = model_results['success_count'] / model_results['total_tasks']
                model_results['avg_time'] = model_results['total_time'] / model_results['total_tasks']
            
            results[model_name] = model_results
            log.info(f"==== Result {model_name}: SR={model_results.get('success_rate', 0):.1%}")
        
        return results
    
    # Сохраняем рещультат в json в директорию results
    def save_results(self, results, filename=None):
        """Сохраняет результаты в JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        # Конвертируем в подходящий для json.dump формат
        serializable_results = {}
        for model, data in results.items():
            serializable_results[model] = {
                'success_rate': data.get('success_rate', 0),
                'success_count': data['success_count'],
                'total_tasks': data['total_tasks'],
                'avg_time': data.get('avg_time', 0),
                'total_time': data['total_time'],
                'token_usage': data['token_usage'],
                'errors': data['errors']
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        log.info(f"==== Results are saved in : {filepath}")
        return filepath
    

def main():    
    # Список моделей для тестирования, если заработает надо добавить еще
    models_to_test = [
        "openai/gpt-oss-20b:free",
        "nvidia/nemotron-nano-12b-v2-vl:free",
        "kwaipilot/kat-coder-pro:free",
        # TODO добавить еще модели
    ]
    
    benchmark = ModelBenchmark()
    
    log.info("==== Starting benchmark")
    results = benchmark.benchmark_models(models_to_test, num_tasks=3) # TODO запустить на больше чем на 3 тасках
    
    benchmark.save_results(results)

if __name__ == "__main__":
    main()
