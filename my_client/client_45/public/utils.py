import os
import platform
import time
import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
operation = platform.system()
if operation == 'Windows':
    file_path = str(__file__).split("\\")[-3]
else:
    file_path = str(__file__).split("/")[-3]

try:
    from public.HTMLTestRunner import HTMLTestRunner
    from public.auto_get_element import auto_get_element
    from public.auto_get_element import auto_get_element
except:
    exec('from my_client.%s.public.HTMLTestRunner import HTMLTestRunner' % file_path)
    exec('from my_client.%s.public.auto_get_element import auto_get_element' % file_path)
    exec("from my_client.%s.public.auto_get_element import *" % file_path)


# 获取测试首页
def util_get_index_page(self, host):
    self.driver.get(host)


# 启动测试并获取报告
def util_run_with_report(self, param: dict):
    base_path = os.path.dirname(os.path.dirname(__file__))
    case_name = param['case_name']
    if operation == 'Windows':
        file_path = base_path + "\\report\\" + case_name + '.html'
    else:
        file_path = base_path + "/report/" + case_name + '.html'

    with open(file_path, 'wb') as f:
        runner = HTMLTestRunner(f, title=case_name + "测试报告",
                                description="用例名称：" + case_name + " 脚本名称：" + param['script_name'], env=param['env'])
        runner.run(unittest.makeSuite(self))


def util_get_ele(self, loc):
    """
    根据定位符获取元素并返回
    """
    return self.driver.find_element(*loc)


def util_click_ele(self, loc):
    util_get_ele(self, loc).click()


def util_send_key(self, loc, value):
    util_get_ele(self, loc).send_keys(value)


def util_switch_to_frame(self, frame_loc):
    """
    切换到对应的iframe  可传入对应frame_element/frame_id/frame_index
    """
    self.driver.switch_to.frame(frame_reference=frame_loc)


def util_switch_to_parent_frame(self, frame_loc):
    """
    切换到对应的iframe  可传入对应frame_element/frame_id/frame_index
    """
    self.driver.switch_to.parent_frame()


def util_switch_to_window(self, tittle):
    """
    切换到对应的window
    """
    handles = webdriver.Chrome().window_handles
    for handle in handles:
        if webdriver.Chrome().title != tittle:
            webdriver.Chrome().switch_to.window(handle)
        else:
            break

def util_wait_element_exist(self, loc):
    """
    显示等待到元素存在
    """
    return WebDriverWait(self.driver, timeout=10).until(
        ec.visibility_of_element_located(loc))



def util_wait_element_clickable(self, loc):
    """
    显示等待到元素可点击
    """
    return WebDriverWait(self.driver, timeout=10).until(
        ec.element_to_be_clickable(loc))

def util_get_element_text(self, loc):
    """
    获取元素文本
    """
    return self.driver.find_element(*loc).text()


def util_get_element_attribute(self, loc, attr_name):
    """
    获取元素属性
    """
    return self.driver.find_element(*loc).get_attribute(attr_name)


# 通过获取定位器接口获取定位器  并进行定位返回元素
def util_get_element(self, loc_id):
    if loc_id == '' or loc_id == ' ' or loc_id is None:
        return None
    res = requests.get("http://127.0.0.1:8000/open_get_locator/%s" % int(loc_id)).json()
    loc = res['tmp_value']
    method = res['tmp_method']
    index = res['index']
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


def util_retry_case(set_up, teardown, retry_num):
    """
    重试方法:
    set_up: 前置方法
    teardown: 后置方法
    retry_num: 重试次数
    """

    def retry_method(case_method):
        def wrapper(*arg, **args):
            for i in range(retry_num):
                try:
                    res = case_method(**args)
                    return res
                except Exception as e:
                    # 执行后置前置
                    teardown(*arg)
                    set_up(*arg)
                    time.sleep(1)
                    if i == retry_num-1:
                        raise e

        return wrapper

    return retry_method
