# Generated by Django 2.2 on 2022-02-18 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uiApp', '0007_db_case_is_auto_excuse'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_project',
            name='excuse_time',
            field=models.CharField(default='00:00', max_length=10),
        ),
        migrations.AddField(
            model_name='db_project',
            name='is_auto',
            field=models.IntegerField(default=0),
        ),
    ]
