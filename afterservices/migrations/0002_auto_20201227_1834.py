# Generated by Django 2.1.15 on 2020-12-27 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StandardInformation', '0002_auto_20201227_1834'),
        ('afterservices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asvisitcontents',
            name='입력자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS현장방문', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asrevisitcontents',
            name='수리기사',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS재방문', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asrevisitcontents',
            name='전AS현장방문',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS재방문', to='afterservices.ASVisitContents'),
        ),
        migrations.AddField(
            model_name='asresults',
            name='내부처리',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS완료', to='afterservices.ASRegisters'),
        ),
        migrations.AddField(
            model_name='asresults',
            name='방문',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS완료', to='afterservices.ASVisitContents'),
        ),
        migrations.AddField(
            model_name='asresults',
            name='완료확인자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS완료', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asresults',
            name='재방문',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS완료', to='afterservices.ASReVisitContents'),
        ),
        migrations.AddField(
            model_name='asrepairrequest',
            name='AS현장방문',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS수리요청', to='afterservices.ASVisitContents'),
        ),
        migrations.AddField(
            model_name='asrepairrequest',
            name='신청자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS수리요청', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asrepairrequest',
            name='신청품목',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS수리요청', to='StandardInformation.SingleProduct'),
        ),
        migrations.AddField(
            model_name='asregisters',
            name='접수자',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS등록', to=settings.AUTH_USER_MODEL),
        ),
    ]