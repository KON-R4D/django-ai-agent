from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor

from ai import agents
from ai.llms import get_openai_model


def get_supervisor(model=None, checkpointer=None):
    llm_model = get_openai_model(model=model)

    return create_supervisor(
        agents=[
            agents.get_document_agent(),
            agents.get_movie_discovery_agent(),
        ],
        model=llm_model,
        prompt=(
            "You manage a document management assistant and a"
            "movie discovery assistant. Assign work to them."
        ),
    ).compile(checkpointer=checkpointer)