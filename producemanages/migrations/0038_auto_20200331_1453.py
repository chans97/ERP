# Generated by Django 2.1.15 on 2020-03-31 14:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producemanages', '0037_monthlyproducelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyproducelist',
            name='작성일',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='workorderregister',
            name='생산일시',
            field=models.DateField(blank=True, default=datetime.date(2020, 3, 31), null=True),
        ),
    ]