from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from typing import List
import time


search_box_class = "input_search"
review_tab_class = "tpj9w._tab-menu"
review_div_class = "pui__vn15t2"
 
def open_chrome(url: str) -> webdriver.Chrome:
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    return driver


def search_naver_map(place: str, driver: webdriver.Chrome) -> None:
    try:
        search_box = driver.find_element(By.CLASS_NAME, search_box_class)
    except Exception as e:
        print(f"Wrong place: {e}")
    search_box.send_keys(place)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

#TODO 현재 문제 있는 부분
# driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[3]/div[4]/div[1]/ul/li['+str(i)+']/div[3]/a').send_keys(Keys.ENTER) # 텍스트 전체 볼 수 있게 클릭
# 이렇게 짤 것
def move_to_review(driver: webdriver.Chrome):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '리뷰')]"))
        )
        element.click()
    except Exception as e:
        print(f"리뷰 페이지로 로딩 중 오류 발생 : {e}")


# def crawling_reviews(count: int, driver: webdriver.Chrome) -> List[str]:
#     data = []
#     divs = driver.find_elements(By.CLASS_NAME, review_div_class)
#     for div in divs:
#         data.append(div.text)

#     return data


def get_review_data(area: str, place: str, count: int, url: str) -> List[str]:
    driver = open_chrome(url)
    search_naver_map(f"{area} {place}", driver)
    move_to_review(driver)
    # review_data = crawling_reviews(count, driver)
    # return review_data



if __name__ == "__main__":
    print(get_review_data("구리", "잉꼬칼국수", 5, "https://map.naver.com/"))