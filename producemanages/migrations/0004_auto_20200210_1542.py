# Generated by Django 2.1.15 on 2020-02-10 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producemanages', '0003_workorder_수리생산'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='rev1',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='workorder',
            name='rev2',
            field=models.IntegerField(default=0),
        ),
    ]
