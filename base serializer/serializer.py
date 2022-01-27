from rest_framework import serializers
from uiApp.models import DB_project


# 定义项目序列化器
class ProjectSerializer(serializers.Serializer):
    """
    name = models.CharField(max_length=30)
    host = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    max_threads = models.IntegerField(default=1)
    auto_host = models.CharField(max_length=200, null=True)
    """
    # 需要与model中的字段一一对应
    # read_only 只进行序列化  反序列化时会忽略
    id = serializers.IntegerField(read_only=True, label='项目id 唯一标识')
    name = serializers.CharField(max_length=20, label='项目名称')
    host = serializers.CharField(max_length=200, label='项目域名')
    author = serializers.CharField(max_length=20, label='项目负责人')
    max_threads = serializers.IntegerField(default=1, label='最大并发数')
    auto_host = serializers.CharField(max_length='200', label='自动化运行的域名')

    def create(self, validated_data):
        project = DB_project.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        instance.name = validated_data['validated_data']
        instance.host = validated_data['host']
        instance.author = validated_data['author']
        instance.max_threads = validated_data['max_threads']
        instance.auto_host = validated_data['auto_host']
        instance.save()

        project = DB_project.objects.get(id=instance.id)
        return project


