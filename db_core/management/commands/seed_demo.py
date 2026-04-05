from __future__ import annotations

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from db_core.seed_demo.run import run_seed_demo


class Command(BaseCommand):
    help = "Наполнение БД демонстрационными данными (конфигурация: db_core.seed_demo.data). Уже существующие записи с теми же id пропускаются."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Разрешить запуск при DEBUG=False (осторожно в production).",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Команда разрешена только при DEBUG=True. Для принудительного запуска укажите --force."
            )

        try:
            run_seed_demo(self.stdout, self.style)
        except ValueError as exc:
            raise CommandError(f"Некорректные данные в db_core/seed_demo/data.py: {exc}") from exc
