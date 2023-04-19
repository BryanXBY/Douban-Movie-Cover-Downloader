import os
import importlib
import subprocess
import requests
from urllib.parse import urljoin

def check_module(module_name):
    loader = importlib.find_loader(module_name)
    if loader is None:
        print(f"{module_name}模块未安装，正在为您安装...")
        subprocess.call(['pip', 'install', module_name])
        print(f"{module_name}模块安装成功")
    else:
        print(f"{module_name}模块已安装")

def download_covers():
    url = "https://movie.douban.com/j/search_subjects"
    params = {
        "type": "movie",
        "tag": "热门",
        "sort": "recommend",
        "page_limit": "20",
        "page_start": "0"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        raise Exception("电影请求出错")
    movies = response.json()["subjects"]
    for movie in movies:
        cover_url = movie["cover"]
        cover_name = f"{movie['title']}.jpg".replace('/', '-')
        cover_path = os.path.join(os.path.dirname(__file__), 'douban', 'covers', cover_name)
        if not os.path.exists(os.path.dirname(cover_path)):
            os.makedirs(os.path.dirname(cover_path))
        response = requests.get(cover_url)
        with open(cover_path, 'wb') as f:
            f.write(response.content)
        print(f"已下载封面：{os.path.abspath(cover_path)}")

if __name__ == '__main__':
    download_covers()
