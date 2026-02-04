import pandas as pd
import numpy as np
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import Pipeline

# 1. Load Dataset

df = pd.read_csv('Badminton Data.csv')
print("Data loaded successfully.")

# 2. Data Preprocessing
def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    
    # Remove 'READ MORE'
    text = text.replace("READ MORE", "")
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but KEEP apostrophes (for don't, can't, etc.)
    # We keep letters, spaces, and '
    text = re.sub(r"[^a-z\s']", '', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

print("Preprocessing data...")
df['cleaned_text'] = df['Review text'].apply(preprocess_text)

# 3. Labeling
# Ratings 4, 5 -> Positive (1)
# Ratings 1, 2 -> Negative (0)
# Rating 3 -> Neutral (Drop)
df = df[df['Ratings'] != 3]
df['label'] = df['Ratings'].apply(lambda x: 1 if x > 3 else 0)

# Check Class Balance
print(f"Class distribution:\n{df['label'].value_counts()}")

# 4. Split Data
X = df['cleaned_text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 5. Build Pipeline

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ('clf', LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced'))
])

# 6. Train Model
print("Training model...")
pipeline.fit(X_train, y_train)

# 7. Evaluate Model
y_pred = pipeline.predict(X_test)
print("\nModel Evaluation:")
print(f"F1 Score: {f1_score(y_test, y_pred, average='weighted'):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 8. Save Model
model_filename = 'sentiment_model.pkl'
joblib.dump(pipeline, model_filename)
print(f"Model saved to {model_filename}")