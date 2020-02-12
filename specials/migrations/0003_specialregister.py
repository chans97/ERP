# Generated by Django 2.1.15 on 2020-02-09 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('specials', '0002_remove_specialapplyregister_제품코드'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('특채등록일', models.DateField()),
                ('특채수량', models.IntegerField()),
                ('특채등록자', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='특채등록', to=settings.AUTH_USER_MODEL)),
                ('특채신청등록', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='특채등록', to='specials.SpecialApplyRegister')),
            ],
            options={
                'verbose_name': '특채등록',
                'verbose_name_plural': '특채등록',
            },
        ),
    ]