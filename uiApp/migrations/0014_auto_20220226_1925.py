# Generated by Django 2.2.27 on 2022-02-26 11:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('uiApp', '0013_auto_20220223_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_case',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='db_case',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='db_pro_user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='db_pro_user',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='db_project',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='db_project',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='db_tester',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='db_tester',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='dbelement',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dbelement',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='dbnotice',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dbnotice',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='dbpage',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dbpage',
            name='update_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
