# Generated by Django 2.1.15 on 2020-02-16 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producemanages', '0008_auto_20200215_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorderregister',
            name='생산일시',
            field=models.DateField(default=datetime.date(2020, 2, 16)),
        ),
    ]