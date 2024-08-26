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
from naive_bayes import preprocess_text
import joblib
from urllib.parse import urljoin 
from tqdm import tqdm
from ConnectDB import DatabaseConnector
class CustomSearch:
    def __init__(self,api_key = Config.API_KEY,search_engine_id = Config.SEARCH_ENGINE_ID):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        # self.df = pd.read_xlsx(domains_path)

    def __gg_search(self,querry,api_key = Config.API_KEY,search_engine_id = Config.SEARCH_ENGINE_ID,  **params):
        base_url = Config.BASE_URL
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": querry,
            **params
        }
        response = httpx.get(base_url, params=params)
        response.raise_for_status()
        return response.json()


    def make_querry(self,content,site,num_of_responses = 30):
        
        querry = content+" "+"site:"+site
        search_res = []
        for i in range(1,num_of_responses,10):
            res = self.__gg_search(querry = querry,start = i)
            search_res.extend(res.get('items', []))
        df = pd.json_normalize(search_res)
        return df
    
class FilterAndSave:
    def __init__(self):
        self.title_clf = joblib.load("model_AI/filter_title/Bayse.pkl")
        self.title_vectorize = joblib.load("model_AI/filter_title/vetorize.pkl")
        self.content_clf = joblib.load("model_AI/filter_content/Bayes.pkl")
        self.content_vectorize = joblib.load("model_AI/filter_content/vectorize.pkl")
        
    def filter_url(self,url):
        try:
            response = requests.get(url, verify = False)
        except:
            return 0
        encoding = response.encoding if response.encoding else 'ISO-8859-1' 
        soup = BeautifulSoup(response.content.decode(encoding), 'html.parser')
        
        title = soup.find('title').text
        title = preprocess_text(title)
        
        title_feature = self.title_vectorize.transform([title])
        title_label = self.title_clf.predict(title_feature)
        if title_label[0] == 0:
            return 0
        paragraphs = soup.find_all('p')
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        article_content = ' '.join([para.text for para in paragraphs])
        heads = ' '.join([head.text for head in headings])
        content = " ".join(article_content.split()) + " " + " ".join(heads.split())
        content = preprocess_text(content)
        content = emphasize_hot_words(content)
        content_feature = self.content_vectorize.transform([content])
        content_label = self.content_clf.predict(content_feature)
        return content_label[0]
    
    def check_file_exists(self,url):
        try:
            response = requests.get(url, timeout=10, verify=False)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')
            list_pdf = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Chuyển đổi URL tương đối sang URL đầy đủ
                full_url = urljoin(url, href)
                if '.pdf' in full_url or '.rar' in full_url or '.zip' in full_url:
                    list_pdf.append(full_url)
            return list_pdf
        except requests.RequestException as e:
            # print(f"Không thể truy cập URL {url}: {e}")    
            return ["0"]   
        
    def get_title(self,url):
        response = requests.get(url, verify = False)
        encoding = response.encoding if response.encoding else 'ISO-8859-1' 
        soup = BeautifulSoup(response.content.decode(encoding), 'html.parser')
        try:
            title = soup.find('title').text
            return title
        except:
            return "no title"
    
    def get_info_url(self,url):
        try:
            if self.filter_url(url) == 0:
                return 
            list_attachs = self.check_file_exists(url)
            return list_attachs
        except:
            return



    

if __name__=="__main__":
    getter = FilterAndSave()
    q = CustomSearch()
    db = DatabaseConnector(server="Admin", database="CrawlDB",username="sa",password="utequyen2372004",use_windows_auth=False)
    db.connect()
    df = pd.read_excel("backend_data/data.xlsx")
    urls = df['Website'].tolist()
    id = df['ID'].tolist()
    for i,url in tqdm(enumerate(urls)):
        try:
            sub_df = q.make_querry(content="tuyển dụng 2024",site=url,num_of_responses=15)
        except:
            continue
        try:
            with Pool(2) as pool:
                res = list(pool.imap(getter.get_info_url,sub_df['link'].tolist()))
        except:
            continue
        # break
        # print(res)
        for index,tmp in enumerate(res):
            id_d = id[index]
            if tmp == None:
                continue
            link = sub_df['link'].tolist()[index]
            attachment = '\n'.join(tmp)
            title = getter.get_title(link)
            db.insert_data('CrawledLinks',domain_id = id_d,crawled_link = link,link_title = title,attachment_url = attachment)
    # print(res)
    
