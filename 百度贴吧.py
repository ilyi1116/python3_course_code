# encoding  = utf-8
import requests
from bs4 import BeautifulSoup
from multiprocessing import pool
import time
import os
import loguru

logger = loguru.logger


def save_page(html):
    if not os.path.exists('./tmp'):
        os.mkdir('./tmp')
    fiel_name = "./tmp/"+time.strftime("%Y%m%d%H%M%S")+".html"
    with open(fiel_name, 'w', encoding='utf-8') as f:
        f.write(html)


def load_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error('error in load {}'.format(url))
        return None
    return response.text


def crawl(url):
    html = load_page(url)
    if html is None:
        return
    logger.info('saving {}'.format(url))
    save_page(html)


if __name__ == "__main__":
    tieba_name = '李毅'
    page_size = 5
    start_url = 'http://tieba.baidu.com/f?'
    url_list = [
        start_url + "kw={}ie=uyf-8&pn={}".format(tieba_name, i*50) for i in range(page_size)]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    # single 5.2xx
    start = time.time()
    # for url in url_list:
    #     crawl(url)
    # multi 1.2xxx
    pool = pool.Pool()
    pool.map(crawl, url_list)
    print(time.time()-start)
