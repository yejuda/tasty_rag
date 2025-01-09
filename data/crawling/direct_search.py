from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)


def switch_frame():
    try:
        iframe_element = wait.until(EC.visibility_of_element_located((By.ID, "entryIframe")))
        driver.switch_to.frame(iframe_element)
    except Exception as e:
        raise f"프레임을 변경할 수 없습니다: {e}"


def move_to_review():
    try:
        review_page = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app-root > div > div > div > div:nth-child(4) > div > div > div.flicking-viewport > div.flicking-camera > a:nth-child(4)")))
        driver.get(review_page.get_attribute('href'))
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app-root > div > div > div > div:nth-child(6) > div:nth-child(3) > div:nth-child(3) > div > ul")))
    except Exception as e:
        raise f"리뷰 페이지로 이동 실패했습니다: {e}" 
    return element.text


def get_restaurant_directly(place: str) -> str:
    url = f"https://map.naver.com/p/search/{place}"
    
    driver.get(url)
    try:
        switch_frame()
        text = move_to_review()
    except Exception as e:
        raise e
    driver.close()
    return text


if __name__ == "__main__":
    print(get_restaurant_directly("잉꼬칼국수"))