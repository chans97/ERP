# Generated by Django 2.1.15 on 2020-12-27 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StandardInformation', '0002_auto_20201227_1834'),
        ('stockrack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockofrackproductoutrequest',
            name='출하요청자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='랙출하요청', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockofrackproductout',
            name='랙출하요청',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='랙출하등록', to='stockrack.StockOfRackProductOutRequest'),
        ),
        migrations.AddField(
            model_name='stockofrackproductout',
            name='출하자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='랙출하등록', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockofrackproductmaker',
            name='랙',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='랙조립', to='StandardInformation.RackProduct'),
        ),
        migrations.AddField(
            model_name='stockofrackproductmaker',
            name='랙조립기사',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='랙조립', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockofrackproductmaker',
            name='랙출하요청',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='랙조립', to='stockrack.StockOfRackProductOutRequest'),
        ),
    ]