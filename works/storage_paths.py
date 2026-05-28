from __future__ import annotations

import os
from typing import Any

from common_core.storage import UploadPathBase

__all__ = ["WorkPreviewUploadPath", "WorkOnlineVersionUploadPath"]


class WorkPreviewUploadPath(UploadPathBase):
    def get_path(self, instance: Any, filename: str) -> str:
        ext = self.ext(filename)
        return f"works/{self.instance_id(instance)}/preview/{self.random_name()}.{ext}"


class WorkOnlineVersionUploadPath(UploadPathBase):
    allowed_exts = {"pdf"}

    def get_path(self, instance: Any, filename: str) -> str:
        ext = self.ext(filename)
        filename_without_extension = os.path.splitext(os.path.basename(filename or ""))[0] or self.random_name()
        return f"works/{self.instance_id(instance)}/online/{filename_without_extension}.{ext}"
