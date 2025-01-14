from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


review_link_css = "#app-root > div > div > div > div:nth-child(4) > div > div > div.flicking-viewport > div.flicking-camera"
review_css = "#app-root > div > div > div > div:nth-child(6) > div:nth-child(3) > div:nth-child(3) > div > ul"

def get_element(driver: Chrome, classname):
    try:
        return driver.find_element(By.CSS_SELECTOR, classname)
    except NoSuchElementException as e:
        raise ValueError(f"Can't find element '{classname}', {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error, {e}")
    

def move_to_link(driver: Chrome, url: str):
    try:
        driver.get(url)
        time.sleep(3)
    except Exception as e:
        raise RuntimeError(f"An unexpected error, {e}")
    

def get_review(driver: Chrome):
    try:
        review_page = driver.find_element(By.CSS_SELECTOR, f"{review_link_css} > a:nth-child(3)")
        if review_page.find_element(By.CSS_SELECTOR, 'span').text != "리뷰":
            review_page = driver.find_element(By.CSS_SELECTOR, f"{review_link_css} > a:nth-child(4)")
        driver.get(review_page.get_attribute('href'))
        time.sleep(5)

        element = driver.find_element(By.CSS_SELECTOR, review_css)

        return element.text
    
    except NoSuchElementException as e:
        raise ValueError(f"Can't loading review page, {e}")
    
    except Exception as e:
        raise RuntimeError(f"An unexpected error, {e}")
