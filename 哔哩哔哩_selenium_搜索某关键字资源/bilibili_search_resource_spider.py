# encoding = utf-8
import time
import json
from config import *
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC

# browser = webdriver.Chrome()
# 设置无头模式
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)


wait = WebDriverWait(browser, TIMEOUT)
fp = open('result.json', 'w', encoding='utf-8')


def get_page(keyword):
    browser.get("https://search.bilibili.com/")
    input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#search-keyword")))
    submit = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#server-search-app > div > div > div.home-input.clearfix > a")))
    input.send_keys(keyword)
    submit.click()

    try:
        last_page = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last")))
        return last_page.text.strip()
    except TimeoutError:
        print("获取全部页码元素等待超时,尝试再次获取...")
        time.sleep(2)
        return get_page(keyword)


def next_page():
    next_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.next > button")))
    next_button.click()


def parse_page():
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#all-list > div.flow-loader > div.mixin-list > ul")))
    html = browser.page_source
    # with open('local.html', 'w', encoding='utf-8') as f:
    #     f.write(html)
    doc = pq(html)
    items = doc("#all-list .flow-loader .mixin-list li").items()

    for item in items:
        video = {
            "title": item.find(".info .title").attr('title'),
            "href": item.find(".info .title").attr('href'),
            "play": item.find(".info span.so-icon.watch-num").text(),
            "date": item.find(".info .so-icon.time").text(),
            "author": item.find(".info .up-name").text()
        }
        save_to_local(video)


def save_to_local(obj):
    fp.write(json.dumps(obj))
    fp.write('\n')
    fp.flush()


def main():
    keyword = KEYWORD
    try:
        last_page = int(get_page(keyword))
    except ValueError:
        print("ValueError: int(get_page(keyword))")
        return
    if last_page < 0:
        print("数据不正确")
        return
    parse_page()
    # for page_num in range(2, last_page):
    #     time.sleep(1)
    #     next_page()
    #     parse_page()
    fp.close()


if __name__ == "__main__":
    main()
