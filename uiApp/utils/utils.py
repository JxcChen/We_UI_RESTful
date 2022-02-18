import re
import subprocess


def excuse_case(testcase, project, host=''):
    if host == '':
        host = project.auto_host
    from uiApp.constant import OPERATION
    # 先进行非空判断
    if testcase.script_name not in ['', ' ', None, 'None']:
        # 判断是脚本形式还是excel形式用例
        if '.py' in testcase.script_name:
            # 根据操作系统的不同 执行不同命令
            if OPERATION == 'Windows':
                subprocess.call(
                    'python my_client/client_%s/case/%s %s %s %s %s' % (
                        testcase.project_id, testcase.script_name, host, testcase.script_name,
                        testcase.name, str(testcase.retry_count)), shell=True
                )
            else:
                subprocess.call(
                    'python3 my_client/client_%s/case/%s %s %s %s %s' % (
                        testcase.project_id, testcase.script_name, host, testcase.script_name,
                        testcase.name, str(testcase.retry_count)), shell=True
                )
        elif '.xls' in testcase.script:
            if OPERATION == "Windows":
                subprocess.call('python my_client/client_%s/public/xls_to_script.py %s %s %s' % (
                    testcase.pro_id, host, testcase.script_name, testcase.name), shell=True)
            else:
                subprocess.call('python3 my_client/client_%s/public/xls_to_script.py %s %s %s' % (
                    testcase.pro_id, host, testcase.script_name, testcase.name), shell=True)


def close_monitor_linux(process):
    # 使用正则
    pid_list = re.findall(r'(\d+)', str(process))
    pid = max([int(i) for i in pid_list])
    subprocess.call('kill -9 %s' % pid, shell=True)