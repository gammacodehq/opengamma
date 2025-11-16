import glob
from datasets import Dataset

# Read the text files completely
texts = []
for file_path in sorted(glob.glob("test/task*.txt")):
    with open(file_path, "r") as f:
        texts.append(f.read())

# Create Hugging Face dataset from the full texts
dataset = Dataset.from_dict({"text": texts})

# Push to Hugging Face Hub (replace 'your-username' and 'dataset-name' with actual values)
dataset.push_to_hub("mikeoxmaul/opengamma-prs")
