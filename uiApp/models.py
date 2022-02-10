from django.db import models


# Create your models here.
class DB_project(models.Model):
    name = models.CharField(max_length=30)
    host = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    max_threads = models.IntegerField(default=1)
    auto_host = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class DB_case(models.Model):
    name = models.CharField(max_length=30)
    project_id = models.CharField(max_length=20)
    script_name = models.CharField(max_length=30, null=True, default='-')
    is_thread = models.IntegerField(default=1)
    retry_count = models.IntegerField(default=1)
    author = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class DB_pro_user(models.Model):
    pro_id = models.IntegerField()
    user_id = models.IntegerField()


class DB_tester(models.Model):
    name = models.CharField(max_length=30)
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=50, null=True)
    type = models.IntegerField(default=1)

    def __str__(self):
        return self.name
