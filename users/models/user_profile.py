from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Case, IntegerField, Value, When
from uuid import uuid4 as uuid

from users.enums import UserRole

from .custom_user.models import CustomUser

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from works.models.work import Work

__all__ = ['UserFavorite', 'UserProfile']


class UserProfile(models.Model):
    """Профиль клиента: избранные произведения (Work). Допустим только для role=client."""

    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    user = models.OneToOneField(CustomUser, related_name='user_profile', on_delete=models.CASCADE)
    favorite_works = models.ManyToManyField(
        'works.Work',
        through='UserFavorite',
        related_name='favorited_in_user_profiles',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'
        ordering = ('created_at',)

    def clean(self):
        super().clean()
        if UserRole(self.user.role) != UserRole.Client:
            raise ValidationError('Профиль пользователя (UserProfile) допустим только для роли client.')

    def favorite_works_ordered_recent_first(self) -> QuerySet['Work']:
        """Произведения из избранного: сначала последние добавленные (по created_at связи UserFavorite)."""

        from works.models.work import Work

        work_ids = list(
            UserFavorite.objects.filter(profile=self)
            .order_by('-created_at')
            .values_list('work_id', flat=True),
        )
        if not work_ids:
            return Work.objects.none()

        preserved = Case(
            *[When(pk=wid, then=Value(idx)) for idx, wid in enumerate(work_ids)],
            output_field=IntegerField(),
        )
        return Work.objects.filter(pk__in=work_ids).order_by(preserved)


class UserFavorite(models.Model):
    """Связь профиль — избранное произведение; порядок по времени добавления."""

    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='favorite_links',
    )
    work = models.ForeignKey(
        'works.Work',
        on_delete=models.CASCADE,
        related_name='favorite_profile_links',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_profile_favorite_link'
        ordering = ('-created_at',)
        constraints = (
            models.UniqueConstraint(
                fields=('profile', 'work'),
                name='user_profile_favorite_link_profile_work_uniq',
            ),
        )

    def clean(self):
        super().clean()
        if UserRole(self.profile.user.role) != UserRole.Client:
            raise ValidationError('Избранное доступно только для профилей клиента.')
