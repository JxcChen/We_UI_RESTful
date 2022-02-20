import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import schedule


path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)

# 设置环境变量
os.environ['DJANGO_SETTINGS_MODULE'] = 'We_UI.settings'
import django

# 启动django
django.setup()

from uiApp.models import *


def send_report_email(receive_list):
    from uiApp.views import CaseReportSummaryView
    # 通过view中方法获取报告总结
    case_view = CaseReportSummaryView()
    report_content = case_view.get({}, pro_id=pro_id).data['data']
    # 声明邮件信息
    mail_send = "360088940@qq.com"
    mail_receive = ""
    # 拼接收件人
    for receive in receive_list:
        mail_receive += receive['email'] + ','
    # 去除末尾逗号
    receive_list.pop(-1)
    mail_host = "smtp.qq.com"  # 声明发送服务器名称
    mail_secret = "wjotabdwqkilcaei"
    # 声明邮件格式
    text = MIMEText(report_content, "html", 'utf-8')
    msg = MIMEMultipart('related')
    msg['From'] = mail_send
    msg['To'] = mail_receive
    msg['Subject'] = '%s项目 UI自动化测试报告' % project.name
    msg.attach(text)  # 设置邮件装载
    try:
        # 获取邮件服务
        server = smtplib.SMTP()
        # 设置服务名称、发件人和收件人信息
        server.connect(mail_host)
        server.login(mail_send, mail_secret)
        server.sendmail(mail_send, mail_receive.split(','), msg.as_string())
        print("邮件发送成功")
        server.close()
    except Exception as e:
        print("邮件发送失败")
        raise e


# 执行用例
def excuse():
    # 获取到对应项目需要进行监控的用例

    cases = DB_case.objects.filter(project_id=pro_id, is_auto_excuse=1)
    from uiApp.utils.utils import excuse_case
    for case in cases:
        # 执行用例
        excuse_case(case, project)
    print('本轮测试执行完毕')
    try:
        # 当项目有配置任务通知时 发送通知
        print(pro_id)
        notice = DBNotice.objects.get(project_id=pro_id)
        if notice.notice_type == 1:
            user_list = notice.user_list.split(',')
            for i in range(len(user_list)):
                user_list[i] = int(user_list[i])

            from django.contrib.auth.models import User
            # id__in=user_list ==> in in (1,2,3)
            # values('email') 取出values字段  格式 [{'email':""},{'email':""}]
            # values_list('email') 取出values字段  格式 [("",),("",)]
            email_list = list(User.objects.filter(id__in=user_list).values('email'))
            # 邮件发送报告
            send_report_email(email_list)
        else:
            # 企微发送报告
            pass
    except Exception as e:
        # 没有配置通知则无需进行通知发送
        raise e
        pass


def monitor():
    # 启动一个无限循环  一直进行监控
    schedule.every().day.at(excuse_time).do(excuse)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    pro_id = sys.argv[1]
    excuse_time = sys.argv[3]
    project = DB_project.objects.get(id=pro_id)
    monitor()
