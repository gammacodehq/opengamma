from datasets import load_dataset

# Load the dataset from Hugging Face
dataset = load_dataset("mikeoxmaul/opengamma-prs")

# Output the first text from the train split
print(dataset["train"][0]["text"])
