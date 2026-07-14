"""
main.py
Smart Automated Email/Document Categorizer - Main Orchestrator

Combines:
1. Automation  -> email_fetcher.py (imaplib, real inbox OR demo mode)
2. ML          -> TF-IDF + Logistic Regression (model/model.pkl, trained via train_model.py)
3. Unique      -> reply_suggester.py (3 auto-reply suggestions per category)

Usage:
    python main.py            # demo mode, uses data/sample_emails.csv as "inbox"
    python main.py --live     # real mode, fetches from actual inbox via IMAP
"""

import sys
import os
import pandas as pd
import joblib
from reply_suggester import suggest_replies

MODEL_PATH = "model/model.pkl"
DEMO_DATA_PATH = "data/sample_emails.csv"


def load_model():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Please run 'python train_model.py' first.")
        sys.exit(1)
    return joblib.load(MODEL_PATH)


def get_demo_inbox(n=8):
    """Simulates an inbox using a few sample emails (unseen-ish combos) for demo purposes."""
    df = pd.read_csv(DEMO_DATA_PATH)
    sample = df.sample(n=n, random_state=7).reset_index(drop=True)
    return [{"subject": f"(demo email {i+1})", "from": "demo@sender.com", "body": row["text"]}
             for i, row in sample.iterrows()]


def get_live_inbox(limit=8):
    from email_fetcher import fetch_recent_emails
    return fetch_recent_emails(limit=limit)


def run(mode="demo"):
    model = load_model()

    if mode == "live":
        print("Fetching live emails from inbox via IMAP...\n")
        inbox = get_live_inbox()
    else:
        print("Running in DEMO mode using data/sample_emails.csv as a simulated inbox...\n")
        inbox = get_demo_inbox()

    print("=" * 80)
    for i, mail_item in enumerate(inbox, start=1):
        text = mail_item["body"]
        category = model.predict([text])[0]
        replies = suggest_replies(category)

        print(f"[{i}] Subject : {mail_item['subject']}")
        print(f"    From    : {mail_item['from']}")
        print(f"    Content : {text[:100]}{'...' if len(text) > 100 else ''}")
        print(f"    >>> Predicted Category: {category}")
        print(f"    >>> Suggested Replies:")
        for j, r in enumerate(replies, start=1):
            print(f"        {j}. {r}")
        print("-" * 80)

    print("Done. Processed", len(inbox), "emails.")


if __name__ == "__main__":
    mode = "live" if "--live" in sys.argv else "demo"
    run(mode)
