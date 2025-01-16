from bs4 import BeautifulSoup
from selenium.webdriver import Chrome


def parsing_bs(driver: Chrome):
    reviews = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    paragraphs = soup.find_all('a')
    for paragraph in paragraphs:
        reviews.append(paragraph.get_text())
    return reviews
