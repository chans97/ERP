# Generated by Django 2.1.15 on 2020-12-27 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StandardInformation', '0002_auto_20201227_1834'),
        ('stockmanages', '0001_initial'),
        ('qualitycontrols', '0002_auto_20201227_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockofmaterialoutrequest',
            name='출고요청자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='자재출고요청', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockofmaterialout',
            name='자재출고요청',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='자재출고등록', to='stockmanages.StockOfMaterialOutRequest'),
        ),
        migrations.AddField(
            model_name='stockofmaterialout',
            name='출고자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='자재출고등록', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockofmaterialinrequest',
            name='수입검사',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='자재입고요청', to='qualitycontrols.MaterialCheck'),
        ),
        migrations.AddField(
            model_name='stockofmaterialinrequest',
            name='입고요청자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='자재입고요청', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockofmaterialinrequest',
            name='자재',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='자재입고요청', to='StandardInformation.Material'),
        ),
        migrations.AddField(
            model_name='stockofmaterialin',
            name='입고자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='자재입고등록', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockofmaterialin',
            name='자재입고요청',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='자재입고등록', to='stockmanages.StockOfMaterialInRequest'),
        ),
        migrations.AddField(
            model_name='stockofmaterialhistory',
            name='자재',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='자재재고기록', to='StandardInformation.Material'),
        ),
        migrations.AddField(
            model_name='stockofmaterial',
            name='자재',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='자재재고', to='StandardInformation.Material'),
        ),
    ]
