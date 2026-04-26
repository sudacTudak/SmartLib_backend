from __future__ import annotations

from typing import Any

from common_core.storage import UploadPathBase

__all__ = ["BookPreviewUploadPath"]


class BookPreviewUploadPath(UploadPathBase):
    def get_path(self, instance: Any, filename: str) -> str:
        ext = self.ext(filename)
        return f"books/{self.instance_id(instance)}/preview/{self.random_name()}.{ext}"

