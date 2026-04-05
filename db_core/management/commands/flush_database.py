from __future__ import annotations

import sys

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Удаляет все данные из таблиц БД (аналог flush): схема и миграции сохраняются. "
        "Требует подтверждения ввода Y или y."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Разрешить запуск при DEBUG=False (крайне осторожно в production).",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Команда разрешена только при DEBUG=True. Для принудительного запуска укажите --force."
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "WARNING: This command will remove ALL data from the database "
                "(all tables will be flushed). This cannot be undone.\n"
                "Are you sure? Type Y or y to confirm:"
            )
        )
        self.stdout.write("", ending="")

        line = sys.stdin.readline().rstrip("\r\n")

        if line.strip().upper() != "Y":
            self.stdout.write(self.style.ERROR("Aborted (expected Y or y)."))
            return

        call_command(
            "flush",
            interactive=False,
            verbosity=options.get("verbosity", 1),
        )
        self.stdout.write(self.style.SUCCESS("Database flushed."))
