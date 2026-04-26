from __future__ import annotations

import os
import uuid
from abc import ABC, abstractmethod
from typing import Any

__all__ = ["UploadPathBase"]


class UploadPathBase(ABC):
    """
    Base helper for Django `upload_to`.

    Subclasses should implement `get_path()`.
    `ext()` validates file extension against `allowed_exts`.
    """

    allowed_exts: set[str] = {"jpg", "jpeg", "png", "webp"}

    def __init__(self, *, id_lookup: str = "id") -> None:
        self.id_lookup = id_lookup

    def ext(self, filename: str) -> str:
        _, ext = os.path.splitext(filename or "")
        ext = ext.lower().lstrip(".")
        if not ext:
            raise ValueError("Не удалось определить расширение файла.")
        if ext not in self.allowed_exts:
            allowed = ", ".join(sorted(self.allowed_exts))
            raise ValueError(f"Недопустимый формат файла .{ext}. Разрешено: {allowed}.")
        return ext

    def random_name(self) -> str:
        return str(uuid.uuid4())

    def instance_id(self, instance: Any) -> str:
        """
        Resolve instance identifier for path construction.

        By default uses `instance.id`, but can be overridden via `id_lookup`.
        """
        value = getattr(instance, self.id_lookup, None)
        if value is None:
            raise ValueError(f"У объекта {type(instance).__name__} нет поля {self.id_lookup!r}.")
        return str(value)

    @abstractmethod
    def get_path(self, instance: Any, filename: str) -> str:
        raise NotImplementedError

    def __call__(self, instance: Any, filename: str) -> str:
        return self.get_path(instance, filename)

