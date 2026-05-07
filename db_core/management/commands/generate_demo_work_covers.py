from __future__ import annotations

import uuid
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from db_core.seed_demo import data as seed_data
from db_core.seed_demo.demo_cover_generator import build_demo_cover_png_for_work, demo_work_specs
from works.models import Work


class Command(BaseCommand):
    help = (
        "Генерирует демо-обложку (один PNG 300×430): синий фон, автор жирным и название тонким sans, "
        "слева сверху. Файл: MEDIA_ROOT/works/<uuid>/preview/demo_cover.png."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Разрешить запуск при DEBUG=False (осторожно в production).",
        )
        parser.add_argument(
            "--skip-db",
            action="store_true",
            help="Только записать файлы в MEDIA_ROOT, не обновлять Work.preview_link.",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Команда разрешена только при DEBUG=True. Для принудительного запуска укажите --force."
            )

        media_root = Path(settings.MEDIA_ROOT)
        media_root.mkdir(parents=True, exist_ok=True)

        specs = demo_work_specs()
        updated = 0
        for work_id, title, author in specs:
            rel = seed_data.work_demo_preview_relative_path(work_id)
            path = media_root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(build_demo_cover_png_for_work(work_id, title, author))

            if not options["skip_db"]:
                wid = uuid.UUID(work_id)
                cnt = Work.objects.filter(pk=wid).update(preview_link=rel)
                if cnt:
                    updated += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Work {work_id!r} нет в БД — файлы записаны, preview_link не обновлён."
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Обложки записаны в {media_root} ({len(specs)} произведений). "
                f"Обновлено preview_link: {updated}."
            )
        )
