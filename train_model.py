"""
train_model.py
Trains a TF-IDF + Logistic Regression text classifier to categorize emails
into: Urgent, Spam, Meeting, Project Update, General

Run: python train_model.py
Output: model/model.pkl (trained pipeline saved with joblib)
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

DATA_PATH = "data/sample_emails.csv"
MODEL_PATH = "model/model.pkl"


def train():
    # 1. Load dataset
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} labeled emails across categories: {df['label'].unique()}")

    X = df["text"]
    y = df["label"]

    # 2. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Build pipeline: TF-IDF vectorizer + Logistic Regression classifier
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    # 4. Train
    pipeline.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = pipeline.predict(X_test)
    print("\n--- Model Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred))

    # 6. Save model
    os.makedirs("model", exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()
