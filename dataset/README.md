# OpenGamma PRS Dataset

Language: RU.

This dataset contains assistant messages extracted from conversations where either the user or assistant message contains the keyword 'резентаци'. Each sample is a full assistant response text.

## Dataset Structure

- **Format**: Text dataset with a single column 'text'
- **Splits**: train (all data)
- **Size**: Varies based on extraction

## Usage

### Loading the Dataset

```python
from datasets import load_dataset

dataset = load_dataset("mikeoxmaul/opengamma-prs")
print(dataset['train'][0]['text'])
```

### Example Output

The first text sample might look like:

```
**Презентация: Редкие животные Алтайского края и их характеристика**  
(документ можно скопировать в Google Slides, PowerPoint или Keynote)
...
```

## Creation

The dataset is created by:
1. Extracting first user and assistant messages from SQLite database conversations.
2. Filtering for messages containing 'резентаци'.
3. Saving each assistant message as a separate text file.
4. Uploading to Hugging Face Hub as a dataset.

## License

MIT
