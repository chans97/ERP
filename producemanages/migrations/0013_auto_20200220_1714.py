# Generated by Django 2.1.15 on 2020-02-20 17:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('producemanages', '0012_auto_20200219_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='produceregister',
            name='작성자',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='생산계획등록', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workorderregister',
            name='생산일시',
            field=models.DateField(default=datetime.date(2020, 2, 20)),
        ),
    ]