# Generated by Django 2.1.15 on 2020-04-17 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afterservices', '0028_auto_20200417_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asregisters',
            name='인계후',
            field=models.CharField(choices=[('현장방문', '현장방문'), ('내부처리', '내부처리'), ('접수보류', '접수보류'), ('접수취소', '접수취소')], default='', max_length=10),
        ),
    ]
