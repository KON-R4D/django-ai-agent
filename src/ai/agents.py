from langgraph.prebuilt import create_react_agent

from ai.llms import get_openai_model
from ai.tools import (
    document_tools
)

def get_document_agent():
    model = get_openai_model()

    agent = create_react_agent(
        model=model,  
        tools=document_tools,  
        prompt="You are a helpful assistant in managing a user's documents within this app"  
    )
    return agent
