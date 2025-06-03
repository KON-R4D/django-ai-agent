from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from tmdb import client as tmdb_client


@tool
def search_movies(query: str, limit:int=5, config:RunnableConfig = {}):
    """
    Search the most recent LIMIT movies from The Movie Database with maximum of 25.

    arguments:
    query: string or lookup search across title or content of document
    limit: number of results
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    print('Searching with user', user_id)
    response = tmdb_client.search_movie(query, raw=False)
    try:
        total_results = int(response.get("total_results"))
    except:
        total_results = -1
    if total_results == 0:
        return []
    if limit > 25:
        limit = 25
    results = response.get("results")[:limit]
    return results
    

@tool
def movie_detail(movie_id: int, config:RunnableConfig = {}):
    """
    Movie detail from The Movie Database if it exists.

    arguments:
    movie_id: integer from movie search
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    print('Searching with user', user_id)
    response = tmdb_client.movie_detail(movie_id, raw=False)
    return response


movie_discovery_tools = [
    search_movies,
    movie_detail
]