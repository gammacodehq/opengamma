import os
from datasets import load_dataset
from functools import cache
import requests
from dotenv import load_dotenv
from sklearn.linear_model import LogisticRegression
import json
load_dotenv()
dataset = load_dataset("mikeoxmaul/opengamma-prs-dedup", streaming=True)
tasks = list(dataset["train"].take(100))

max_iter = 10

@cache
def get_embedding(index):
        text = tasks[index]["text"]
        key = os.getenv("OPENROUTER_KEY")
        response = requests.post(
                "https://openrouter.ai/api/v1/embeddings",
                headers={
                        "Authorization": f"Bearer {key}",
                        "Content-Type": "application/json",
                },
                json={
                        "model": "sentence-transformers/paraphrase-minilm-l6-v2",
                        "input": text,
                }
        )
        data = response.json()
        embedding = data["data"][0]["embedding"]
        return embedding

original = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16, 18, 20, 23, 24, 25, 27, 28, 31, 33, 34, 35, 36, 37, 38, 39, 40, 43, 47, 49, 51, 52, 54, 55, 56, 57, 59, 61, 62, 63, 64, 66, 68, 73, 74, 77, 78, 79, 81, 82, 83, 84, 85, 86, 87, 88, 91, 92, 93, 94, 95, 98, 99 ]
basic = [ 2, 8, 10, 12, 13, 16, 20, 29, 35, 36, 37, 40, 47, 51, 55, 57, 61, 66, 71, 72, 73, 74, 81, 83, 90, 92, 94, 96 ]
detailed = [ 4, 7, 10, 15, 23, 29, 30, 31, 35, 40, 41, 43, 44, 45, 46, 68, 79, 81, 82, 84, 85, 86, 92, 93, 95, 98 ]
structured = [ 1, 6, 10, 16, 17, 28, 31, 33, 34, 35, 37, 39, 41, 43, 44, 46, 51, 52, 54, 57, 61, 62, 64, 65, 69, 71, 72, 74, 76, 79, 80, 83, 84, 85, 87, 88, 91, 99 ]

all_indices = set(original)
all_indices.update(basic)
all_indices.update(detailed)
all_indices.update(structured)

X = []
y = []
for idx in original:
    emb = get_embedding(idx)
    X.append(emb)
    y.append(0)
for idx in basic:
    emb = get_embedding(idx)
    X.append(emb)
    y.append(1)
for idx in detailed:
    emb = get_embedding(idx)
    X.append(emb)
    y.append(2)
for idx in structured:
    emb = get_embedding(idx)
    X.append(emb)
    y.append(3)
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(max_iter=max_iter)
clf.fit(X, y)


X = []
y = []
for idx in original:
    emb = get_embedding(idx)
    X.append(emb)
    y.append(0)
for idx in basic:
    emb = get_embedding(idx)
    X.append(emb)
    y.append(1)
for idx in detailed:
    emb = get_embedding(idx)
    X.append(emb)
    y.append(2)
for idx in structured:
    emb = get_embedding(idx)
    X.append(emb)
    y.append(3)
clf = LogisticRegression(max_iter=1000)
clf.fit(X, y)
with open('classifier_tensors.json', 'w') as f:
    json.dump({'weights': clf.coef_.tolist(), 'bias': clf.intercept_.tolist()}, f)


class Model:
        def __init__(self, clf):
                self.clf = clf
        def predict(self, emb):
                return self.clf.predict([emb])[0]

model = Model(clf)

def eval(model):
        score = 0
        for idx in all_indices:
                emb = get_embedding(idx)
                cls = model.predict(emb)
                if (cls == 0 and idx in original) or (cls == 1 and idx in basic) or (cls == 2 and idx in detailed) or (cls == 3 and idx in structured):
                        score += 1
        return score


s = eval(model)
print(f"Score: {s}%")
