from django.db import models


# Create your models here.
class DB_project(models.Model):
    name = models.CharField(max_length=30)
    host = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    author_name = models.CharField(max_length=40, default="-")
    max_threads = models.IntegerField(default=1)
    auto_host = models.CharField(max_length=200, null=True)
    is_auto = models.IntegerField(default=0)  # 0:关 1:开
    excuse_time = models.CharField(default='00:00',max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DB_case(models.Model):
    name = models.CharField(max_length=30)
    project_id = models.CharField(max_length=20)
    script_name = models.CharField(max_length=30, null=True, default='-')
    is_auto_excuse = models.IntegerField(default=0)  # 0：不参与自动化  1：参与自动化
    is_thread = models.IntegerField(default=1)
    retry_count = models.IntegerField(default=1)
    author = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DB_pro_user(models.Model):
    pro_id = models.IntegerField()
    user_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pro_id


class DB_tester(models.Model):
    name = models.CharField(max_length=30)
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=50, null=True)
    type = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# 任务通知库
class DBNotice(models.Model):
    notice_type = models.IntegerField(default=1)
    user_list = models.CharField(max_length=30,null=True)
    webhook = models.CharField(max_length=50,null=True)
    project_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_id


# 测试任务库  后期完成
# class DB_task(models.Model):
#     name = models.CharField(max_length=30)
#     case_list = models.CharField(max_length=50)
#     author = models.CharField(max_length=30)
#     project_id = models.IntegerField()
#     excuse_result = models.IntegerField(default=0)  # 0: 未执行/1: 成功/2: 失败
#     excuse_time = models.IntegerField()
#     task_level = models.IntegerField(default=1)
#     case_count = models.IntegerField()
#
#     def __str__(self):
#         return self.name


# 页面数据
class DBPage(models.Model):
    name = models.CharField(max_length=50)
    project_id = models.IntegerField()
    author = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# 页面元素
class DBElement(models.Model):
    name = models.CharField(max_length=50)
    page_id = models.IntegerField()
    element_location = models.CharField(max_length=300,null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    loc_method = models.CharField(max_length=20)
    index = models.IntegerField(default=0)

    def __str__(self):
        return self.name
