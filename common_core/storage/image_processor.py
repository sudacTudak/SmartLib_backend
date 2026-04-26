from __future__ import annotations

import os
from dataclasses import dataclass
from io import BytesIO
from typing import Any

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps
from rest_framework.exceptions import ValidationError

from common_core.enums import AppStrEnum

__all__ = [
    "ImageFormat",
    "DEFAULT_ALLOWED_IMAGE_FORMATS",
    "ImageProcessor",
    "ImageProcessorConfig",
]


class ImageFormat(AppStrEnum):
    JPEG = "JPEG"
    PNG = "PNG"
    WEBP = "WEBP"

    @property
    def file_ext(self) -> str:
        return {
            ImageFormat.JPEG: ".jpg",
            ImageFormat.PNG: ".png",
            ImageFormat.WEBP: ".webp",
        }[self]

    @property
    def content_type(self) -> str:
        return {
            ImageFormat.JPEG: "image/jpeg",
            ImageFormat.PNG: "image/png",
            ImageFormat.WEBP: "image/webp",
        }[self]


DEFAULT_ALLOWED_IMAGE_FORMATS: set[str] = set(ImageFormat.items())


@dataclass(frozen=True, slots=True)
class ImageProcessorConfig:
    allowed_formats: set[str] = None  # type: ignore[assignment]
    max_side: int | None = 1024
    jpeg_quality: int = 85
    webp_quality: int = 80

    def __post_init__(self):
        if self.allowed_formats is None:
            object.__setattr__(self, "allowed_formats", DEFAULT_ALLOWED_IMAGE_FORMATS)


class ImageProcessor:
    def __init__(self, config: ImageProcessorConfig | None = None) -> None:
        self.config = config or ImageProcessorConfig()

    def validate(self, file_obj: Any) -> ImageFormat:
        """
        Validate image by content and return detected format.
        """
        if file_obj is None:
            raise ValidationError("Файл не передан.")

        pos = getattr(file_obj, "tell", lambda: 0)()
        try:
            img = Image.open(file_obj)
            img.verify()
            fmt = (img.format or "").upper()
        except Exception as exc:  # noqa: BLE001
            raise ValidationError("Файл не является корректным изображением.") from exc
        finally:
            try:
                file_obj.seek(pos)
            except Exception:
                pass

        if fmt not in self.config.allowed_formats:
            allowed = ", ".join(sorted(self.config.allowed_formats))
            raise ValidationError(f"Недопустимый формат изображения: {fmt or 'UNKNOWN'}. Разрешено: {allowed}.")

        return ImageFormat(fmt)

    def process(self, file_obj: Any) -> InMemoryUploadedFile:
        """
        Validate that `file_obj` is a real image and return a resized/recompressed file.
        """
        image_format = self.validate(file_obj)

        # Re-open for actual processing (verify() makes image unusable for some operations)
        img = Image.open(file_obj)
        img = ImageOps.exif_transpose(img)

        # Resize
        if self.config.max_side is not None:
            w, h = img.size
            max_current = max(w, h)
            if max_current > self.config.max_side:
                scale = self.config.max_side / max_current
                new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
                img = img.resize(new_size, Image.LANCZOS)

        out = BytesIO()
        save_kwargs: dict[str, Any] = {}

        if image_format == ImageFormat.JPEG:
            if img.mode not in ("RGB",):
                img = img.convert("RGB")
            save_kwargs.update({"optimize": True, "quality": self.config.jpeg_quality, "progressive": True})
            img.save(out, format=image_format.value, **save_kwargs)
        elif image_format == ImageFormat.PNG:
            save_kwargs.update({"optimize": True})
            img.save(out, format=image_format.value, **save_kwargs)
        else:  # WEBP
            save_kwargs.update({"quality": self.config.webp_quality, "method": 6})
            img.save(out, format=image_format.value, **save_kwargs)

        out_ext = image_format.file_ext
        out_content_type = image_format.content_type

        out.seek(0)
        base, _ = os.path.splitext(getattr(file_obj, "name", "upload"))
        out_name = f"{base}{out_ext}"

        return InMemoryUploadedFile(
            file=out,
            field_name=getattr(file_obj, "field_name", None),
            name=out_name,
            content_type=out_content_type,
            size=out.getbuffer().nbytes,
            charset=None,
        )

