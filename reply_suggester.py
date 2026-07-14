"""
reply_suggester.py
Given a predicted category, suggests 3 ready-to-send automated replies.
This is the "unique factor" feature of the project.
"""

REPLY_TEMPLATES = {
    "Urgent": [
        "Thank you for flagging this. I am looking into it right now and will update you within the hour.",
        "This has been escalated to the concerned team on priority. We will resolve it as soon as possible.",
        "Acknowledged as urgent. Please stay online, I am joining a call to resolve this immediately."
    ],
    "Spam": [
        "This message has been identified as spam/promotional and moved to the spam folder automatically.",
        "No action needed - this appears to be an unsolicited/promotional email.",
        "This sender has been flagged for review as potential spam."
    ],
    "Meeting": [
        "Thank you for the invite, I confirm my availability for the meeting.",
        "I have a scheduling conflict, could we move this meeting to another slot?",
        "Noted, I will join the meeting and share the agenda points beforehand."
    ],
    "Project Update": [
        "Thanks for the update, this looks great. Please proceed to the next phase.",
        "Received the status update, will review and share feedback by tomorrow.",
        "Great progress! Please also share the updated timeline for remaining tasks."
    ],
    "General": [
        "Thank you for your email, I will get back to you shortly.",
        "Noted, thanks for sharing this information.",
        "Received, will review and respond soon if further input is needed."
    ]
}


def suggest_replies(category: str):
    """Return 3 suggested replies for a given predicted category."""
    return REPLY_TEMPLATES.get(category, REPLY_TEMPLATES["General"])
