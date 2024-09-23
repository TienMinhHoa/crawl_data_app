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
    # print(q.make_query(content="tuyển dụng 2024",site="https://www.longbien.hanoi.gov.vn/"))
    # breakpoint
    response = httpx.get('http://localhost:8888/api/domain?page=0&limit=1')
    # breakpoint()
    res_json = json.loads(response.text)['data']
    id = [idx['id'] for idx in res_json]
    urls = [idx['urlDomain'] for idx in res_json]
    
    print(len(urls))
    for  url in tqdm(urls):
        res = []
        try:
            sub_df = q.make_query(
                content="tuyển dụng 2024", site=url, num_of_responses=15)
        except Exception as e:
            print(f"make query failed {e}")
            continue

        try:
            # with Pool(1) as pool:
            #     res = list(pool.imap(getter.get_info_url,
            #                sub_df['link'].tolist()))
            for url in sub_df['link'].tolist():
                res.append(getter.get_info_url(url))
        except Exception as e:
            # print(f"get info failed {e}")
            # print(sub_df)
            # print(url)
            continue
        # print(res)
        for index, tmp in enumerate(res):
            id_d = id[index]
            if tmp is None:
                continue
            link = sub_df['link'].tolist()[index]
            attachment = '\n'.join(tmp)
            title = getter.get_title(link)
            data = {
                    "crawledLink":link,
                    "linkTitle":title,
                    "attachmentUrl":attachment,
                    "domainId":id_d
                    }
            print(data)
            httpx.post("http://localhost:8888/api/crawled-link",json = data)
