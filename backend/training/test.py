import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the trained model and tokenizer
model_path = "muril_hate_speech_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Custom dataset for tokenization
class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=128):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        inputs = self.tokenizer(text, padding="max_length", truncation=True, max_length=self.max_length, return_tensors="pt")
        inputs = {k: v.squeeze() for k, v in inputs.items()}  # Remove extra dimension
        return inputs

# Function for batch predictions
def classify_text_in_batches(text_list, batch_size=8):
    dataset = TextDataset(text_list, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size)
    
    all_predictions = []
    model.eval()
    with torch.no_grad():
        for batch in dataloader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            predictions = torch.argmax(outputs.logits, axis=1)
            all_predictions.extend(predictions.cpu().numpy())
    
    return np.array(all_predictions)

# Load the test data
test_data = pd.read_csv('../preprocessing/test_data.csv')
test_texts = test_data['text'].tolist()
test_labels = test_data['label'].tolist()

# Run predictions on the test set in batches
predictions = classify_text_in_batches(test_texts, batch_size=8)  # Adjust batch_size if still encountering OOM

# Calculate Accuracy, Precision, Recall, F1-Score
accuracy = accuracy_score(test_labels, predictions)
precision, recall, f1, _ = precision_recall_fscore_support(test_labels, predictions, average='binary')

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")

# Detailed Classification Report
print("\nClassification Report:")
print(classification_report(test_labels, predictions, target_names=["Non-hate", "Hate"]))

# Confusion Matrix
conf_matrix = confusion_matrix(test_labels, predictions)
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Non-hate", "Hate"], yticklabels=["Non-hate", "Hate"])
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.title("Confusion Matrix")
plt.show()
