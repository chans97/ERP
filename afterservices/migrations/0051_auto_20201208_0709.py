# Generated by Django 2.1.15 on 2020-12-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afterservices', '0050_auto_20201202_0457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asrevisitcontents',
            name='단품',
        ),
        migrations.RemoveField(
            model_name='asrevisitcontents',
            name='랙',
        ),
        migrations.RemoveField(
            model_name='asrevisitcontents',
            name='접수제품분류',
        ),
        migrations.AddField(
            model_name='asrevisitcontents',
            name='현장택배',
            field=models.CharField(blank=True, choices=[('현장', '현장'), ('택배', '택배')], default='현장', max_length=10),
        ),
    ]
