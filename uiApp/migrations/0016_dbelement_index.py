# Generated by Django 2.2.27 on 2022-02-27 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uiApp', '0015_dbelement_loc_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbelement',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]
