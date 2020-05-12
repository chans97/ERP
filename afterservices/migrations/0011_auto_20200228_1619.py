# Generated by Django 2.1.15 on 2020-02-28 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StandardInformation', '0009_auto_20200215_0913'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('afterservices', '0010_auto_20200228_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='asrevisitcontents',
            name='단품',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS재방문', to='StandardInformation.SingleProduct'),
        ),
        migrations.AddField(
            model_name='asrevisitcontents',
            name='랙',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS재방문', to='StandardInformation.RackProduct'),
        ),
        migrations.AddField(
            model_name='asrevisitcontents',
            name='수리기사',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS재방문', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asrevisitcontents',
            name='접수제품분류',
            field=models.CharField(blank=True, choices=[('단품', '단품'), ('랙', '랙')], default='단품', max_length=10),
        ),
        migrations.AddField(
            model_name='asvisitcontents',
            name='단품',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS현장방문', to='StandardInformation.SingleProduct'),
        ),
        migrations.AddField(
            model_name='asvisitcontents',
            name='랙',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS현장방문', to='StandardInformation.RackProduct'),
        ),
        migrations.AddField(
            model_name='asvisitcontents',
            name='수리기사',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AS현장방문', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asvisitcontents',
            name='접수제품분류',
            field=models.CharField(blank=True, choices=[('단품', '단품'), ('랙', '랙')], default='단품', max_length=10),
        ),
    ]
