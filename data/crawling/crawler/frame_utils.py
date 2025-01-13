from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def get_element(driver, classname):
    try:
        return driver.find_element(By.CSS_SELECTOR, classname)
    except NoSuchElementException as e:
        raise ValueError(f"Can't find element '{classname}' : {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error: {e}")