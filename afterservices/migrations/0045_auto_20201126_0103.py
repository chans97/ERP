# Generated by Django 2.1.15 on 2020-11-26 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afterservices', '0044_auto_20201126_0041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asregisters',
            name='단품',
        ),
        migrations.RemoveField(
            model_name='asregisters',
            name='랙',
        ),
        migrations.RemoveField(
            model_name='asregisters',
            name='방문요청일',
        ),
        migrations.RemoveField(
            model_name='asregisters',
            name='불량분류',
        ),
        migrations.RemoveField(
            model_name='asregisters',
            name='불량분류코드',
        ),
        migrations.RemoveField(
            model_name='asregisters',
            name='의뢰처',
        ),
        migrations.RemoveField(
            model_name='asregisters',
            name='인계후',
        ),
        migrations.RemoveField(
            model_name='asregisters',
            name='접수제품분류',
        ),
        migrations.AlterField(
            model_name='asregisters',
            name='처리방법',
            field=models.CharField(blank=True, choices=[('내부처리', '내부처리'), ('현장방문', '현장방문'), ('접수보류', '접수보류'), ('접수취소', '접수취소'), ('택배수령', '택배수령')], default='담당자연결', max_length=10, null=True),
        ),
    ]
