import os
import re
import shutil
import subprocess
import threading
import time

from django import http
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from uiApp.models import *
from uiApp.serializer import *
from uiApp.utils.return_data import return_json_data
from django.db.models import Q
from uiApp.constant import OPERATION
from uiApp.utils.utils import *


# 项目列表视图
class ProjectListView(APIView):
    # 获取项目列表
    def get(self, request):
        query_data = request.query_params
        user_id = query_data['user_id']
        pro_list = list(DB_pro_user.objects.filter(user_id=user_id).values('pro_id'))
        res_list = []
        for project in pro_list:
            pro = DB_project.objects.get(id=project['pro_id'])
            res_list.append(pro)
        serializer = ProjectSerializer(instance=res_list, many=True)
        res_pro_list = serializer.data
        res_host_list = {}
        # 将路径切割成列表进行返回
        for pro in res_pro_list:
            host_list = pro['host'].split(',')
            res_host_list[str(pro['id'])] = host_list

        res = {
            "res_pro_list": res_pro_list,
            "res_host_list": res_host_list
        }
        return Response(return_json_data(1, '成功', res))

    # 新增项目
    def post(self, request):
        query_data = request.data
        if not query_data['name']:
            return Response(return_json_data(-1, '项目名称不能为空', ''), status=status.HTTP_400_BAD_REQUEST)
        query_data['author_name'] = str(request.user)
        # 先判断数据库中是否已存在同名项目
        is_exit = True if len(DB_project.objects.filter(name=query_data['name'])) > 0 else False
        if is_exit:
            return Response(return_json_data(-2, '该项目已存在', ''), status=status.HTTP_400_BAD_REQUEST)
        else:
            pro = ProjectSerializer(data=query_data)
            # 先将新增的项目落库
            pro.is_valid(raise_exception=True)
            pro_instance = pro.save()
            # 将项目和用户存入中间表
            pro_user = {'pro_id': pro_instance.id, 'user_id': int(pro_instance.author)}
            user_pro = UserProSerializers(data=pro_user)
            user_pro.is_valid(raise_exception=True)
            user_pro.save()
            res_pro = ProjectSerializer(instance=pro_instance).data
            # 创建项目调试包
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            demo_path = os.path.join(base_path, 'my_client/demo_client')

            new_path = os.path.join(base_path, 'my_client/client_' + str(res_pro['id']))
            shutil.copytree(demo_path, new_path)
            return Response(return_json_data(1, '成功', res_pro))


