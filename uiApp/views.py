import os
import shutil
import subprocess

from django import http

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from uiApp.models import *
from uiApp.serializer import *
from uiApp.utils.return_data import return_json_data
from django.db.models import Q


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
        # 先判断数据库中是否已存在同名项目
        is_exit = True if len(DB_project.objects.filter(name=query_data['name'])) > 0 else False
        if is_exit:
            return Response(return_json_data(3, '该项目已存在', ''), status=status.HTTP_200_OK)
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
            print(res_pro)
            new_path = os.path.join(base_path, 'my_client/client_' + str(res_pro['id']))
            shutil.copytree(demo_path, new_path)
            return Response(return_json_data(1, '成功', res_pro))


class ProjectDetailView(APIView):
    # 修改项目
    def put(self, request, pk):
        query_data = request.data
        # 先判断 是否已存在相同名称项目
        is_exit = True if len(DB_project.objects.filter(~Q(id=pk), name=query_data['name'])) else False
        if is_exit:
            return Response(return_json_data(3, '该项目已存在', ''), status=status.HTTP_200_OK)
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
        DB_project.objects.get(id=pk).delete()
        DB_pro_user.objects.get(pro_id=pk).delete()
        return Response(return_json_data(1, '删除成功', ''), status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class CaseListView(APIView):
    # 获取用例列表
    def get(self, request):
        """
        获取项目对应的所有用例
        """
        request_data = request.query_params
        cases = DB_case.objects.filter(project_id=request_data['pro_id']).all()
        res_list = CaseSerializers(instance=cases, many=True).data
        return Response(return_json_data('1', "成功", res_list))

    # 新增用例
    def post(self, request):
        """
        新增用例
        """
        request_data = request.data
        print(request_data)
        request_data['is_thread'] = int(request_data['is_thread'])
        # 获取参数
        name = request_data['name']
        if name == '' or name is None:
            return Response(return_json_data(0, '用例名称不能为空', []))
        # 进行序列化
        serializer = CaseSerializers(data=request_data)
        serializer.is_valid(raise_exception=True)
        case_instance = serializer.save()
        case_dict = CaseSerializers(instance=case_instance).data
        return Response(return_json_data(1, '添加成功', case_dict), status=status.HTTP_200_OK)


class CaseDetailView(APIView):
    # 修改用例
    def put(self, request, pro_id):
        """
        修改用例
        """
        requestData = request.data
        requestData['is_thread'] = int(requestData['is_thread'])
        # 获取参数
        name = requestData['name']
        if not name:
            return http.JsonResponse({'code': 0, 'msg': '用例名称不能为空', 'case': {}})
        case = DB_case.objects.get(id=pro_id)
        serializer = CaseSerializers(data=requestData, instance=case)
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
            print(OPERATION)
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
