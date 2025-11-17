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

class PromptBenchmark:
    # Инициализация
    def __init__(self, model="openai/gpt-oss-20b:free"):
        self.model = model
        self.dataset = load_dataset("mikeoxmaul/opengamma-prs", streaming=True)
        self.results_dir = Path("results/prompt_benchmark")
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    # Возвращаем промпты для тестирования
    def get_prompts_to_test(self):
        """Возвращает список промптов для тестирования"""
        
        # Базовый промпт (текущий)
        basic_prompt = """Generate Python code for python-pptx presentation. OUTPUT MUST BE PURE PYTHON CODE ONLY.

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

                        NOW GENERATE PURE PYTHON CODE:"""
        
        # Детальный промпт с примерами из документации
        detailed_prompt = """Generate Python code for python-pptx presentation. OUTPUT MUST BE PURE PYTHON CODE ONLY.

                        PYTHON-PPTX SPECIFICS:
                        - Use Presentation() to create presentation
                        - Use slide_layouts[] for slide types: 0=Title, 1=Title and Content, 5=Title only
                        - Use Inches() for measurements
                        - Add slides with prs.slides.add_slide(layout)
                        - Set text with shape.text = "text"
                        - Save with prs.save('test.pptx')

                        CODE STRUCTURE:
                        from pptx import Presentation
                        from pptx.util import Inches

                        prs = Presentation()
                        slide = prs.slides.add_slide(prs.slide_layouts[0])
                        slide.shapes.title.text = "Title"
                        prs.save('test.pptx')

                        OUTPUT MUST BE PURE PYTHON CODE ONLY. NO COMMENTS. NO EXPLANATIONS."""

        # Минималистичный промпт
        minimal_prompt = """Generate python-pptx code. Output ONLY Python code.

                        from pptx import Presentation
                        prs = Presentation()
                        slide = prs.slides.add_slide(prs.slide_layouts[0])
                        slide.shapes.title.text = "Title"
                        prs.save('test.pptx')

                        Continue with more slides:"""

        # Строгий промпт с шаблоном
        structured_prompt = """PYTHON CODE ONLY. NO COMMENTS. FOLLOW TEMPLATE:

                        from pptx import Presentation
                        from pptx.util import Inches

                        prs = Presentation()
                        slide = prs.slides.add_slide(prs.slide_layouts[0])
                        slide.shapes.title.text = "TITLE"
                        slide.placeholders[1].text = "SUBTITLE"

                        # ADD MORE SLIDES WITH DIFFERENT LAYOUTS

                        prs.save('test.pptx')"""

        return {
            "basic_prompt": basic_prompt,
            "detailed_prompt": detailed_prompt, 
            "minimal_prompt": minimal_prompt,
            "structured_prompt": structured_prompt
        }
    
    # Непосредственно бенчмарк
    def benchmark_prompts(self, prompts, num_tasks=10):        
        results = {}
        
        for prompt_name, prompt_content in prompts.items():
            log.info(f"==== Testing prompt: {prompt_name}")
            
            prompt_results = {
                'success_count': 0,
                'total_tasks': 0,
                'total_time': 0,
                'token_usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0},
                'errors': [],
                'prompt_length': len(prompt_content)
            }
            
            tasks = self.dataset["train"].take(num_tasks)
            
            for i, task in enumerate(tasks):
                task_text = task["text"]
                log.info(f"==== Task {i+1}/{num_tasks}: {task_text[:100]}...")
                
                try:
                    start_time = time.time()
                    result, token_stats = invoke_func(self.model, prompt_content, task_text)
                    execution_time = time.time() - start_time
                    
                    prompt_results['total_tasks'] += 1
                    prompt_results['total_time'] += execution_time
                    prompt_results['token_usage']['prompt_tokens'] += token_stats['prompt_tokens']
                    prompt_results['token_usage']['completion_tokens'] += token_stats['completion_tokens']
                    prompt_results['token_usage']['total_tokens'] += token_stats['total_tokens']
                    
                    if result == 1:
                        prompt_results['success_count'] += 1
                        log.info(f"==== Success ({execution_time:.2f}с)")
                    else:
                        log.info(f"==== Error ({execution_time:.2f}с)")
                        
                except Exception as e:
                    log.error(f"==== Exception: {e}")
                    prompt_results['errors'].append(str(e))
            
            # Считаем метрики
            if prompt_results['total_tasks'] > 0:
                prompt_results['success_rate'] = prompt_results['success_count'] / prompt_results['total_tasks']
                prompt_results['avg_time'] = prompt_results['total_time'] / prompt_results['total_tasks']
            
            results[prompt_name] = prompt_results
            log.info(f"==== Result {prompt_name}: SR={prompt_results.get('success_rate', 0):.1%}")
        
        return results
    
    # Сохраняем результат в json в директорию results
    def save_results(self, results, filename=None):
        """Сохраняет результаты в JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"prompt_benchmark_results_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        # Конвертируем в подходящий для json.dump формат
        serializable_results = {}
        for prompt_name, data in results.items():
            serializable_results[prompt_name] = {
                'success_rate': data.get('success_rate', 0),
                'success_count': data['success_count'],
                'total_tasks': data['total_tasks'],
                'avg_time': data.get('avg_time', 0),
                'total_time': data['total_time'],
                'token_usage': data['token_usage'],
                'prompt_length': data['prompt_length'],
                'errors': data['errors']
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        log.info(f"==== Results are saved in : {filepath}")
        return filepath
    

def main():    
    # Используем лучшую модель из предыдущего бенчмарка
    model = "openai/gpt-oss-20b:free"
    
    benchmark = PromptBenchmark(model=model)
    
    prompts = benchmark.get_prompts_to_test()
    
    log.info("==== Starting prompt benchmark")
    results = benchmark.benchmark_prompts(prompts, num_tasks=1) # TODO запустить на больше чем на 1 таске
    
    benchmark.save_results(results)

if __name__ == "__main__":
    main()
