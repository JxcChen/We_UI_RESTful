from selenium import webdriver
from .default_page import DefaultPage


class App:
    @staticmethod
    def init_driver():
        driver = webdriver.Chrome()
        return driver

    def start(self):
        driver = self.init_driver()
        driver.implicitly_wait(10)
        return DefaultPage(driver)
