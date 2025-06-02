from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from documents.models import Document

@tool
def list_documents(config:RunnableConfig):
    """
    Get documents for the current user
    """
    # print(config)
    metadata = config.get('metadata') or config.get('configurable')
    user_id = metadata.get('user_id')
    qs = Document.objects.filter(owner_id=user_id, active=True)
    response_data = []
    for obj in qs:
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
    metadata = config.get('metadata') or config.get('configurable')
    user_id = metadata.get('user_id')
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