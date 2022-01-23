import json
import os
import shutil

from django import http
from django.shortcuts import render
from django.views import View

from uiApp.models import *


# Create your views here.

def login(request):
    requestData = json.loads(request.body.decode())
    username = requestData['username']
    password = requestData['password']
    if not username:
        return http.JsonResponse({'code': 2, 'msg': '用户名不能为空'})
    if not password:
        return http.JsonResponse({'code': 2, 'msg': '密码不能为空'})
    count = DB_tester.objects.filter(username=username,password=password).count()
    if count == 0:
        return http.JsonResponse({'code': 0, 'msg': '用户名或密码错误'})
    else:
        # 生成token
        pass

class ProjectInfoView(View):

    def get(self, request):
        """
        获取项目列表
        """
        author = request.GET.get('author')
        if author == '' or author is None:
            projects = DB_project.objects.all()
        else:
            projects = DB_project.objects.filter(author=author).all()
        pro_list = []
        for project in projects:
            pro_dict = {
                "id": project.id,
                "name": project.name,
                "author": project.author,
                'host': project.host,
                'max_threads': project.max_threads,
                'auto_host': project.auto_host
            }
            pro_list.append(pro_dict)
        return http.JsonResponse({'code': 1, 'msg': '成功', 'pro_list': pro_list})

    def post(self, request):
        """
        添加项目
        """
        requestData = json.loads(request.body.decode())
        # 获取参数
        name = requestData['name']
        host = requestData['host']
        author = requestData['author']

        # 校验参数
        if name == '' or name is None:
            return http.JsonResponse({'code': 0, 'msg': '项目名称不能为空', 'project': {}})
        if host == '' or host is None:
            return http.JsonResponse({'code': 0, 'msg': '项目路径不能为空', 'project': {}})
        if author == '' or author is None:
            requestData['author'] = 'admin'
            # return http.JsonResponse({'code': 0, 'msg': '负责人不能为空', 'project': {}})
        # 数据落库
        project = DB_project.objects.create(**requestData)
        # 创建项目调试包
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        demo_path = os.path.join(base_path, 'my_client/demo_client')
        new_path = os.path.join(base_path, 'my_client/client_' + str(project.id))
        shutil.copytree(demo_path, new_path)
        # 返回响应
        project_dict = {
            "id": project.id,
            "name": project.name,
            "author": project.author,
            'host': project.host,
            'max_threads': project.max_threads
        }
        return http.JsonResponse({'code': 1, 'msg': '添加成功', 'project': project_dict})

    def put(self, request, pro_id):
        """
        编辑项目
        """
        requestData = json.loads(request.body.decode())
        # 获取参数
        name = requestData['name']
        host = requestData['host']
        author = requestData['author']
        # 校验参数
        if name == '' or name is None:
            return http.JsonResponse({'code': 0, 'msg': '项目名称不能为空', 'project': {}})
        if host == '' or host is None:
            return http.JsonResponse({'code': 0, 'msg': '项目路径不能为空', 'project': {}})
        if author == '' or author is None:
            requestData['author'] = 'admin'
            # return http.JsonResponse({'code': 0, 'msg': '负责人不能为空', 'project': {}})
        # 数据落库
        try:
            DB_project.objects.filter(id=pro_id).update(**requestData)
        except:
            return http.JsonResponse({'code': 1, 'msg': '该项目不存在', 'project': ''})
        project = DB_project.objects.get(id=pro_id)
        # 返回响应
        project_dict = {
            "id": project.id,
            "name": project.name,
            "author": project.author,
            'host': project.host,
            'max_threads': project.max_threads
        }
        return http.JsonResponse({'code': 1, 'msg': '修改成功', 'project': project_dict})

    def delete(self, request, pro_id):
        """
        删除项目
        """
        try:
            DB_project.objects.get(id=pro_id).delete()
        except:
            return http.JsonResponse({'code': 0, 'msg': '删除失败'})
        return http.JsonResponse({'code': 1, 'msg': '删除成功'})


class CaseInfoView(View):
    def get(self, request, pk):
        """
        获取项目对应的所有用例
        """
        cases = DB_case.objects.filter(project_id=pk).all()
        case_list = []
        for case in cases:
            case_dict = {
                'id': case.id,
                'name': case.name,
                'script_name': case.script_name,
                'is_threads': "是" if case.is_thread == 1 else "否",
                'retry_count': case.retry_count
            }
            case_list.append(case_dict)

        return http.JsonResponse({'code': 1, 'msg': '成功', 'case_list': case_list})

    def post(self, request, pk):
        """
        新增用例
        """
        requestData = json.loads(request.body.decode())
        requestData['is_thread'] = int(requestData['is_thread'])
        # 获取参数
        name = requestData['name']
        if name == '' or name is None:
            return http.JsonResponse({'code': 0, 'msg': '用例名称不能为空', 'project': {}})
        if pk == '' or pk is None:
            return http.JsonResponse({'code': 0, 'msg': '请先创建项目', 'project': {}})
        case = DB_case.objects.create(**requestData, project_id=pk)
        case_dict = {
            'id': case.id,
            'name': case.name,
            'script_name': case.script_name,
            'is_threads': case.is_thread,
            'retry_count': case.retry_count
        }
        return http.JsonResponse({'code': 1, 'msg': '添加成功', 'case_dict': case_dict})

    def put(self, request, pk):
        """
        修改用例
        """
        requestData = json.loads(request.body.decode())
        requestData['is_thread'] = int(requestData['is_thread'])
        # 获取参数
        name = requestData['name']
        if not name:
            return http.JsonResponse({'code': 0, 'msg': '用例名称不能为空', 'case': {}})
        try:
            DB_case.objects.filter(id=pk).update(**requestData)
        except Exception as e:
            print(e)
            return http.JsonResponse({'code': 0, 'msg': '该用例不存在', 'case': {}})
        case = DB_case.objects.get(id=pk)
        case_dict = {
            'id': case.id,
            'name': case.name,
            'script_name': case.script_name,
            'is_threads': case.is_thread,
            'retry_count': case.retry_count
        }
        return http.JsonResponse({'code': 1, 'msg': '修改成功', 'case': case_dict})

    def delete(self, request, pk):
        """
        删除项目
        """
        try:
            DB_case.objects.get(id=pk).delete()
        except Exception as e:
            print(e)
            return http.JsonResponse({'code': 0, 'msg': '删除失败'})
        return http.JsonResponse({'code': 1, 'msg': '删除成功'})


class CaseScriptView(View):
    def post(self, request, pro_id):
        script_file = request.FILES.get("file", None)
        if not script_file:
            return http.JsonResponse({'code': 0, 'msg': '未上传脚本'})
        script_name = str(script_file)
        # 将脚本文件放入对应调试包
        with open('my_client/client_%s/case/%s' % (pro_id, script_name), 'wb') as f:
            for content in script_file.chunks():
                f.write(content)
        return http.JsonResponse({'code': 1, 'msg': '上传成功'})
