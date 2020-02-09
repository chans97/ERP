from django.db import models
from core.models import TimeStampedModel
from orders import models as orders_models
from users import models as users_models
from StandardInformation import models as SI_models

# Create your models here.
class ASRegisters(TimeStampedModel):
    pass


class ASVisitRequests(TimeStampedModel):
    pass


class ASVisitContents(TimeStampedModel):
    pass


class ASReVisitContents(TimeStampedModel):
    pass


class ASResults(TimeStampedModel):
    pass
