# Generated by Django 2.1.15 on 2020-08-27 23:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producemanages', '0059_auto_20200826_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorderregister',
            name='생산일시',
            field=models.DateField(blank=True, default=datetime.date(2020, 8, 27), null=True),
        ),
    ]
