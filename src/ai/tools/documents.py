from asgiref.sync import async_to_sync

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from django.db.models import Q

from documents.models import Document
from mypermit import permit_client as permit


@tool
def search_query_documents(query: str, limit:int=5, config:RunnableConfig = {}):
    """
    Search the most recent LIMIT documents for the current user  with maximum of 25.

    arguments:
    query: string or lookup search across title or content of document
    limit: number of results
    """
    # print(config)
    if limit > 25:
        limit = 25
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    default_lookups = {

        "active": True,
        
    }

    has_perms = async_to_sync(permit.check)(f"{user_id}", "read", "document")
    if not has_perms:
        raise Exception("You do not have permission to do search the documents.")

    qs = Document.objects.filter(**default_lookups).filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    ).order_by("-created_at")
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
def list_documents(limit:int = 5, config:RunnableConfig= {}):
    """
    List the most recent LIMIT documents for the current user with maximum of 25.

    agruments
    limit: number of results
    """
    if limit > 25:
        limit = 25
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    has_perms = async_to_sync(permit.check)(f"{user_id}", "read", "document")
    if not has_perms:
        raise Exception("You do not have permission to list all documents.")
    qs = Document.objects.filter(active=True).order_by("-created_at")
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
    
    has_perms = async_to_sync(permit.check)(f"{user_id}", "read", "document")
    if not has_perms:
        raise Exception("You do not have permission to get individual documents.")
    try:
        obj = Document.objects.get(id=document_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    response_data =  {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    return response_data



@tool
def create_document(title:str, content:str, config:RunnableConfig):
    """
    Create a new document to store for the user.

    Arguments are:
    title: string max characters of 120
    content: long form text in many paragraphs or pages
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    has_perms = async_to_sync(permit.check)(f"{user_id}", "create", "document")
    if not has_perms:
        raise Exception("You do not have permission to create individual documents.")
    
    obj = Document.objects.create(title=title, content=content, owner_id=user_id, active=True)
    response_data =  {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    return response_data


@tool
def update_document(document_id:int, title:str =None, content:str = None, config:RunnableConfig={}):
    """
    Update a document for a user by the document id and related arguments.

    Arguments are:
    document_id: id of document (required)
    title: string max characters of 120 (optional)
    content: long form text in many paragraphs or pages (optional)
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    has_perms = async_to_sync(permit.check)(f"{user_id}", "update", "document")
    if not has_perms:
        raise Exception("You do not have permission to update individual documents.")
    try:
        obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    
    if title is not None:
        obj.title = title
    if content is not None:
        obj.content = content
    if title or content:
        obj.save()
    # obj = Document.objects.create(title=title, content=content, owner_id=user_id, active=True)
    response_data =  {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    return response_data



@tool
def delete_document(document_id:int, config:RunnableConfig):
    """
    Delete the document for the current user by document_id
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    has_perms = async_to_sync(permit.check)(f"{user_id}", "delete", "document")
    if not has_perms:
        raise Exception("You do not have permission to delete individual documents.")
    try:
        obj = Document.objects.get(id=document_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    
    # has_object_perms = async_to_sync(permit.check)(f"{user_id}", "delete", f"document:{obj.id}")
    # if not has_object_perms:
    #     raise Exception("You do not have permission to delete individual documents.")
    obj.delete()
    response_data =  {"message": "success"}
    return response_data

document_tools = [
    create_document,
    list_documents,
    get_document,
    delete_document
]