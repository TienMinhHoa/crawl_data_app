import os
import joblib
import httpx
import requests
import warnings
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from naive_bayes import preprocess_text
from naive_content import emphasize_hot_words


load_dotenv()
warnings.filterwarnings('ignore')


class CustomSearch:
    API_KEY = os.getenv("API_KEY")
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
    BASE_URL = os.getenv("BASE_URL")
    ROOT_API = os.getenv("ROOT_API")

    def __init__(self):
        pass

    def __gg_search(self,
                    query,
                    **params):
        params = {
            "key": self.API_KEY,
            "cx": self.SEARCH_ENGINE_ID,
            "q": query,
            **params
        }
        response = httpx.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    def make_query(self, content, site, num_of_responses=30):
        query = content + " " + "site:" + site
        search_res = []
        for i in range(1, num_of_responses, 10):
            res = self.__gg_search(query=query, start=i)
            search_res.extend(res.get('items', []))
        df = pd.json_normalize(search_res)
        return df


class FilterAndSave:
    def __init__(self):
        self.title_clf = joblib.load("model_AI/filter_title/Bayse.pkl")
        self.title_vectorize = joblib.load(
            "model_AI/filter_title/vetorize.pkl")
        self.content_clf = joblib.load("model_AI/filter_content/Bayes.pkl")
        self.content_vectorize = joblib.load(
            "model_AI/filter_content/vectorize.pkl")

    def filter_url(self, url):
        try:
            response = requests.get(url, verify=False)
        except Exception:
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
        content = " ".join(article_content.split()) + \
            " " + " ".join(heads.split())
        content = preprocess_text(content)
        content = emphasize_hot_words(content)
        content_feature = self.content_vectorize.transform([content])
        content_label = self.content_clf.predict(content_feature)

        return content_label[0]

    def check_file_exists(self, url):
        try:
            response = requests.get(url, timeout=10, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            list_pdf = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if "https" not in href:
                    full_url = urljoin(url, href)
                else:
                    full_url = href
                if '.pdf' in full_url or \
                    '.rar' in full_url or \
                        '.zip' in full_url:
                    list_pdf.append(full_url)
            return list_pdf
        except requests.RequestException as e:
            print(f"cannot access {url}: {e}")
            return ["0"]

    def get_title(self, url):
        try:
            response = requests.get(url, verify=False)
        except:
            print("cannot access")
            return "no title access"
        encoding = response.encoding if response.encoding else 'ISO-8859-1'
        soup = BeautifulSoup(response.content.decode(encoding), 'html.parser')
        try:
            title = soup.find('title').text
            return title
        except Exception:
            return "no title"

    def get_info_url(self, url):
        try:
            if self.filter_url(url) == 0:
                return
            list_attachs = self.check_file_exists(url)

            return list_attachs
        except Exception as e:
            # print(f"cannot find attach: {e}")
            return
