import os
import sys

import schedule

path = os.path.dirname(os.path.dirname(__file__))
print(path)
sys.path.append(path)

# 设置环境变量
os.environ['DJANGO_SETTINGS_MODULE'] = 'We_UI.settings'
import django

# 启动django
django.setup()

from uiApp.models import *


# 执行用例
def excuse():
    # 获取到对应项目需要进行监控的用例

    cases = DB_case.objects.filter(project_id=pro_id, is_auto_excuse=1)
    from uiApp.utils.utils import excuse_case
    for case in cases:
        # 执行用例
        excuse_case(case, project)
    print('本轮测试执行完毕')


def monitor():
    excuse()
    # 启动一个无限循环  一直进行监控
    schedule.every(2).minutes.do(excuse)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    pro_id = sys.argv[1]
    project = DB_project.objects.get(id=pro_id)
    monitor()
