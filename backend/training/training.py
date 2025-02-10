import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, Dataset
import pandas as pd

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the MuRIL tokenizer and model
model_name = "google/muril-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2).to(device)

# Load the preprocessed data
train_data = pd.read_csv('../preprocessing/train_data.csv')
val_data = pd.read_csv('../preprocessing/val_data.csv')
test_data = pd.read_csv('../preprocessing/test_data.csv')

# Convert to Hugging Face dataset format
train_dataset = Dataset.from_pandas(train_data)
val_dataset = Dataset.from_pandas(val_data)
test_dataset = Dataset.from_pandas(test_data)

# Tokenize the datasets
def tokenize(batch):
    return tokenizer(batch['text'], padding=True, truncation=True, max_length=128)

train_dataset = train_dataset.map(tokenize, batched=True)
val_dataset = val_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

# Set format for PyTorch
train_dataset.set_format(type="torch", columns=['input_ids', 'attention_mask', 'label'])
val_dataset.set_format(type="torch", columns=['input_ids', 'attention_mask', 'label'])
test_dataset.set_format(type="torch", columns=['input_ids', 'attention_mask', 'label'])

# Define training arguments with matching save and evaluation strategy
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",       # Set evaluation to occur every epoch
    save_strategy="epoch",             # Set saving to occur every epoch
    learning_rate=2e-5,
    per_device_train_batch_size=16,    # Increased batch size
    per_device_eval_batch_size=16,     # Increased batch size for evaluation
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True        # This will now work correctly
)



# Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

# Fine-tune the model
trainer.train()

# Evaluate the model on the test set
test_results = trainer.evaluate(test_dataset)
print("Test Results:", test_results)

# Save the model and tokenizer
model.save_pretrained("muril_hate_speech_model")
tokenizer.save_pretrained("muril_hate_speech_model")


