from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from common_core.management.arguments import ArgumentSpecSet
from positions.models import StaffPosition
from users.enums import UserRole
from users.models import CustomUser, StaffProfile, UserPermission
from django.conf import settings

from typing import cast


class Command(BaseCommand):
    help = "Create admin user with full permissions and StaffProfile."

    def add_arguments(self, parser):
        # Оставляем инфраструктуру ArgumentSpec / ArgumentSpecSet для будущих параметров.
        specs = ArgumentSpecSet(())
        specs.add_to_parser(parser)

    @transaction.atomic
    def handle(self, *args, **options):
        admin_data = cast(dict, settings.SUPER_ADMIN)
        email = str(admin_data.get('email')).strip().lower()

        try:
            user = CustomUser.objects.get(email=email)
            created = False

            user = cast(CustomUser, user)

            if UserRole(user.role) != UserRole.Admin:
                raise CommandError(f'found user {user.email} with invalid role: {user.role}')

        except CustomUser.DoesNotExist:
            password: str = str(admin_data.get('password'))
            user = CustomUser(
                email=email,
                first_name=str(admin_data.get("first_name")),
                last_name=str(admin_data.get("last_name")),
                role=UserRole.Admin.value,
                is_staff=True,
                is_active=True,
                is_superuser=True,
            )
            user.set_password(password)
            user.save()
            created = True

        position_name = str(admin_data.get("position_name"))
        try:
            position = StaffPosition.objects.get(name=position_name)
        except StaffPosition.DoesNotExist as exc:
            raise CommandError(
                f"StaffPosition with name '{position_name}' does not exist. "
                "Run initial data migration/seed before create_admin."
            ) from exc

        if created:
            StaffProfile.objects.create(
                user=user,
                position=position,
            )

        permission_objs = UserPermission.objects.all()
        user.user_permissions.set(permission_objs)

        action = "created" if created else "found"
        self.stdout.write(self.style.SUCCESS(f"Admin {action}: {user.email}"))
