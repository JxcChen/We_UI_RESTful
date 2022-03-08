from selenium import webdriver

from .base_page import BasePage


class DefaultPage(BasePage):
    # 登录
    def login(self, account, pwd):
        pwd_btn = self.open_get_element(10)
        pwd_btn.click()
        account_input = self.open_get_element(11)
        account_input.send_keys(account)
        pwd_input = self.open_get_element(12)
        pwd_input.send_keys(pwd)
