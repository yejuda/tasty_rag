from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
xpaths_file_path = os.path.join(current_dir, 'xpaths.json')

with open(xpaths_file_path, 'r') as file:
    xpaths = json.load(file)


def get_element(driver: Chrome, classname):
    try:
        if classname in xpaths.keys():
            return driver.find_element(By.CSS_SELECTOR, xpaths[classname])
        return None
    except NoSuchElementException:
        return None

def move_to_link(driver: Chrome, url: str):
    driver.get(url)
    time.sleep(3)


def is_first_place(driver: Chrome):
    first_place = get_element(driver=driver, classname="first_place_css_none_img")
    if not first_place:
        first_place = get_element(driver=driver, classname="first_place_css_img")
    if first_place:
        return first_place
    else:
        return None


def move_to_first_place(driver: Chrome):
    first_place = is_first_place(driver)
    if first_place:
        first_place.click()
        time.sleep(5)


def get_review_url(driver: Chrome) -> str:
    review_page = get_element(driver, "review_link_css_third")
    if not review_page:
        return None
    if review_page.find_element(By.CSS_SELECTOR, 'span').text != "리뷰":
        review_page =  get_element(driver, "review_link_css_fourth")
    return review_page.get_attribute('href')
    


#TODO 더 많은 리뷰를 가져오게 리뷰 페이지 열기
# def open_review_page(driver: Chrome):
#     more_btn = get_element(driver, more_css)
#     print(more_btn.text)
#     more_btn.click()
#     time.sleep(5)

