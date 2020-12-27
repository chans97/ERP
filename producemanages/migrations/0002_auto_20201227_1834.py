# Generated by Django 2.1.15 on 2020-12-27 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StandardInformation', '0002_auto_20201227_1834'),
        ('producemanages', '0001_initial'),
        ('orders', '0002_auto_20201227_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorderregister',
            name='생산담당자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='작업지시서등록', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='workorderregister',
            name='작업지시서',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='작업지시서등록', to='producemanages.WorkOrder'),
        ),
        migrations.AddField(
            model_name='workorder',
            name='생산계획',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='작업지시서', to='producemanages.ProduceRegister'),
        ),
        migrations.AddField(
            model_name='produceregister',
            name='생산의뢰',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='생산계획', to='orders.OrderProduce'),
        ),
        migrations.AddField(
            model_name='produceregister',
            name='작성자',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='생산계획등록', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='monthlyproducelist',
            name='단품모델',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='월별생산계획', to='StandardInformation.SingleProduct'),
        ),
        migrations.AddField(
            model_name='monthlyproducelist',
            name='작성자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='월별생산계획', to=settings.AUTH_USER_MODEL),
        ),
    ]