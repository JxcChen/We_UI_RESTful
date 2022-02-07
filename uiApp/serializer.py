from django.contrib.auth.models import User
from rest_framework import serializers
from uiApp.models import *


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


# 定义用例序列化器
class CaseSerializers(serializers.ModelSerializer):
    class Meta:
        # 指定model
        model = DB_case
        fields = "__all__"


# 定义用例序列化器
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        # 指定model
        model = User
        fields = "__all__"


# 定义用例序列化器
class UserProSerializers(serializers.ModelSerializer):
    class Meta:
        # 指定model
        model = DB_pro_user
        fields = "__all__"
