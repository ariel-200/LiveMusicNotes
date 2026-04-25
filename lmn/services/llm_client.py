from django.conf import settings
from google import genai
from google.genai import types

def get_client():
    return genai.Client(api_key=settings.GEMINI_API_KEY)

def prompt(system_instruction, user_input):
    client = get_client()
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        )
    )
    return response.text