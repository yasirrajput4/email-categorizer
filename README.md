# 📧 Smart Automated Email/Document Categorizer

### 7th Semester Internship Mini-Project — Python for Automation + Machine Learning

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge)](https://email-categorizer.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

**🔗 Live App:** [email-categorizer.streamlit.app](https://email-categorizer.streamlit.app)

---

## Overview

Companies receive huge volumes of emails daily. This project automatically **fetches
emails**, **classifies** them into categories using Machine Learning, and **suggests
ready-to-send replies** — reducing manual triage time.

## Demo

![App Screenshot](https://github.com/user-attachments/assets/6da81c80-4e00-49c1-b702-7f4955aebcdc)

Try it live here: **[email-categorizer.streamlit.app](https://email-categorizer.streamlit.app)**

## Categories

`Urgent` | `Spam` | `Meeting` | `Project Update` | `General`

## Features

- 📥 **Automated email fetching** from a real Gmail inbox via IMAP
- 🤖 **ML-based classification** into 5 categories (TF-IDF + Logistic Regression, ~90% accuracy)
- 💬 **3 AI-suggested replies** per email, tailored to the predicted category
- ✏️ **Editable replies** — pick a suggestion, tweak it, or write your own from scratch
- 📤 **One-click sending** directly from the app via SMTP
- 🌐 **Browser-based UI** (Streamlit) — no terminal needed
- 🔒 **Secure by design** — uses Gmail App Passwords, never stores credentials to disk

## Tech Stack

| Component                 | Tool/Library                                  |
| ------------------------- | --------------------------------------------- |
| Automation (fetch emails) | `imaplib`, `email`                            |
| Automation (send replies) | `smtplib`                                     |
| ML (text classification)  | `scikit-learn` — TF-IDF + Logistic Regression |
| Data handling             | `pandas`                                      |
| Model persistence         | `joblib`                                      |
| Web interface             | `streamlit`                                   |

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
├── app.py                    # Streamlit web app (browser-based UI) — deployed live
├── requirements.txt
└── .gitignore                # excludes venv/, __pycache__/, .env from git
```

## How It Works

1. **Automation layer** (`email_fetcher.py` / `reply_sender.py`): connects to a real
   Gmail inbox using `imaplib` (IMAP protocol) to pull the latest emails, and `smtplib`
   (SMTP + STARTTLS) to send replies back — all using a secure Gmail App Password.
2. **ML layer** (`train_model.py`): a `TfidfVectorizer` converts email text into
   numeric features, and a `LogisticRegression` classifier predicts the category.
   Achieves ~90% accuracy on the sample dataset.
3. **Unique feature** (`reply_suggester.py`): for every predicted category, the system
   returns 3 pre-drafted, context-appropriate replies — e.g., an "Urgent" email gets
   escalation-style replies, a "Meeting" email gets availability-confirmation replies.
   The user can pick one, edit it, or write a custom reply before sending.

## Quick Start (Try it online)

No installation needed — just open the live app:
👉 **[email-categorizer.streamlit.app](https://email-categorizer.streamlit.app)**

- Click **"Load Demo Emails"** in the sidebar to see it work instantly with sample data.
- Or enter your Gmail address + [App Password](https://myaccount.google.com/apppasswords)
  to fetch and reply to your real inbox.

## Run Locally

```bash
# Step 0: Clone the repo
git clone https://github.com/yasirrajput4/email-categorizer.git
cd email-categorizer

# Step 1: Create and activate a virtual environment (recommended)
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Train the model (creates model/model.pkl)
python train_model.py

# Step 4: Run in DEMO mode (no real inbox needed — uses sample_emails.csv)
python main.py

# Step 4 (alternative): Run in LIVE mode against a real Gmail inbox
export EMAIL_USER="youremail@gmail.com"
export EMAIL_PASS="your_16_char_gmail_app_password"
python main.py --live

# Step 4 (alternative): Run the Web App (Streamlit) instead of the terminal
streamlit run app.py
```

> Once done working, run `deactivate` to exit the virtual environment.
> When active, your terminal prompt will show `(venv)` at the start.

## Web App Guide

Run locally with `streamlit run app.py`, or just use the **[live version](https://email-categorizer.streamlit.app)**.

- **Demo mode**: sidebar → "Demo (sample data)" → click "Load Demo Emails" — shows
  color-coded category badges for each email.
- **Live mode**: sidebar → enter Gmail address + App Password → "Live (real Gmail
  inbox)" → click "Fetch Live Emails".
- **Replying**: open the "Reply" section under any email → pick one of the 3
  suggested replies (or "Write my own") → edit the text freely → click
  "Send Reply". This uses `smtplib` to actually send the email (requires the
  same Gmail address + App Password entered in the sidebar). In demo mode you
  can type any address to test-send since the sample emails have no real sender.

> **Note on live mode:** Gmail requires an "App Password" (not your normal password) —
> generate one from Google Account → Security → 2-Step Verification → App Passwords.
> Never hardcode credentials in code; they are read from environment variables, and
> nothing is ever saved to disk.

## Sample Output (Terminal Mode)

```
[7] Subject : (demo email 7)
    Content : Critical bug in payment gateway, needs fix before end of day...
    >>> Predicted Category: Urgent
    >>> Suggested Replies:
        1. Thank you for flagging this. I am looking into it right now...
        2. This has been escalated to the concerned team on priority...
        3. Acknowledged as urgent. Please stay online, I am joining a call...
```

## Deployment

This app is deployed on **[Streamlit Community Cloud](https://streamlit.io/cloud)**,
directly from this GitHub repo (`app.py` as the entry point). Any push to `main` auto-redeploys the live app.

**Live URL:** https://email-categorizer.streamlit.app

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

## Future Enhancements

- Replace Logistic Regression with a fine-tuned transformer model (e.g., DistilBERT)
- Auto-move categorized emails into corresponding IMAP folders
- Analytics dashboard showing category-wise email volume trends
- Support for multiple email providers (Outlook, Yahoo)
- Feedback loop to retrain the model on corrected classifications

## Author

**Yasir Rajput**
7th Semester, Computer Science and Engineering
SAL Institute of Technology & Engineering Research
