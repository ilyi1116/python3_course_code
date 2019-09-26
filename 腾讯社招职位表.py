# encoding = utf-8
import json
import requests
import loguru
import os
import time
import math
from datetime import datetime
from multiprocessing import pool
from pprint import pprint

logger = loguru.logger


def get_position_categories(start_url):
    category_dict = None
    response = requests.get(start_url, timeout=10)
    raw_dict = json.loads(response.text)
    if raw_dict is None or raw_dict == {} or 'Data' not in raw_dict:
        category_dict = None
    else:
        category_dict = raw_dict['Data']
    return category_dict


def get_positions(url):
    response = requests.get(url, timeout=10)
    raw_dict = json.loads(response.text)
    posts = raw_dict['Data']['Posts']
    if posts is None:
        return None
    return {"Positions": posts}


def save_positions(data):
    if data is None:
        return
    if not os.path.exists('./tmp'):
        os.mkdir('./tmp')
    fiel_name = "./tmp/"+time.strftime("%Y%m%d%H%M%S")+".json"
    fp = open(fiel_name, 'w', encoding='utf-8')
    json.dump(data, fp, ensure_ascii=False)
    fp.close()
    logger.info('successfully saved {}'.format(fiel_name))


def crawl(url):
    positions = get_positions(url)
    time.sleep(2)
    #logger.info('saving {}'.format(url))
    save_positions(positions)


if __name__ == "__main__":
    start_url = "https://careers.tencent.com/tencentcareer/api/post/ByCategories?language=zh-cn"
    position_url = "https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={}&countryId=&cityId=&bgIds=&productId=&categoryId={}&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn"
    position_categories = get_position_categories(start_url)
    position_urls = []
    # # 假设每个大类下面有5个小类
    for position_category in position_categories:
        total_pages = math.ceil(int(position_category['PostNumber'])/10)
        total_pages = 5 if total_pages > 5 else total_pages
        categoryId = str(position_category['CategoryId'])
        for i in range(1, total_pages):
            timestamp = int(datetime.now().timestamp()*1000)
            position_urls.append(position_url.format(timestamp, categoryId, i))

        for sub_category in range(1, 6):
            sub_categoryId = categoryId + "00{}".format(sub_category)
            for i in range(1, total_pages % 10 + 1):
                timestamp = int(datetime.now().timestamp()*1000)
                position_urls.append(position_url.format(
                    timestamp, sub_categoryId, i))
    # with open('urls.txt', 'w') as f:
    #     f.write('\n'.join(position_urls))
    pool = pool.Pool()
    pool.map(crawl, position_urls)
