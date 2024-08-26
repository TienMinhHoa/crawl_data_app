import httpx
import json
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool
from connect_db import DatabaseConnector
from custom_search import CustomSearch, FilterAndSave


if __name__ == "__main__":
    getter = FilterAndSave()
    q = CustomSearch()
    db = DatabaseConnector(server="localhost",
                           database="crawldb",
                           username="root",
                           password="nghia",
                           port=3307)
    db.connect()
    df = pd.read_excel("backend_data/data.xlsx")
    urls = df['Website'].tolist()
    id = df['ID'].tolist()
    res = httpx.get(f'{q.ROOT_API}/domain?page=0&limit=6')
    breakpoint()
    res_json = json.loads(res.text)['data']
    for i, url in tqdm(enumerate(urls)):
        try:
            sub_df = q.make_query(
                content="tuyển dụng 2024", site=url, num_of_responses=15)
        except Exception:
            continue

        try:
            with Pool(2) as pool:
                res = list(pool.imap(getter.get_info_url,
                           sub_df['link'].tolist()))
        except Exception:
            continue

        for index, tmp in enumerate(res):
            id_d = id[index]
            if tmp is None:
                continue
            link = sub_df['link'].tolist()[index]
            attachment = '\n'.join(tmp)
            title = getter.get_title(link)
            db.insert_data('crawledlinks', domain_id=id_d, crawled_link=link,
                           link_title=title, attachment_url=attachment)
