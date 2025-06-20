from bs4 import BeautifulSoup
from selenium.webdriver import Chrome


def parsing_bs_review(driver: Chrome):
    reviews = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    paragraphs = soup.find_all('a')
    for paragraph in paragraphs:
        reviews.append(paragraph.get_text())
    return reviews



def parsing_bs_address(driver: Chrome):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    place_element = soup.select_one('#app-root > div > div > div > div:nth-child(5) > div > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div > a > span:nth-child(1)')
    return place_element.get_text()