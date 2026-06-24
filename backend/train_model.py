import os
import json
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

FAKE_PATH = os.path.join(PROJECT_DIR, "data", "Fake.csv")
TRUE_PATH = os.path.join(PROJECT_DIR, "data", "True.csv")
MODEL_DIR = os.path.join(PROJECT_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "fake_news_model.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

def load_dataset():
    fake = pd.read_csv(FAKE_PATH)
    true = pd.read_csv(TRUE_PATH)

    fake["label"] = "FAKE"
    true["label"] = "REAL"

    df = pd.concat([fake, true], ignore_index=True)
    df["title"] = df["title"].fillna("")
    df["text"] = df["text"].fillna("")
    df["content"] = (df["title"] + " " + df["text"]).str.strip()

    df = df[df["content"].str.len() > 20]
    df = df.drop_duplicates(subset=["content"])

    return df

def train():
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        df["content"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            stop_words="english",
            max_features=50000,
            ngram_range=(1, 2),
            min_df=2
        )),
        ("model", LogisticRegression(max_iter=1000, C=2.0))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    metrics = {
        "accuracy": round(float(accuracy), 4),
        "labels": ["FAKE", "REAL"],
        "total_rows_used": int(len(df)),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=["FAKE", "REAL"]).tolist(),
        "classification_report": classification_report(y_test, y_pred, output_dict=True)
    }

    joblib.dump(pipeline, MODEL_PATH)

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("Model trained successfully.")
    print(f"Accuracy: {metrics['accuracy'] * 100:.2f}%")
    print(f"Model saved at: {MODEL_PATH}")

if __name__ == "__main__":
    train()
