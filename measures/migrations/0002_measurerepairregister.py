# Generated by Django 2.1.15 on 2020-02-09 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StandardInformation', '0003_auto_20200209_1734'),
        ('measures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasureRepairRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('수리일', models.DateField()),
                ('수리부문', models.CharField(max_length=100)),
                ('수리내용', models.CharField(max_length=100)),
                ('수리내용사진첨부', models.ImageField(blank=True, help_text='계측기수리 사진을 첨부해주세요.', null=True, upload_to='images')),
                ('특이사항', models.TextField()),
                ('계측기', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StandardInformation.Measure')),
                ('수리자', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='계측기수리등록', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '계측기수리등록',
                'verbose_name_plural': '계측기수리등록',
            },
        ),
    ]
