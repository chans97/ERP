# Generated by Django 2.1.15 on 2020-04-13 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qualitycontrols', '0049_auto_20200413_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialcheck',
            name='검사지침서',
            field=models.CharField(blank=True, choices=[('CAE SHI-16-01', 'CAE SHI-16-01'), ('PCB SHI 10-01', 'PCB SHI 10-01'), ('트랜스 SHI 11-06', '트랜스 SHI 11-06'), ('사출 성형품 SHI 16-02', '사출 성형품 SHI 16-02')], max_length=32, null=True),
        ),
    ]