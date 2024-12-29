from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

def crawling_review(place: str):
    url = f"https://map.naver.com/p/search/{place}"
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 5)

    try:
        iframe_element = wait.until(EC.visibility_of_element_located((By.ID, "entryIframe")))

        driver.switch_to.frame(iframe_element)
    except Exception as e:
        print(f"Frame Switch Error: {e}")

    try:
        review_page = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app-root > div > div > div > div:nth-child(4) > div > div > div.flicking-viewport > div.flicking-camera > a:nth-child(4)")))
        driver.get(review_page.get_attribute('href'))
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app-root > div > div > div > div:nth-child(6) > div:nth-child(3) > div:nth-child(3) > div > ul")))
        result = element.text
    except Exception as e:
        print("리뷰 페이지로 이동 실패:", e)
    
    driver.close()
    return result


if __name__ == "__main__":
    print(solution("잉꼬칼국수"))