# Generated by Django 2.1.15 on 2020-02-12 19:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producemanages', '0005_auto_20200210_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorderregister',
            name='생산일시',
            field=models.DateField(default=datetime.date(2020, 2, 12)),
        ),
    ]
