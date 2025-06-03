from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from documents.models import Document

@tool
def list_documents(config:RunnableConfig):
    """
    List the most recent 5 documents for the current user
    """
    # print(config)
    limit = 5
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    qs = Document.objects.filter(owner_id=user_id, active=True).order_by("-created_at")
    response_data = []
    for obj in qs[:limit]:
        # serialize our django data into python dicts
        # django rest framework
        # django ninja
        # django model_to_dict
        # pydantic
        response_data.append(
            {
                "id": obj.id,
                "title": obj.title
            }
        )
    return response_data

@tool
def get_document(document_id:int, config:RunnableConfig):
    """
    Get the details of a document for the current user
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    try:
        obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    response_data =  {
        "id": obj.id,
        "title": obj.title
    }
    return response_data




document_tools = [
    list_documents,
    get_document
]