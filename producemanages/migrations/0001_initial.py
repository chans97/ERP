# Generated by Django 2.1.15 on 2020-02-07 14:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProduceRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('생산계획등록코드', models.CharField(max_length=50)),
                ('현재공정', models.CharField(blank=True, choices=[('예비작업', '예비작업'), ('조립', '조립'), ('검사', '검사')], default='예비작업', max_length=10, null=True)),
                ('현재공정달성율', models.CharField(blank=True, choices=[('0%', '0%'), ('25%', '25%'), ('50%', '50%'), ('75%', '75%'), ('100%', '100%')], default='0%', max_length=10, null=True)),
                ('계획생산량', models.IntegerField(null=True)),
                ('일일생산량', models.IntegerField(null=True)),
                ('누적생산량', models.IntegerField(blank=True, null=True)),
                ('특이사항', models.CharField(blank=True, max_length=100, null=True)),
                ('생산의뢰', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='생산계획', to='orders.OrderProduce')),
            ],
            options={
                'verbose_name': '생산계획등록',
                'verbose_name_plural': '생산계획등록',
            },
        ),
        migrations.CreateModel(
            name='RepairRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('불량위치및자재', models.TextField(max_length=300)),
                ('특이사항', models.TextField(max_length=300)),
                ('수리내용', models.TextField(max_length=300)),
                ('실수리수량', models.IntegerField()),
                ('폐기수량', models.IntegerField()),
            ],
            options={
                'verbose_name': '수리내역서',
                'verbose_name_plural': '수리내역서',
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('작업지시코드', models.CharField(max_length=30, null=True)),
                ('수량', models.IntegerField(null=True)),
                ('특이사항', models.CharField(blank=True, max_length=100, null=True)),
                ('생산계획', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='작업지시서', to='producemanages.ProduceRegister')),
            ],
            options={
                'verbose_name': '작업지시서',
                'verbose_name_plural': '작업지시서',
            },
        ),
        migrations.CreateModel(
            name='WorkOrderRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('생산일시', models.DateField(default=datetime.date(2020, 2, 7))),
                ('생산수량', models.IntegerField(null=True)),
                ('특이사항', models.CharField(blank=True, max_length=100, null=True)),
                ('생산담당자', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='작업지시서등록', to=settings.AUTH_USER_MODEL)),
                ('작업지시서', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='작업지시서등록', to='producemanages.WorkOrder')),
            ],
            options={
                'verbose_name': '작업지시서등록',
                'verbose_name_plural': '작업지시서등록',
            },
        ),
    ]
