from rest_framework import serializers
from uiApp.models import DB_project


# 定义项目序列化器
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定model
        model = DB_project
        # 指定需要的字段
        fields = "__all__"
        # 设置只读字段
        read_only_fields = ["id"]
        # 设置字段额外约束
        extra_kwargs = {
            "max_threads": {
                "max_value": 5,
                "min_value": 0
            }
        }
