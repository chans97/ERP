# Generated by Django 2.1.15 on 2020-02-27 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualitycontrols', '0014_auto_20200227_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lowmetarial',
            name='검토일',
            field=models.DateField(blank=True, default=datetime.date(2020, 2, 27), null=True),
        ),
        migrations.AlterField(
            model_name='lowmetarial',
            name='처리방안',
            field=models.CharField(choices=[('재작업', '재작업'), ('수리', '수리'), ('특채(수리후)', '특채(수리후)'), ('특채(무수리)', '특채(무수리)'), ('반품', '반품'), ('폐기', '폐기'), ('기타', '기타')], default='기타', max_length=10, null=True),
        ),
    ]
