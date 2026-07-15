# Smart Automated Email/Document Categorizer

### 7th Semester Internship Mini-Project — Python for Automation + Machine Learning

## Overview

Companies receive huge volumes of emails daily. This project automatically **fetches
emails**, **classifies** them into categories using Machine Learning, and **suggests
ready-to-send replies** — reducing manual triage time.

## Categories

`Urgent` | `Spam` | `Meeting` | `Project Update` | `General`

## Tech Stack

| Component                 | Tool/Library                                  |
| ------------------------- | --------------------------------------------- |
| Automation (fetch emails) | `imaplib`, `email`                            |
| ML (text classification)  | `scikit-learn` — TF-IDF + Logistic Regression |
| Data handling             | `pandas`                                      |
| Model persistence         | `joblib`                                      |

## Project Structure

```
email-categorizer/
├── data/
│   └── sample_emails.csv     # 50 labeled sample emails (training data)
├── model/
│   └── model.pkl             # trained ML pipeline (created after training)
├── train_model.py            # trains TF-IDF + Logistic Regression classifier
├── email_fetcher.py          # imaplib-based real inbox fetcher (automation)
├── reply_suggester.py        # rule-based reply suggestion engine (unique feature)
├── reply_sender.py           # smtplib-based reply sender (send/edit/write own reply)
├── main.py                   # terminal orchestrator: fetch -> classify -> suggest replies
├── app.py                    # Streamlit web app (browser-based UI)
├── requirements.txt
└── .gitignore                # excludes venv/, __pycache__/, .env from git
```

## How It Works

1. **Automation layer** (`email_fetcher.py`): connects to a real Gmail inbox using
   `imaplib` (IMAP protocol) and pulls the latest unread emails (subject + body).
2. **ML layer** (`train_model.py`): a `TfidfVectorizer` converts email text into
   numeric features, and a `LogisticRegression` classifier (works just as well with
   `MultinomialNB` if you want to swap it) predicts the category. Achieves ~90%
   accuracy on the sample dataset.
3. **Unique feature** (`reply_suggester.py`): for every predicted category, the system
   returns 3 pre-drafted, context-appropriate replies — e.g., an "Urgent" email gets
   escalation-style replies, a "Meeting" email gets availability-confirmation replies.

## Setup & Run

```bash
# Step 0: Create and activate a virtual environment (recommended)
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Step 1: Install dependencies (inside the venv, won't touch your system Python)
pip install -r requirements.txt

# Step 2: Train the model (creates model/model.pkl)
python train_model.py

# Step 3: Run in DEMO mode (no real inbox needed — uses sample_emails.csv)
python main.py

# Step 3 (alternative): Run in LIVE mode against a real Gmail inbox
export EMAIL_USER="youremail@gmail.com"
export EMAIL_PASS="your_16_char_gmail_app_password"
python main.py --live

# Step 3 (alternative): Run the Web App (Streamlit) instead of the terminal
streamlit run app.py
```

## Web App (Recommended for Demo/Viva)

Instead of terminal output, run the Streamlit web interface — opens automatically
in your browser at `http://localhost:8501`:

```bash
streamlit run app.py
```

- **Demo mode**: sidebar → "Demo (sample data)" → click "Load Demo Emails" — shows
  color-coded category badges for each email.
- **Live mode**: sidebar → enter Gmail address + App Password → "Live (real Gmail
  inbox)" → click "Fetch Live Emails".
- **Replying**: open the "Reply" section under any email → pick one of the 3
  suggested replies (or "Write my own") → edit the text freely → click
  "Send Reply". This uses `smtplib` to actually send the email (requires the
  same Gmail address + App Password entered in the sidebar). In demo mode you
  can type any address to test-send since the sample emails have no real sender.

> Once done working, run `deactivate` to exit the virtual environment.
> When active, your terminal prompt will show `(venv)` at the start.

> **Note on live mode:** Gmail requires an "App Password" (not your normal password) —
> generate one from Google Account → Security → 2-Step Verification → App Passwords.
> Never hardcode credentials in code; they are read from environment variables.

## Sample Output

```
[7] Subject : (demo email 7)
    Content : Critical bug in payment gateway, needs fix before end of day...
    >>> Predicted Category: Urgent
    >>> Suggested Replies:
        1. Thank you for flagging this. I am looking into it right now...
        2. This has been escalated to the concerned team on priority...
        3. Acknowledged as urgent. Please stay online, I am joining a call...
```

## Pushing to GitHub

```bash
# 1. Initialize git (run inside the email_categorizer folder)
git init

# 2. Add a .gitignore (already included in this project) so venv/, __pycache__/,
#    and .env credentials are NEVER pushed

# 3. Stage and commit
git add .
git commit -m "Initial commit: Smart Email Categorizer (Python Automation + ML)"

# 4. Create a new empty repo on GitHub (via github.com -> New Repository)
#    Do NOT initialize it with a README there — you already have one locally.

# 5. Link your local repo to GitHub and push
git branch -M main
git remote add origin https://github.com/yasirrajput4/email-categorizer.git
git push -u origin main
```

> **Important:** `.gitignore` already excludes `venv/` and `.env`. Double-check
> before pushing that no real email/password ever gets committed — if you tested
> live mode locally, those credentials only lived in your terminal session as
> environment variables, not in any file, so they're safe by default.
