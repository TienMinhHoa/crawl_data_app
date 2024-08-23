import pandas as pd
import httpx
import Config
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
import warnings
import time 
from multiprocessing import Pool
warnings.filterwarnings('ignore')
from naive_content import  emphasize_hot_words
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
        # print("error")
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


from naive_bayes import preprocess_text
import joblib
title_clf = joblib.load("model_AI/filter_title/Bayse.pkl")
title_vectorize = joblib.load("model_AI/filter_title/vetorize.pkl")
content_clf = joblib.load("model_AI/filter_content/Bayes.pkl")
content_vectorize = joblib.load("model_AI/filter_content/vectorize.pkl")
from tqdm import tqdm

# def check_double(url):
def filter_url(url):
    response = requests.get(url, verify = False)
    encoding = response.encoding if response.encoding else 'ISO-8859-1' 
    soup = BeautifulSoup(response.content.decode(encoding), 'html.parser')
    
    title = soup.find('title').text
    title = preprocess_text(title)
    
    title_feature = title_vectorize.transform([title])
    title_label = title_clf.predict(title_feature)
    if title_label[0] == 0:
        return 0
    paragraphs = soup.find_all('p')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    article_content = ' '.join([para.text for para in paragraphs])
    heads = ' '.join([head.text for head in headings])
    content = " ".join(article_content.split()) +" "+ " ".join(heads.split())
    content = preprocess_text(content)
    content = emphasize_hot_words(content)
    content_feature = content_vectorize.transform([content])
    content_label = content_clf.predict(content_feature)
    return content_label
def filter_file(df):
    result= []
    for i,row in df.iterrows():
        try:
            title = row['title']
            title = preprocess_text(title)
            
            feature = title_vectorize.transform([title])
            label = title_clf.predict(feature)
            # print(label)
            if label[0] == 1:
                if title.strip() == 'thông báo' or len(title.split(" ")) <= 5:
                    print(f"{title} not thông báo")
                    continue
                print(title)
                result.append(row)
            else:
                print(f"{title} not")
        except Exception as e:
            print(e)
    return pd.DataFrame(result,columns=df.columns.tolist())
from urllib.parse import urljoin   
def check_file_exists(url):
    try:
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        # Tìm tất cả các liên kết trong trang web
        list_pdf = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Chuyển đổi URL tương đối sang URL đầy đủ
            full_url = urljoin(url, href)
            if '.pdf' in full_url or '.rar' in full_url or '.zip' in full_url:
                list_pdf.append(full_url)

    except requests.RequestException as e:

        # print(f"Không thể truy cập URL {url}: {e}")    
        return [0]   
    return list_pdf




    

if __name__=="__main__":
# res = filter_file("Save_info/main_data/thue.csv")
# url = 'https://thads.moj.gov.vn/tphochiminh/noidung/thongbao/lists/thongbao/view_detail.aspx?itemid=531'

    df = pd.read_csv("D:/pypy/Crawl_data/Save_info/2024/8/20/main_version_0.csv")
    urls = df['link'].tolist()
    with Pool(2) as pool:
        res = list(tqdm(pool.imap(check_file_exists,urls),total=len(urls)))
    print(res)

