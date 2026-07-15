"""
reply_sender.py
Automation component: sends an email reply using smtplib (SMTP over TLS).
Uses the same Gmail App Password credentials as email_fetcher.py.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr


def extract_email_address(raw_from: str) -> str:
    """Extracts just the email address from a 'Name <email@x.com>' style string."""
    name, addr = parseaddr(raw_from)
    return addr or raw_from


def send_reply(to_address, subject, body, in_reply_to=None, references=None,
               smtp_server="smtp.gmail.com", smtp_port=587):
    """
    Sends an email using SMTP + STARTTLS.
    Reads sender credentials from EMAIL_USER / EMAIL_PASS environment variables
    (same App Password used for fetching, set via the sidebar or shell env).
    """
    user = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")

    if not user or not password:
        raise EnvironmentError(
            "EMAIL_USER / EMAIL_PASS not set. Enter your Gmail address and "
            "App Password in the sidebar first."
        )

    to_address = extract_email_address(to_address)

    if not subject.lower().startswith("re:"):
        subject = f"Re: {subject}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_address

    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = references or in_reply_to

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(user, [to_address], msg.as_string())

    return True