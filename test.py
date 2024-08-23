import requests
from bs4 import BeautifulSoup
import os

def get_article_content(url):
    try:
        response = requests.get(url, verify = False)
        encoding = response.encoding if response.encoding else 'ISO-8859-1' 
        soup = BeautifulSoup(response.content.decode(encoding), 'html.parser')
        paragraphs = soup.find_all('p')
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        # title = soup.find('title').text

        # Lấy văn bản từ các thẻ
        article_content = ' '.join([para.text for para in paragraphs])
        heads = ' '.join([head.text for head in headings])
        # print("############################")
        
        if not os.path.exists("data_ai_content"):
            os.mkdir("data_ai_content")
        article_content = " ".join(article_content.split())
        heads = " ".join(heads.split())
        # print(article_content)
        # with open(f"data_ai_content/{str(len(os.listdir('data_ai_content')))}.txt","a",encoding = 'utf8') as file:
        #     file.write(article_content)
        return heads+" "+article_content
    except:
        return url
def get_title(url):
    try:
        response = requests.get(url, verify = False)
        encoding = response.encoding if response.encoding else 'ISO-8859-1' 
        soup = BeautifulSoup(response.content.decode(encoding), 'html.parser')
        title = soup.find_all('title').text
        return title
    except:
        return "Not relevant"
# Ví dụ sử dụng
# url = "https://moha.gov.vn/thong-bao/ke-hoach-so-1728kh-bnv-ngay-2932024-cua-bo-noi-vu-thuc-hien-cong-tac-phong-chong-tham-nhung-tieu-cuc-nam-2024-1907.html"
# content = get_article_content(url)
# print(content.strip())
# print(title.strip())

# from multiprocessing import Pool
# from tqdm import tqdm
# import pandas as pd
# import warnings
# warnings.filterwarnings("ignore")

# if __name__=='__main__':
#     df = pd.read_csv("Save_info/2024/8/20/main_version_0.csv")

#     link = df['link'].tolist()

#     with Pool(max(os.cpu_count()-2,1)) as pool:
#         a = list(tqdm(pool.imap(get_article_content,link),total = len(link)))
#     # print(a)
#     for item in tqdm(a):

#         with open(f"data_ai_content/{str(len(os.listdir('data_ai_content')))}.txt","a",encoding = 'utf8') as file:
#             file.write(item)
