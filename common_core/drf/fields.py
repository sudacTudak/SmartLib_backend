from __future__ import annotations

from typing import Any

from rest_framework import serializers

from common_core.storage import ImageProcessor, ImageProcessorConfig

__all__ = ["ProcessedImageField"]


class ProcessedImageField(serializers.ImageField):
    """
    DRF ImageField with image validation + minification performed by `common_core.storage.ImageProcessor`.
    """

    def __init__(
        self,
        *args,
        allowed_formats: set[str] | None = None,
        max_side: int | None = 1024,
        jpeg_quality: int = 85,
        webp_quality: int = 80,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._processor = ImageProcessor(
            ImageProcessorConfig(
                allowed_formats=allowed_formats,
                max_side=max_side,
                jpeg_quality=jpeg_quality,
                webp_quality=webp_quality,
            )
        )

    def to_internal_value(self, data: Any):
        file_obj = super().to_internal_value(data)
        if file_obj is None:
            return None
        return self._processor.process(file_obj)

