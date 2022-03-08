from .baidu.search_page import SearchPage
from selenium import webdriver


class App:
    @staticmethod
    def init_driver():
        driver = webdriver.Chrome()
        return driver

    def start(self):
        driver = self.init_driver()
        driver.implicitly_wait(10)
        return SearchPage(driver)
