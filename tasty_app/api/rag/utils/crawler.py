import time
from typing import Dict, List, Union
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from etc.css_path import css_urls
from etc.logger import init_logger


class Crawler:
    def __init__(self) -> None:
        self.reviews = []

        # self.options = webdriver.ChromeOptions()
        # self.options.add_argument("headless")

        self.driver = webdriver.Chrome()
        self.logger = init_logger(__file__, "DEBUG")
    
    
    def __del__(self) -> None:
        try:
            self.driver.close()
        except Exception:
            pass

    
    def get_review(self, place: str) -> Dict[str, str]:
        address = None
        reviews = []

        try:
            self._move_to_link(url=f"https://map.naver.com/p/search/{place}")
            self.logger.info("Searching Place..")
            time.sleep(3)

            try:
                self._switch_frame(frame_name="searchIframe") 
                self._move_to_first_place()
                  
            except NoSuchElementException as e:
                try:
                    self.logger.info(f"Find variable places.. Choice first place: {e}")
                    self._switch_frame(frame_name="entryIframe")

                except NoSuchElementException as e:
                    self.logger.error(f"Can't find first place")
                    return

                except Exception as e:
                    self .logger.error(f"Unexpected Error: {e}")
                    return 

            address = self._parsing_data_with_html("address")
            self._switch_frame(frame_name="entryIframe")

            self.logger.info(f"Parsing review..")
            self.driver.get(self._get_review_url())
            time.sleep(3)
            reviews = self._parsing_data_with_html("reviews")
        
        except Exception as e:
            print(e)         

        return {"name": place, "address": address, "reviews": reviews}


    def _switch_frame(self, frame_name: str):
        try:
            self.driver.switch_to.default_content()
            self.logger.info(f"Success switch frame {frame_name}")
            if frame_name != "root":
                self.driver.switch_to.frame(frame_name)

        except NoSuchFrameException as e:
            self.logger.error(f"Faild switch {frame_name}: {e}")

        except Exception as e:
            self .logger.error(f"Unexpected Error: {e}")


    def _move_to_first_place(self):
        try:
            first_place = self.driver.find_element(By.CSS_SELECTOR, css_urls["first_place_css_none_img"])   

        except NoSuchElementException:
                try:  
                    first_place = self.driver.find_element(By.CSS_SELECTOR, css_urls["first_place_css_img"])

                except NoSuchElementException as e:
                    self.logger.error(f"Can't not find elements: {e}")
                    return 

        except Exception as e:
            self.logger.error(f"Can't not find first place {e}")
            return
        
        first_place.click()
        self.logger.info(f"Success move to first place")
        time.sleep(5)
    

    def _parsing_data_with_html(self, data: str) -> Union[List[str], str]:
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        try:
            if data == "reviews":
                reviews = []
                
                paragraphs = soup.find_all('a')
                for paragraph in paragraphs:
                    reviews.append(paragraph.get_text())
                
                self.logger.info(f"Success parse reviews")

                return reviews
            
            elif data == "address":
                place_element = soup.select_one('#app-root > div > div > div > div:nth-child(5) > div > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(1) > div > a > span:nth-child(1)')
                address = place_element.get_text()
                self.logger.info(f"Success parse address {place_element}")
                return address
            
        except Exception as e:
            self.logger.error(f"Can't parsing data with {data}: {e}")


    def _move_to_link(self, url: str):
        self.driver.get(url)
        time.sleep(3)


    def _get_review_url(self) -> str:
        try:
            review_page = self.driver.find_element(By.CSS_SELECTOR, css_urls["review_link_css_third"])
            if review_page.find_element(By.CSS_SELECTOR, 'span').text != "리뷰":
                review_page = self.driver.find_element(By.CSS_SELECTOR, css_urls["review_link_css_fourth"])
            return review_page.get_attribute('href')
        
        except NoSuchElementException as ne:
            self.logger.error(f"Not found review elements: {ne}")
            
        except Exception as e:
            self.logger.error(f"Unexpected Error: {e}")
        
        
