from bs4 import BeautifulSoup


def parsing_bs(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup