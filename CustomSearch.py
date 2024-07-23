import pandas as pd
import httpx
import Config


def gg_search(query,api_key = Config.API_KEY,search_engine_id = Config.SEARCH_ENGINE_ID,  **params):
    base_url = Config.BASE_URL
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        **params
    }
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def make_querry(content,site,num_of_responses = 10):
    pass
