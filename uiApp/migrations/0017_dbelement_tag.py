# Generated by Django 2.2.27 on 2022-03-01 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uiApp', '0016_dbelement_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbelement',
            name='tag',
            field=models.CharField(default='', max_length=500),
        ),
    ]
