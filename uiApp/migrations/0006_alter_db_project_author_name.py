# Generated by Django 3.2 on 2022-02-12 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uiApp', '0005_auto_20220212_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_project',
            name='author_name',
            field=models.CharField(default='-', max_length=40),
        ),
    ]