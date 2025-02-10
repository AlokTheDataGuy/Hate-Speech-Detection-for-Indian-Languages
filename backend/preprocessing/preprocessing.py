import pandas as pd
import re
from sklearn.model_selection import train_test_split

# Function to clean text (remove unwanted symbols, emojis, etc.)
def clean_text(text):
    if pd.isna(text):
        return ""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove usernames (e.g., @username)
    text = re.sub(r'@\w+', '', text)
    # Remove emojis and special characters except non-English alphabets
    text = re.sub(r'[^\w\s]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load datasets with proper encoding for multi-language support
df_bangla = pd.read_csv('../dataset/bangla.csv', header=0, encoding='utf-8')
df_english = pd.read_csv('../dataset/english.csv', header=0, encoding='utf-8')
df_hindi = pd.read_csv('../dataset/hindi.csv', header=0, encoding='utf-8')
df_marathi = pd.read_csv('../dataset/marathi.csv', header=0, encoding='utf-8')

# Combine all datasets
df_combined = pd.concat([df_marathi, df_bangla, df_english, df_hindi], ignore_index=True)

# Drop rows with NaN in text or label column
df_combined = df_combined.dropna(subset=['text', 'label'])

# Ensure the label column is integer type
df_combined['label'] = df_combined['label'].astype(int)

# Clean the text data
df_combined['text'] = df_combined['text'].apply(clean_text)

# Remove any rows where text is empty after cleaning
df_combined = df_combined[df_combined['text'] != ""]

# Shuffle data
df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)

# Split text and labels
X = df_combined['text']
y = df_combined['label']

# Split dataset into train (80%), validation (10%), and test (10%) sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

# Combine text and labels into one DataFrame for each split
train_data = pd.DataFrame({'text': X_train, 'label': y_train})
val_data = pd.DataFrame({'text': X_val, 'label': y_val})
test_data = pd.DataFrame({'text': X_test, 'label': y_test})

# Save the combined data to CSV files with UTF-8 encoding
train_data.to_csv('train_data.csv', index=False, encoding='utf-8')
val_data.to_csv('val_data.csv', index=False, encoding='utf-8')
test_data.to_csv('test_data.csv', index=False, encoding='utf-8')

print("Data preprocessing and splitting completed. Files saved as 'train_data.csv', 'val_data.csv', and 'test_data.csv'.")
