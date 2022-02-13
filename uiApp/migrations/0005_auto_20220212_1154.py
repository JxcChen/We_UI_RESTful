# Generated by Django 3.2 on 2022-02-12 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uiApp', '0004_alter_db_tester_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_pro_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='db_project',
            name='author_name',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='db_case',
            name='script_name',
            field=models.CharField(default='-', max_length=30, null=True),
        ),
    ]
