# Generated by Django 2.2 on 2022-02-17 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uiApp', '0006_alter_db_project_author_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_case',
            name='is_auto_excuse',
            field=models.IntegerField(default=0),
        ),
    ]
