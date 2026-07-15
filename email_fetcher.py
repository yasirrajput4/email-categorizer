"""
email_fetcher.py
Automation component: connects to a real inbox using imaplib and fetches
recent unread emails (subject + body).

SETUP (Gmail example):
1. Enable 2-Step Verification on your Google account.
2. Create an "App Password": Google Account -> Security -> App Passwords.
3. Set environment variables before running (do NOT hardcode passwords):
       export EMAIL_USER="youremail@gmail.com"
       export EMAIL_PASS="your_16_char_app_password"
4. Run: python main.py --live

If EMAIL_USER / EMAIL_PASS are not set, main.py automatically falls back
to demo mode using data/sample_emails.csv so the project still runs
end-to-end for a viva/demo without a real inbox.
"""

import imaplib
import email
from email.header import decode_header
import os


def clean(text):
    if isinstance(text, bytes):
        try:
            return text.decode()
        except Exception:
            return text.decode("utf-8", errors="ignore")
    return text


def fetch_recent_emails(limit=10, imap_server="imap.gmail.com"):
    """
    Connects to the mailbox via IMAP and fetches the `limit` most recent emails.
    Returns a list of dicts: [{"subject": ..., "from": ..., "body": ...}, ...]
    """
    user = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")

    if not user or not password:
        raise EnvironmentError(
            "EMAIL_USER / EMAIL_PASS not set. Set them as environment variables "
            "or run main.py in demo mode (default)."
        )

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(user, password)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()
    latest_ids = mail_ids[-limit:] if len(mail_ids) > limit else mail_ids

    results = []
    for mid in reversed(latest_ids):
        status, msg_data = mail.fetch(mid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        subject = clean(subject)

        from_ = msg.get("From")
        message_id = msg.get("Message-ID")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = clean(part.get_payload(decode=True))
                    break
        else:
            body = clean(msg.get_payload(decode=True))

        results.append({"subject": subject, "from": from_, "body": body, "message_id": message_id})

    mail.logout()
    return results