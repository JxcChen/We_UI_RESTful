import requests
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

try:
    from public.HTMLTestRunner import HTMLTestRunner
    from public.auto_get_element import auto_get_element
except:
    exec('from my_client.%s.public.HTMLTestRunner import HTMLTestRunner' % file_path)
    exec('from my_client.%s.public.auto_get_element import auto_get_element' % file_path)


class BasePage:

    def __init__(self, driver: Chrome):
        self.driver = driver
        self.current_element = None

    # 获取测试首页
    def get_index_page(self, host):
        self.driver.get(host)

    def get_element(self, loc):
        """
        根据定位符获取元素并返回
        """
        return self.driver.find_element(*loc)

    def click_ele(self, loc):
        self.get_element(self, loc).click()

    def util_send_key(self, loc, value):
        self.get_element(self, loc).send_keys(value)

    def switch_to_frame(self, frame_loc):
        """
        切换到对应的iframe  可传入对应frame_element/frame_id/frame_index
        """
        self.driver.switch_to.frame(frame_reference=frame_loc)

    def switch_to_parent_frame(self, frame_loc):
        """
        切换到对应的iframe  可传入对应frame_element/frame_id/frame_index
        """
        self.driver.switch_to.parent_frame()

    def switch_to_window(self, tittle):
        """
        切换到对应的window
        """
        handles = self.driver.window_handles
        for handle in handles:
            if self.driver.title != tittle:
                self.driver.switch_to.window(handle)
            else:
                break

    def wait_element_exist(self, loc):
        """
        显示等待到元素存在
        """
        return WebDriverWait(self.driver, timeout=10).until(
            ec.visibility_of_element_located(loc))

    def wait_element_clickable(self, loc):
        """
        显示等待到元素可点击
        """
        return WebDriverWait(self.driver, timeout=10).until(
            ec.element_to_be_clickable(loc))

    def get_element_text(self, loc):
        """
        获取元素文本
        """
        text = self.driver.find_element(*loc).get_attribute('innerText')
        return text

    def get_element_attribute(self, loc, attr_name):
        """
        获取元素属性
        """
        return self.driver.find_element(*loc).get_attribute(attr_name)

    # 通过获取定位器接口获取定位器  并进行定位返回元素
    @staticmethod
    def util_get_element(self, loc_id):
        if loc_id == '' or loc_id == ' ' or loc_id is None:
            return None
        res = requests.get("http://127.0.0.1:8001/api/open_get_element/%s/" % int(loc_id)).json()
        data = res['data']
        loc = data['element_location']
        method = data['loc_method']
        index = data['index']
        locator = ()
        if 'id' == method:
            locator = (By.ID, loc)
        elif 'name' == method:
            locator = (By.NAME, loc)
        elif 'css' == method:
            locator = (By.CSS_SELECTOR, loc)
        elif 'xpath' == method:
            locator = (By.XPATH, loc)
        elif 'tag' in method:
            locator = (By.TAG_NAME, loc)
        try:
            ele = self.driver.find_elements(*locator)[index]
        except Exception as e:
            ele = auto_get_element(self.driver, res)
        return ele
