import os
import platform
import re
import sys
import time
import unittest

# 导入utils包
# from my_client.client_10.public.utils import *

if platform.system() == 'Windows':
    file_path = str(__file__).split("\\")[-3]
else:
    file_path = str(__file__).split("/")[-3]

try:
    from public.utils import *
    from page.baidu.search_page import SearchPage
    from page.app_start import App
except:
    exec("from my_client.%s.public.utils import *" % file_path)
    exec("from my_client.%s.page.baidu.search_page import *" % file_path)
    exec("from my_client.%s.page.app_start import App" % file_path)


class Test(unittest.TestCase):
    search = App().start()
    retry_num = 0
    @classmethod
    def tearDownClass(cls):
        cls.search.driver.quit()

    def setUp(self):
        self.search.get_index_page(host)

    def tearDown(self, method_name='None'):
        if env == 'local':
            picture_name = "../report/picture/%s-%s.png" % (case_name, method_name)
        else:
            picture_name = "uiApp/static/res_picture/%s-%s.png" % (case_name, method_name)
        self.search.get_screenshot(picture_name)

    # @util_retry_case(setUp, tearDown, retry_num)
    def test_01(self):
        '这里是用例描述'
        self.search.search_key('pageObject')
        time.sleep(10)

    # def test_02(self):
    #     '这里是用例描述'
    #     self.search.search_key2('pageObject2222')
    #     time.sleep(10)


if __name__ == '__main__':
    param = {}
    retry_num = 0
    try:
        # 获取第二个系统参数
        host = sys.argv[1]
        script_name = sys.argv[2]
        case_name = sys.argv[3]
        Test.retry_num = int(sys.argv[4])
        env = "online"
    except Exception as e:
        raise e
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

    util_run_with_report(Test, param)
