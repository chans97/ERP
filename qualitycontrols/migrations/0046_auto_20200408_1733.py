# Generated by Django 2.1.15 on 2020-04-08 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualitycontrols', '0045_auto_20200408_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairregister',
            name='불량위치및자재',
            field=models.TextField(max_length=300, null=True),
        ),
    ]