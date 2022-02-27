import os
import platform
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

# 导入utils包
# from my_client.client_10.public.utils import *

if platform.system() == 'Windows':
    file_path = str(__file__).split("\\")[-3]
else:
    file_path = str(__file__).split("/")[-3]

try:
    from public.utils import *
except:
    exec("from my_client.%s.public.utils import *" % file_path)

param = {}
retry_num = 0
try:
    # 获取第二个系统参数
    host = sys.argv[1]
    script_name = sys.argv[2]
    case_name = sys.argv[3]
    retry_num = int(sys.argv[4])
    env = "online"
except:
    # ====================== 本地调试需要手动输入以下内容 ======================
    # ======================       host:调试地址      ======================
    # ====================== script_name:当前脚本文件名称 ====================
    # ======================    case_name:用例名称  =========================
    host = "https://www.baidu.com"
    script_name = "test_demo.py"
    case_name = "本地调试"
    retry_num = 2
    env = "local"
param["script_name"] = script_name
param["case_name"] = case_name
param["env"] = env


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        util_get_index_page(self, host)

    def tearDown(self, method_name='None'):
        if env == 'local':
            picture_name = "../report/picture/%s-%s.png" % (case_name, method_name)
        else:
            picture_name = "uiApp/static/res_picture/%s-%s.png" % (case_name, method_name)
        self.driver.get_screenshot_as_file(picture_name)

    @util_retry_case(setUp, tearDown, retry_num)
    def test_01(self):
        '这里是用例描述'
        search_input = (By.ID, "su")
        self.driver.find_element(*search_input).send_keys("hello world")

    def test_02(self):
        '这里是用例描述'
        search_input = (By.ID, "kw")
        self.driver.find_element(*search_input).send_keys("自动化")


if __name__ == '__main__':
    util_run_with_report(Test, param)
