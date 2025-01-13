'''
1. Selenium으로 원하는 리뷰 페이지 이동
2. bs4로 현재 리뷰 내용들 가져오기
'''

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from data.crawling.crawler.function import switch_frame, get_element
from bs4 import BeautifulSoup
import time

options = ChromeOptions()
# options.add_argument('--headless')

driver = webdriver.Chrome(options=options)

def search_place(place: str):
    url = f"https://map.naver.com/p/search/{place}"
    driver.get(url)
    time.sleep(5)
    switch_frame(driver=driver, frame_name="searchIframe")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()
    return soup
    # tmp = get_element(driver=driver, classname=".place_on_pcmap")
    # return tmp


if __name__ == "__main__":
    print(search_place("스타벅스"))