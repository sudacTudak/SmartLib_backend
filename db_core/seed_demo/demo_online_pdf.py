from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from django.conf import settings

from db_core.seed_demo import data as seed_data
from works.models import Work

ASSETS_DIR = Path(__file__).resolve().parent / "assets"


def install_demo_online_pdfs(*, media_root: Path | None = None) -> int:
    """
    Копирует демо-PDF из ``db_core/seed_demo/assets/`` в MEDIA_ROOT
    и проставляет ``Work.online_version_link`` (относительный путь, как у обложек).
    """
    root = media_root or Path(settings.MEDIA_ROOT)
    root.mkdir(parents=True, exist_ok=True)

    updated = 0
    for work_id, asset_filename in seed_data.DEMO_ONLINE_PDF_BY_WORK_ID.items():
        source = ASSETS_DIR / asset_filename
        if not source.is_file():
            raise FileNotFoundError(f"Нет демо PDF: {source}")

        relative = seed_data.work_demo_online_relative_path(work_id, asset_filename)
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

        count = Work.objects.filter(pk=uuid.UUID(work_id)).update(online_version_link=relative)
        updated += count

    return updated
