import pandas as pd
import httpx
import Config


def gg_search(querry,api_key = Config.API_KEY,search_engine_id = Config.SEARCH_ENGINE_ID,  **params):
    base_url = Config.BASE_URL
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": querry,
        **params
    }
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def make_querry(content,site,num_of_responses = 10):
    querry = content+" "+"site:"+site
    search_res = []
    for i in range(1,num_of_responses,10):
        res = gg_search(querry = querry,start = i)
        search_res.extend(res.get('items', []))
    df = pd.json_normalize(search_res)
    return df

res = make_querry("tuyển dụng 2024",site = "http://gialam.hanoi.gov.vn")
print(res.head())
