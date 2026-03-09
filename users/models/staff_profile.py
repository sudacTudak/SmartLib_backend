from django.db import models

from users.models import CustomUser

# TODO: Закончить модель после внедрения авторизации и permissions
# class StaffProfile(models.Model):
#     user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.DO_NOTHING, primary_key=True)
#     library_branch = models.ForeignKey(CustomUser, related_name='staff', on_delete=models.DO_NOTHING, primary_key=True)
#     position = models.CharField(max_length=255, blank=False, null=False)