from .llm_client import prompt

SPAM_SYSTEM_INSTRUCTIONS = """
    You are a spam filter. This app is used to allow people to upload notes about concerts they haveattended.
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
    return response == "SPAM"