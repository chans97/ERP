# Generated by Django 2.1.15 on 2020-02-09 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StandardInformation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockOfMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('실수량', models.IntegerField(blank=True, null=True)),
                ('입고요청포함수량', models.IntegerField(blank=True, null=True)),
                ('출고요청제외수량', models.IntegerField(blank=True, null=True)),
                ('자재', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='자재재고', to='StandardInformation.Material')),
            ],
            options={
                'verbose_name': '자재재고',
                'verbose_name_plural': '자재재고',
            },
        ),
        migrations.CreateModel(
            name='StockOfMaterialHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('실수량', models.IntegerField(blank=True, null=True)),
                ('입고요청포함수량', models.IntegerField(blank=True, null=True)),
                ('출고요청제외수량', models.IntegerField(blank=True, null=True)),
                ('자재', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='자재재고기록', to='StandardInformation.Material')),
            ],
            options={
                'verbose_name': '자재재고기록용',
                'verbose_name_plural': '자재재고기록용',
            },
        ),
        migrations.CreateModel(
            name='StockOfMaterialIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('입고일', models.DateField(null=True)),
                ('입고수량', models.IntegerField(null=True)),
                ('입고유형', models.CharField(choices=[('일반', '일반'), ('반납', '반납')], default='일반', max_length=10, null=True)),
                ('입고자', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='자재입고등록', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '자재입고등록',
                'verbose_name_plural': '자재입고등록',
            },
        ),
        migrations.CreateModel(
            name='StockOfMaterialInRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('입고요청수량', models.IntegerField()),
                ('입고요청일', models.DateField()),
                ('입고요청자', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='자재입고요청', to=settings.AUTH_USER_MODEL)),
                ('자재', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='자재입고요청', to='StandardInformation.Material')),
            ],
            options={
                'verbose_name': '자재입고요청',
                'verbose_name_plural': '자재입고요청',
            },
        ),
        migrations.CreateModel(
            name='StockOfMaterialOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('출고일', models.DateField(null=True)),
                ('출고수량', models.IntegerField(null=True)),
                ('출고유형', models.CharField(choices=[('생산', '생산'), ('AS', 'AS')], default='생산', max_length=10, null=True)),
            ],
            options={
                'verbose_name': '자재출고등록',
                'verbose_name_plural': '자재출고등록',
            },
        ),
        migrations.CreateModel(
            name='StockOfMaterialOutRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('출고요청수량', models.IntegerField()),
                ('출고요청일', models.DateField()),
                ('자재', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='자재출고요청', to='StandardInformation.Material')),
                ('출고요청자', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='자재출고요청', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '자재출고요청',
                'verbose_name_plural': '자재출고요청',
            },
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
            model_name='stockofmaterialin',
            name='자재입고요청',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='자재입고등록', to='stockmanages.StockOfMaterialInRequest'),
        ),
    ]
