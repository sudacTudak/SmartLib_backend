from django.dispatch import receiver
from django.db.models.signals import post_migrate

from users.enums import UserPermissions
from users.models import UserPermission


@receiver(post_migrate)
def create_db_permissions(sender, **kwargs):
    for perm in UserPermissions:
        UserPermission.objects.get_or_create(code=perm.value)