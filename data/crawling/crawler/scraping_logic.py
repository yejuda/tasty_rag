from selenium import webdriver
import time

from .frame_utils import switch_frame
from .element_utils import get_review_url, move_to_link, move_to_first_place
from .bs_utils import parsing_bs_address, parsing_bs_review

first_place_css = "#_pcmap_list_scroll_container > ul > li:nth-child(1) > div:nth-child(1) > a > div > div > span"


def get_review(place: str):
    driver = webdriver.Chrome()
    move_to_link(driver=driver, url=f"https://map.naver.com/p/search/{place}")
    time.sleep(3)

    try:
        switch_frame(driver=driver, frame_name="searchIframe")
        move_to_first_place(driver)
        address = parsing_bs_address(driver)
        switch_frame(driver=driver, frame_name="entryIframe")   
    except:
        switch_frame(driver=driver, frame_name="entryIframe")
        address = parsing_bs_address(driver)
    finally:
        driver.get(get_review_url(driver))
        time.sleep(3)
        reviews = parsing_bs_review(driver)
    driver.close()

    return reviews, address


if __name__ == "__main__":
    places = [
        "부엉이산장",
        "카페베베",
        "리얼파스타",
        "청록미나리식당",
        '미성식당찌개',
        '대접육류',
        '구들장왕돌판삼겹살',
        '잉꼬칼국수',
        '아쎄커 유쎄피카페',
        "로디어카페",
        "아띠카페카페"
    ]
    result = {}
    for place in places[:3]:
        result[place] = get_review(place)
    print(result)