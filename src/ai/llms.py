from django.conf import settings
from langchain_openai import ChatOpenAI


def get_openai_api_key():
    # ApiKey.objects.get(provider='openai', org='CFE)
    return settings.OPENAI_API_KEY


def get_openai_model(model="gpt-4o"):
    if model is None:
        model = "gpt-4o-mini"
    return ChatOpenAI(
        model=model,
        temperature=0,
        max_retries=2,
        api_key=get_openai_api_key(), 
    )