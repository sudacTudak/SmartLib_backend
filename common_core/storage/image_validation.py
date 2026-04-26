from __future__ import annotations

from typing import Any

from rest_framework.exceptions import ValidationError

from common_core.storage.image_processor import ImageProcessor, ImageProcessorConfig

__all__ = ["validate_uploaded_image"]


def validate_uploaded_image(file_obj: Any, *, allowed_formats: set[str]) -> None:
    """
    Validate that uploaded file is a real image (by content) and has allowed format.

    `allowed_formats` are Pillow format names: {"JPEG", "PNG", "WEBP"}.
    """
    if file_obj is None:
        return

    # Backward-compatible wrapper around ImageProcessor validation.
    processor = ImageProcessor(ImageProcessorConfig(allowed_formats=allowed_formats))
    try:
        processor.validate(file_obj)
    except ValidationError:
        raise

