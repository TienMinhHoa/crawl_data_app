import requests
from bs4 import BeautifulSoup
import chardet

def get_article_content(url):
    # try:
    # Gửi yêu cầu HTTP đến URL
    response = requests.get(url, verify = False)
    print(response.encoding)
    # response.encoding = 'iso-8859-1'
    # response.raise_for_status()  # Kiểm tra nếu yêu cầu thành công
    encoding = response.encoding if response.encoding else 'ISO-8859-1' 
    print(encoding)
    # Phân tích cú pháp HTML của trang web
    soup = BeautifulSoup(response.content.decode(encoding), 'html.parser')

    # Tìm các thẻ chứa nội dung bài viết
    # Bạn có thể cần thay đổi thẻ và lớp tùy theo cấu trúc của trang web cụ thể
    paragraphs = soup.find_all('p')
    title = soup.find('title').text

    # Lấy văn bản từ các thẻ
    article_content = ' '.join([para.text for para in paragraphs])
    # byte_string = article_content.encode("iso-8859-1")
    # decoded_string = byte_string.decode('iso-8859-1', errors='replace')
    return article_content,paragraphs,title
    # except requests.exceptions.RequestException as e:
    #     print(f"Error fetching {url}: {e}")
    #     return None

# Ví dụ sử dụng
url = "https://thads.moj.gov.vn/noidung/thongbao/Pages/tbbc.aspx"
content,paras,title = get_article_content(url)
print(title)
