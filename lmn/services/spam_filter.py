from .llm_client import prompt

SPAM_SYSTEM_INSTRUCTIONS = """
    You are a spam filter. This app is used to allow people to upload notes about concerts they have attended.
    Detect spam or nonrelevant information such as advertising, abusive material,
    sexual or explicit content, or any content not relevant to a concert experience.
    If content is relevant to a concert, but also explicit or abusive, mark it as spam.
    Reply with only: SPAM or NOT_SPAM
    """

def is_spam(title, text):
    """
    Will return true if the response is determined to be spam.
    """
    user_text = f"Text Title: {title}\nText body: {text}"
    response = prompt(SPAM_SYSTEM_INSTRUCTIONS, user_text)
    return response.strip() == "SPAM"


def check_note_spam(note_pk):
    """
    Checks a saved note for spam and updates its spam_status. Designed to run in a background thread.
    """
    from lmn.models import Note, SPAM_STATUS_SPAM, SPAM_STATUS_APPROVED
    from django.db import connection
    try:
        note = Note.objects.get(pk=note_pk)
        status = SPAM_STATUS_SPAM if is_spam(note.title, note.text) else SPAM_STATUS_APPROVED
        Note.objects.filter(pk=note_pk).update(spam_status=status)
    except Exception:
        pass  # leave as PENDING on failure
    finally:
        connection.close()