# 项目详情视图
class ProjectDetailView(APIView):
    # 获取项目详情
    def get(self, request, pk):
        projects = DB_project.objects.get(id=pk)
        res_pro = ProjectSerializer(instance=projects).data
        return Response(return_json_data(1, '成功', res_pro), status=status.HTTP_200_OK)

    # 修改项目
    def put(self, request, pk):
        query_data = request.data
        if not query_data['name']:
            return Response(return_json_data(-1, '项目名称不能为空', ''), status=status.HTTP_400_BAD_REQUEST)
        # 先判断 是否已存在相同名称项目
        # is_exit = True if len(DB_project.objects.filter(~Q(id=pk), name=query_data['name'])) else False
        is_exit = DB_project.objects.filter(~Q(id=pk), name=query_data['name']).exists()
        if is_exit:
            return Response(return_json_data(-3, '该项目已存在', ''), status=status.HTTP_400_BAD_REQUEST)
        else:
            # 获取待修改的项目
            old_pro = DB_project.objects.get(id=pk)
            # 使用序列化器进行修改
            pro = ProjectSerializer(data=query_data, instance=old_pro)
            # 检测字段正确性
            pro.is_valid(raise_exception=True)
            # 进行修改
            pro.save()
            new_pro = DB_project.objects.get(id=pk)
            res_pro = ProjectSerializer(instance=new_pro).data
            return Response(return_json_data(1, '修改成功', res_pro), status=status.HTTP_201_CREATED)

    # 删除项目
    def delete(self, request, pk):

        project = DB_project.objects.get(id=pk)
        if request.user.id != 1 and project.author != str(request.user.id):
            return Response(return_json_data(-3, '无权限', ''))
        project.delete()
        DB_pro_user.objects.filter(pro_id=pk).delete()
        return Response(return_json_data(1, '删除成功', ''), status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# 配置协作人员
class ProjectMemberView(APIView):
    # 获取配置人员
    def get(self, request):
        request_params = request.query_params
        pro_id = request_params['project_id']
        # 获取当前项目的协作人员id列表
        users = DB_pro_user.objects.filter(~Q(user_id=request.user.id), pro_id=pro_id).all().values()
        user_list = []
        for s in users:
            user_list.append(s['user_id'])
        return Response(return_json_data(1, "成功", user_list))

    # 配置协作人员
    def post(self, request):
        query_data = request.data
        users = query_data['users']
        project_id = query_data['project_id']
        # 先将原本的数据删除
        DB_pro_user.objects.filter(~Q(user_id=request.user.id), pro_id=project_id).delete()
        for user in users:
            # 更新写作人员列表
            DB_pro_user.objects.create(pro_id=project_id, user_id=user)
        return Response(return_json_data(1, "配置成功", ""))


# 用例列表视图
class CaseListView(APIView):
    # 获取用例列表
    def get(self, request):
        """
        获取项目对应的所有用例
        """
        request_data = request.query_params
        current_page = int(request_data['current_page'])
        page_size = int(request_data['page_size'])
        case_set = DB_case.objects.filter(project_id=request_data['pro_id'])
        cases = case_set[(current_page-1)*page_size:current_page * page_size]
        count = case_set.count()
        res_list = CaseSerializers(instance=cases, many=True).data
        res = {
            'count': count,
            'res_list': res_list
        }
        return Response(return_json_data('1', "成功", res))

    # 新增用例
    def post(self, request):
        """
        新增用例
        """
        request_data = request.data
        request_data['is_thread'] = int(request_data['is_thread'])
        # 获取参数
        name = request_data['name']
        script_name = request_data['script_name']
        if name == '' or name is None:
            return Response(return_json_data(-1, '用例名称不能为空', []), status=status.HTTP_400_BAD_REQUEST)
        if script_name == '' or script_name is None:
            return Response(return_json_data(-1, '用例脚本不能为空', []), status=status.HTTP_400_BAD_REQUEST)
        # 进行序列化
        serializer = CaseSerializers(data=request_data)
        serializer.is_valid(raise_exception=True)
        case_instance = serializer.save()
        case_dict = CaseSerializers(instance=case_instance).data
        return Response(return_json_data(1, '添加成功', case_dict), status=status.HTTP_200_OK)


# 用例详情视图
class CaseDetailView(APIView):
    # 修改用例
    def put(self, request, pro_id):
        """
        修改用例
        """
        request_data = request.data

        request_data['is_thread'] = int(request_data['is_thread'])
        request_data['is_auto_excuse'] = int(request_data['is_auto_excuse'])
        # 获取参数
        name = request_data['name']
        if not name:
            return http.JsonResponse(return_json_data(-1, '用例名称不能为空', ''), status=status.HTTP_400_BAD_REQUEST)
        case = DB_case.objects.get(id=pro_id)
        serializer = CaseSerializers(data=request_data, instance=case)
        serializer.is_valid(raise_exception=True)
        case_instance = serializer.save()
        case = CaseSerializers(instance=case_instance)
        return Response(return_json_data(1, '成功', case.data), status=status.HTTP_201_CREATED)

    # 删除用例
    def delete(self, request, pro_id):
        """
        删除项目
        """
        try:
            DB_case.objects.get(id=pro_id).delete()
        except Exception as e:
            return http.JsonResponse({'code': 0, 'msg': '删除失败'})
        return http.JsonResponse({'code': 1, 'msg': '删除成功'})


# 上传脚本视图
class CaseScriptView(APIView):
    # 上传脚本
    def post(self, request, pro_id):
        query_data = request.data
        script_file = query_data['file']
        if not script_file:
            return Response({'code': 0, 'msg': '未上传脚本'})
        script_name = str(script_file)
        # 将脚本文件放入对应调试包
        with open('my_client/client_%s/case/%s' % (pro_id, script_name), 'wb') as f:
            for content in script_file.chunks():
                f.write(content)
        return Response({'code': 1, 'msg': '上传成功'})


# 执行脚本视图
class CaseExcuseView(APIView):
    # 执行脚本
    def get(self, request, case_id):
        case = DB_case.objects.get(id=case_id)
        pro_id = case.project_id
        case_name = case.name
        script_name = case.script_name
        retry_count = case.retry_count
        host = request.query_params['host']
        # 判断是否已经上传了脚本
        if script_name in ['', ' ', None, 'None']:
            return Response(return_json_data(0, "请先上传脚本", ''))
        # 已上传脚本用例 执行脚本
        # 先判断是脚本文件还是excel文件
        if '.py' in script_name:
            # 根据操作系统执行脚本
            from uiApp.constant import OPERATION
            if OPERATION == "Windows":
                subprocess.call('python my_client/client_%s/case/%s %s %s %s %s' % (
                    pro_id, script_name, host, script_name, case_name, str(retry_count)),
                                shell=True)
            else:
                subprocess.call(
                    'python3 my_client/client_%s/case/%s %s %s %s %s' % (
                        pro_id, script_name, host, script_name, case_name, str(retry_count)),
                    shell=True)
        return Response(return_json_data(1, "执行成功", ''))


# 并发执行用例
class ConcurrentExcuseCaseView(APIView):
    # 并发执行用例
    def get(self, request):
        request_data = request.query_params
        project_id = request_data['project_id']
        host = request.query_params['host']
        # 获取该项目下需要并发执行的用例以及最大并发数
        concurrent_case = DB_case.objects.filter(project_id=project_id, is_thread=1)
        project = DB_project.objects.get(id=project_id)

        # 声明一个线程列表
        threads_pool = []
        # 根据并发的用例来创建多个线程

        for case in concurrent_case:
            # target:指定线程执行的函数  args:传给函数的参数 需要传入元祖
            t = threading.Thread(target=excuse_case, args=(case, project, host))
            # 设置守护线程
            t.setDaemon(True)
            threads_pool.append(t)

        # 遍历执行用例
        max_threads = project.max_threads
        for i in range(0, len(threads_pool), max_threads):
            # 获取最大并发数内的执行线程
            tmp = threads_pool[i:i + max_threads]
            # 遍历执行
            for t in tmp:
                t.start()  # 执行线程

            for t in tmp:
                t.join()
        return Response(return_json_data(1, "执行完成", ""))


# 查看用例报告视图
class CaseReportView(APIView):
    # 查看测试报告
    def get(self, request, case_id):
        case = DB_case.objects.get(id=int(case_id))
        case_name = case.name
        # 返回测试报告路径
        # 先判断用例是否已经执行
        report_path = 'client_%s/report/%s.html' % (case.project_id, case_name)
        if os.path.exists('my_client/' + report_path):
            return render(request, report_path)
        else:
            return Response(return_json_data(3, "用例还未执行", ''))


# 查看报告总结
class CaseReportSummaryView(APIView):
    def get(self, request, pro_id=''):
        # 获取项目对应的全部用例
        pro_name = DB_project.objects.filter(id=pro_id)[0].name
        cases = list(DB_case.objects.filter(project_id=pro_id).values())
        # 声明结果变量
        res = '<h3>【%s项目用例总结】</h3>' % pro_name
        total_case = 0
        pass_case = 0
        fail_case = 0
        # 存放错误用例名称
        fail_case_list = []
        # 遍历用例报告获取总结数据
        for case in cases:
            try:
                with open(r'my_client/client_%s/report/%s.html' % (pro_id, case['name']), 'r', encoding='utf-8') as f:
                    # 读取报告内容
                    content = f.read()
                    # 使用正则匹配结果
                    results = re.findall(r"<td name='sum'>(.*?)</td>", content)
                    total_case += int(results[0])
                    pass_case += int(results[1])
                    fail_or_error = int(results[2]) + int(results[3])
                    fail_case += fail_or_error
                    if fail_or_error > 0:
                        fail_case_list.append(case['name'])
            except FileNotFoundError as e:
                # 如果没找到文件的话表示该用例还未执行  直接跳过即可
                continue
            except Exception as e:
                raise e
        res += "当前总共有【%s】条用例。<br/>通过用例数：%s 失败用例数：%s<br/>" % (str(total_case), str(pass_case), str(fail_case))
        res += "失败用例名称：" + ",".join(fail_case_list) + "<br/>"
        res += "想查看用例结果详情可以点击用例后的报告按钮"
        return Response(return_json_data(1, "获取成功", res))


# 用户列表视图
class UserListView(APIView):
    # 获取用户列表
    def get(self, request):
        user_list = User.objects.all()
        res_list = UserSerializers(instance=user_list, many=True).data
        for res in res_list:
            res.pop('password')
        return Response(return_json_data(1, "成功", res_list), status=status.HTTP_200_OK)

    def post(self, request):
        request_data = request.data
        current_user = request.user.id
        if current_user != '1':
            return Response(return_json_data(-2, "无权限", ''), status=status.HTTP_400_BAD_REQUEST)
        username = request_data['username']
        password = request_data['password']
        if not username:
            return Response(return_json_data(-1, "用户名不能为空", ''))
        if not password:
            return Response(return_json_data(-1, "密码不能为空", ''))
        if len(User.objects.filter(username=username)) > 0:
            return Response(return_json_data(-3, "该用户已存在", ''))
        User.objects.create_user(**request_data)
        return Response(return_json_data(1, "创建成功", ''), status=status.HTTP_201_CREATED)


# 用户详情视图
class UserDetailView(APIView):
    # 获取用户列表
    def put(self, request, user_id):
        request_data = request.data
        current_user = request.user.id
        if current_user != 1 and current_user != int(user_id):
            return Response(return_json_data(-2, "无权限", ''), status=status.HTTP_400_BAD_REQUEST)
        try:
            del request_data['user_type']
            User.objects.filter(id=user_id).update(**request_data)
        except:
            # 进行密码修改
            user = authenticate(username=request.user, password=request_data['old_password'])
            # 如果原密码错误则直接返回
            if not user:
                return Response(return_json_data(-100, "原始密码错误", ''), status=status.HTTP_400_BAD_REQUEST)
            user.set_password(request_data['new_password'])
            user.save()

        return Response(return_json_data(1, "修改成功", ''), status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        if request.user.id != 1:
            return Response(return_json_data(-3, "无权限", ''), status=status.HTTP_200_OK)
        User.objects.filter(id=user_id).delete()
        return Response(return_json_data(1, "创建成功", ''))


# 下载调试包
def download(request, project_id):
    # 1 声明压缩包名称
    zip_file = 'my_client/CLIENT_%s.zip' % project_id
    # 2 对原有的压缩包进行删除
    try:
        os.remove(zip_file)
    except:
        pass
    # 3 调用压缩方法对文件进行压缩
    from uiApp.utils.zip_utils import zip_file_path
    zip_file_path('my_client/client_%s' % project_id, 'my_client', 'CLIENT_%s.zip' % project_id)
    time.sleep(1)
    # 4 封装响应体 将压缩包进行返回
    try:
        file = open(zip_file, 'rb')
    except:
        return Response(return_json_data(3, "未找到对应的调试包", ''))
    response = HttpResponse(file)
    # 设置请求头
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % 'CLIENT_%s.zip' % project_id
    time.sleep(1)
    # 5 删除压缩文件
    try:
        os.remove(zip_file)
    except:
        pass
    # 6 返回响应
    return response


# 上传脚本视图
class UploadUtilsView(APIView):
    # 上传脚本
    def post(self, request, pro_id):
        query_data = request.data
        utils_file = query_data['file']
        if not utils_file:
            return Response(return_json_data(0, '未上传脚本', ''))
        utils_file_name = str(utils_file)
        if '.py' not in utils_file_name:
            return Response(return_json_data(-1, '必须上传python文件', ''), status=status.HTTP_400_BAD_REQUEST)
        # 将工具类放入对应公用包中
        with open('my_client/client_%s/public/%s' % (pro_id, utils_file_name), 'wb') as f:
            for content in utils_file.chunks():
                f.write(content)
        return Response(return_json_data(1, '上传成功', ''), status=status.HTTP_201_CREATED)


# 自动化任务视图
class MonitorView(APIView):
    # 开启自动化任务
    def get(self, request, project_id):
        excuse_time = request.query_params['excuse_time']
        # 先判断监控是否已经开启
        try:
            # 如果没输出则会报错  报错代表未开启监控

            if OPERATION == 'Windows':
                script = 'monitor.py %s WEB ' % project_id
                script_time = script + excuse_time
                res = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline',
                                              shell=True)
                for i in str(res).split(r'\n'):

                    if script_time in i:
                        return Response(return_json_data(0, "自动化任务已开启", ''), status=status.HTTP_200_OK)
                    # 若修改了定时时间 则需要关闭重启
                    if script in i and script_time not in i:
                        # 关闭监控 修改任务时间
                        # 使用正则获取pid
                        pid = re.findall(r'(\d+)', i)[-1]
                        subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)

            else:

                subprocess.check_output(
                    'ps -ef | grep "monitor.py %s WEB" | grep -v grep' % project_id,
                    shell=True)
                try:
                    subprocess.check_output(
                        'ps -ef | grep "monitor.py %s WEB %s" | grep -v grep' % (project_id, excuse_time),
                        shell=True)
                    # 开启则直接返回
                    return Response(return_json_data(0, "自动化任务已开启", ''), status=status.HTTP_200_OK)
                except:
                    # 关闭监控
                    process = subprocess.check_output('ps -ef | grep "monitor.py %s WEB" | grep -v grep' % project_id,
                                                      shell=True)
                    close_monitor_linux(process)

        # 未开启 则调用monitor开启监控
        except:
            pass

        # 开启监控
        def start_monitor():
            if OPERATION == 'Windows':
                subprocess.call('python uiApp/monitor.py %s WEB %s' % (project_id, excuse_time), shell=True)
            else:
                subprocess.call('python3 uiApp/monitor.py %s WEB %s' % (project_id, excuse_time), shell=True)

        monitor_thread = threading.Thread(target=start_monitor)
        # 设置守护线程
        monitor_thread.setDaemon(True)
        # 执行线程
        monitor_thread.start()
        # 更新数据库中项目数据
        DB_project.objects.filter(id=project_id).update(is_auto=1, excuse_time=excuse_time)
        return Response(return_json_data(1, "自动化任务开启成功", ''), status=status.HTTP_200_OK)

    # 关闭自动化任务
    def delete(self, request, project_id):
        pass
        if OPERATION == 'Windows':
            res = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline',
                                          shell=True)
            script = 'monitor.py %s WEB' % project_id
            for i in str(res).split(r'\n'):
                # 若修改了定时时间 则需要关闭重启
                if script in i:
                    # 关闭监控 修改任务时间
                    # 使用正则获取pid
                    pid = re.findall(r'(\d+)', i)[-1]
                    subprocess.call('taskkill /T /F /PID %s' % pid, shell=True)
        else:
            process = subprocess.check_output('ps -ef | grep "monitor.py %s WEB" | grep -v grep' % project_id,
                                              shell=True)
            close_monitor_linux(process)
        # 更新数据库中项目数据
        DB_project.objects.filter(id=project_id).update(is_auto=0)
        return Response(return_json_data(1, "关闭成功", ''), status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# 自动化任务通知列表视图
class NoticeListView(APIView):
    # 新增任务通知
    def post(self, request):
        request_data = request.data
        if request_data['notice_type'] == 1:
            if not request_data['user_list']:
                return Response(return_json_data(-1, '配置人员列表不能为空', ''), status=status.HTTP_400_BAD_REQUEST)
        else:
            if not request_data['webhook']:
                return Response(return_json_data(-1, 'webhook不能为空', ''), status=status.HTTP_400_BAD_REQUEST)
        try:
            # 如果原本已经存在对应项目的通知就删除
            DBNotice.objects.filter(project_id=request_data['project_id']).all().delete()
        except:
            pass
        serializer = NoticeSerializers(data=request_data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        res = NoticeSerializers(instance=instance).data
        return Response(return_json_data(1, '保存成功', res), status=status.HTTP_201_CREATED)


# 自动化任务通知详情视图
class NoticeDetailView(APIView):
    # 获取任务通知详情
    def get(self, request, project_id):
        try:
            notice = DBNotice.objects.get(project_id=project_id)
        except:
            return Response(return_json_data(1, '未创建定时任务', ''), status=status.HTTP_200_OK)
        res = NoticeSerializers(instance=notice).data
        return Response(return_json_data(1, '成功', res), status=status.HTTP_200_OK)


# 页面列表视图
class PageListView(APIView):
    # 获取页面列表
    def get(self, request):
        request_data = request.query_params
        project_id = request_data['project_id']
        page_list = DBPage.objects.filter(project_id=project_id)
        res_list = PageSerializers(instance=page_list, many=True).data
        return Response(return_json_data(1, '成功', res_list), status=status.HTTP_200_OK)

    # 新增页面
    def post(self, request):
        request_data = request.data
        # 判断该页面是否存在
        if DBPage.objects.filter(project_id=request_data['project_id'], name=request_data['name']).exists():
            return Response(return_json_data(-2, '该页面已存在', ''), status=status.HTTP_400_BAD_REQUEST)
        page_serializers = PageSerializers(data=request_data)
        page_serializers.is_valid(raise_exception=True)
        instance = page_serializers.save()
        page_instance = PageSerializers(instance=instance).data
        return Response(return_json_data(1, '创建成功', page_instance), status=status.HTTP_201_CREATED)


# 页面详情试图
class PageDetailView(APIView):
    # 编辑页面
    def put(self, request, page_id):
        request_data = request.data
        try:
            old_page = DBPage.objects.get(id=page_id)
        except:
            return Response(return_json_data(-4, "该页面不存在", ''), status.HTTP_400_BAD_REQUEST)
        page_serializers = PageSerializers(data=request_data, instance=old_page)
        page_serializers.is_valid(raise_exception=True)
        instance = page_serializers.save()
        res = PageSerializers(instance=instance).data
        return Response(return_json_data(1, '修改成功', res), status=status.HTTP_201_CREATED)

    # 删除元素
    def delete(self, request, page_id):
        request_data = request.data
        try:
            old_page = DBPage.objects.get(id=page_id)
        except:
            return Response(return_json_data(-4, "该页面不存在", ''), status.HTTP_400_BAD_REQUEST)
        old_page.delete()
        # 删除页面下所有的元素信息
        # DBElement.objects.filter(page_id=page_id).delete()
        return Response(return_json_data(1, '删除成功', ''), status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# 元素列表视图
class ElementListView(APIView):
    # 获取页面下的元素列表
    def get(self, request):
        request_data = request.query_params
        ele_list = DBElement.objects.filter(page_id=request_data['page_id'])
        res_list = ElementSerializers(instance=ele_list, many=True).data
        return Response(return_json_data(1, '成功', res_list), status=status.HTTP_200_OK)

    # 新增元素
    def post(self, request):
        request_data = request.data
        # 判断该页面是否存在
        if DBElement.objects.filter(page_id=request_data['page_id'], name=request_data['name']).exists():
            return Response(return_json_data(-2, '该元素已存在', ''), status=status.HTTP_400_BAD_REQUEST)
        ele_serializers = ElementSerializers(data=request_data)
        ele_serializers.is_valid(raise_exception=True)
        instance = ele_serializers.save()
        page_instance = ElementSerializers(instance=instance).data
        return Response(return_json_data(1, '创建成功', page_instance), status=status.HTTP_201_CREATED)


# 元素详情试图
class ElementDetailView(APIView):
    # 获取元素详情
    def get(self, request, element_id):
        try:
            ele = DBElement.objects.get(element_id)
        except:
            return Response(return_json_data(-4, '该元素不存在', ''), status=status.HTTP_400_BAD_REQUEST)
        res = ElementSerializers(instance=ele)
        return Response(return_json_data(1, '成功', res), status=status.HTTP_200_OK)

    # 编辑元素
    def put(self, request, element_id):
        request_data = request.data
        try:
            old_ele = DBElement.objects.get(id=element_id)
        except:
            return Response(return_json_data(-4, "该元素不存在", ''), status.HTTP_400_BAD_REQUEST)
        ele_serializers = ElementSerializers(data=request_data, instance=old_ele)
        ele_serializers.is_valid(raise_exception=True)
        instance = ele_serializers.save()
        res = ElementSerializers(instance=instance).data
        return Response(return_json_data(1, '修改成功', res), status=status.HTTP_201_CREATED)

    # 删除元素
    def delete(self, request, element_id):
        try:
            old_ele = DBElement.objects.get(id=element_id)
        except:
            return Response(return_json_data(-4, "该元素不存在", ''), status.HTTP_400_BAD_REQUEST)
        old_ele.delete()
        return Response(return_json_data(1, '删除成功', ''), status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
