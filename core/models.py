from django.db import models
from . import managers


class TimeStampedModel(models.Model):

    """Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomCoreManager()

    class Meta:
        abstract = True


class partnermigrate(models.Model):

    Excelfile = models.FileField(null=True, upload_to="migrate")
