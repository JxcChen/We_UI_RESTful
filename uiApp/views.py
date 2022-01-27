from django import http

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from uiApp.models import DB_project
from uiApp.serializer import ProjectSerializer


class ProjectListView(GenericAPIView):
    # 设置queryset 和 serializer_class属性
    # queryset : 目标model的全部数据
    # serializer_class: 序列化器
    queryset = DB_project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request):
        projects = self.get_queryset()
        pro_list = self.get_serializer(instance=projects, many=True)
        return http.JsonResponse({'code': 0, ',msg': '成功', 'data': pro_list.data})

    def post(self, request):
        request_data = request.data
        # 进行反序列化
        project = self.get_serializer(data=request_data)
        # 进行参数校验 raise_exception:有异常直接抛出
        project.is_valid(raise_exception=True)
        # 入库  要现在序列化器中重写 create方法
        res = project.save()
        return Response({'code': 0, ',msg': '成功', 'data': project.data}, status=status.HTTP_201_CREATED)


class ProjectDetailView(GenericAPIView):
    queryset = DB_project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, pk):
        project = self.get_object()
        serializer = self.get_serializer(instance=project)
        return http.JsonResponse({'code': 0, ',msg': '成功', 'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        project = self.get_object()
        request_data = request.data
        serializer = self.get_serializer(instance=project, data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'code': 0, ',msg': '成功', 'data': project.data}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        DB_project.objects.filter(id=pk).delete()
        return Response({'code': 0, ',msg': '成功'}, status=status.HTTP_204_NO_CONTENT)
