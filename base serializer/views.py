from django import http
from django.views import View
import json
from uiApp.models import DB_project
from uiApp.serializer import ProjectSerializer


class ProjectListView(View):
    def get(self, request):
        projects = DB_project.objects.all()
        # 对数据进行序列化后返回
        # instance传入要序列化的对象  many表示该对象是否存在多个
        pro_list = ProjectSerializer(instance=projects, many=True)
        return http.JsonResponse({'code': 0, ',msg': '成功', 'data': pro_list.data})

    def post(self, request):
        request_data = json.loads(request.body.decode())
        print(request_data)
        # 进行反序列化
        project = ProjectSerializer(data=request_data)
        # 进行参数校验 raise_exception:有异常直接抛出
        project.is_valid()
        # 入库  要现在序列化器中重写 create方法
        res = project.save()
        return http.JsonResponse({'code': 0, ',msg': '成功', 'data': res})


class ProjectDetailView(View):

    def put(self, request, pro_id):
        pro = DB_project.objects.get(id=pro_id)
        request_data = json.loads(request.body.decode())
        project = ProjectSerializer(instance=pro,data=request_data)
        project.is_valid(raise_exception=True)
        res = project.save()
        return http.JsonResponse({'code': 0, ',msg': '成功', 'data': res})