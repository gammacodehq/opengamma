from datasets import load_dataset
import json
import logging
import numpy as np
from pathlib import Path
import sklearn
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

class DatasetDeduplicator:
    # Инициализация
    def __init__(self):
        self.dataset = load_dataset("mikeoxmaul/opengamma-prs")
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    # Считаем эмбеддинги для всех текстов
    def calculate_embeddings(self, texts):
        model = self.model
            
        log.info(f"==== Calculating embeddings for {len(texts)} texts")
        embeddings = model.encode(texts, show_progress_bar=True)
        log.info(f"==== Embeddings calculated: {embeddings.shape}")
        return embeddings
    
    # Считаем матрицу косинусных расстояний
    def calculate_similarity_matrix(self, embeddings):        
        log.info("==== Calculating cosine similarity matrix")
        similarity_matrix = cosine_similarity(embeddings)
        
        # Из нее нам нужна тролько часть над главное диагональю
        similarities = similarity_matrix[np.triu_indices(len(embeddings), k=1)]
        log.info(f"==== Similarity matrix calculated: {similarity_matrix.shape}")
        
        return similarity_matrix, similarities
    
    # Считаем все нужные статистики
    def analyze_similarities(self, similarities):
        import numpy as np
        
        stats = {
            'min': np.min(similarities),
            'max': np.max(similarities),
            'mean': np.mean(similarities),
            'median': np.median(similarities),
            'percentile_5': np.percentile(similarities, 5),
            'percentile_25': np.percentile(similarities, 25),
            'percentile_75': np.percentile(similarities, 75),
            'percentile_95': np.percentile(similarities, 95)
        }
        
        return stats
    
    # Находим дубликаты на основе посчитаных эмбеддингов, дубликатами считаем такие, которые отличаются менне чем на threshold
    def find_duplicates(self, texts, embeddings, threshold=None):
        similarity_matrix, similarities = self.calculate_similarity_matrix(embeddings)
        stats = self.analyze_similarities(similarities)
        if threshold is None:
            threshold = stats['percentile_5']
        log.info(f"==== Using threshold: {threshold:.3f}")
        
        keep_indices = [0]
        duplicate_indices = []

        for i in range(1, len(texts)):
            if keep_indices:
                current_embedding = embeddings[i].reshape(1, -1)
                saved_embeddings = embeddings[keep_indices]
                
                similarities = cosine_similarity(current_embedding, saved_embeddings)
                max_similarity = np.max(similarities)
                
                if max_similarity < threshold:
                    keep_indices.append(i)
                else:
                    # Находим наиболее похожую задачу
                    most_similar_idx = keep_indices[np.argmax(similarities)]
                    duplicate_indices.append({
                        'duplicate_index': i,
                        'original_index': most_similar_idx,
                        'similarity': float(max_similarity),
                        'duplicate_text': texts[i][:200] + "..." if len(texts[i]) > 200 else texts[i],
                        'original_text': texts[most_similar_idx][:200] + "..." if len(texts[most_similar_idx]) > 200 else texts[most_similar_idx]
                    })
            else:
                keep_indices.append(i)
        
        log.info(f"==== Duplicate search complete: {len(keep_indices)} to keep, {len(duplicate_indices)} to remove")
        return keep_indices, duplicate_indices, stats, threshold

    # Сохраняем результат в json в директорию results    
    def save_deduplication_report(self, original_count, final_count, duplicate_indices, stats, threshold):
        duplicate_indices_sorted = sorted(duplicate_indices, key=lambda x: x['duplicate_index'])
        indices_to_remove = [item['duplicate_index'] for item in duplicate_indices_sorted]
        
        report = {
            'original_dataset_size': original_count,
            'recommended_dataset_size': final_count,
            'reduction_percent': (1 - final_count / original_count) * 100,
            'similarity_threshold': threshold,
            'similarity_statistics': stats,
            'indices_to_remove': indices_to_remove,
            'duplicate_details': duplicate_indices_sorted
        }
        
        report_path = Path("results/deduplication")

        with open(report_path / "deduplication_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        log.info(f"==== Results are saved in : {report_path}/deduplication_report.json")
        
        return report
    
    # Запускаем дедубликацию
    def run_deduplication(self, threshold=None):
        log.info("==== Starting dataset deduplication")
        
        texts = [item['text'] for item in self.dataset['train']]
        log.info(f"==== Original dataset size: {len(texts)} tasks")
        
        embeddings = self.calculate_embeddings(texts)
        if embeddings is None:
            return None
        
        keep_indices, duplicate_indices, stats, used_threshold = self.find_duplicates(texts, embeddings, threshold)
        
        report = self.save_deduplication_report(
            len(texts), len(keep_indices), duplicate_indices, stats, used_threshold
        )
        
        log.info(f"==== Deduplication completed: {len(keep_indices)}/{len(texts)} tasks recommended to keep")
        
        return report


def main():
    deduplicator = DatasetDeduplicator()
    deduplicator.run_deduplication(threshold=0.8)

if __name__ == "__main__":
    main()