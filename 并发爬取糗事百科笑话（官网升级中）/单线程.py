# encoding  = utf-8
import requests
from bs4 import BeautifulSoup
from multiprocessing import pool
import time
import os
import json
import loguru
import re

logger = loguru.logger
local_fp = open('qsbk_single.json', 'a', encoding='utf-8')


def get_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    html = response.text
    return html


def parse_page(html):
    if html is None:
        return
    soup = BeautifulSoup(html, 'lxml')
    box = soup.find('div', id="footzoon")
    title_list = box.find_all('h3')
    content_list = box.find_all('div', id='endtext')
    date_click_list = box.text.strip().split('糗事百科')[1:]

    for title, content, date_click in zip(title_list, content_list, date_click_list):
        joke = dict()
        joke['title'], joke['content'] = title.text.strip(), content.text.strip()
        try:
            joke['date'] = date_click.split()[0]+date_click.split()[1]
            joke['click'] = re.match(
                r"Click:(\d+).*?", date_click.split()[2]).group(1)
        except Exception as e:
            continue
        local_fp.write(json.dumps(joke))
        local_fp.write('\n')


def main():
    url = "http://www.lovehhy.net/Joke/Detail/QSBK/{}"
    for i in range(1, 5):
        html = get_page(url.format(i))
        parse_page(html)
        time.sleep(1)
    local_fp.close()


if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time()-start)