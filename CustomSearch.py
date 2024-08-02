import pandas as pd
import httpx
import Config
from datetime import datetime
import os

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


def make_querry(content,site,num_of_responses = 30):
    querry = content+" "+"site:"+site
    search_res = []
    for i in range(1,num_of_responses,10):
        res = gg_search(querry = querry,start = i)
        search_res.extend(res.get('items', []))
    df = pd.json_normalize(search_res)
    return df

def export_latest(name,data):    
    if os.path.exists(f"Save_info/main_data/{name}.csv"):
        df = pd.read_csv(f"Save_info/main_data/{name}.csv")
        titles = df['title'].values
        for i,row in data.iterrows():
            if row['title'] in titles:
                continue
            pd.concat([df,row])
        try:
            df.to_csv(f"Save_info/main_data/{name}.csv",index =False)
            print("save main data sucess")
            return True
        except Exception as e:
            print(e)
            return False
    else:
        data.to_csv(f"Save_info/main_data/{name}.csv",index = False)
        print("error")
        return False
def export_csv(name,data):
    time = datetime.now()
    date = time.day
    month = time.month
    year = time.year
    year_path = os.path.join(Config.SAVE_PATH,str(year))
    month_path = os.path.join(year_path,str(month))
    day_path = os.path.join(month_path,str(date))

    if not os.path.exists(year_path):
        os.makedirs(year_path)
    if not os.path.exists(month_path):
        os.makedirs(month_path)
    if not os.path.exists(day_path):
        os.makedirs(day_path)

    version = len(os.listdir(day_path))
    try:
        data.to_csv(f"{day_path}/{name}_version_{str(version)}.csv")
        export_latest(name,data)
    except Exception as e:
        print(e)
        return e
    return "Export success"


res = make_querry("tuyển dụng 2024",site = "http://gialam.hanoi.gov.vn")
print(export_csv('HA_Noi',res))
print(res.head())
