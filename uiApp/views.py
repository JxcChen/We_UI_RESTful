from django import http

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from uiApp.models import *
from uiApp.serializer import *
from uiApp.utils.return_data import return_json_data
from django.db.models import Q


class ProjectListView(APIView):
    def get(self, request):
        query_data = request.query_params
        user_id = query_data['user_id']
        pro_list = list(DB_pro_user.objects.filter(user_id=user_id).values('pro_id'))
        res_list = []
        for project in pro_list:
            pro = DB_project.objects.get(id=project['pro_id'])
            res_list.append(pro)
        serializer = ProjectSerializer(instance=res_list, many=True)
        return Response(return_json_data(1, '成功', serializer.data))

    def post(self, request):
        query_data = request.data
        # 先判断数据库中是否已存在同名项目
        is_exit = True if len(DB_project.objects.filter(name=query_data['name'])) > 0 else False
        if is_exit:
            return Response(return_json_data(3,'该项目已存在',''),status=status.HTTP_200_OK)
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
            return Response(return_json_data(1, '成功', res_pro))


class ProjectDetailView(APIView):
    def put(self,request,pk):
        query_data = request.data
        # 先判断 是否已存在相同名称项目
        is_exit = True if len(DB_project.objects.filter(~Q(id=pk), name=query_data['name'])) else False
        if is_exit:
            return Response(return_json_data(3,'该项目已存在',''),status=status.HTTP_200_OK)
        else:
            # 获取待修改的项目
            old_pro = DB_project.objects.get(id=pk)
            # 使用序列化器进行修改
            pro = ProjectSerializer(data=query_data,instance=old_pro)
            # 检测字段正确性
            pro.is_valid(raise_exception=True)
            # 进行修改
            pro.save()
            new_pro = DB_project.objects.get(id=pk)
            res_pro = ProjectSerializer(instance=new_pro).data
            return Response(return_json_data(1, '修改成功', res_pro),status=status.HTTP_201_CREATED)

    def delete(self,request,pk):
        DB_project.objects.get(id=pk).delete()
        DB_pro_user.objects.get(pro_id=pk).delete()
        return Response(return_json_data(1, '删除成功', ''), status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
