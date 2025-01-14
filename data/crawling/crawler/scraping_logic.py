from selenium import webdriver
import time

from .frame_utils import switch_frame
from .element_utils import get_element, get_review, move_to_link


def search_place(place: str):
    driver = webdriver.Chrome()
    try:
        move_to_link(driver=driver, url=f"https://map.naver.com/p/search/{place}")
        switch_frame(driver=driver, frame_name="searchIframe")
    
        reviews = get_review(driver=driver)
    
    except ValueError:
        first_place = get_element(driver=driver, classname=".Ryr1F > ul > .UEzoS.rTjJo > .CHC5F > a")
        first_place.click()
        time.sleep(5)

        switch_frame(driver=driver, frame_name="root")
        switch_frame(driver=driver, frame_name="entryIframe")
        
        reviews = get_review(driver=driver)
        
    except Exception as e:
        print(e)

    finally:
        driver.close()

    return reviews


if __name__ == "__main__":
    print(search_place("스타벅스"))
    print(search_place("잉꼬칼국수"))