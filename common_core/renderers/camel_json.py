from __future__ import annotations

from rest_framework.renderers import JSONRenderer

from common_core.case import keys_to_camel_case

__all__ = ["CamelCaseJSONRenderer"]


class CamelCaseJSONRenderer(JSONRenderer):
    """
    Render all JSON responses in camelCase, while keeping internal Python/DB in snake_case.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return super().render(
            keys_to_camel_case(data),
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context,
        )

