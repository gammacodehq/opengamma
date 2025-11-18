import json
from pathlib import Path
from datasets import load_dataset, Dataset


def main():
    # Load the deduplication report
    report_path = Path("results/deduplication/deduplication_report.json")
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    indices_to_remove = set(report["indices_to_remove"])

    # Load the original dataset
    dataset = load_dataset("mikeoxmaul/opengamma-prs")

    # Filter the train split to remove duplicates
    train_data = dataset["train"]
    filtered_data = [
        item for i, item in enumerate(train_data) if i not in indices_to_remove
    ]

    # Create a new dataset from the filtered data
    new_dataset = Dataset.from_list(filtered_data)

    # Upload to Hugging Face Hub with the new name
    new_dataset.push_to_hub("mikeoxmaul/opengamma-prs-dedup")


if __name__ == "__main__":
    main()
