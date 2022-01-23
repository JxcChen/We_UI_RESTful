import os
import platform
import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from public.auto_get_element import auto_get_element

operation = platform.system()
if operation == 'Windows':
    file_path = str(__file__).split("\\")[-3]
else:
    file_path = str(__file__).split("/")[-3]

try:
    from public.HTMLTestRunner import HTMLTestRunner
except:
    exec('from my_client.%s.public.HTMLTestRunner import HTMLTestRunner' % file_path)

try:
    from public.auto_get_element import auto_get_element
except Exception as e:
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
