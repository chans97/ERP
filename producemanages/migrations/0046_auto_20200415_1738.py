# Generated by Django 2.1.15 on 2020-04-15 17:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producemanages', '0045_auto_20200414_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorderregister',
            name='생산일시',
            field=models.DateField(blank=True, default=datetime.date(2020, 4, 15), null=True),
        ),
    ]