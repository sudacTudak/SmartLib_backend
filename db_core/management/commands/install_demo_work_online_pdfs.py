from __future__ import annotations

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from db_core.seed_demo.demo_online_pdf import install_demo_online_pdfs


class Command(BaseCommand):
    help = (
        "Копирует демо-PDF онлайн-версий из db_core/seed_demo/assets/ в MEDIA_ROOT "
        "(works/<work_id>/online/<filename>.pdf) и обновляет Work.online_version_link."
    )

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
            updated = install_demo_online_pdfs()
        except FileNotFoundError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Демо PDF установлены в {settings.MEDIA_ROOT}. Обновлено online_version_link: {updated}."
            )
        )
