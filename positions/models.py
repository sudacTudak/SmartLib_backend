from django.db import models
from rest_framework.fields import CharField

from .constants import POSITION_NAME_MIN_LENGTH, POSITION_NAME_MAX_LENGTH


class Position(models.Model):
    id = models.UUIDField(primary_key=True)
    name = CharField(min_length=POSITION_NAME_MIN_LENGTH, max_length=POSITION_NAME_MAX_LENGTH)