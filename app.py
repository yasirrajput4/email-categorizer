"""
app.py
Streamlit web interface for the Smart Email/Document Categorizer.

Run with:
    streamlit run app.py

Features:
- Load demo emails or fetch live emails from a real Gmail inbox (IMAP)
- ML model predicts a category (color-coded) for each email
- Pick one of 3 AI-suggested replies, edit it, or write your own
- Send the reply directly from the app (SMTP)
"""

import os
import streamlit as st
import pandas as pd
import joblib

from reply_suggester import suggest_replies
from reply_sender import send_reply, extract_email_address

MODEL_PATH = "model/model.pkl"
DEMO_DATA_PATH = "data/sample_emails.csv"

CATEGORY_COLORS = {
    "Urgent": "#e74c3c",
    "Spam": "#7f8c8d",
    "Meeting": "#2980b9",
    "Project Update": "#27ae60",
    "General": "#8e44ad",
}


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


def clear_reply_widget_state():
    """
    BUGFIX: Streamlit keeps a widget's old value in session_state once its `key`
    has been created, even if you pass a different `value=` on the next render.
    Without this, reloading a new batch of emails would keep showing the reply
    text/choice from whatever was previously stored under reply_text_0,
    reply_choice_0, etc. (e.g. always showing the old "Spam" reply). Clearing
    these keys before loading a fresh inbox forces each widget to re-initialize
    from the new email's actual suggested replies.
    """
    prefixes = ("reply_text_", "reply_choice_", "reply_to_")
    for k in list(st.session_state.keys()):
        if k.startswith(prefixes):
            del st.session_state[k]


def get_demo_inbox(n=8, seed=None):
    df = pd.read_csv(DEMO_DATA_PATH)
    sample = df.sample(n=n, random_state=seed).reset_index(drop=True)
    return [
        {
            "subject": f"(demo email {i + 1})",
            "from": "",  # left blank on purpose - demo senders aren't real addresses
            "body": row["text"],
            "message_id": None,
            "is_demo": True,
        }
        for i, row in sample.iterrows()
    ]


def get_live_inbox(limit=8):
    from email_fetcher import fetch_recent_emails
    fetched = fetch_recent_emails(limit=limit)
    for item in fetched:
        item["is_demo"] = False
    return fetched


def render_email_card(idx, mail_item, category, replies):
    color = CATEGORY_COLORS.get(category, "#34495e")

    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**Subject:** {mail_item['subject']}")
            if mail_item.get("from"):
                st.caption(f"From: {mail_item['from']}")
        with col2:
            st.markdown(
                f"<span style='background-color:{color};color:white;"
                f"padding:4px 10px;border-radius:12px;font-size:0.8em;"
                f"font-weight:600;'>{category}</span>",
                unsafe_allow_html=True,
            )

        st.write(mail_item["body"][:300] + ("..." if len(mail_item["body"]) > 300 else ""))

        reply_key = f"reply_text_{idx}"
        choice_key = f"reply_choice_{idx}"
        to_key = f"reply_to_{idx}"

        with st.expander("Reply", expanded=False):
            options = [f"Suggestion {i+1}" for i in range(len(replies))] + ["Write my own"]
            choice = st.radio("Start from:", options, key=choice_key, horizontal=True)

            if choice == "Write my own":
                default_text = st.session_state.get(reply_key, "")
            else:
                sel_idx = int(choice.split()[-1]) - 1
                default_text = replies[sel_idx]

            reply_text = st.text_area(
                "Edit your reply before sending:",
                value=default_text,
                key=reply_key,
                height=120,
            )

            if mail_item.get("is_demo"):
                to_address = st.text_input(
                    "Send to (demo email has no real sender - enter an address to test):",
                    key=to_key,
                    placeholder="you@example.com",
                )
            else:
                to_address = mail_item.get("from", "")
                st.caption(f"Will be sent to: {extract_email_address(to_address)}")

            if st.button("Send Reply", key=f"send_{idx}", type="primary"):
                if not to_address:
                    st.error("Please enter a recipient email address.")
                elif not reply_text.strip():
                    st.error("Reply text can't be empty.")
                else:
                    try:
                        with st.spinner("Sending..."):
                            send_reply(
                                to_address=to_address,
                                subject=mail_item["subject"],
                                body=reply_text,
                                in_reply_to=mail_item.get("message_id"),
                            )
                        st.success(f"Reply sent to {extract_email_address(to_address)}")
                    except Exception as e:
                        st.error(f"Failed to send: {e}")


def main():
    st.set_page_config(page_title="Smart Email Categorizer", page_icon="📧", layout="centered")
    st.title("📧 Smart Automated Email Categorizer")
    st.caption("Python for Automation + Machine Learning — 7th Sem Internship Project")

    if not os.path.exists(MODEL_PATH):
        st.error("Model not found. Run `python train_model.py` first, then reload this page.")
        return

    model = load_model()

    st.sidebar.header("Gmail Credentials")
    st.sidebar.caption(
        "Needed to fetch live emails AND to send replies. Uses an App Password "
        "(not your real password). Nothing is saved to disk."
    )
    email_user = st.sidebar.text_input("Gmail address", key="email_user_input")
    email_pass = st.sidebar.text_input("App Password", type="password", key="email_pass_input")
    if email_user and email_pass:
        os.environ["EMAIL_USER"] = email_user
        os.environ["EMAIL_PASS"] = email_pass

    st.sidebar.header("Inbox Source")
    mode = st.sidebar.radio("Mode", ["Demo (sample data)", "Live (real Gmail inbox)"])

    if mode == "Demo (sample data)":
        n = st.sidebar.slider("Number of demo emails", 3, 15, 8)
        if st.sidebar.button("Load Demo Emails", type="primary"):
            clear_reply_widget_state()
            st.session_state["inbox"] = get_demo_inbox(n=n)

    else:
        limit = st.sidebar.slider("Number of emails to fetch", 3, 20, 8)
        if st.sidebar.button("Fetch Live Emails", type="primary"):
            if not email_user or not email_pass:
                st.sidebar.error("Please enter both email and app password above.")
            else:
                try:
                    clear_reply_widget_state()
                    with st.spinner("Connecting to inbox and fetching emails..."):
                        st.session_state["inbox"] = get_live_inbox(limit=limit)
                except Exception as e:
                    st.sidebar.error(f"Failed to fetch emails: {e}")

    inbox = st.session_state.get("inbox", [])

    if inbox:
        st.subheader(f"Processed {len(inbox)} email(s)")
        for idx, mail_item in enumerate(inbox):
            category = model.predict([mail_item["body"]])[0]
            replies = suggest_replies(category)
            render_email_card(idx, mail_item, category, replies)
    else:
        st.info("Use the sidebar to load demo emails or fetch from a live inbox.")


if __name__ == "__main__":
    main()